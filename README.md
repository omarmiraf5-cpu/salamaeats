# Salaama Eats Ltd — Website

An elegant, single-page static website for Salaama Eats Ltd, a halal Mediterranean grill located at 16773 71 St, Edmonton, AB. The design draws on Andalusian courtyard architecture (Moorish arches, geometric tile-inspired lattice texture) paired with Somali &amp; Arab hospitality — a black, gold and red palette, italic serif display type, a full-bleed framed hero with a script logotype, a sliding "Chef's Selection" of Somali dishes, and a "Heritage" section telling that story.

## Structure

- `index.html` — page markup and content
- `style.css` — all styling (black background, Cormorant Garamond + Jost)
- `theme-tangerine.css` — **alternate** accent theme (tangerine-orange instead of the muted gold/red).
  Background, text and every other surface stay exactly as `style.css` defines them — it only overrides
  the accent color. Remove its `<link>` from `index.html` to return to the original gold/red accent.
- `script.js` — nav, scroll reveal, signature-dish slider (arrows, dots, drag-to-scroll, autoplay), menu tabs, testimonial carousel, arch tilt, reservation form
- `assets/fonts/` — self-hosted woff2 fonts (Great Vibes, Cormorant Garamond, Jost) — no external font requests
- `assets/logo-mark.webp` / `assets/logo-full.webp` — the owner's real logo (chef-hat/flame emblem, and the
  full lockup with "Salaama Eats Mediterranean Grill"), background keyed to transparent so it drops onto
  both the light header and the dark footer. Used in the header, the in-hero nav, the footer, and the
  preloader. `assets/favicon-{32,180,512}.png` are cropped from the same source. See
  `tools/process_logo.py` and `assets/branding/logo-source.jpg` to regenerate these from a new logo photo.
- `assets/dishes/photos/` — 4 real customer/owner-submitted photos, used for the hero, heritage arch,
  gallery and Chef's Selection slider
- `assets/dishes/menu/` — small thumbnails for every menu-list item (56 of them), cropped from the 5
  physical menu-board photos the owner sent and trimmed to remove background margin. See
  `tools/crop_menu_boards.py` for how these were made if the boards are re-shot and need re-cropping.
- `assets/dishes/` — fallback SVG illustrations for dishes that don't have a photo yet

## Running locally

No build step required. Serve the folder with any static server, e.g.:

```
npx serve .
```

or simply open `index.html` in a browser.

## Things to customize before launch

- Replace placeholder phone number, email, and hours in the "Visit" section of `index.html`.
- **The site now uses real photographs** (`assets/dishes/photos/`) for the hero, the heritage arch, the
  Chef's Selection slider and the gallery, captioned with real menu items (Rice & Meat Meal, Beef Shanks,
  Haneeth, Lime Chicken). Note: the photo-to-dish pairing was my best guess by visual match, not confirmed
  — double check the captions in `index.html` are actually correct for each photo. The original SVG
  illustrations remain in `assets/dishes/` as a fallback for dishes without a photo yet, and can be
  regenerated with `python3 tools/gen_dishes.py`.

  **To add more real photographs:** drop them into `assets/dishes/photos/` (the file name only matters for
  `tools/use_photos.py`'s automatic wiring — see that script and `assets/dishes/photos/README.md` for the
  slug list) and either update `index.html` by hand or run `python3 tools/use_photos.py`.
- **The menu (`#menu` in `index.html`) now reflects the real, physical menu boards**: Lunch & Dinner,
  Salads, Dessert, Bubble Tea & Iced Coffee, and Coffee & Smoothies — 56 items total, each with a real
  photo thumbnail. One thing from the photographed menu still needs the owner's confirmation: item 16 and
  item 20 are both listed as "Rice & Veggies" but priced differently ($18 vs $21.60) with no distinguishing
  detail visible in the photo.
- The arch frames (`.arch-frame`) crop whatever image you give them into a rounded-arch shape, and each dish card's `.dish-media` is sized for a vertical food photo.
- Add or reorder dishes in the "Chef's Selection" slider by editing the `.dish-card` articles in `index.html` — the arrows, dots, and autoplay adapt to however many cards are present.
- Confirm the exact city/province/postal code for 16773 71 St and update the address and embedded map accordingly.
- Wire the reservation form (`#reserveForm` in `script.js`) to a real backend, email service, or reservation platform (e.g. OpenTable, Resy) — it currently only shows a confirmation message client-side.
- Add real social links in the footer and "Visit" section.
