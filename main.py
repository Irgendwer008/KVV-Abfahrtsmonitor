from datetime import timedelta, datetime
import pandas as pd
import tkinter as tk
import tkinter.font as tkfont
import xml.etree.ElementTree as ET
import yaml

from data_classes import Station, StopPoint, Departure, get_departures_from_xml
from gui import Window
from KVV import KVV

#TODO: handle empty departures

# optional
#TODO: situation banner
#TODO: QR-code to repo

def error(*args):
    print("ERROR!\n\n", *args)

# Import config 
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    
windows_config = config["windows"]
stations_config = config["stations"]
credentials_config = config["credentials"]

kvv = KVV(url=credentials_config["url"], requestor_ref=credentials_config["requestor_ref"])

# Init GUI windows
root = tk.Tk()
root.withdraw()

default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="liberation sans", size=60)

def create_windows_from_config() -> None:

    for window_config in windows_config:
        
        stop_points: list[StopPoint] = []
        
        for stop_point in stations_config[window_config["station"]]:
            stop_points.append(StopPoint(stop_point["stop_point_ref"], stop_point["prefix"], stop_point["suffix"]))
        
        station = Station(window_config["station"], stop_points)
        
        all_stations.append(station)
        windows.append(Window(window_config, station))

all_stations: list[Station] = []
windows: list[Window] = []
create_windows_from_config()

# Gather a list of all needed stop points, so that if two windoes use the same station the station's stop points don't have to get requested twice from the API
all_stop_points: list[StopPoint] = []
for window in windows:
    for stop_point in window.station.stop_points:
        if stop_point not in all_stop_points:
            all_stop_points.append(stop_point)

def update_data():
    # Get the current list of departures from all occuring stations
    departures: list[Departure] = []
    tree = ET.parse("response.xml")
    for stop_point in all_stop_points:
        #response = kvv.get(stop_point.stop_point_ref, number_of_results=4)
        try:
            #tree = ET.ElementTree(ET.fromstring(response))
            departures.extend(get_departures_from_xml(stop_point.stop_point_ref, tree, all_stations))
        except Exception as e:
            error(e) #error(e, f"\nresponse:\n{response}")
    
    # Gather a list of all departures for any one window and populate it
    for window in windows:
        window_departures: list[Departure] = []
        for departure in departures:
            if departure.station == window.station:
                window_departures.append(departure)
        
        window.refresh(window_departures)
    
update_data()

# Parse XML from file
#response = 'response.xml'
#tree = ET.parse(response)

root.mainloop()