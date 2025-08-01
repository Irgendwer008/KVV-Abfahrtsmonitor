import ttkbootstrap as ttk

class Display:
    def __init__(self, displayconfig):
        self.window = ttk.Toplevel()
        self.window.geometry(f"{displayconfig['window']['width']}x{displayconfig['window']['height']}+{displayconfig['window']['position_x']}+{displayconfig['window']['position_y']}")
        #self.window.attributes("-fullscreen", True)
        self.window.wm_attributes('-type', 'splash')
        self.window.bind("<Control-q>", quit)