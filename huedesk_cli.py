#! python3
"""
huedesk_cli.py - Command-line interface for generating wallpapers
with colors and gradients.

Written by Sergey Torshin @torshin5ergey
"""

import re
from image_generator import (generate_random_colors, parse_color,
                             create_solid_color_image, create_gradient_color_image,
                             ParserError, ImageGeneratorError)


def main_cli(parser, args):
    """Run with command-line options (arguments)."""
    try:
        width, height = map(int, args.dimensions.lower().split('x'))

        # Random colors
        match = re.match(r'^random(\d)*$', (args.color))
        if match:
            rand_color_count = match.group(1)
            try:
                colors_number = int(rand_color_count)
                if 1 <= colors_number <= 4:
                    colors = generate_random_colors(colors_number)
                else:
                    parser.error("Invalid number of colors. Should be between 1 and 4")
            except TypeError:
                colors = generate_random_colors()
        else:
            colors = parse_color(args.color)

        output_path = args.output
        if len(colors) == 1:
            create_solid_color_image(width, height, *colors, output_path)
        elif len(colors) in (2, 3, 4):
            create_gradient_color_image(width, height, colors, output_path)
        print("\033[32m" + f"Success! Wallpaper saved as {output_path}" + "\033[0m")
    except ParserError as e:
        print("\033[31m" + f"Cannot parse color. {e}" + "\033[0m")
        parser.print_help()
    except ImageGeneratorError as e:
        print("\033[31m" + f"Cannot create image. {e}" + "\033[0m")
        parser.print_help()
