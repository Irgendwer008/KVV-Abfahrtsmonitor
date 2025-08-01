import ttkbootstrap as ttk

root = ttk.Window(title = "KVV Abfahrtsmonitor", themename = "darkly")
root.withdraw()

w0, h0 = 2000, 2000
w1, h1 = 200, 100

window0 = ttk.Toplevel()
window0.geometry(f"{w0}x{h0}+0+0")
window0.attributes("-fullscreen", True)
window0.bind("<Control-q>", quit)

window1 = ttk.Toplevel()
window1.geometry(f"{w1}x{h1}+{w0}+{h0}")
window1.attributes("-fullscreen", True)
window1.bind("<Control-q>", quit)

root.mainloop()