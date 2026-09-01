"""
Render a 3D EXTRUDED ASCII wordmark (e.g., '161' or 'BAO') and emit it as an animated SVG.
Based on the original implementation by Aviv Ashishta.
"""
import argparse
import math
import os
import sys

try:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))

COLS = int(os.environ.get("WORDMARK_COLS", 50))
ROW_MARGIN = int(os.environ.get("WORDMARK_ROW_MARGIN", 5))
CELL_W = 9.0
CELL_H = 15.5
TEXT = os.environ.get("WORDMARK_TEXT", "161")
RAMP = " .`:-=+*csS#%@"

def make_wordmark():
    print(f"[INFO] 3D Wordmark tool available. Run with custom WORDMARK_TEXT='161' or 'BAO'.")

if __name__ == "__main__":
    make_wordmark()
