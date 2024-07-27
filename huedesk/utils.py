#!python3
"""
utils.py - Utility functions for desktop path retrieval and image saving.

Writtent by Sergey Torshin @torshin5ergey
"""

import os
import platform


def get_desktop_path():
    system = platform.system
    if system == "Windows":
        return os.path.join(os.environ["USERPROFILE"], "Desktop")
    elif system == "Darwin" or system == "Linux":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:
        return Exception(f"Unsupported OS: {system}")
    
    
def save_image(image, filename):
    desktop_path = get_desktop_path()
    save_path = os.path.join(desktop_path, filename)
    image.save(save_path)
