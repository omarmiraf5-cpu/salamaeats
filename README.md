# Salama Eats Ltd — Website

An elegant, single-page static website for Salama Eats Ltd, a halal Mediterranean grill located at 16773 71 St, Edmonton, AB.

## Structure

- `index.html` — page markup and content
- `style.css` — all styling (dark charcoal + gold, Playfair Display + Inter)
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
- Swap the CSS gradient placeholders (`.hero-bg`, `.g-item`, `.media-frame`) for real photography.
- Confirm the exact city/province/postal code for 16773 71 St and update the address and embedded map accordingly.
- Wire the reservation form (`#reserveForm` in `script.js`) to a real backend, email service, or reservation platform (e.g. OpenTable, Resy) — it currently only shows a confirmation message client-side.
- Add real social links in the footer and "Visit" section.
