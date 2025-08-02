from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font as tkfont
from datetime import datetime, timedelta

from data_classes import Departure, get_time_from_now

class Window:
    def __init__(self, windowconfig):
        self.window = tk.Toplevel()
        self.window.geometry(f"{windowconfig['width']}x{windowconfig['height']}+{windowconfig['position_x']}+{windowconfig['position_y']}")
        #self.window.attributes("-fullscreen", True)
        self.window.wm_attributes('-type', 'splash')
        self.window.bind("<Control-q>", quit)

        self.stationname = tk.StringVar(value="Z10 Abfahrtsmonitor")
        
        self.icons = {
            "stop": ImageTk.PhotoImage(Image.open("images/stop_icon.png").resize((60, 60))),
        }

        self.headerframe = tk.Frame(self.window, height=80, background="orange")
        self.headerframe.pack(side="top", fill="x", expand=False, anchor="n")

        self.stopiconlabel = tk.Label(self.headerframe, image=self.icons["stop"], bg="orange")
        self.stopiconlabel.pack(side="left", padx=10, pady=10)
        
        self.stationlabel = tk.Label(self.headerframe, textvariable=self.stationname, font=("lucida", 40), anchor="w", justify="left", bg="orange")
        self.stationlabel.pack(side="left", padx=10, pady=10)

        self.timelabel = tk.Label(self.headerframe, text="", font=("lucida", 40), anchor="w", justify="right", bg="orange")
        self.timelabel.pack(side="right", padx=20, pady=20)
        def time():
            string = datetime.now().strftime('%H:%M:%S %p')
            self.timelabel.config(text=string)
            self.timelabel.after(1000, time)
        time()
        
        self.departuresframe = tk.Frame(self.window)
        self.departuresframe.pack(side="top", fill="both", anchor="n", expand=True)

        self.departure_entries: list[Departure_Entry] = []
        
    #def refresh

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