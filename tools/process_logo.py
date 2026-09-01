#!/usr/bin/env python3
"""Turn the owner-supplied logo photo into the site's transparent-background
logo assets and favicons.

The source (assets/branding/logo-source.jpg) is a photo of the gold/black
"Salaama Eats" emblem lockup on a solid black card. This script crops out
the mark and the full lockup, keys out the black background to transparency
(so the logo drops cleanly onto both the light header and the dark footer),
and writes the favicon PNGs.

USAGE

    python3 tools/process_logo.py

Re-run any time assets/branding/logo-source.jpg is replaced with a new
photo of the logo — the crop boxes below assume the same framing (a
1500-tall portrait photo with the emblem centered) and may need adjusting
for a different framing. Use the grid-overlay technique documented in
tools/crop_menu_boards.py to re-derive coordinates if so.
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "branding", "logo-source.jpg")
OUT = os.path.join(ROOT, "assets")

# Crop boxes against the 692x1500 source photo. The photo has a "Markup"
# pencil-icon overlay near the bottom (an iOS Photos edit-mode artifact) —
# all boxes stop above it.
FULL_LOCKUP_BOX = (0, 410, 692, 1082)      # emblem + "Salaama Eats Mediterranean Grill"
MARK_BOX = (95, 405, 590, 820)             # emblem only (hat, flame, fork/knife, S·E monogram)
FAVICON_SRC_BOX = (95, 405, 590, 900)      # emblem, a little taller for balanced padding


def chroma_key(im, low=6, high=42):
    """Make near-black pixels transparent with a soft ramp, so anti-aliased
    gold edges don't get a hard cutout line."""
    arr = np.array(im.convert("RGB")).astype(np.float32)
    lum = arr.max(axis=2)
    alpha = np.clip((lum - low) / (high - low), 0, 1)
    alpha = (alpha * 255).astype(np.uint8)
    return Image.fromarray(np.dstack([arr.astype(np.uint8), alpha]), "RGBA")


def autocrop_alpha(im, pad=8):
    arr = np.array(im)
    ys, xs = np.where(arr[:, :, 3] > 10)
    w, h = im.size
    x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + 1 + pad)
    y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + 1 + pad)
    return im.crop((x0, y0, x1, y1))


def main():
    src = Image.open(SRC).convert("RGB")

    full = autocrop_alpha(chroma_key(src.crop(FULL_LOCKUP_BOX)), pad=10)
    full.save(os.path.join(OUT, "logo-full.webp"), "WEBP", quality=92)

    mark = autocrop_alpha(chroma_key(src.crop(MARK_BOX)), pad=8)
    mark.save(os.path.join(OUT, "logo-mark.webp"), "WEBP", quality=92)

    fav = autocrop_alpha(chroma_key(src.crop(FAVICON_SRC_BOX)), pad=20)
    w, h = fav.size
    side = max(w, h)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(fav, ((side - w) // 2, (side - h) // 2), fav)
    for size in (512, 180, 32):
        square.resize((size, size), Image.LANCZOS).save(
            os.path.join(OUT, f"favicon-{size}.png")
        )

    print("wrote logo-full.webp, logo-mark.webp, favicon-{512,180,32}.png")


if __name__ == "__main__":
    main()
