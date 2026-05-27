#!/usr/bin/env python3
"""
crop_title.py  <input.png>  <output.png>

Removes a matplotlib/seaborn figure title from the top of the image.

Detection strategy:
  1. Sample the background colour from the four corners.
  2. Scan rows from the top; a row is "text" if enough pixels differ
     significantly from the background (i.e. dark title text on background).
  3. Find the last "text" row in the top 25 % of the image → that is the
     bottom of the title.  Add a small margin and crop from there down.

If no title text is detected the file is saved unchanged.
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image

# A pixel is "different from background" if any channel deviates by this much
DIFF_THRESHOLD  = 20
# A row is a "text row" if at least this fraction of pixels differ from bg
TEXT_ROW_RATIO  = 0.02
# Only look for the title in the top fraction of the image
# (matplotlib titles sit in the first ~10 % — well above any in-plot labels)
SEARCH_FRACTION = 0.10
# Extra blank pixels to include below the detected title bottom
MARGIN_PX       = 4


def bg_colour(arr: np.ndarray) -> np.ndarray:
    """Estimate background colour from the four corners (3-pixel average)."""
    samples = np.concatenate([
        arr[:3,  :3 ].reshape(-1, arr.shape[2]),
        arr[:3,  -3:].reshape(-1, arr.shape[2]),
        arr[-3:, :3 ].reshape(-1, arr.shape[2]),
        arr[-3:, -3:].reshape(-1, arr.shape[2]),
    ])
    return samples.mean(axis=0)


def find_crop_row(arr: np.ndarray) -> int:
    """Return the first row after the title (0 = nothing to crop)."""
    bg   = bg_colour(arr)
    h    = arr.shape[0]
    limit = int(h * SEARCH_FRACTION)

    last_text_row = -1
    for r in range(limit):
        row  = arr[r, :, :3].astype(float)
        diff = np.abs(row - bg[:3]).max(axis=1)
        if (diff > DIFF_THRESHOLD).mean() > TEXT_ROW_RATIO:
            last_text_row = r

    if last_text_row == -1:
        return 0
    return min(last_text_row + 1 + MARGIN_PX, h)


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.png> <output.png>")
        sys.exit(1)

    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    img  = Image.open(src).convert("RGB")
    arr  = np.array(img)

    crop_row = find_crop_row(arr)
    if crop_row == 0:
        print(f"{src.name}: no title detected – copying as-is")
    else:
        print(f"{src.name}: cropping top {crop_row}px")

    cropped = img.crop((0, crop_row, img.width, img.height))
    cropped.save(dst)
    print(f"Saved → {dst}")


if __name__ == "__main__":
    main()
