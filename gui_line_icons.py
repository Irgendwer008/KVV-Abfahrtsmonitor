import tkinter as tk
from typing import Literal

def create_icon(parent, 
                mode: Literal["all", "unknown", "air", "bus", "trolleyBus", "tram", "coach", "rail", "intercityRail", "urbanRail", "metro", "water", "cable-way", "funicular", "taxi"],
                width,
                height,
                radius,
                text,
                background_color,
                icon_color,
                text_color,
                font) -> tk.Canvas:
    
    if mode == "rail":
        return create_rounded_label(parent, width, height, radius, text, background_color, icon_color, text_color, font)
    elif mode == "tram":
        return create_square_label(parent, width, height, text, background_color, icon_color, text_color, font)
    #elif mode == "bus":
    #    return create_circle_label(parent, width/2, text, background_color, icon_color, text_color, font)
    else:
        return create_hexagon_label(parent, width, height, text, background_color, icon_color, text_color, font)

def create_rounded_label(parent, width, height, radius, text, background_color, icon_color, text_color, font) -> tk.Canvas:
    # Create Canvas
    canvas = tk.Canvas(parent, width=width, height=height, bg=background_color, highlightthickness=0)
    
    # Draw rounded rectangle
    canvas.create_arc(0, 0, 2*radius, 2*radius, start=90, extent=90, fill=icon_color, outline=icon_color)
    canvas.create_arc(width - 2*radius, 0, width, 2*radius, start=0, extent=90, fill=icon_color, outline=icon_color)
    canvas.create_arc(0, height - 2*radius, 2*radius, height, start=180, extent=90, fill=icon_color, outline=icon_color)
    canvas.create_arc(width - 2*radius, height - 2*radius, width, height, start=270, extent=90, fill=icon_color, outline=icon_color)
    
    # Draw center rectangles
    canvas.create_rectangle(radius, 0, width - radius, height, fill=icon_color, outline=icon_color)
    canvas.create_rectangle(0, radius, width, height - radius, fill=icon_color, outline=icon_color)

    # Add the text
    canvas.create_text(width // 2, height // 2, text=text, fill=text_color, font=font)

    return canvas

def create_square_label(parent, width, height, text, background_color, icon_color, text_color, font) -> tk.Canvas:
    # Create Canvas
    canvas = tk.Canvas(parent, width=width, height=height, bg=background_color, highlightthickness=0)
    
    # Draw rectangle
    canvas.create_rectangle(0, 0, width, height, fill=icon_color, outline=icon_color)

    # Add the text
    canvas.create_text(width // 2, height // 2, text=text, fill=text_color, font=font)

    return canvas


def create_circle_label(parent, radius, text, background_color, icon_color, text_color, font) -> tk.Canvas:
    # Create Canvas
    canvas = tk.Canvas(parent, width=radius, height=radius, bg=background_color, highlightthickness=0)
    
    # Draw circle
    canvas.create_oval(0, 0, 2*radius, 2*radius, fill=icon_color, outline=icon_color)

    # Add the text
    canvas.create_text(radius // 2, radius // 2, text=text, fill=text_color, font=font)

    return canvas

def create_hexagon_label(parent, width, height, text, background_color, icon_color, text_color, font) -> tk.Canvas:
    
    width = max(width, height * 5 / 4)
    
    # Create Canvas
    canvas = tk.Canvas(parent, width=width, height=height, bg=background_color, highlightthickness=0)
    
    # Draw hexagon
    points = [height/3, 0,              # Top left
              width-height/3, 0,        # Top right
              width, height/2,          # Right
              width-height/3, height,   # Bottom right
              height/3, height,         # Bottom left
              0, height/2]              # Left
    
    canvas.create_polygon(points, fill=icon_color, outline=icon_color)

    # Add the text
    canvas.create_text(width // 2, height // 2, text=text, fill=text_color, font=font)

    return canvas