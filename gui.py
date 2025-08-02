from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime, timedelta

from data_classes import Station, Departure, get_time_from_now
from gui_line_icons import create_icon

class Window:
    def __init__(self, window_config: dict, station: Station):
        
        self.station = station
        
        window = tk.Toplevel()
        window.geometry(f"{window_config['width']}x{window_config['height']}+{window_config['position_x']}+{window_config['position_y']}")
        #window.attributes("-fullscreen", True)
        window.wm_attributes('-type', 'splash')
        window.bind("<Control-q>", quit)
        
        self.height = window_config["height"]
        self.width = window_config["width"]
        
        header_height = int(self.height / 15)
        self.departure_entry_height = int(self.height / 10)
        self.padding_size = int(self.height / 75)
        self.header_font = ("liberation sans", int(self.height / 25))
        self.departure_entry_font = ("liberation sans", int(self.height / 25))

        self.stationname = tk.StringVar(value=self.station.name)
        
        self.icons = {
            "stop": ImageTk.PhotoImage(Image.open("images/stop_icon.png").resize((int(header_height), int(header_height)))),
        }

        self.headerframe = tk.Frame(window, background="orange")
        self.headerframe.pack(side="top", fill="x", expand=False, anchor="n")

        self.stopiconlabel = tk.Label(self.headerframe, image=self.icons["stop"], bg="orange")
        self.stopiconlabel.pack(side="left", padx=self.padding_size, pady=self.padding_size)
        
        self.stationlabel = tk.Label(self.headerframe, textvariable=self.stationname, font=self.header_font, anchor="w", justify="left", bg="orange")
        self.stationlabel.pack(side="left", padx=self.padding_size)

        self.timelabel = tk.Label(self.headerframe, text="", font=self.header_font, anchor="w", justify="right", bg="orange")
        self.timelabel.pack(side="right", padx=self.padding_size)
        def time():
            string = datetime.now().strftime('%H:%M:%S')
            self.timelabel.config(text=string)
            self.timelabel.after(1000, time)
        
        time()
        
        self.departuresframe = tk.Frame(window)
        self.departuresframe.pack(side="top", fill="both", anchor="n", expand=True)

        self.departure_entries: list[Departure_Entry] = []
        
    def refresh(self, departures: list[Departure] | None):
        for child in self.departuresframe.winfo_children():
            child.destroy()
        
        if departures.__len__() < 1 or departures is None:
            return
        
        self.departure_entries.clear()

        for departure in departures:
            self.departure_entries.append(Departure_Entry(self, departure, self.departure_entries.__len__()))

class Departure_Entry:
    def __init__(self, window: Window, departure: Departure, index: int):
        
        height = window.departure_entry_height
        padding = int(height / 8)
        
        if index % 2:
            background = "white"
        else:
            background = "#EEEEEE"

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
        frame = tk.Frame(window.departuresframe, bg=background, height=height)
        frame.pack(side="top", fill="x", ipadx=padding*2, ipady=padding)
        frame.pack_propagate(0)

        icon_width = int(height * (departure.line_number.__len__()*0.4) + 2.5 * padding)
        icon_height = height - 2* padding
        line_icon = create_icon(frame, departure.mode, icon_width, icon_height, int((icon_height) / 4), departure.line_number, background, departure.background_color, departure.text_color, window.departure_entry_font)
        line_icon.place(anchor="center", x=height, rely=0.5)

        destination_label = tk.Label(frame, text=departure.destination, bg=background, font=window.departure_entry_font)
        destination_label.place(anchor="w", x=2*height, rely=0.5, relheight=0.8)

        platform_text = departure.stop_point.prefix + departure.platform + departure.stop_point.suffix if departure.platform is not None else ""
        platform_label = tk.Label(frame, text=platform_text, bg=background, font=window.departure_entry_font)
        platform_label.place(anchor="center", relx=0.8, rely=0.5, relheight=0.8)

        time_value = tk.Label(frame, text=time_str, bg=background, font=window.departure_entry_font)
        time_value.place(anchor="e", x=window.width-padding, rely=0.5, relheight=0.8)