#! python3
"""
image-generator.py - Parse colors and generate gradient/solid color wallpaper

Written by Sergey Torshin @torshin5ergey
"""

from typing import Literal, Tuple, List
from random import randint
from PIL import Image


class ParserError(Exception):
    """Custom HueDesk exception.
    For errors in the input color format.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ImageGeneratorError(Exception):
    """Custom HueDesk exception.
    For errors in the image generation process.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def generate_random_colors(count=None) -> List[Tuple[int, int, int]]:
    """Generate a list of random colors.
    
    Args:
        count (int, optional): The number of colors to generate. If not
        specified, a random number between 1 and 4 will be used. (default is None)
        
    Returns:
        colors (List[Tuple[int, int, int]]): A list of tuples representing RGB
                                             colors. Each tuple contains three
                                             integers (0-255).
    """
    colors = []
    if count is None:
        count = randint(1, 4)
    for _ in range(1, count+1):
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        colors.append(color)
    return colors


def parse_color(color: str) -> List[Tuple[int, int, int]]:
    """Parse the color input to a list of RGB tuples.
    
    Args:
        color (str): The color input in R,G,B or #HEX format.
        
    Returns:
        List[Tuple[int, int, int]]: A list of RGB tuples with colors.
        
    Raises:
        ParserError: If the input color format is invalid.
    """
    colors = []  # Output colors list
    color_parts = color.split('-')
    if not (1 <= len(color_parts) <= 4):
        raise ParserError("Invalid color format. Invalid number of colors. "
                          "Should be between 1 and 4.")
    for c in color_parts:
        current_color = c.lstrip('#')
        if ',' in current_color:  # RGB format
            try:
                r, g, b = map(int, current_color.split(','))
                if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                    raise ParserError("Invalid RGB format. Values must be " \
                                      "between 0 and 255.")
                colors.append((r, g, b))
            except ValueError as e:
                raise ParserError("Invalid RGB format. Should be three " \
                                  "integers separated by commas.") from e
        elif len(current_color) in [3, 6]:  # HEX format
            try:
                if len(current_color) == 3:
                    current_color = ''.join([c * 2 for c in current_color])
                r = int(current_color[0:2], 16)
                g = int(current_color[2:4], 16)
                b = int(current_color[4:6], 16)
                colors.append((r, g, b))
            except ValueError as e:
                raise ParserError("Invalid HEX format. " \
                                  "Should be #RGB or #RRGGBB.") from e
        else:
            raise ParserError("Invalid color format. " \
                              "Use R,G,B or #RRGGBB (#RGB).")
    return colors


def create_solid_color_image(width: int, height: int,
                             color: Tuple[int, int, int],
                             output_path: str,
                             mode: Literal['preview', 'generate'] = 'generate'
                             ) -> None:
    """Create and save solid color image.
    
    Args:
        width (int): The width of the image.
        height (int): The height of the iamge.
        color (Tuple[int, int, int]): An RGB color tuple.
        output_path (str): The output path for saving iamge.
        mode (Literal['preview', 'generate'], optional): Processing mode. Defaults to 'generate'.
    
    Returns:
        None: Saves image in the output_path.
    
    Raises:
        ImageGeneratorError: If the image processing mode is invalid.
    """
    max_scaled_width = 1000  # Maximum width for scaled preview
    output_width, output_height = width, height
    if mode == 'preview':
        if width > 1000:
            ratio = max_scaled_width / width
            output_width, output_height = int(width * ratio), int(height * ratio)
    image = Image.new('RGB', (output_width, output_height), color)
    if mode == 'preview':
        image.show()
    elif mode == 'generate':
        image.save(output_path)
    else:
        raise ImageGeneratorError("Invalid image processing mode.")


def create_gradient_color_image(width: int, height: int,
                                colors: List[Tuple[int, int, int]],
                                output_path: str,
                                mode: Literal['preview', 'generate'] = 'generate'
                                ) -> None:
    """Create and save a gradient color image.
    
    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        colors (List[Tuple[int, int, int]]): A list of RGB tuples representing colors.
        output_path (str): The output path for the image.
        mode (Literal['preview', 'generate'], optional): Processing mode. Defaults to 'generate'.
        
    Returns:
        None: Saves image in the output_path.
        
    Raises:
        ImageGeneratorError: If the image processing mode or number of colors is invalid.
    """
    max_scaled_width = 1000  # Maximum width for scaled preview
    output_width, output_height = width, height
    if mode == 'generate':
        output_width, output_height = width, height
    elif mode == 'preview':
        if width > 1000:
            ratio = max_scaled_width / width
            output_width, output_height = int(width * ratio), int(height * ratio)
    num_colors = len(colors)

    image = Image.new('RGB', (width, height))  # Default black image
    if num_colors == 2:
        image = generate_2point_gradient(output_width, output_height, colors)
    elif num_colors == 3:
        image = generate_3point_gradient(output_width, output_height, colors)
    elif num_colors == 4:
        image = generate_4point_gradient(output_width, output_height, colors)

    if mode == 'generate':
        image.save(output_path)
    elif mode == 'preview':
        image.show()
    else:
        raise ImageGeneratorError("Invalid image processing mode.")


def generate_2point_gradient(width: int, height: int,
                             colors: List[Tuple[int, int, int]]):
    """Generate a gradient image with two corner colors.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        colors (List[Tuple[int, int, int]]): A list of two RGB color tuples representing the colors at
                                             the corners of the image in the following order:
                                             top-left, bottom-right.

    Returns:
        Image: An RGB image object with the gradient applied.
    """
    image = Image.new('RGB', (width, height))
    # Assign colors to corners: top-left and bottom-right
    color_tl = colors[0]
    color_br = colors[1]
    # Iterate over each pixel and calculate interpolated colors
    for y in range(height):
        for x in range(width):
            # Calculate the distance from top-left corner to current pixel
            # Total distance from top-left to bottom-right
            distance_tl = (x + y) / (width + height - 2)
            # Interpolate colors from top-left to bottom-right
            r = int(color_tl[0] + distance_tl * (color_br[0] - color_tl[0]))
            g = int(color_tl[1] + distance_tl * (color_br[1] - color_tl[1]))
            b = int(color_tl[2] + distance_tl * (color_br[2] - color_tl[2]))
            image.putpixel((x, y), (r, g, b))
    return image


def generate_3point_gradient(width: int, height: int,
                             colors: List[Tuple[int, int, int]]):
    """Generate a gradient image with three point colors.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        colors (List[Tuple[int, int, int]]): A list of three RGB color tuples representing the colors at
                                             the corners of the image in the following order:
                                             top-left, bottom-left, fullheight-right.

    Returns:
        Image: An RGB image object with the gradient applied.
    """
    image = Image.new('RGB', (width, height))
    # Assign colors to corners: top-left, top-right, bottom-left
    color_tl = colors[0]
    color_tr = colors[1]
    color_bl = colors[2]
    # Iterate over each pixel and calculate interpolated colors
    for y in range(height):
        for x in range(width):
            # Interpolate colors from top-left to bottom-right
            r_tl = color_tl[0]
            g_tl = color_tl[1]
            b_tl = color_tl[2]

            r_tr = color_tr[0]
            g_tr = color_tr[1]
            b_tr = color_tr[2]

            r_bl = color_bl[0]
            g_bl = color_bl[1]
            b_bl = color_bl[2]

            # Interpolate between top-left and top-right
            r_top = int(r_tl + (x / (width - 1)) * (r_tr - r_tl))
            g_top = int(g_tl + (x / (width - 1)) * (g_tr - g_tl))
            b_top = int(b_tl + (x / (width - 1)) * (b_tr - b_tl))
            # Interpolate between top-left and bottom-left
            r_left = int(r_tl + (y / (height - 1)) * (r_bl - r_tl))
            g_left = int(g_tl + (y / (height - 1)) * (g_bl - g_tl))
            b_left = int(b_tl + (y / (height - 1)) * (b_bl - b_tl))
            # Combine the interpolated colors
            r = int(r_left + (x / (width - 1)) * (r_top - r_left))
            g = int(g_left + (x / (width - 1)) * (g_top - g_left))
            b = int(b_left + (x / (width - 1)) * (b_top - b_left))
            image.putpixel((x, y), (r, g, b))
    return image


def generate_4point_gradient(width: int, height: int,
                             colors: List[Tuple[int, int, int]]):
    """Generate a gradient image with four corner colors.
    
    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        colors (List[Tuple[int, int, int]]): A list of four RGB color tuples at
                                             the corners of the image in the following order:
                                             top-left, top-right, bottom-left, bottom-right.

    Returns:
        Image: An RGB image object with the four corners gradient.
    """
    image = Image.new('RGB', (width, height))
    # Assign colors to corners: top-left, top-right, bottom-left, bottom-right
    color_tl = colors[0]
    color_tr = colors[1]
    color_bl = colors[2]
    color_br = colors[3]
    # Iterate over each pixel and calculate interpolated colors
    for y in range(height):
        for x in range(width):
            # Calculate distances from corners to current pixel
            dist_x = x / (width - 1)
            dist_y = y / (height - 1)
            # Interpolate horizontally between top-left and top-right
            r_top = int(color_tl[0] + dist_x * (color_tr[0] - color_tl[0]))
            g_top = int(color_tl[1] + dist_x * (color_tr[1] - color_tl[1]))
            b_top = int(color_tl[2] + dist_x * (color_tr[2] - color_tl[2]))
            # Interpolate horizontally between bottom-left and bottom-right
            r_bottom = int(color_bl[0] + dist_x * (color_br[0] - color_bl[0]))
            g_bottom = int(color_bl[1] + dist_x * (color_br[1] - color_bl[1]))
            b_bottom = int(color_bl[2] + dist_x * (color_br[2] - color_bl[2]))
            # Interpolate vertically between top and bottom
            r = int(r_top + dist_y * (r_bottom - r_top))
            g = int(g_top + dist_y * (g_bottom - g_top))
            b = int(b_top + dist_y * (b_bottom - b_top))
            image.putpixel((x, y), (r, g, b))
    return image
