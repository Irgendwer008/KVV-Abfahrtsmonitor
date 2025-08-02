from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
from typing import Literal
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET
import yaml
from zoneinfo import ZoneInfo
    
@dataclass
class StopPoint:
    stop_point_ref: str
    prefix: str
    suffix: str
    
@dataclass
class Station:
    name: str
    stop_points: list[StopPoint]

@dataclass
class Departure:
    line_number: str
    destination: str
    platform: str
    station: Station
    stop_point: StopPoint
    mode: Literal["all", "unknown", "air", "bus", "trolleyBus", "tram", "coach", "rail", "intercityRail", "urbanRail", "metro", "water", "cable-way", "funicular", "taxi"]
    background_color: str
    text_color: str
    planned_time: datetime
    estimated_time: datetime | None = None
    

def get_stations_from_config() -> list["Station"]:
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    stations: list[Station] = []
    
    for station in config["stations"]:
        
        stop_points = []
        
        for stop_point in station["stop_points"]:
            stop_points.append(StopPoint(
                stop_point_ref=stop_point,
                prefix=stop_point["prefix"],
                suffix=stop_point["suffix"]
            ))
        
        stations.append(Station(
            name=station["name"],
            stop_points=stop_points
        ))
    
    return stations

def get_hex_color(line_name: str) -> str:
    url = "https://raw.githubusercontent.com/Traewelling/line-colors/refs/heads/main/line-colors.csv"
    
    urlretrieve(url, "line-colors.csv")

    df = pd.read_csv(url)
    filtered_df = df[df['shortOperatorName'].str.contains('kvv', case=False, na=False)]
    
    result = filtered_df[filtered_df["lineName"] == line_name]

    try:
        if result.empty:
            raise IndexError("Line name not found")
        return result["backgroundColor"].array[0], result["textColor"].array[0]
    except IndexError:
        return ("#006EFF", "#FFFFFF")
    
def get_time_from_now(time: datetime) -> timedelta:
    return time - datetime.now().replace(tzinfo=ZoneInfo("Europe/Berlin"))

def format_platform(platform: str) -> str:
    words = platform.split(" ")
    if len(words) > 1:
        return " ".join(words[1:])
    else:
        return platform

def get_departures_from_xml(stop_point_ref: str, tree: ET.ElementTree, all_stations: list[Station]) -> list["Departure"]:
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
            line_number = event.find('.//tri:PublishedLineName/tri:Text', ns).text.split(" ")[-1]
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
            background_color, text_color = get_hex_color(line_number)

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
            
    departures.sort(key=lambda x: (x.estimated_time if x.estimated_time is not None else x.planned_time))      
        

    return departures