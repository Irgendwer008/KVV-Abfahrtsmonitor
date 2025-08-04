from datetime import datetime
from PIL import Image, ImageTk
import pyqrcode
import tkinter as tk

from data_classes import Station, Departure
from helper_functions import get_time_from_now
from gui_line_icons import LineIcons

class Window:
    @staticmethod
    def create_windows(windows_config: list, all_stations: dict[Station], icon_handler: LineIcons, colors_config: dict, general_config: dict) -> list["Window"]:
        windows: list[Window] = []
        
        
        for window_config in windows_config:
            for station in all_stations:
                if station.name == window_config["station"]:
                    break
            windows.append(Window(window_config, station, icon_handler, colors_config, general_config))
        
        return windows

    def __init__(self, window_config: dict, station: Station, icon_handler: LineIcons, colors_config: dict[str], general_config: dict, number_of_departure_entries: int = 10):
        
        self.station = station
        self.icon_handler = icon_handler
        self.general_config = general_config
        self.colors_config = colors_config
        self.number_of_departure_entries=number_of_departure_entries
        
        window = tk.Toplevel()
        self.window = window
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

        self.headerframe = tk.Frame(window, background=self.colors_config["header_background"])
        self.headerframe.place(anchor="nw", x=0, y=0, height=header_height, width=self.width)

        self.stopiconlabel = tk.Label(self.headerframe, image=self.icons["stop"], bg=self.colors_config["header_background"])
        self.stopiconlabel.pack(side="left", padx=self.padding_size, pady=self.padding_size)
        
        self.stationlabel = tk.Label(self.headerframe, textvariable=self.stationname, font=self.header_font, anchor="w", justify="left", fg=self.colors_config["header_text"], bg=self.colors_config["header_background"])
        self.stationlabel.pack(side="left", padx=self.padding_size)

        self.timelabel = tk.Label(self.headerframe, text="", font=self.header_font, anchor="w", justify="right", fg=self.colors_config["header_text"], bg=self.colors_config["header_background"])
        self.timelabel.pack(side="right", padx=self.padding_size)
        
        def time():
            string = datetime.now().strftime('%H:%M:%S')
            self.timelabel.config(text=string)
            self.timelabel.after(1000, time)
        
        time()
        
        self.qr_code = QRCodeLabel(self.headerframe, header_height, general_config["QR-Code-content"], self.colors_config["qr_code_background"], self.colors_config["qr_code_foregreound"])
        self.qr_code.configure(height=header_height, width=header_height)
        self.qr_code.pack(side="right")
        self.qr_code.pack_propagate(0)
        
        self.departuresframe = tk.Frame(window)
        self.departuresframe.place(x=0, y=header_height, height=self.height-header_height, width=self.width)

        self.departure_entries: list[Departure_Entry] = []
        
        self.departure_entries.append(Departure_Entry_Header(self))
        
        for i in range(number_of_departure_entries):
            self.departure_entries.append(Departure_Entry(self))
        
    def refresh(self, departures: list[Departure] | None):
        
        departures.sort(key=lambda x: (x.estimated_time if x.estimated_time is not None else x.planned_time))
        
        #TODO: handle no departures
        if len(departures) < 1 or departures is None:
            return
        
        for i in range(len(departures)):
            self.departure_entries[i + 1].update(departures[i], self.icon_handler, i)
            if i + 1 >= self.number_of_departure_entries:
                break
    
        for departure_entry in self.departure_entries[i + 2:]:
            departure_entry.clear(i)

class Departure_Entry:
    def __init__(self, window: Window):
        self.window = window
        self.height = window.departure_entry_height
        self.padding = int(self.height / 8)
        self.font = window.departure_entry_font
        background = self.window.colors_config["departure_entry_lighter"]
        text_color = self.window.colors_config["departure_entry_text"]
        
        # Create tkVars
        self.destination_var = tk.StringVar()
        self.platform_var = tk.StringVar()
        self.time_text_var = tk.StringVar()

        # Create the departure entry frame and its content
        self.frame = tk.Frame(window.departuresframe, bg=background, height=self.height)
        self.frame.pack(side="top", fill="x", ipadx=self.padding*2)
        self.frame.pack_propagate(0)

        self.destination_label = tk.Label(self.frame, textvariable=self.destination_var, fg=text_color, bg=background, font=self.font)
        self.destination_label.place(anchor="w", x=2*self.height, rely=0.5, relheight=0.8)
        
        self.platform_label = tk.Label(self.frame, textvariable=self.platform_var, fg=text_color, bg=background, font=self.font)
        self.platform_label.place(anchor="center", relx=0.8, rely=0.5, relheight=0.8)

        self.time_label = tk.Label(self.frame, textvariable=self.time_text_var, fg=text_color, bg=background, font=self.font)
        self.time_label.place(anchor="e", x=window.width-self.padding, rely=0.5, relheight=0.8)
        
        self.line_icon_label = tk.Label(self.frame, bg=background)
        self.line_icon_label.place(anchor="center", x=self.height, rely=0.5)
    
    def update(self, departure: Departure, icon_handler: LineIcons, index: int):
        
        if index % 2:
            background = self.window.colors_config["departure_entry_darker"]
        else:
            background = self.window.colors_config["departure_entry_lighter"]
            
        self.frame.configure(background=background)
        self.destination_label.configure(background=background)
        self.platform_label.configure(background=background)
        self.time_label.configure(background=background)

        # Choose estimated time if one is available, otherwise use planned time
        if departure.estimated_time is None:
            time_shown = departure.planned_time
        else:
            time_shown = departure.estimated_time
            
        timedelta = get_time_from_now(time_shown, self.window.general_config["time_zone"])
        seconds = timedelta.total_seconds()

        # Format the time string based on the remaining time scale
        if seconds < 60:
            time_str = "Jetzt"
        elif seconds < 3600:
            time_str = f"{int(seconds // 60)} min"
        else:
            time_str = f"{int(seconds // 3600)} h {int((seconds % 3600) // 60)} min"

        # Scalar for general size appearance of icon size
        icon_scale = 0.8

        # Preprocess line number
        text = departure.line_number
        if text == "InterCityExpress": text = "ICE"
        if text == "InterCity": text = "IC"
        # Some black magic to make nice icon dimension while being adaptive to line number length
        icon_width = int(icon_scale * (self.height * (text.__len__()*0.4) + 2.5 * self.padding))
        icon_height = int(icon_scale * (self.height - 2* self.padding))
        
        # Create the icon (-> gui_line_icons.py)
        self.line_icon_label.configure(image=icon_handler.get_icon(departure.mode, icon_width, icon_height, int((icon_height) / 4), text, background, departure.background_color, departure.text_color, self.font), background=background)

        # Platform formatting stuff
        prefix = departure.stop_point.prefix if departure.stop_point.prefix is not None else ""
        suffix = departure.stop_point.suffix if departure.stop_point.suffix is not None else ""
        platform_text = (prefix + " " + departure.platform + " " + suffix) if departure.platform is not None else (prefix + " N/A " + suffix)
        
        # Update tkVars
        self.destination_var.set(departure.destination)
        self.platform_var.set(platform_text)
        self.time_text_var.set(time_str)
        
    def clear(self, index: int):
        self.line_icon_label.destroy()
        self.destination_var.set("")
        self.platform_var.set("")
        self.time_text_var.set("")
        
        if index % 2:
            self.frame.configure(background=self.window.colors_config["departure_entry_darker"])
        else:
            self.frame.configure(background=self.window.colors_config["departure_entry_lighter"])
        
class Departure_Entry_Header(Departure_Entry):
    def __init__(self, window: Window):
        
        header_font = (window.departure_entry_font[0], int(window.departure_entry_font[1] / 2))
        
        height = window.departure_entry_height / 2
        padding = int(height / 8)
        
        background = window.colors_config["departure_entry_darker"]
        text_color = window.colors_config["departure_entry_text"]

        # Create the departure entry frame and its content
        frame = tk.Frame(window.departuresframe, bg=background, height=height)
        frame.pack(side="top", fill="x", ipadx=padding*2)
        frame.pack_propagate(0)

        line_icon = tk.Label(frame, text="Linie", fg=text_color, bg=background, font=header_font)
        line_icon.place(anchor="center", x=2 * height, rely=0.5)

        destination_label = tk.Label(frame, text="Richtung", fg=text_color, bg=background, font=header_font)
        destination_label.place(anchor="w", x=4*height, rely=0.5, relheight=0.8)

        platform_label = tk.Label(frame, text="Gleis / Bstg.", fg=text_color, bg=background, font=header_font)
        platform_label.place(anchor="center", relx=0.8, rely=0.5, relheight=0.8)

        time_label = tk.Label(frame, text="Ankunft", fg=text_color, bg=background, font=header_font)
        time_label.place(anchor="e", x=window.width-padding, rely=0.5, relheight=0.8)
     
# https://stackoverflow.com/questions/57128265/qrcode-displaying-in-tkinter-gui-python   
class QRCodeLabel(tk.Label):
    def __init__(self, parent, size: int, qr_data, background: str, foreground: str):
        super().__init__(parent)
        
        qrcode = pyqrcode.create(qr_data)
        tmp_png_file = "images/QRCode.png"        
        qrcode.png(tmp_png_file, scale=1, quiet_zone=2, background=(int(background[1:3], 16), int(background[3:5], 16), int(background[5:7], 16), 255), module_color=(int(foreground[1:2], 16), int(foreground[3:4], 16), int(foreground[4:5], 16), 255))
        
        self.original = Image.open(tmp_png_file)
        resized = self.original.resize((size, size))
        
        self.image = ImageTk.PhotoImage(resized)
        
        self.configure(image=self.image)