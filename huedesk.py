#! python3
"""
huedesk.py -- Generate gradient/solid color wallpaper

Written by Sergey Torshin @torshin5ergey
"""

import argparse
import curses
from PIL import Image


class HueDeskError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def create_solid_color_image(width, height, color, output_path):
    """Create and save solid color image.
    """
    image = Image.new('RGB', (width, height), color)
    image.save(output_path)


def main_cli(parser, args):
    """Run with options (arguments).
    """
    dim = args.dimensions.split('x')
    try:
        width = int(dim[0])
        height = int(dim[1])
        color = tuple(map(int, args.color.split(',')))  # Преобразуем строку в кортеж RGB
        output_path = args.output
        create_solid_color_image(width, height, color, output_path)
        print(f"Success! Wallpaper saved as {output_path}")
    except:
        print(f"Error: Wrong options format.")
        parser.print_help()
    

def main_curses(stdscr):
    """Run without options (arguments) in CLI.
    """
    # Define output colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Success
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Red

    curses.curs_set(0)  # Enable cursor
    stdscr.clear()
    stdscr.refresh()

    # Parameters
    menu_items = ['Width (px): ', 'Height (px): ', 'Color (R,G,B): ', 'Output path: ', 'GENERATE  ', 'EXIT  ']
    max_len = len(max(menu_items, key=len))
    menu_values = ['', '', '', 'wallpaper.png', '', '']
    '''
    menu = {
        'Width (px): ': '',
        'Height (px): ': '',
        'Color (R,G,B): ': '',
        'Output path: : ': 'wallpaper.png',
        'GENERATE': '',
        'EXIT': '',
    }
    '''

    current_row = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Setup wallpaper:')
        # Вывод меню
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
    """Edit image parameter in CLI.
    """
    curses.echo()
    stdscr.move(current_row + 1, max_len)  # Set cursor
    stdscr.clrtoeol()  # Clear value
    stdscr.refresh()
    value = stdscr.getstr(current_row + 1, max_len, 50).decode('utf-8').strip()
    curses.noecho()
    if value:
        menu_values[current_row] = value


def generate_image(stdscr, menu_items, menu_values):
    """Generate image.
    """
    try:
        width = int(menu_values[0])
        height = int(menu_values[1])
        # Width and height validation
        if width <= 1 or height <= 1:
            raise HueDeskError("The 'width' and 'height' must be greater than 1")
        color = tuple(map(int, menu_values[2].split(',')))
        # Color validation
        if not (0 <= color[0] <= 255 and 0 <= color[1] <= 255 and 0 <= color[2] <= 255):
            raise HueDeskError("The 'color' must be from 0 to 255 for every component")
        output_path = menu_values[3]

        # Generate image
        create_solid_color_image(width, height, color, output_path)

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
    parser.add_argument('-d', '--dimensions', type=str, default='1920x1080', help="Wallpaper dimensions 'WIDTHxHEIGHT' in pixels (default is 1920x1080.)")
    parser.add_argument('-c', '--color', type=str, help='Color in R,G,B (e.g. 255,0,0 for red).')
    parser.add_argument('-o', '--output', type=str, default='wallpaper.png', help='Output image (default is wallpaper.png).')

    args, unknown = parser.parse_known_args()

    if unknown:
        print('Error. Unknown option.')
        parser.print_help()
    elif all(vars(args).values()):
        main_cli(parser, args)
    else:
        curses.wrapper(main_curses)

if __name__ == '__main__':
    main()
