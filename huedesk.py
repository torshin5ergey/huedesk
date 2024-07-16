#! python3
"""
huedesk.py - Create solid/gradient wallpaper.

Usage:
    huedesk.py - CLI mode.
    huedesk.py [-h] [-d DIMENSIONS] [-c COLOR] [-o OUTPUT] - one-line mode.
    

Written by Sergey Torshin @torshin5ergey
"""

import argparse
from curses import wrapper

from huedesk_curses import main_curses
from huedesk_cli import main_cli


def main():
    """Main script function.
    
    Parses command-line arguments and runs either CLI mode or curses interactive mode.
    """
    parser = argparse.ArgumentParser(description='Create solid/gradient wallpaper.')
    parser.add_argument('-d', '--dimensions', type=str, default='1920x1080',
                        help="Wallpaper dimensions <WIDTHxHEIGHT> in pixels "
                            "(default is 1920x1080).")
    parser.add_argument('-c', '--color', type=str,
                        help='Color in <R,G,B> or <#HEX> for solid color. '
                            'Or start-end format for up to 4-color gradient '
                            '(e.g., 255,0,0 or #FF0000 or #FF0000-#00FF00). '
                            'You can also specify <random> for a random number '
                            'of colors (1 to 4), or <randomN> for exactly N random '
                            'colors (e.g., random or random3).')
    parser.add_argument('-o', '--output', type=str, default='wallpaper.png',
                        help='Output image path (default is wallpaper.png).')

    args, unknown = parser.parse_known_args()

    if unknown:
        print('Invalid options format. Unknown option.')
        parser.print_help()
    elif all(vars(args).values()):
        main_cli(parser, args)
    else:
        wrapper(main_curses)
        print("\033[31m" + "Error. The window size is too small to display the interface.\n"
              "Increase the window size or use the one-line mode." + "\033[0m")

if __name__ == '__main__':
    main()
