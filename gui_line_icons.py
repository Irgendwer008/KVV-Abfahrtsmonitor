from PIL import Image, ImageDraw, ImageFont, ImageTk
from typing import Literal


class LineIcons:
    def __init__(self):
        self.icon_cache: dict[str, ImageTk.PhotoImage] = {}

    def get_icon(self,
                 mode: Literal["all", "unknown", "air", "bus", "trolleyBus", "tram", "coach", "rail", "intercityRail", "urbanRail", "metro", "water", "cable-way", "funicular", "taxi"],
                 width,
                 height,
                 radius,
                 text,
                 background_color,
                 icon_color,
                 text_color,
                 font) -> ImageTk.PhotoImage:

        if text in self.icon_cache:
            return self.icon_cache[text]

        img = self._create_icon(mode, width, height, radius, text, background_color, icon_color, text_color, font)
        photo = ImageTk.PhotoImage(img)
        self.icon_cache[text] = photo
        return photo

    def _create_icon(self,
                     mode,
                     width,
                     height,
                     radius,
                     text,
                     background_color,
                     icon_color,
                     text_color,
                     font) -> Image:

        if mode == "rail":
            return self._create_rounded_label(width, height, radius, text, background_color, icon_color, text_color, font)
        elif mode == "tram":
            return self._create_square_label(width, height, text, background_color, icon_color, text_color, font)
        #elif mode == "bus":
        #    return self._create_circle_label(parent, width/2, text, background_color, icon_color, text_color, font)
        else:
            return self._create_hexagon_label(width, height, text, background_color, icon_color, text_color, font)

    def _create_base_image(self, width, height, background_color) -> Image:
        return Image.new("RGBA", (width, height), (0, 0, 0, 0))

    def _draw_text_centered(self, draw, width, height, text, font, fill):
        try:
            pil_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font[1])
        except:
            pil_font = ImageFont.load_default()

        
        ascent, descent = pil_font.getmetrics()
        # Total font height
        total_height = ascent + descent

        bbox = draw.textbbox((0, 0), text, font=pil_font)
        text_width = bbox[2] - bbox[0]

        x = (width - text_width) / 2
        # Adjust y to center the baseline vertically inside the image
        y = (height - total_height) / 2

        draw.text((x, y), text, font=pil_font, fill=fill)

    def _create_rounded_label(self, width, height, radius, text, background_color, icon_color, text_color, font) -> Image:
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)

        draw.rectangle([radius, 0, width - radius, height], fill=icon_color)
        draw.rectangle([0, radius, width, height - radius], fill=icon_color)

        draw.pieslice([0, 0, 2 * radius, 2 * radius], 180, 270, fill=icon_color)
        draw.pieslice([width - 2 * radius, 0, width, 2 * radius], 270, 360, fill=icon_color)
        draw.pieslice([0, height - 2 * radius, 2 * radius, height], 90, 180, fill=icon_color)
        draw.pieslice([width - 2 * radius, height - 2 * radius, width, height], 0, 90, fill=icon_color)

        self._draw_text_centered(draw, width, height, text, font, text_color)
        return img

    def _create_square_label(self, width, height, text, background_color, icon_color, text_color, font) -> Image:
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, width, height], fill=icon_color)
        self._draw_text_centered(draw, width, height, text, font, text_color)
        return img

    def _create_hexagon_label(self, width, height, text, background_color, icon_color, text_color, font) -> Image:
        width = max(int(width), int(height * 5 / 4))
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)

        points = [
            (height / 3, 0),
            (width - height / 3, 0),
            (width, height / 2),
            (width - height / 3, height),
            (height / 3, height),
            (0, height / 2)
        ]
        draw.polygon(points, fill=icon_color)
        self._draw_text_centered(draw, width, height, text, font, text_color)
        return img
