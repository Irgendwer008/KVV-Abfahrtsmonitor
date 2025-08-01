import ttkbootstrap as ttk

class Window:
    def __init__(self, windowconfig):
        self.window = ttk.Toplevel()
        self.window.geometry(f"{windowconfig['width']}x{windowconfig['height']}+{windowconfig['position_x']}+{windowconfig['position_y']}")
        #self.window.attributes("-fullscreen", True)
        self.window.wm_attributes('-type', 'splash')
        self.window.bind("<Control-q>", quit)