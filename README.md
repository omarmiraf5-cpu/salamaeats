# Salama Eats Ltd — Website

An elegant, single-page static website for Salama Eats Ltd, a halal Mediterranean grill located at 16773 71 St, Edmonton, AB. The design draws on Andalusian courtyard architecture (Moorish arches, geometric tile-inspired lattice texture) paired with Somali &amp; Arab hospitality — a black, gold and red palette, italic serif display type, a sliding "Chef's Selection" of Somali dishes, and a "Heritage" section telling that story.

## Structure

- `index.html` — page markup and content
- `style.css` — all styling (black + gold/red, Cormorant Garamond + Jost)
- `script.js` — nav, scroll reveal, signature-dish slider (arrows, dots, drag-to-scroll, autoplay), menu tabs, testimonial carousel, arch tilt, reservation form
- `assets/` — favicon and static assets
- `assets/dishes/` — hand-built SVG illustrations of Somali dishes (bariis iskukaris, hilib ari, suqaar,
  digaag qumbe, canjeero, sambusa, malawah, xalwo, shaah, muufo, basbaas), used by the dish slider,
  the hero and heritage arches, and the gallery

## Running locally

No build step required. Serve the folder with any static server, e.g.:

```
npx serve .
```

or simply open `index.html` in a browser.

## Things to customize before launch

- Replace placeholder phone number, email, and hours in the "Visit" section of `index.html`.
- **The dish images are vector illustrations, not photographs.** They are original artwork drawn to match
  the site's palette, so there are no licensing constraints, but real photographs of your actual dishes
  will always look better. Every image is now a plain `<img>` tag — drop a photo into `assets/dishes/`
  and change the `src` (they are cropped with `object-fit: cover`, so any aspect ratio works).
  Regenerate or tweak them with `tools/gen_dishes.py` (`python3 tools/gen_dishes.py`).

  **To use real photographs:** drop them into `assets/dishes/photos/` named after the dish
  (`bariis-iskukaris.jpg`, `hilib-ari.jpg`, …) and run `python3 tools/use_photos.py`. Photos you
  supply are wired into the slider, the hero and heritage arches, and the gallery automatically;
  dishes without a photo keep their illustration, so you can add them a few at a time.
  See `assets/dishes/photos/README.md` for the full name list and shooting notes.
- The arch frames (`.arch-frame`) crop whatever image you give them into a rounded-arch shape, and each dish card's `.dish-media` is sized for a vertical food photo.
- Add or reorder dishes in the "Chef's Selection" slider by editing the `.dish-card` articles in `index.html` — the arrows, dots, and autoplay adapt to however many cards are present.
- Confirm the exact city/province/postal code for 16773 71 St and update the address and embedded map accordingly.
- Wire the reservation form (`#reserveForm` in `script.js`) to a real backend, email service, or reservation platform (e.g. OpenTable, Resy) — it currently only shows a confirmation message client-side.
- Add real social links in the footer and "Visit" section.
