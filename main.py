from log import logger

import tkinter as tk
import tkinter.font as tkfont
import xml.etree.ElementTree as ET

from config import Config
from data_classes import Station, StopPoint, Departure
from gui import Window
from gui_line_icons import LineIcons
from helper_functions import create_stations, \
                             get_all_used_stoppoints, \
                             download_line_color_list, \
                             get_departures_from_xml, \
                             get_departures_for_window
from KVV import KVV
#TODO: handle empty departures
#TODO: handle http errors
#TODO: popup window for error handling
#TODO: extensive comments
#TODO: make icon drawer use text box size for icon width adaptation

# optional
#TODO: Add custom file names
#TODO: situation banner
#TODO: no hardcoded string

logger.info("starting KVV-Abfahrtsmonitore...")

# Get config from config file and check it for integrity
config = Config()

# Init KVV API handler
kvv = KVV(url=config.credentials["url"], requestor_ref=config.credentials["requestor_ref"])

# Init Icon handler
icons = LineIcons()

# Init GUI windows
root = tk.Tk()

default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="liberation sans", size=60)

# Init all windows and stations from config
stations: dict[Station] = create_stations(config.stations)
windows: list[Window] = Window.create_windows(config, stations, icons)
root.withdraw()

# Gather a list of all needed stop points, so that if two windoes use the same station the station's stop points don't have to get requested twice from the API
all_stop_points: list[StopPoint] = get_all_used_stoppoints(windows)

def update_departure_entries():
    # Get the current list of departures from all occuring stations
    all_departures: list[Departure] = []
    #tree = ET.parse("response.xml")
    for stop_point in all_stop_points:
        response = kvv.get(stop_point.stop_point_ref, number_of_results=10)
        try:
            tree = ET.ElementTree(ET.fromstring(response))
            all_departures.extend(get_departures_from_xml(stop_point.stop_point_ref, tree, stations, (config.colors["default_icon_background"], config.colors["default_icon_text"]), config.general["SEV-lines use normal line icon colors"]))
        except Exception as e:
            logger.exception("error in creating departures from xml tree", stack_info=True)
    
    # Gather a list of all departures for any one window and populate it
    for window in windows:
        window_departures = get_departures_for_window(window, all_departures)
        window.refresh(window_departures)
    
    root.after(30000, update_departure_entries)

def update_data():
    # Donwload latest line colors for use in line icons
    if download_line_color_list("line-colors.csv"):
        icons.icon_cache.clear() # (Only) clear old icons if new line colors could be downloaded.
    
    root.after(300000, update_data) # Update daily: 86400000ms
    
update_data()
update_departure_entries()

root.mainloop()