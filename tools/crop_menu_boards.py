#!/usr/bin/env python3
"""Crop individual dish thumbnails out of photographed menu boards.

The restaurant's physical menu is 5 printed boards, each a photo collage:
a price list on the left, and a small photo per item arranged in a grid on
the right. This script crops each item's photo out of the board image and
saves it as a thumbnail in assets/dishes/menu/, trimming the near-black
background margin so the crop fills a square list-thumbnail cleanly.

USAGE

  1. Save the 5 board photos as board1.jpg .. board5.jpg in some folder
     (e.g. this directory, or /tmp/boards).
  2. If the boards have been reshot (new layout, new items, moved photos),
     the crop coordinates in BOARD_CROPS below need updating — see
     "Finding new crop coordinates" further down.
  3. Run:
         python3 tools/crop_menu_boards.py /path/to/board/photos
     With no argument it looks in tools/board_photos/.

  Output goes to assets/dishes/menu/<slug>.webp. Re-running overwrites
  existing files with the same slug, so it's safe to re-run after fixing
  a crop box.

FINDING NEW CROP COORDINATES

  Board photos in this project were saved at 1035x1600px. To find crop
  boxes for a reshot board, overlay a coordinate grid and read pixel
  positions off it:

      from PIL import Image, ImageDraw
      im = Image.open('boardN.jpg').convert('RGB')
      d = ImageDraw.Draw(im)
      w, h = im.size
      for x in range(0, w, 50):
          d.line([(x,0),(x,h)], fill=(255,0,0) if x%100==0 else (255,150,150))
          if x % 100 == 0: d.text((x+2,2), str(x), fill=(255,0,0))
      for y in range(0, h, 50):
          d.line([(0,y),(w,y)], fill=(0,255,0) if y%100==0 else (150,255,150))
          if y % 100 == 0: d.text((2,y+2), str(y), fill=(0,255,0))
      im.save('boardN_grid.png')

  View boardN_grid.png, read off the (x0, y0, x1, y1) box for each dish
  photo (give it a little slack — the auto-trim step below tightens it),
  and update BOARD_CROPS. Build a contact sheet to sanity-check a whole
  board at once before trusting it — see the git history of this file
  (or ask Claude) for the contact-sheet snippet.
"""
import os
import sys

from PIL import Image

try:
    import numpy as np
except ImportError:
    sys.exit("Run: pip install numpy pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "dishes", "menu")

# (board_file, {slug: (x0, y0, x1, y1)})
# Order within each board matches the item numbering on that board.
BOARD_CROPS = {
    "board1.jpg": {  # Drinks: bubble tea + iced coffee
        "brown-sugar-bubble-tea": (515, 305, 645, 555),
        "matcha-bubble-tea": (680, 385, 780, 580),
        "coffee-bubble-tea": (820, 300, 940, 505),
        "hong-kong-bubble-tea": (515, 610, 645, 815),
        "taro-bubble-tea": (680, 690, 780, 885),
        "strawberry-bubble-tea": (820, 600, 940, 805),
        "iced-americano": (515, 905, 650, 1085),
        "iced-caramel-macchiato": (670, 1005, 785, 1140),
        "iced-spanish-latte": (810, 900, 945, 1075),
        "iced-dark-mocha-latte": (520, 1160, 645, 1320),
        "iced-white-mocha-latte": (670, 1290, 775, 1400),
        "iced-vanilla-latte": (815, 1195, 940, 1320),
        "iced-hazelnut-latte": (795, 1425, 930, 1560),
        "iced-salted-caramel-latte": (550, 1425, 650, 1560),
        "iced-strawberry-coffee-latte": (325, 1390, 440, 1560),
    },
    "board2.jpg": {  # Lunch/Dinner items 1-12
        "ribs-6pc": (548, 240, 692, 412),
        "beef-shanks": (735, 275, 947, 412),
        "lamb-chops": (543, 458, 720, 607),
        "haneeth": (788, 468, 947, 637),
        "quarter-chicken": (548, 653, 712, 832),
        "chicken-leg": (778, 663, 947, 842),
        "lime-chicken": (568, 903, 707, 1077),
        "chicken-wings": (763, 903, 942, 1077),
        "rice-chicken-veggies": (553, 1118, 702, 1292),
        "chicken-skewers-veggies": (763, 1118, 942, 1302),
        "rice-beef-kebab": (563, 1348, 682, 1522),
        "chicken-skewers": (768, 1353, 927, 1522),
    },
    "board3.jpg": {  # Dessert
        "cheesecake": (548, 220, 710, 362),
        "cake-with-frosting": (765, 250, 950, 475),
        "brownie": (543, 445, 745, 620),
        "biscuit-cake": (763, 565, 950, 760),
        "caramel-cake": (603, 800, 858, 985),
        "sambuusa": (663, 1015, 897, 1105),
        "mini-cake": (608, 1140, 842, 1385),
    },
    "board4.jpg": {  # Drinks: hot coffee + smoothies
        "tea": (538, 245, 690, 372),
        "espresso": (778, 300, 927, 400),
        "coffee-americano": (568, 458, 712, 572),
        "cappuccino": (758, 495, 937, 622),
        "latte": (553, 640, 687, 745),
        "peach-smoothie": (793, 745, 917, 907),
        "avocado-smoothie": (573, 855, 662, 987),
        "banana-smoothie": (798, 1015, 887, 1177),
        "mango-smoothie": (573, 1085, 662, 1232),
        "strawberry-smoothie": (793, 1270, 897, 1402),
        "watermelon-smoothie": (573, 1335, 672, 1492),
    },
    "board5.jpg": {  # Lunch/Dinner items 13-20 + Salads
        "lemon-salmon": (548, 225, 707, 412),
        "fish-veggies": (758, 325, 950, 552),
        "chicken-skewers-fries-rice": (548, 468, 707, 682),
        "rice-veggies-16": (745, 615, 950, 747),
        "tomato-soup-dip": (618, 780, 897, 882),
        "rice-meat-meal-family": (578, 925, 707, 1132),
        "chicken-alfredo": (753, 965, 927, 1127),
        "rice-veggies-20": (688, 1155, 872, 1277),
        "pomegranate-salad": (158, 1345, 322, 1552),
        "mixed-veggie-salad": (428, 1355, 617, 1552),
        "green-salad": (728, 1350, 867, 1552),
    },
}


def trim_dark_border(im, mean_thresh=16, pad=0):
    """Trim rows/cols that are essentially pure black background — a
    column only counts as background if its *average* brightness is
    still near-black, so a single stray highlight can't save it.

    pad defaults to 0 on purpose: padding back in a couple of "safety"
    pixels sounds harmless, but at the crop boundary those pixels are
    frequently still part of the black background (the transition from
    background to content is often a hard 1-2px edge, not a gradient),
    which reintroduces the exact black sliver this function exists to
    remove. If a future crop shows anti-aliasing fringe, prefer widening
    the crop box in BOARD_CROPS over adding padding here.
    """
    arr = np.array(im.convert("L")).astype(np.float32)
    h, w = arr.shape
    col_bg = arr.mean(axis=0) < mean_thresh
    row_bg = arr.mean(axis=1) < mean_thresh

    def first_last_false(mask):
        idx = np.where(~mask)[0]
        return (0, len(mask)) if len(idx) == 0 else (idx[0], idx[-1] + 1)

    x0, x1 = first_last_false(col_bg)
    y0, y1 = first_last_false(row_bg)
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(w, x1 + pad), min(h, y1 + pad)
    if x1 - x0 < 15 or y1 - y0 < 15:
        return im  # trim collapsed the image — source probably isn't on a dark bg
    return im.crop((x0, y0, x1, y1))


def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "board_photos"
    )
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for board_file, crops in BOARD_CROPS.items():
        path = os.path.join(src_dir, board_file)
        if not os.path.isfile(path):
            print(f"skip {board_file}: not found in {src_dir}")
            continue
        im = Image.open(path).convert("RGB")
        for slug, box in crops.items():
            crop = im.crop(box)
            crop = trim_dark_border(crop)
            crop.thumbnail((500, 500), Image.LANCZOS)
            crop.save(os.path.join(OUT, f"{slug}.webp"), "WEBP", quality=82)
            total += 1
        print(f"{board_file}: {len(crops)} items")
    print(f"\n{total} thumbnails written to {os.path.relpath(OUT, ROOT)}/")


if __name__ == "__main__":
    main()
