from PIL import Image, ImageTk
import tkinter as tk
from datetime import datetime

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
        
        self.stationlabel = tk.Label(self.headerframe, textvariable=self.stationname, font=("Helvetica", 60), anchor="w", justify="left", bg="orange")
        self.stationlabel.pack(side="left", padx=10, pady=10)

        self.timelabel = tk.Label(self.headerframe, text="", font=("Helvetica", 60), anchor="w", justify="right", bg="orange")
        self.timelabel.pack(side="right", padx=20, pady=20)
        def time():
            string = datetime.now().strftime('%H:%M:%S %p')
            self.timelabel.config(text=string)
            self.timelabel.after(1000, time)
        time()
        
        self.departuresframe = tk.Frame(self.window)
        self.departuresframe.pack(side="top", fill="both", anchor="n", expand=True)