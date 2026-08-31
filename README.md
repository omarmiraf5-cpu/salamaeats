# Salama Eats Ltd — Website

An elegant, single-page static website for Salama Eats Ltd, a halal Mediterranean grill located at 16773 71 St, Edmonton, AB. The design draws on Andalusian courtyard architecture (Moorish arches, geometric tile-inspired lattice texture) paired with Somali &amp; Arab hospitality — an ivory/charcoal palette with terracotta and gold accents, italic serif display type, and a "Heritage" section telling that story.

## Structure

- `index.html` — page markup and content
- `style.css` — all styling (ivory/charcoal + terracotta/gold, Cormorant Garamond + Jost)
- `script.js` — nav, scroll reveal, menu tabs, testimonial carousel, reservation form
- `assets/` — favicon and static assets

## Running locally

No build step required. Serve the folder with any static server, e.g.:

```
npx serve .
```

or simply open `index.html` in a browser.

## Things to customize before launch

- Replace placeholder phone number, email, and hours in the "Visit" section of `index.html`.
- Swap the CSS gradient placeholders (`.arch-photo`, `.g-item`) for real photography — the Moorish arch frames (`.arch-frame`) are designed to crop a photo into a rounded-arch shape.
- Confirm the exact city/province/postal code for 16773 71 St and update the address and embedded map accordingly.
- Wire the reservation form (`#reserveForm` in `script.js`) to a real backend, email service, or reservation platform (e.g. OpenTable, Resy) — it currently only shows a confirmation message client-side.
- Add real social links in the footer and "Visit" section.
