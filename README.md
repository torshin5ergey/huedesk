# HueDesk

This script generates solid or gradient wallpapers in various formats.
It can be used either in CLI mode or in an interactive mode.

## Description



## Usage

### CLI Mode

Run the script in a command-line interface mode.
```bash
huedesk [-h] [-d DIMENSIONS] [-c COLOR] [-o OUTPUT]
```
**Options**

`-d, --dimensions`: Specify the wallpaper dimensions in pixels. Format should be <WIDTHxHEIGHT>. Default is 1920x1080.

`-c, --color`: Color in <R,G,B> or <#HEX> for solid color. Or start-end format for up to 4-color gradient (e.g., `255,0,0` or `#FF0000` or `'#FF0000-#00FF00'`).You can also specify <random> for a random number of colors (1 to 4), or <randomN> for exactly N random colors (e.g., `random` or `random3`).

`-o, --output`: Specify the output image path. Default is wallpaper.png.

`-h, --help`: Show help message.

### Interactive Mode

Run the script in interactive mode.
```bash
huedesk
```

## Contents

`huedesk.py`: 
`huedesk_cli.py`: 
`huedesk_curses.py`: 
`image_generator.py`: 
`requirements.txt`: 
`samples/`: 
`README.md`: This readme file.

## How to run source code

1. Clone this repository

git clone https://github.com/torshin5ergey/python-playground.git
Go to this project directory
cd python-playground/automate_boring_stuff_projects/regex_search
Run Python file with desired options (e.g.)
python regex_search.py -i <pattern>
*Compile into an executable (optional):
pyinstaller regex_search.spec

## Examples for CLI mode

Create solid color gray *rgb(59, 68, 75)* image with dimensions *560x315* px and *solid_color_wallpaper.png* name.
```bash
huedesk -d 560x315 -c 59,68,75 -o solid_color_wallpaper.png
```
![Solid color gray image](./samples/solid_color_wallpaper.png)

Create two point gradient color *hex(f53cab) hex(354882)* image with dimensions *560x315* px and *two_point_wallpaper.png* name.
```bash
huedesk -d 560x315 -c 'f53cab-354882' -o two_point_wallpaper.png
```
![Two point gradient color image](./samples/two_point_wallpaper.png)

Create three point gradient color *hex(#35b38f) hex(fad433) rgb(71, 149, 223)* image with dimensions *560x315* px and *three_point_gradient_wallpaper.png* name.
```bash
huedesk -d 560x315 -c '#35b38f-fad433-71,149,223' -o three_point_gradient_wallpaper.png
```
![Three point gradient color image](./samples/three_point_gradient_wallpaper.png)

Create four point gradient color *hex(42b0b0) rgb(103, 116, 157) hex(#ab3775) hex(f4b85b)* image with dimensions *560x315* px and *four_point_gradient_wallpaper.png* name.
```bash
huedesk -c '42b0b0-103,116,157-#ab3775-f4b85b' -o four_point_gradient_wallpaper.png -d 560x315
```
![Four point gradient color image](./samples/four_point_gradient_wallpaper.png)

Create random number of random colors image with default dimensions *1920x1080* px and *random_wallpaper.png* name.
```bash
huedesk -c random -o random_wallpaper.png
```
![Four point gradient color image](./samples/random_wallpaper.png)

Create two point random colors gradient image with default dimensions *1920x1080* px and *random2_wallpaper.png* name.
```bash
huedesk -o random2_wallpaper.png -c random2
```
![Two point gradient color image](./samples/random2_wallpaper.png)

## Requirements

- [pillow](https://pypi.org/project/pillow/)~=10.4.0 (optional, if you want to run source code)
- [windows-curses](https://pypi.org/project/windows-curses/)~=2.3.3 (optional, for Windows platforms if you want to run source code)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (optional, for compiling source code into executable)

## Author

Sergey Torshin [@torshin5ergey](https://github.com/torshin5ergey)