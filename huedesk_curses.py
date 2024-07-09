#! python3
"""
huedesk_curses.py - Interactive curses mode for generating wallpapers.

Written by Sergey Torshin @torshin5ergey
"""


import sys
import curses
import re
from typing import Literal, List, Tuple
from image_generator import (generate_random_colors, parse_color,
                             create_solid_color_image,
                             create_gradient_color_image)


LOGO = (
    " _             _         _ ",
    "| |_ _ _ ___ _| |___ ___| |_ ",
    "|   | | | -_| . | -_|_ -| '_|",
    "|_|_|___|___|___|___|___|_,_|"
)

class HueDeskCursesError(Exception):
    """Custom HueDesk exception.
    For errors in the curses mode."""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def process_image(stdscr, menu_items: List[str], menu_values: List[str],
                   mode: Literal['generate', 'preview'] = 'generate') -> None:
    """Generate the image from interactive curses mode.
    
    Args:
        menu_items (List[str]): A list of menu items.
        menu_values (List[str]): A list of menu values.
        mode (Literal['generate', 'preview'], optional): Processing mode. Defaults to 'generate'.
        
    Raises:
        ValueError: If dimension or color format is invalid.
        HueDeskCursesError: If there is an error in generating the wallpaper.
    """
    try:
        width = int(menu_values[0])
        height = int(menu_values[1])
        # Width and height validation
        if width <= 1 or height <= 1:
            raise HueDeskCursesError("Invalid dimensions foramt. " \
                               "The values must be greater than 1")

        # Random colors
        match = re.match(r'^random(\d)*$', menu_values[2])
        if match:
            rand_color_count = match.group(1)
            try:
                colors_number = int(rand_color_count)
                if 1 <= colors_number <= 4:
                    color = generate_random_colors(colors_number)
                else:
                    raise HueDeskCursesError("Invalid number of colors. " \
                                             "Should be between 1 and 4")
            except TypeError:
                color = generate_random_colors()
        else:
            color = parse_color(menu_values[2])

        output_path = menu_values[3]
        # Generate image
        if len(color) == 1:
            create_solid_color_image(width, height, *color, output_path, mode)
        elif len(color) in (2, 3, 4):
            create_gradient_color_image(width, height, color, output_path, mode)
        else:
            raise HueDeskCursesError("Invalid number of colors. " \
                                     "Should be between 1 and 4")

        if mode == 'generate':
            stdscr.addstr(len(menu_items) + 6, 0, "Success! " \
                      f"Wallpaper saved as {output_path}.", curses.color_pair(1))
        elif mode == 'preview':
            stdscr.addstr(len(menu_items) + 6, 0, "Success! " \
                      "Wallpaper opened in scaled preview mode.", curses.color_pair(1))
        else:
            raise HueDeskCursesError
    except ValueError:
        stdscr.addstr(len(menu_items) + 6, 0, "Warning: " \
                      "Wrong parameters format.", curses.color_pair(2))
    except HueDeskCursesError as e:
        stdscr.addstr(len(menu_items) + 6, 0, "Warning: " \
                      f"{e}.", curses.color_pair(2))
    except Exception as e:
        stdscr.addstr(len(menu_items) + 6, 0, "Error: " \
                      f"Can't create wallpaper. {e}", curses.color_pair(2))
    stdscr.getch()
    stdscr.refresh()


def main_curses(stdscr):
    """Run in curses interactive mode."""
    # Define output colors
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) # Success
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Red

    curses.curs_set(0)  # Disable cursor
    stdscr.clear()
    stdscr.refresh()

    # Parameters
    menu_items = ['Width (px)', 'Height (px)', 'Color (R,G,B or #HEX)',
                  'Output path', 'PREVIEW', 'GENERATE', 'EXIT']
    max_len = len(max(menu_items, key=len))
    sep_len = 2  # Menu columns separator whitespace
    menu_values = ['1920', '1080', '', 'wallpaper.png', '', '', '']

    current_row = 0
    while True:
        stdscr.clear()
        # Display logo
        for row in range(4):
            stdscr.addstr(row, 0, LOGO[row])
        stdscr.addstr(4, 7, 'Setup wallpaper')
        # Display menu
        for idx, item in enumerate(menu_items):
            if item in ('PREVIEW', 'GENERATE', 'EXIT'):
                attr = curses.A_REVERSE if idx == current_row else curses.A_BOLD
            else:
                attr = curses.A_REVERSE if idx == current_row else curses.A_NORMAL
            stdscr.addstr(idx + 5, 0, item.ljust(max_len+sep_len), attr)
            stdscr.addstr(idx + 5, max_len+sep_len, str(menu_values[idx]), attr)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(menu_items)
        elif key == curses.KEY_UP:
            current_row = (current_row - 1) % len(menu_items)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if menu_items[current_row].strip() == 'GENERATE':
                process_image(stdscr, menu_items, menu_values)
            elif menu_items[current_row].strip() == 'PREVIEW':
                process_image(stdscr, menu_items, menu_values, mode='preview')
            elif menu_items[current_row].strip() == 'EXIT':
                sys.exit()
            else:
                edit_parameter(stdscr, menu_values, current_row, (max_len, sep_len))


def edit_parameter(stdscr, menu_values: List[str], current_row: int,
                   params: Tuple[int, int]) -> None:
    """Edit an image parameter in interactive mode.

    Args:
        menu_values (list): A list of current parameter values.
        current_row (int): An index of the parameter to edit in menu_values.
        params: Tuple[int, int]: Maximum parameters lenght and separator length.

    Returns:
        None: Updates menu_values in place.
    """
    curses.echo()
    stdscr.move(current_row + 5, params[0]+params[1])  # Set cursor
    stdscr.clrtoeol()  # Clear value
    stdscr.refresh()
    curses.curs_set(2)  # Enable blinking cursor
    value = stdscr.getstr(current_row + 5, params[0]+params[1], 50).decode('utf-8').strip()
    curses.noecho()
    curses.curs_set(0)  # Disable cursor
    if value:
        menu_values[current_row] = value
