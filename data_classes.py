from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

def get_hex_color(line_name: str) -> str:
    url = "https://raw.githubusercontent.com/Traewelling/line-colors/refs/heads/main/line-colors.csv"

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
        return " ".join(words[1:-1])
    else:
        return platform

@dataclass
class Departure:
    line_number: str
    destination: str
    platform: str
    background_color: str
    text_color: str
    planned_time: datetime
    estimated_time: datetime | None = None

def get_departures_from_xml(tree: ET.ElementTree) -> list["Departure"]:
    tree_root = tree.getroot()

    # Define namespaces
    ns = {
        'tri': 'http://www.vdv.de/trias',
        'siri': 'http://www.siri.org.uk/siri'
    }

    departures: list[Departure] = []

    for event_result in tree_root.findall('.//tri:StopEventResult', ns):
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
        platform = format_platform(event.find('.//tri:PlannedBay/tri:Text', ns).text)

        # Get colors from github table
        background_color, text_color = get_hex_color(line_number)

        departure = Departure(
            line_number=line_number,
            platform=platform,
            destination=destination,
            background_color=background_color,
            text_color=text_color,
            planned_time=planned_time,
            estimated_time=estimated_time
        )

        departures.append(departure)

    return departures