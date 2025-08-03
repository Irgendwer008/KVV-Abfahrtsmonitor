from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime, timedelta

from abc import abstractmethod
from data_classes import Station, Departure
from gui_line_icons import create_icon
from helper_functions import get_time_from_now

class Window:
    @abstractmethod
    def create_windows(windows_config: list, all_stations: dict[Station]) -> list["Window"]:
        windows: list[Window] = []
        
        
        for window_config in windows_config:
            for station in all_stations:
                if station.name == window_config["station"]:
                    break
            windows.append(Window(window_config, station))
        
        return windows

    def __init__(self, window_config: dict, station: Station, number_of_departure_entries: int = 8):
        
        self.number_of_departure_entries=number_of_departure_entries
        
        self.station = station
        
        window = tk.Toplevel()
        window.geometry(f"{window_config['width']}x{window_config['height']}+{window_config['position_x']}+{window_config['position_y']}")
        #window.attributes("-fullscreen", True)
        window.wm_attributes('-type', 'splash')
        window.bind("<Control-q>", quit)
        
        self.height = window_config["height"]
        self.width = window_config["width"]
        
        header_height = int(self.height / 12)
        departure_frame_height = self.height - header_height
        self.departure_entry_height = int(((departure_frame_height) / (number_of_departure_entries * 2 + 1)) * 2)
        self.padding_size = int(self.height / 75)
        self.header_font = ("liberation sans", int(self.height / 25))
        self.departure_entry_font = ("liberation sans", int(self.height / 25))

        self.stationname = tk.StringVar(value=self.station.name)
        
        self.icons = {
            "stop": ImageTk.PhotoImage(Image.open("images/stop_icon.png").resize((int(header_height - 2 * self.padding_size), int(header_height - 2 * self.padding_size)))),
        }

        self.headerframe = tk.Frame(window, background="orange")
        self.headerframe.place(anchor="nw", x=0, y=0, height=header_height, width=self.width)

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
        self.departuresframe.place(x=0, y=header_height, height=self.height-header_height, width=self.width)

        self.departure_entries: list[Departure_Entry] = []
        
        self.departure_entries.append(Departure_Entry_Header(self))
        
    def refresh(self, departures: list[Departure] | None):
        
        departures.sort(key=lambda x: (x.estimated_time if x.estimated_time is not None else x.planned_time))    
        
        for child in self.departuresframe.winfo_children()[1:]:
            child.destroy()
        
        if len(departures) < 1 or departures is None:
            return
        
        self.departure_entries.clear()

        for departure in departures:
            self.departure_entries.append(Departure_Entry(self, departure, len(self.departure_entries)))
            if len(self.departure_entries) >= self.number_of_departure_entries:
                break
            
        
        for departure_entry in self.departure_entries[1:]:
            departure_entry.frame.pack(side="top", fill="x", ipadx=departure_entry.padding*2)
            departure_entry.frame.pack_propagate(0)
        
        if len(self.departure_entries) % 2:
            background = "white"
        else:
            background = "#EEEEEE"
        
        self.departuresframe.configure(background=background)

class Departure_Entry:
    def __init__(self, window: Window, departure: Departure, index: int):
        
        height = window.departure_entry_height
        padding = int(height / 8)
        
        self.padding = padding
        
        if index % 2:
            background = "#EEEEEE"
        else:
            background = "white"

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
        self.frame = tk.Frame(window.departuresframe, bg=background, height=height)
        self.frame.pack(side="top", fill="x", ipadx=padding*2)
        self.frame.pack_propagate(0)

        # Scalar for general size appearance of icon size
        icon_scale = 0.8

        # Some black magic to make nice icon dimension while being adaptive to line number length
        icon_width = int(icon_scale * (height * (departure.line_number.__len__()*0.4) + 2.5 * padding))
        icon_height = int(icon_scale * (height - 2* padding))
        # Create the icon (-> gui_line_icons.py)
        line_icon = create_icon(self.frame, departure.mode, icon_width, icon_height, int((icon_height) / 4), departure.line_number, background, departure.background_color, departure.text_color, window.departure_entry_font)
        line_icon.place(anchor="center", x=height, rely=0.5)

        destination_label = tk.Label(self.frame, text=departure.destination, bg=background, font=window.departure_entry_font)
        destination_label.place(anchor="w", x=2*height, rely=0.5, relheight=0.8)

        # Platform formatting stuff
        prefix = departure.stop_point.prefix if departure.stop_point.prefix is not None else ""
        suffix = departure.stop_point.suffix if departure.stop_point.suffix is not None else ""
        platform_text = (prefix + departure.platform + suffix) if departure.platform is not None else ""
        
        platform_label = tk.Label(self.frame, text=platform_text, bg=background, font=window.departure_entry_font)
        platform_label.place(anchor="center", relx=0.8, rely=0.5, relheight=0.8)

        time_value = tk.Label(self.frame, text=time_str, bg=background, font=window.departure_entry_font)
        time_value.place(anchor="e", x=window.width-padding, rely=0.5, relheight=0.8)

class Departure_Entry_Header(Departure_Entry):
    def __init__(self, window: Window):
        
        header_font = (window.departure_entry_font[0], int(window.departure_entry_font[1] / 2))
        
        height = window.departure_entry_height / 2
        padding = int(height / 8)
        
        background = "#EEEEEE"

        # Create the departure entry frame and its content
        frame = tk.Frame(window.departuresframe, bg=background, height=height)
        frame.pack(side="top", fill="x", ipadx=padding*2)
        frame.pack_propagate(0)

        line_icon = tk.Label(frame, text="Linie", bg=background, font=header_font)
        line_icon.place(anchor="center", x=2 * height, rely=0.5)

        destination_label = tk.Label(frame, text="Richtung", bg=background, font=header_font)
        destination_label.place(anchor="w", x=4*height, rely=0.5, relheight=0.8)

        platform_label = tk.Label(frame, text="Gleis / Bstg.", bg=background, font=header_font)
        platform_label.place(anchor="center", relx=0.8, rely=0.5, relheight=0.8)

        time_value = tk.Label(frame, text="Ankunft", bg=background, font=header_font)
        time_value.place(anchor="e", x=window.width-padding, rely=0.5, relheight=0.8)