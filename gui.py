from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime, timedelta

from data_classes import Station, Departure, get_time_from_now

class Window:
    def __init__(self, window_config: dict, station: Station):
        
        self.station = station
        
        window = tk.Toplevel()
        window.geometry(f"{window_config['width']}x{window_config['height']}+{window_config['position_x']}+{window_config['position_y']}")
        #window.attributes("-fullscreen", True)
        window.wm_attributes('-type', 'splash')
        window.bind("<Control-q>", quit)
        
        header_height = int(window_config["height"] / 15)
        self.padding_size = int(window_config["height"] / 75)
        self.font = ("liberation sans", int(window_config["height"] / 25))

        self.stationname = tk.StringVar(value=self.station.name)
        
        self.icons = {
            "stop": ImageTk.PhotoImage(Image.open("images/stop_icon.png").resize((int(header_height), int(header_height)))),
        }

        self.headerframe = tk.Frame(window, background="orange")
        self.headerframe.pack(side="top", fill="x", expand=False, anchor="n")

        self.stopiconlabel = tk.Label(self.headerframe, image=self.icons["stop"], bg="orange")
        self.stopiconlabel.pack(side="left", padx=self.padding_size, pady=self.padding_size)
        
        self.stationlabel = tk.Label(self.headerframe, textvariable=self.stationname, font=self.font, anchor="w", justify="left", bg="orange")
        self.stationlabel.pack(side="left", padx=self.padding_size)

        self.timelabel = tk.Label(self.headerframe, text="", font=self.font, anchor="w", justify="right", bg="orange")
        self.timelabel.pack(side="right", padx=self.padding_size)
        def time():
            string = datetime.now().strftime('%H:%M:%S %p')
            self.timelabel.config(text=string)
            self.timelabel.after(1000, time)
        time()
        
        self.departuresframe = tk.Frame(window)
        self.departuresframe.pack(side="top", fill="both", anchor="n", expand=True)

        self.departure_entries: list[Departure_Entry] = []
        
    def refresh(self):
        for child in self.departuresframe.winfo_children():
            child.destroy()

class Departure_Entry:
    def __init__(self, parent, departure: Departure):

        # Choose estimated time if one is available, otherwise use planned time
        if departure.estimated_time is None:
            time_shown = departure.planned_time
        else:
            time_shown = departure.estimated_time
            
        timedelta = get_time_from_now(time_shown)
        seconds = timedelta.total_seconds()

        # Format the time string based on the remaining time scale
        if seconds < 60:
            time_str = "Jetzt"
        elif seconds < 3600:
            time_str = f"{int(seconds // 60)} min"
        else:
            time_str = f"{int(seconds // 3600)} h {int((seconds % 3600) // 60)} min"

        # Create the departure entry frame and its content
        self.frame = tk.Frame(parent, bg="white")
        self.frame.pack(side="top", fill="x", padx=10, pady=(10, 0))

        self.line_label = tk.Label(self.frame, text=departure.line_number, bg=departure.background_color, fg=departure.text_color)
        self.line_label.pack(side="left", padx=5)

        self.destination_label = tk.Label(self.frame, text=departure.destination, bg="white")
        self.destination_label.pack(side="left", padx=5)

        self.time_value = tk.Label(self.frame, text=time_str, bg="white")
        self.time_value.pack(side="left", padx=5)