#!/usr/bin/env python3
"""Swap the placeholder dish illustrations for real photographs.

Drop your photos into  assets/dishes/photos/  naming each file after the dish
slug (see SLUGS below), then run:

    python3 tools/use_photos.py

Every photo found is wired into index.html — the dish slider, the hero and
heritage arches, and the gallery. Dishes with no photo keep their illustration,
so you can add photos a few at a time.

    python3 tools/use_photos.py --list      show what is wired up right now
    python3 tools/use_photos.py --revert    go back to the illustrations
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
PHOTO_DIR = os.path.join(ROOT, "assets", "dishes", "photos")
EXTS = ("jpg", "jpeg", "png", "webp", "avif")

SLUGS = [
    "salama-platter", "bariis-iskukaris", "hilib-ari", "digaag-shiilan",
    "suqaar", "digaag-qumbe", "canjeero", "sambusa", "malawah", "xalwo",
    "shaah", "muufo", "basbaas",
]


def current_src(html, slug):
    """What the page currently points at for this dish, if anything."""
    m = re.search(rf'assets/dishes/(?:photos/)?{re.escape(slug)}\.(?:svg|{"|".join(EXTS)})', html)
    return m.group(0) if m else None


def find_photo(slug):
    for ext in EXTS:
        p = os.path.join(PHOTO_DIR, f"{slug}.{ext}")
        if os.path.isfile(p):
            return f"assets/dishes/photos/{slug}.{ext}"
    return None


def retarget(html, slug, new_path):
    pattern = rf'assets/dishes/(?:photos/)?{re.escape(slug)}\.(?:svg|{"|".join(EXTS)})'
    return re.subn(pattern, new_path, html)


def main():
    if not os.path.isfile(HTML):
        sys.exit(f"index.html not found at {HTML}")
    html = open(HTML).read()
    revert = "--revert" in sys.argv
    listing = "--list" in sys.argv

    if listing:
        print(f"{'dish':<20} {'in use':<46} photo available?")
        for slug in SLUGS:
            cur = current_src(html, slug) or "— not on the page —"
            have = find_photo(slug)
            print(f"{slug:<20} {cur:<46} {'yes: ' + have if have else 'no'}")
        return

    os.makedirs(PHOTO_DIR, exist_ok=True)
    changed = 0
    swapped = []
    for slug in SLUGS:
        if current_src(html, slug) is None:
            continue                                   # dish not used on the page
        if revert:
            target = f"assets/dishes/{slug}.svg"
        else:
            target = find_photo(slug)
            if not target:
                continue
        if current_src(html, slug) == target:
            continue                                   # already correct
        html, n = retarget(html, slug, target)
        if n:
            changed += n
            swapped.append((slug, target))

    if not changed:
        if revert:
            print("Already using the illustrations — nothing to change.")
        else:
            have_any = any(find_photo(s) for s in SLUGS)
            if not have_any:
                print(f"No photos found in {os.path.relpath(PHOTO_DIR, ROOT)}/")
                print("Add files named after the dish, e.g. bariis-iskukaris.jpg, then run this again.")
                print("Recognised names: " + ", ".join(SLUGS))
            else:
                print("Everything is already pointing at your photos.")
        return

    open(HTML, "w").write(html)
    for slug, target in swapped:
        print(f"  {slug:<20} -> {target}")
    print(f"\nUpdated {changed} image reference(s) in index.html.")
    if not revert:
        print("Tip: landscape or square photos both work — they are cropped with object-fit: cover.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:      # e.g. `--list | head`
        try:
            sys.stdout.close()
        finally:
            os._exit(0)
