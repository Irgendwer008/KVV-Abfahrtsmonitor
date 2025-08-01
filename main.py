import ttkbootstrap as ttk
import yaml

from display import Display

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

root = ttk.Window()
root.withdraw()

for display_config in config["displays"].values():
    display = Display(display_config)

root.mainloop()