from datetime import timedelta, datetime
import pandas as pd
import tkinter as tk
import tkinter.font as tkfont
import xml.etree.ElementTree as ET
import yaml

from data_classes import Station
from gui import Window, Departure_Entry
from KVV import get as get_kvv_data




# Import config 
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    
windows_config = config["windows"]
stations_config = config["stations"]
credentials_config = config["credentials"]

# Init GUI windows
root = tk.Tk()
root.withdraw()

default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="liberation sans", size=60)

windows: list[Window] = []

for window_config in windows_config:
    
    stop_points = []
    
    for stop_point in stations_config[window_config["station"]]:
        stop_points.append(stop_point)
    
    station = Station(window_config["station"], stop_points)
    
    windows.append(Window(window_config, station))
    
    

# Parse the XML
#response = 'response.xml'
#tree = ET.parse(response)
response = get_kvv_data(credentials_config["url"], credentials_config["requestor_ref"], "de:08212:3", 8, timedelta(minutes=4)).content.decode('utf-8')
tree = ET.ElementTree(ET.fromstring(response))

# response = get_kvv_data(config["credentials"]["url"], config["credentials"]["requestor_ref"], "de:08212:3", 8, timedelta(minutes=0))
# 
# print("Status code:", response.status_code)
# print("Headers:", response.headers)
# print("Raw response:")
# print(response.text)
# 
# with open("response.xml", "w") as file:
#     file.write(response.content.decode('utf-8'))

root.mainloop()