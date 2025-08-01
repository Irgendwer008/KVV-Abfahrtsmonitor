from datetime import timedelta
import tkinter as tk
import yaml

from gui import Window
from KVV import get as get_kvv_data

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

root = tk.Tk()
root.withdraw()

windows = []

for window in config["windows"]:
    windows.append(Window(window))

root.mainloop()

# response = get_kvv_data(config["credentials"]["url"], config["credentials"]["requestor_ref"], "de:08212:3", 8, timedelta(minutes=0))
# 
# print("Status code:", response.status_code)
# print("Headers:", response.headers)
# print("Raw response:")
# print(response.text)
# 
# with open("response.xml", "w") as file:
#     file.write(response.content.decode('utf-8'))