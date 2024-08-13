# HueDesk

**HueDesk** generates solid or gradient color wallpapers in various formats.

## Description

**HueDesk** is designed for generating custom wallpapers with solid colors or gradients. The tool offers two modes of operation:
- **CLI Mode**: For users who prefer working from the command line, **HueDesk** provides a range of options to specify dimensions, colors, and output file names. This mode supports both solid colors and gradients with up to four colors.
- **Interactive Mode**: For a more user-friendly experience, **HueDesk** includes an interactive mode that simplifies the process of generating wallpapers by guiding users through a series of prompts.

### Key Features

- **CLI and Interactive modes**: Choose what you prefer more.
- **Flexible Color Options**: Specify colors using **RGB** values or **HEX** codes. For gradients, you can use multiple colors in various formats, including gradients with up to four points and random color combinations.
- **Custom Dimensions**: Adjust the size of generated wallpaper to fit any screen resolution by specifying dimensions in pixels.
- **Output Options**: Save  generated wallpapers with custom file names and formats.
- **Interactive Prompts**: Use the interactive mode for an easy-to-use interface.

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

## Project Structure

```
-/
│
├── huedesk.spec           # PyInstaller spec
├── README.md              # This README
├── .gitignore             # Gitignore
├── requirements.txt       # Dependencies
├── samples/               # Sample images
│
└── huedesk/               # Main package directory
    ├── __init__.py        # Package initializer
    ├── cli_mode.py        # CLI mode script
    ├── curses_mode.py     # Curses mode script
    ├── image_generator.py # Image generator script
    ├── main.py            # Main script
    └── utils.py           # Utility functions

```

## How to run source code

1. Clone this repository
```bash
git clone https://github.com/torshin5ergey/huedesk.git
```
2. Go to this project directory
```bash
cd huedesk
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Run the code
    - For interactive mode:
    ```bash
    python huedesk/main.py
    ```
    - For CLI mode (according to [Usage for CLI Mode](#cli-mode))
    ```
    python huedesk/main.py [-h] [-d DIMENSIONS] [-c COLOR] [-o OUTPUT]
    ```

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