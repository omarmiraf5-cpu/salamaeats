# Put your dish photos here

Name each photo after its dish, then run `python3 tools/use_photos.py` from the
project root. Any dish you have a photo for gets swapped in automatically; the
rest keep their illustration, so you can add photos a few at a time.

## File names

| File name (any of `.jpg` `.jpeg` `.png` `.webp` `.avif`) | Dish |
|---|---|
| `bariis-iskukaris.jpg` | Bariis Iskukaris — spiced rice with lamb |
| `hilib-ari.jpg`        | Hilib Ari — slow-roasted goat |
| `suqaar.jpg`           | Suqaar — diced beef with peppers |
| `digaag-qumbe.jpg`     | Digaag Qumbe — chicken in coconut sauce |
| `canjeero.jpg`         | Canjeero — fermented pancake |
| `sambusa.jpg`          | Sambusa — spiced beef pastry |
| `malawah.jpg`          | Malawah — sweet layered pancake |
| `xalwo.jpg`            | Xalwo — cardamom halwa |
| `shaah.jpg`            | Shaah — spiced tea |
| `muufo.jpg`            | Muufo — cornmeal flatbread |
| `basbaas.jpg`          | Basbaas — chilli relish |

## Shooting notes

- **Any shape works.** Photos are cropped with `object-fit: cover`, centred
  slightly above middle, so keep the dish roughly centred with a little room
  around it.
- **Aim for ~1600px on the long edge.** Bigger is fine; under ~800px will look
  soft on retina screens.
- **Shoot on a dark surface** if you can — a dark wood table, slate, or a black
  tray. The site is black and gold, so dark backgrounds blend beautifully and
  bright white backgrounds will look like cut-out boxes.
- **Use window light, not overhead lights.** Place the plate next to a window,
  with the light coming from the side or slightly behind the dish. Turn the
  restaurant's ceiling lights off — mixing them with daylight causes odd colour.
- **Straight down or ~30° low angle** both work well; be consistent across the set.
- A phone camera is genuinely fine. Wipe the lens, tap to focus on the food, and
  take a few frames.

## Useful commands

```bash
python3 tools/use_photos.py           # wire in every photo found here
python3 tools/use_photos.py --list    # show what's currently used
python3 tools/use_photos.py --revert  # go back to the illustrations
```
