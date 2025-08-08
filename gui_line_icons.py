from PIL import Image, ImageDraw, ImageFont, ImageTk
from typing import Literal


class LineIcons:
    """Class for a line icon handler that creates and caches line icons
    """    
    def __init__(self):
        """Init the cache
        """        
        self.icon_cache: dict[str, ImageTk.PhotoImage] = {}

    def get_icon(self,
                 mode: Literal["all", "unknown", "air", "bus", "trolleyBus", "tram", "coach", "rail", "intercityRail", "urbanRail", "metro", "water", "cable-way", "funicular", "taxi"],
                 width: int,
                 height: int,
                 radius: int,
                 text: str,
                 background_color: str,
                 icon_color: str,
                 text_color: str,
                 font) -> ImageTk.PhotoImage:
        """Get the line icon either from cache or by creating a new one

        Args:
            mode (Literal["all", "unknown", "air", "bus", "trolleyBus", "tram", "coach", "rail", "intercityRail", "urbanRail", "metro", "water", "cablee-way", "funicular", "taxi"]): Mode of transport; used for icon form decision
            width (int): width of icon
            height (int): height of icon
            radius (int): cornerradius of icon, if applicable
            text (str): Text to write in the icon (line number)
            background_color (str): Background color
            icon_color (str): Icon color
            text_color (str): Text color
            font (_Ink): Font to use for line number text

        Returns:
            ImageTk.PhotoImage: returns the requested icon
        """        

        # return icon from cache if icon for this line already exists
        if text in self.icon_cache:
            return self.icon_cache[text]

        # else, create a new icon, save it to the cache and return it
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
        """This function decides, which shape the icon is going to have based on mode of transport

        Args:
            mode (Literal["all", "unknown", "air", "bus", "trolleyBus", "tram", "coach", "rail", "intercityRail", "urbanRail", "metro", "water", "cablee-way", "funicular", "taxi"]): Mode of transport of the line
            width (int): width of the icon
            height (int): height of the icon
            radius (int): cornerraidus of the icon (if applicable)
            text (str): Line number string to be displayed inside the image
            background_color (str): background color hex code
            icon_color (str): icon color hex code
            text_color (str): text color hex code
            font (_Ink): font of the line number

        Returns:
            Image: Image of the created icon
        """        

        if mode == "rail":
            return self._create_rounded_label(width, height, radius, text, background_color, icon_color, text_color, font)
        elif mode == "tram":
            return self._create_square_label(width, height, text, background_color, icon_color, text_color, font)
        elif mode == "bus":
            return self._create_banner_label(width, height, text, background_color, icon_color, text_color, font)
        else:
            return self._create_hexagon_label(width, height, text, background_color, icon_color, text_color, font)

    def _create_base_image(self, width, height, background_color) -> Image:
        """Creates the base image for an icon

        Args:
            width (int): width of the icon
            height (int): height of the icon
            background_color (hex color code): Background color

        Returns:
            Image: Image of the base icon
        """        
        return Image.new("RGBA", (width, height), (0, 0, 0, 0))

    def _draw_text_centered(self, draw: ImageDraw, width: int, height: int, text: str, font, fill):
        try:
            pil_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font[1])
        except:
            pil_font = ImageFont.load_default()

        # Get the ascent and descent of the font to calculate the vertical centering
        ascent, descent = pil_font.getmetrics()
        # Total font height
        total_height = ascent + descent

        # Calculate the bounding box of the text to center it horizontally
        bbox = draw.textbbox((0, 0), text, font=pil_font)
        text_width = bbox[2] - bbox[0]

        # Calculate the x and y position to center the text
        x = (width - text_width) / 2
        y = (height - total_height) / 2

        draw.text((x, y), text, font=pil_font, fill=fill)


    ###############################
    # Icon shape creation methods #
    ###############################
    
    # The following methods create the different shapes of icons

    def _create_rounded_label(self, width, height, radius, text, background_color, icon_color, text_color, font) -> Image:
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)

        # create two overlapping center rectangles
        draw.rectangle([radius, 0, width - radius, height], fill=icon_color)
        draw.rectangle([0, radius, width, height - radius], fill=icon_color)
        # add four pieslices in the corners
        draw.pieslice([0, 0, 2 * radius, 2 * radius], 180, 270, fill=icon_color)
        draw.pieslice([width - 2 * radius, 0, width, 2 * radius], 270, 360, fill=icon_color)
        draw.pieslice([0, height - 2 * radius, 2 * radius, height], 90, 180, fill=icon_color)
        draw.pieslice([width - 2 * radius, height - 2 * radius, width, height], 0, 90, fill=icon_color)

        self._draw_text_centered(draw, width, height, text, font, text_color)
        return img

    def _create_square_label(self, width, height, text, background_color, icon_color, text_color, font) -> Image:
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)
        
        # create one single rectangle
        draw.rectangle([0, 0, width, height], fill=icon_color)
        
        self._draw_text_centered(draw, width, height, text, font, text_color)
        return img

    def _create_hexagon_label(self, width, height, text, background_color, icon_color, text_color, font) -> Image:
        width = max(int(width), int(height * 5 / 4))
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)

        # create a hexagon shape
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

    def _create_banner_label(self, width, height, text, background_color, icon_color, text_color, font) -> Image:
        width = max(int(width), int(height * 5 / 4))
        img = self._create_base_image(width, height, background_color)
        draw = ImageDraw.Draw(img)

        # create a banner shape
        points = [
            (0, 0),
            (width, 0),
            (width - height / 5, height / 2),
            (width, height),
            (0, height),
            (height / 5, height / 2)
        ]
        
        draw.polygon(points, fill=icon_color)
        self._draw_text_centered(draw, width, height, text, font, text_color)
        return img
