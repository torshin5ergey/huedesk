#! python3
"""
huedesk.py -- Generate gradient/solid color wallpaper

Written by Sergey Torshin @torshin5ergey
"""

import argparse
import curses
from PIL import Image
from random import sample
from typing import Tuple, List


class HueDeskError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def parse_color(color: str) -> List[Tuple[int, int, int]]:
    """Parse the color input to a list of RGB tuples."""
    colors = []  # Output colors list
    color_parts = color.split('-')
    
    for c in color_parts:
        current_color = c.lstrip('#')
        if ',' in color:  # RGB format
            try:
                r, g, b = map(int, current_color.split(','))
                if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
                    raise HueDeskError("Invalid RGB format. Values must be between 0 and 255.")
                colors.append((r, g, b))
            except ValueError:
                raise HueDeskError("Invalid RGB format. Should be three integers separated by commas.")
        elif len(current_color) in [3, 6]:  # HEX format
            try:
                if len(current_color) == 3:
                    current_color = ''.join([c * 2 for c in current_color])
                r = int(current_color[0:2], 16)
                g = int(current_color[2:4], 16)
                b = int(current_color[4:6], 16)
                colors.append((r, g, b))
            except ValueError:
                raise HueDeskError("Invalid HEX format. Should be #RGB or #RRGGBB.")
        else:
            raise HueDeskError("Invalid color format. Use R,G,B or #RRGGBB (#RGB).")
    return colors


def create_solid_color_image(width: int, height: int, color: Tuple[int, int, int], output_path: str) -> None:
    """Create and save solid color image."""
    image = Image.new('RGB', (width, height), color)
    image.save(output_path)


def create_gradient_color_image(width: int, height: int, colors: List[Tuple[int, int, int]], output_path: str) -> None:
    """Create and save a gradient color image."""
    image = Image.new('RGB', (width, height))
    num_colors = len(colors)
    
    if num_colors == 2:
        # Assign colors to corners: top-left and bottom-right
        color_tl = colors[0]
        color_br = colors[1]
        
        # Iterate over each pixel and calculate interpolated colors
        for y in range(height):
            for x in range(width):
                # Calculate the distance from top-left corner to current pixel
                distance_tl = (x + y) / (width + height - 2)  # Total distance from top-left to bottom-right
                
                # Interpolate colors from top-left to bottom-right
                r = int(color_tl[0] + distance_tl * (color_br[0] - color_tl[0]))
                g = int(color_tl[1] + distance_tl * (color_br[1] - color_tl[1]))
                b = int(color_tl[2] + distance_tl * (color_br[2] - color_tl[2]))
                
                image.putpixel((x, y), (r, g, b))
    
    if num_colors == 3:
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
    
    if num_colors == 4:
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
    
    image.save(output_path)


def main_cli(parser, args):
    """Run with command-line options (arguments)."""
    try:
        width, height = map(int, args.dimensions.lower().split('x'))
        color = parse_color(args.color)
        output_path = args.output
        
        if len(color) == 1:
            create_solid_color_image(width, height, *color, output_path)
        else:
            create_gradient_color_image(width, height, color, output_path)
        print(f"Success! Wallpaper saved as {output_path}")
    except:
        print(f"Invalid options format.")
        parser.print_help()


def main_curses(stdscr):
    """Run in interactive mode."""
    # Define output colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Success
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Red

    curses.curs_set(0)  # Enable cursor
    stdscr.clear()
    stdscr.refresh()

    # Parameters
    menu_items = ['Width (px): ', 'Height (px): ', 'Color (R,G,B or #HEX): ', 'Output path: ', 'GENERATE  ', 'EXIT  ']
    max_len = len(max(menu_items, key=len))
    menu_values = ['', '', '', 'wallpaper.png', '', '']

    current_row = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Setup wallpaper:')
        # Display menu
        for idx, item in enumerate(menu_items):
            attr = curses.A_REVERSE if idx == current_row else curses.A_NORMAL
            stdscr.addstr(idx + 1, 0, item.rjust(max_len), attr)
            stdscr.addstr(idx + 1, max_len, str(menu_values[idx]), attr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(menu_items)
        elif key == curses.KEY_UP:
            current_row = (current_row - 1) % len(menu_items)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_items[current_row].strip() == 'GENERATE':
                generate_image(stdscr, menu_items, menu_values)
            elif menu_items[current_row].strip() == 'EXIT':
                return
            else:
                edit_parameter(stdscr, menu_values, current_row, max_len)


def edit_parameter(stdscr, menu_values, current_row, max_len):
    """Edit an image parameter in interactive mode."""
    curses.echo()
    stdscr.move(current_row + 1, max_len)  # Set cursor
    stdscr.clrtoeol()  # Clear value
    stdscr.refresh()
    value = stdscr.getstr(current_row + 1, max_len, 50).decode('utf-8').strip()
    curses.noecho()
    if value:
        menu_values[current_row] = value


def generate_image(stdscr, menu_items, menu_values):
    """Generate the image from interactive mode."""
    try:
        width = int(menu_values[0])
        height = int(menu_values[1])
        # Width and height validation
        if width <= 1 or height <= 1:
            raise HueDeskError("Invalid dimensions foramt. The values must be greater than 1.")
        color = parse_color(menu_values[2])
        output_path = menu_values[3]
        # Generate image
        if len(color) == 1:
            create_solid_color_image(width, height, *color, output_path)
        else:
            create_gradient_color_image(width, height, color, output_path)

        stdscr.addstr(len(menu_items) + 2, 0, f"Success! Wallpaper saved as {output_path}.", curses.color_pair(1))
    except ValueError:
        stdscr.addstr(len(menu_items) + 2, 0, "Warning: Wrong parameters format.", curses.color_pair(2))
    except HueDeskError as e:
        stdscr.addstr(len(menu_items) + 2, 0, f"Warning: {e}.", curses.color_pair(2))
    except:
        stdscr.addstr(len(menu_items) + 2, 0, "Error: Can't create wallpaper.", curses.color_pair(2))
    stdscr.getch()
    stdscr.refresh()
    

def main():
    parser = argparse.ArgumentParser(description='Create solid/gradient wallpaper.')
    parser.add_argument('-d', '--dimensions', type=str, default='1920x1080', help="Wallpaper dimensions 'WIDTHxHEIGHT' in pixels (default is 1920x1080).")
    parser.add_argument('-c', '--color', type=str, help='Color in R,G,B or HEX for solid color. Or start-end format for up to 4-color gradient (e.g., 255,0,0 or #FF0000 or #FF0000-#00FF00).')
    parser.add_argument('-o', '--output', type=str, default='wallpaper.png', help='Output image path (default is wallpaper.png).')

    args, unknown = parser.parse_known_args()

    if unknown:
        print('Invalid options format. Unknown option.')
        parser.print_help()
    elif all(vars(args).values()):
        main_cli(parser, args)
    else:
        curses.wrapper(main_curses)

if __name__ == '__main__':
    main()
