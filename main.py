from datetime import timedelta, datetime
import pandas as pd
import tkinter as tk
import tkinter.font as tkfont
import yaml

from gui import Window, Departure_Entry
from KVV import get as get_kvv_data




import xml.etree.ElementTree as ET

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Parse the XML
#response = 'response.xml'
#tree = ET.parse(response)
response = get_kvv_data(config["credentials"]["url"], config["credentials"]["requestor_ref"], "de:08212:3", 8, timedelta(minutes=4)).content.decode('utf-8')
tree = ET.ElementTree(ET.fromstring(response))

root = tk.Tk()
root.withdraw()

default_font = tkfont.nametofont("TkDefaultFont")
default_font.configure(family="liberation sans", size=60)

windows: list[Window] = []

for window in config["windows"]:
    windows.append(Window(window))

window = windows[0]
    
    departure = Departure_Entry(window.departuresframe, )

    window.departure_entries.append(departure)

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