from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui import Window
from data_classes import Station, StopPoint, Departure
from log import logger

from datetime import datetime, timedelta
import pandas as pd
from urllib.request import urlretrieve
from urllib.error import HTTPError
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

def create_stations(stations_config: dict) -> list[Station]:
    stations: dict[Station] = []
    
    for station_name in stations_config:
        
        stop_points = []
        
        for stop_point in stations_config[station_name]:
            # get stop_point_ref
            stop_point_ref = stop_point["stop_point_ref"]
            
            # get optional prefix and suffix
            prefix = None
            suffix = None
            try:
                prefix = stop_point["prefix"]
            except KeyError:
                pass
            try:
                suffix = stop_point["suffix"]
            except KeyError:
                pass
            
            stop_points.append(StopPoint(
                stop_point_ref=stop_point_ref,
                prefix=prefix,
                suffix=suffix
            ))
            
            if prefix is None: logger.debug(f"station {station_name} / {stop_point_ref} doesn't have a prefix configured")
            if suffix is None: logger.debug(f"station {station_name} / {stop_point_ref} doesn't have a suffix configured")
        
        stations.append(Station(
            name=station_name,
            stop_points=stop_points
        ))
    
    return stations

def get_all_used_stoppoints(windows: list["Window"]):
    all_stop_points: list[StopPoint] = []
    
    for window in windows:
        for stop_point in window.station.stop_points:
            if stop_point not in all_stop_points:
                all_stop_points.append(stop_point)
    
    return all_stop_points
    
def download_line_color_list(filename: str):
    #TODO: change to use official kvv data
    url = "https://raw.githubusercontent.com/Traewelling/line-colors/refs/heads/main/line-colors.csv"
    try:
        urlretrieve(url, filename)
    except HTTPError:
        logger.exception("Line color data could not be downloaded!y")

def get_line_color(line_name: str, filename: str, fallback_colors: tuple[str, str]) -> str:
    if line_name == "InterCityExpress" or line_name == "InterCity":
        return ("#EC0016", "#FFFFFF")
    
    df = pd.read_csv(filename)
    filtered_df = df[df['shortOperatorName'].str.contains('kvv', case=False, na=False)]
    
    result = filtered_df[filtered_df["lineName"] == line_name]
    
    print(line_name, line_name[0:3], line_name[3:])

    try:
        if result.empty:
            if line_name[0:3] == "SEV":
                result = filtered_df[filtered_df["lineName"] == line_name[3:]]
                if result.empty:
                    raise IndexError("Line name not found")
            else: 
                raise IndexError("Line name not found")
        return result["backgroundColor"].array[0], result["textColor"].array[0]
    except IndexError:
        return fallback_colors
    
def get_time_from_now(time: datetime) -> timedelta:
    return time - datetime.now().replace(tzinfo=ZoneInfo("Europe/Berlin"))

def format_platform(platform: str) -> str:
    words = platform.split(" ")
    if len(words) > 1:
        return " ".join(words[1:])
    else:
        return platform

def get_departures_from_xml(stop_point_ref: str, tree: ET.ElementTree, all_stations: list[Station], fallback_line_icon_colors: tuple[str, str]) -> list["Departure"]:
    tree_root = tree.getroot()

    # Define namespaces
    ns = {
        'tri': 'http://www.vdv.de/trias',
        'siri': 'http://www.siri.org.uk/siri'
    }

    departures: list[Departure] = []

    for event_result in tree_root.findall('.//tri:StopEventResult', ns):
        if event_result.find('.//tri:StopPointRef', ns).text.startswith(stop_point_ref):
            event = event_result.find('tri:StopEvent', ns)
            
            # Get departure times
            planned_time = datetime.fromisoformat(event.find('.//tri:ServiceDeparture/tri:TimetabledTime', ns).text)
            try:
                estimated_time = datetime.fromisoformat(event.find('.//tri:ServiceDeparture/tri:EstimatedTime', ns).text)
            except Exception:
                estimated_time = None

            # Get line name and destination
            published_line_name = event.find('.//tri:PublishedLineName/tri:Text', ns).text
            # TODO: make not hardcoded
            if published_line_name.split(" ")[1] == "SEV":
                line_number = "SEV" + published_line_name.split(" ")[-1]
            elif published_line_name.split(" ")[-1] == "InterCityExpress":
                line_number = "ICE" + published_line_name.split(" ")[1:2]
            elif published_line_name.split(" ")[-1] == "InterCity":
                line_number = "IC" + published_line_name.split(" ")[1:2]
            elif published_line_name.split(" ")[-1] == "Flixbus":
                line_number = "FLX" + published_line_name.split(" ")[-1]
            else: 
                line_number = published_line_name.split(" ")[-1]
            destination = event.find('.//tri:DestinationText/tri:Text', ns).text
            
            # platform
            try:
                platform = format_platform(event.find('.//tri:PlannedBay/tri:Text', ns).text)
            except AttributeError:
                platform = None
            
            # get stop_point
            for station in all_stations:
                for stop_point in station.stop_points:
                    if stop_point.stop_point_ref == stop_point_ref:
                        departure_station = station
                        departure_stop_point = stop_point
            
            # mode
            mode = event.find('.//tri:Mode/tri:PtMode', ns).text

            # Get colors from github table
            background_color, text_color = get_line_color(line_number, "line-colors.csv", fallback_line_icon_colors)

            departure = Departure(
                line_number=line_number,
                destination=destination,
                platform=platform,
                station=departure_station,
                stop_point=departure_stop_point,
                mode=mode,
                background_color=background_color,
                text_color=text_color,
                planned_time=planned_time,
                estimated_time=estimated_time
            )

            departures.append(departure)

    return departures

def get_departures_for_window(window: "Window", all_departures: list[Departure]):
    window_departures: list[Departure] = []
    
    for departure in all_departures:
        if departure.station == window.station:
            window_departures.append(departure)
            
    return window_departures
