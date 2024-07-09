# HueDesk

This script generates solid or gradient wallpapers in various formats.
It can be used either in CLI mode or in an interactive curses mode.

## Description



## Usage



## Contents

regex_search.py: Script for regex search.
regex_search.spec: PyInstaller specification file for building executable.
test.txt: Example text file for testing regex searches.
README.md: This readme file.

## How to run source code

1. Clone this repository

git clone https://github.com/torshin5ergey/python-playground.git
Go to this project directory
cd python-playground/automate_boring_stuff_projects/regex_search
Run Python file with desired arguments (e.g.)
python regex_search.py -i <pattern>
*Compile into an executable (optional):
pyinstaller regex_search.spec

## Requirements

- [pillow](https://pypi.org/project/pillow/)~=10.4.0 (optional, if you want to run source code)
- [windows-curses](https://pypi.org/project/windows-curses/)~=2.3.3 (optional, for Windows platforms if you want to run source code)
- [PyInstaller](https://pypi.org/project/pyinstaller/) (optional, for compiling source code into executable)

## Author

Sergey Torshin [@torshin5ergey](https://github.com/torshin5ergey)