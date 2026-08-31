#!/usr/bin/env python3
"""Generate elegant SVG illustrations of Somali dishes for Salama Eats.

Style: dark ceramic plate on near-black ground, gold rim, warm food tones —
matching the site's black / gold / red palette.
"""
import math
import random
import os

W, H = 800, 900
CX, CY = 400, 470          # plate centre
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "dishes")

GOLD = "#c89b4c"
GOLD_LT = "#e6c67d"
RED = "#cc3d3f"


def defs(glow="gold", plate_dark="#1a1410", plate_light="#2b211a"):
    glow_col = "rgba(230,198,125,0.30)" if glow == "gold" else "rgba(204,61,63,0.30)"
    return f'''
<defs>
  <radialGradient id="bgGlow" cx="50%" cy="38%" r="62%">
    <stop offset="0%" stop-color="{glow_col.replace('rgba','rgb').replace(',0.30)',')')}" stop-opacity="0.30"/>
    <stop offset="100%" stop-color="#0b0907" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="plateGrad" cx="42%" cy="34%" r="72%">
    <stop offset="0%" stop-color="{plate_light}"/>
    <stop offset="100%" stop-color="{plate_dark}"/>
  </radialGradient>
  <radialGradient id="foodGlow" cx="50%" cy="45%" r="55%">
    <stop offset="0%" stop-color="#e6c67d" stop-opacity="0.22"/>
    <stop offset="100%" stop-color="#e6c67d" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="rimGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="{GOLD_LT}"/>
    <stop offset="45%" stop-color="{GOLD}"/>
    <stop offset="100%" stop-color="#7d5f2b"/>
  </linearGradient>
  <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <filter id="soft2" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="3"/>
  </filter>
</defs>'''


def ground():
    return f'''
<rect width="{W}" height="{H}" fill="#0b0907"/>
<rect width="{W}" height="{H}" fill="url(#bgGlow)"/>
<ellipse cx="{CX}" cy="{CY+300}" rx="330" ry="46" fill="#000" opacity="0.55" filter="url(#soft)"/>'''


def plate(r=300, rim=True, bowl=False):
    s = ''
    if bowl:
        s += f'<ellipse cx="{CX}" cy="{CY}" rx="{r}" ry="{int(r*0.86)}" fill="url(#plateGrad)"/>'
        s += f'<ellipse cx="{CX}" cy="{CY}" rx="{r}" ry="{int(r*0.86)}" fill="none" stroke="url(#rimGrad)" stroke-width="5" opacity="0.95"/>'
        s += f'<ellipse cx="{CX}" cy="{CY+8}" rx="{int(r*0.80)}" ry="{int(r*0.66)}" fill="#120d0a" opacity="0.85"/>'
    else:
        s += f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="url(#plateGrad)"/>'
        s += f'<circle cx="{CX}" cy="{CY}" r="{r}" fill="none" stroke="url(#rimGrad)" stroke-width="5" opacity="0.95"/>'
        s += f'<circle cx="{CX}" cy="{CY}" r="{int(r*0.86)}" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity="0.4"/>'
    # ceramic sheen
    s += f'<ellipse cx="{CX-110}" cy="{CY-150}" rx="150" ry="70" fill="#fff" opacity="0.05" filter="url(#soft)" transform="rotate(-25 {CX-110} {CY-150})"/>'
    return s


def steam(x, y, n=3, spread=70, op=0.16):
    out = ''
    for i in range(n):
        sx = x + (i - (n - 1) / 2) * spread
        out += (f'<path d="M{sx} {y} c -20 -45 22 -70 2 -115 c -18 -40 16 -60 4 -96" '
                f'fill="none" stroke="#f3e9d8" stroke-width="7" stroke-linecap="round" '
                f'opacity="{op}" filter="url(#soft2)"/>')
    return out


def food_glow(r=250):
    return f'<circle cx="{CX}" cy="{CY-10}" r="{r}" fill="url(#foodGlow)"/>'


# ---------------------------------------------------------------- ingredients

def rice_mound(rng, cx, cy, rx, ry, count=900, palette=None, raisins=0, seedlings=True):
    """A mound of individual rice grains."""
    palette = palette or ["#f0d79a", "#e8c97f", "#dcb862", "#f5e3b6", "#cfa54e"]
    out = [f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#8d6a33" opacity="0.55"/>']
    for _ in range(count):
        # sample inside ellipse, denser toward centre for a mounded look
        t = rng.random() ** 0.55
        a = rng.uniform(0, 2 * math.pi)
        gx = cx + math.cos(a) * rx * t
        gy = cy + math.sin(a) * ry * t
        # lift grains near the centre to suggest a heap
        gy -= (1 - t) * ry * 0.30
        rot = rng.uniform(0, 180)
        gl = rng.uniform(7, 12)
        gw = rng.uniform(2.6, 4.0)
        col = rng.choice(palette)
        op = rng.uniform(0.72, 1.0)
        out.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{gl:.1f}" ry="{gw:.1f}" '
                   f'fill="{col}" opacity="{op:.2f}" transform="rotate({rot:.0f} {gx:.1f} {gy:.1f})"/>')
    for _ in range(raisins):
        t = rng.random() ** 0.6
        a = rng.uniform(0, 2 * math.pi)
        gx = cx + math.cos(a) * rx * t * 0.92
        gy = cy + math.sin(a) * ry * t * 0.92 - (1 - t) * ry * 0.25
        rr = rng.uniform(6, 9)
        out.append(f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{rr:.1f}" ry="{rr*0.78:.1f}" fill="#4b2418" opacity="0.95"/>')
        out.append(f'<ellipse cx="{gx-rr*0.3:.1f}" cy="{gy-rr*0.3:.1f}" rx="{rr*0.3:.1f}" ry="{rr*0.22:.1f}" fill="#7d4230" opacity="0.7"/>')
    return ''.join(out)


def meat_chunk(rng, cx, cy, w, h, rot=0, base="#8a4a24", top="#b06a33", char=True):
    """An irregular braised-meat piece."""
    pts = []
    n = 9
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = 1 + rng.uniform(-0.13, 0.13)
        pts.append((cx + math.cos(a) * w * rr, cy + math.sin(a) * h * rr))
    d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
    out = f'<g transform="rotate({rot:.0f} {cx:.1f} {cy:.1f})">'
    out += f'<path d="{d}" fill="{base}"/>'
    out += (f'<ellipse cx="{cx-w*0.18:.1f}" cy="{cy-h*0.22:.1f}" rx="{w*0.55:.1f}" ry="{h*0.45:.1f}" '
            f'fill="{top}" opacity="0.85"/>')
    out += (f'<ellipse cx="{cx-w*0.28:.1f}" cy="{cy-h*0.34:.1f}" rx="{w*0.26:.1f}" ry="{h*0.17:.1f}" '
            f'fill="#d99a55" opacity="0.55"/>')
    if char:
        for _ in range(3):
            bx = cx + rng.uniform(-w * 0.5, w * 0.5)
            by = cy + rng.uniform(-h * 0.45, h * 0.5)
            out += (f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rng.uniform(5,11):.1f}" '
                    f'ry="{rng.uniform(3,6):.1f}" fill="#4a2413" opacity="0.5"/>')
    out += '</g>'
    return out


def herb(rng, cx, cy, s=1.0, col="#6f8f4a"):
    """A small coriander/parsley sprig."""
    out = f'<g transform="translate({cx:.1f} {cy:.1f}) scale({s:.2f}) rotate({rng.uniform(0,360):.0f})">'
    for a in (-52, -18, 18, 52):
        out += (f'<ellipse cx="{math.cos(math.radians(a))*16:.1f}" cy="{math.sin(math.radians(a))*16:.1f}" '
                f'rx="12" ry="7" fill="{col}" opacity="0.9" '
                f'transform="rotate({a} {math.cos(math.radians(a))*16:.1f} {math.sin(math.radians(a))*16:.1f})"/>')
    out += f'<circle cx="0" cy="0" r="4" fill="{col}" opacity="0.8"/>'
    out += '</g>'
    return out


def chili(cx, cy, rot=0, col=RED):
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<path d="M{cx-34} {cy} q 20 -17 40 -3 q 18 12 30 4" fill="none" stroke="{col}" '
            f'stroke-width="11" stroke-linecap="round"/>'
            f'<path d="M{cx-34} {cy} q 8 -12 -6 -16" fill="none" stroke="#6f8f4a" stroke-width="6" stroke-linecap="round"/>'
            f'</g>')


def lemon_wedge(cx, cy, r=40, rot=0):
    return (f'<g transform="rotate({rot} {cx} {cy})">'
            f'<path d="M{cx} {cy} m -{r} 0 a {r} {r} 0 0 1 {2*r} 0 Z" fill="#e8c34e"/>'
            f'<path d="M{cx} {cy} m -{r*0.82:.0f} 0 a {r*0.82:.0f} {r*0.82:.0f} 0 0 1 {2*r*0.82:.0f} 0 Z" fill="#f5df8f"/>'
            + ''.join(f'<path d="M{cx} {cy} L{cx + math.cos(math.radians(180 + i*36))*r*0.78:.1f} '
                      f'{cy + math.sin(math.radians(180 + i*36))*r*0.78:.1f}" stroke="#e8c34e" stroke-width="2.5" opacity="0.8"/>'
                      for i in range(1, 5))
            + f'</g>')


def wrap(body, glow="gold"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            + defs(glow) + ground() + body + '</svg>')


def write(name, body, glow="gold"):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(wrap(body, glow))
    return path


# ---------------------------------------------------------------- dishes

def bariis_iskukaris():
    rng = random.Random(11)
    b = plate() + food_glow()
    b += rice_mound(rng, CX, CY + 10, 236, 176, count=1150, raisins=26)
    # lamb pieces crowning the rice
    for (mx, my, w, h, rot) in [(CX - 78, CY - 58, 66, 44, -14), (CX + 62, CY - 40, 72, 46, 12),
                                (CX - 6, CY + 44, 78, 48, 6), (CX + 96, CY + 58, 58, 38, -20)]:
        b += meat_chunk(rng, mx, my, w, h, rot)
    for _ in range(7):
        b += herb(rng, CX + rng.uniform(-200, 200), CY + rng.uniform(-140, 150), rng.uniform(0.5, 0.85))
    b += lemon_wedge(CX + 176, CY + 130, 42, rot=-30)
    b += steam(CX, CY - 210, 3, 76)
    return b


def hilib_ari():
    rng = random.Random(23)
    b = plate() + food_glow()
    b += rice_mound(rng, CX, CY + 62, 232, 130, count=700, palette=["#efd79c", "#e3c274", "#d6b25e", "#f6e7bb"])
    # generous goat/lamb pieces
    layout = [(CX - 92, CY - 46, 84, 56, -12), (CX + 66, CY - 66, 78, 52, 16),
              (CX - 10, CY - 118, 70, 46, 4), (CX + 118, CY + 10, 66, 44, -24),
              (CX - 150, CY + 22, 62, 42, 22), (CX + 16, CY + 6, 88, 54, -6)]
    for (mx, my, w, h, rot) in layout:
        b += meat_chunk(rng, mx, my, w, h, rot, base="#7d4020", top="#a85f2c")
    # bone
    b += (f'<g transform="rotate(-18 {CX+40} {CY-30})">'
          f'<rect x="{CX+16}" y="{CY-40}" width="86" height="20" rx="10" fill="#efe6d2" opacity="0.92"/>'
          f'<circle cx="{CX+16}" cy="{CY-30}" r="15" fill="#efe6d2" opacity="0.92"/>'
          f'<circle cx="{CX+102}" cy="{CY-30}" r="15" fill="#efe6d2" opacity="0.92"/></g>')
    for _ in range(6):
        b += herb(rng, CX + rng.uniform(-190, 190), CY + rng.uniform(-150, 150), rng.uniform(0.5, 0.8))
    b += chili(CX - 150, CY + 150, rot=10)
    b += steam(CX, CY - 220, 3, 80)
    return b


def suqaar():
    rng = random.Random(37)
    b = plate(bowl=True) + food_glow(220)
    rng2 = random.Random(5)
    # glossy pan sauce beneath the pile
    b += f'<ellipse cx="{CX}" cy="{CY+16}" rx="212" ry="150" fill="#5c2c14" opacity="0.9"/>'
    b += f'<ellipse cx="{CX-70}" cy="{CY-40}" rx="80" ry="42" fill="#8a4a24" opacity="0.5" filter="url(#soft2)"/>'
    # onion + pepper strips underneath
    for _ in range(30):
        t = rng2.random() ** 0.5
        a = rng2.uniform(0, 2 * math.pi)
        x = CX + math.cos(a) * 190 * t
        y = CY + math.sin(a) * 138 * t
        col = rng2.choice([RED, "#d1552f", "#6f8f4a", "#e8d9bd"])
        b += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{rng2.uniform(46,76):.1f}" height="13" rx="6.5" '
              f'fill="{col}" opacity="0.95" transform="rotate({rng2.uniform(0,360):.0f} {x:.1f} {y:.1f})"/>')
    # a generous heap of seared diced beef
    cubes = []
    for _ in range(72):
        t = rng2.random() ** 0.62
        a = rng2.uniform(0, 2 * math.pi)
        x = CX + math.cos(a) * 176 * t
        y = CY + math.sin(a) * 128 * t - (1 - t) * 34
        cubes.append((y, x, rng2.uniform(38, 56), rng2.uniform(0, 90)))
    for (y, x, s, rot) in sorted(cubes):           # paint back-to-front
        col = rng2.choice(["#8a4a24", "#9c5628", "#7a3d1d", "#a86230", "#6d3618"])
        b += (f'<g transform="rotate({rot:.0f} {x:.1f} {y:.1f})">'
              f'<rect x="{x-s/2:.1f}" y="{y-s/2+4:.1f}" width="{s:.1f}" height="{s:.1f}" rx="9" fill="#000" opacity="0.35"/>'
              f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s:.1f}" height="{s:.1f}" rx="9" fill="{col}"/>'
              f'<rect x="{x-s/2+5:.1f}" y="{y-s/2+5:.1f}" width="{s*0.52:.1f}" height="{s*0.38:.1f}" rx="7" '
              f'fill="#c8813e" opacity="0.6"/>'
              f'<rect x="{x-s/2+s*0.55:.1f}" y="{y-s/2+s*0.6:.1f}" width="{s*0.3:.1f}" height="{s*0.24:.1f}" rx="5" '
              f'fill="#4a2413" opacity="0.4"/></g>')
    for _ in range(7):
        b += herb(rng, CX + rng.uniform(-180, 180), CY + rng.uniform(-130, 130), rng.uniform(0.55, 0.9))
    b += steam(CX, CY - 190, 3, 70, op=0.2)
    return b


def canjeero():
    rng = random.Random(51)
    b = plate() + food_glow(230)
    # stack of three folded fermented pancakes
    for i, (dx, dy, rr) in enumerate([(-26, 40, -8), (14, 8, 6), (-4, -34, -3)]):
        cx, cy = CX + dx, CY + dy
        b += (f'<g transform="rotate({rr} {cx} {cy})">'
              f'<ellipse cx="{cx}" cy="{cy+8}" rx="196" ry="150" fill="#000" opacity="0.4" filter="url(#soft2)"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="196" ry="150" fill="#d9b06b"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="196" ry="150" fill="none" stroke="#a9803c" stroke-width="4" opacity="0.85"/>')
        # the characteristic honeycomb holes
        hr = random.Random(100 + i)
        for _ in range(210):
            t = hr.random() ** 0.5
            a = hr.uniform(0, 2 * math.pi)
            hx = cx + math.cos(a) * 180 * t
            hy = cy + math.sin(a) * 136 * t
            rad = hr.uniform(4, 12)
            b += (f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{rad:.1f}" fill="#a97f3d" '
                  f'opacity="{hr.uniform(0.4,0.85):.2f}"/>')
            b += (f'<circle cx="{hx-rad*0.25:.1f}" cy="{hy-rad*0.25:.1f}" r="{rad*0.45:.1f}" fill="#f0d5a0" '
                  f'opacity="{hr.uniform(0.2,0.5):.2f}"/>')
        b += (f'<ellipse cx="{cx-70}" cy="{cy-58}" rx="76" ry="44" fill="#f3ddaf" opacity="0.28" '
              f'filter="url(#soft2)"/></g>')
    # ghee / honey pooling on top
    b += (f'<path d="M{CX-92} {CY-54} q 46 40 104 12 q 42 -20 66 18" fill="none" stroke="#e0a63f" '
          f'stroke-width="15" stroke-linecap="round" opacity="0.9"/>')
    b += f'<ellipse cx="{CX+96}" cy="{CY-16}" rx="40" ry="23" fill="#e0a63f" opacity="0.85"/>'
    b += steam(CX, CY - 200, 2, 90, op=0.14)
    return b


def digaag_qumbe():
    rng = random.Random(67)
    b = plate(bowl=True) + food_glow(220)
    # coconut sauce pool
    b += f'<ellipse cx="{CX}" cy="{CY+6}" rx="216" ry="168" fill="#efe3c9" opacity="0.95"/>'
    b += f'<ellipse cx="{CX}" cy="{CY+6}" rx="216" ry="168" fill="#e7d3ad" opacity="0.5"/>'
    b += f'<ellipse cx="{CX-70}" cy="{CY-56}" rx="86" ry="48" fill="#fbf3e0" opacity="0.5" filter="url(#soft2)"/>'
    # golden turmeric swirls
    for i in range(4):
        yy = CY - 70 + i * 46
        b += (f'<path d="M{CX-160} {yy} q 70 {26 if i%2 else -26} 150 0 q 60 {-22 if i%2 else 22} 130 2" '
              f'fill="none" stroke="#dda945" stroke-width="7" opacity="0.5" stroke-linecap="round"/>')
    # chicken pieces
    for (mx, my, w, h, rot) in [(CX - 84, CY - 40, 76, 50, -10), (CX + 70, CY - 58, 70, 46, 14),
                                (CX + 10, CY + 40, 84, 52, 4), (CX - 110, CY + 62, 62, 42, 20),
                                (CX + 128, CY + 44, 60, 40, -18)]:
        b += meat_chunk(rng, mx, my, w, h, rot, base="#c98a3e", top="#e0aa5c", char=False)
    for _ in range(7):
        b += herb(rng, CX + rng.uniform(-180, 180), CY + rng.uniform(-130, 130), rng.uniform(0.5, 0.85))
    b += chili(CX + 132, CY - 118, rot=-14)
    b += steam(CX, CY - 200, 3, 74, op=0.18)
    return b


def sambusa():
    rng = random.Random(83)
    b = plate() + food_glow(230)
    # three golden pastry triangles
    def tri(cx, cy, s, rot):
        pts = [(cx, cy - s), (cx - s * 0.92, cy + s * 0.72), (cx + s * 0.92, cy + s * 0.72)]
        d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ' Z'
        g = f'<g transform="rotate({rot} {cx} {cy})">'
        g += f'<path d="{d}" fill="#000" opacity="0.4" transform="translate(0 9)" filter="url(#soft2)"/>'
        g += f'<path d="{d}" fill="#d59b4d"/>'
        g += f'<path d="{d}" fill="url(#foodGlow)" opacity="0.5"/>'
        # blistered pastry highlights + seam
        g += (f'<path d="M{cx:.1f} {cy-s*0.92:.1f} L{cx:.1f} {cy+s*0.66:.1f}" stroke="#b97f38" '
              f'stroke-width="3" opacity="0.6"/>')
        for _ in range(9):
            bx = cx + rng.uniform(-s * 0.6, s * 0.6)
            by = cy + rng.uniform(-s * 0.4, s * 0.55)
            g += (f'<ellipse cx="{bx:.1f}" cy="{by:.1f}" rx="{rng.uniform(6,13):.1f}" ry="{rng.uniform(4,8):.1f}" '
                  f'fill="#eab767" opacity="{rng.uniform(0.3,0.6):.2f}"/>')
        g += (f'<path d="M{cx-s*0.9:.1f} {cy+s*0.7:.1f} L{cx+s*0.9:.1f} {cy+s*0.7:.1f}" stroke="#a86f2f" '
              f'stroke-width="4" opacity="0.7"/>')
        g += '</g>'
        return g
    # three samosas laid out with clear separation, all sitting upright
    b += tri(CX - 132, CY - 84, 88, -7)
    b += tri(CX + 122, CY - 88, 86, 8)
    b += tri(CX - 22, CY + 66, 104, -2)
    # dipping sauce
    b += f'<ellipse cx="{CX+176}" cy="{CY+148}" rx="70" ry="64" fill="#000" opacity="0.4" filter="url(#soft2)"/>'
    b += f'<circle cx="{CX+174}" cy="{CY+140}" r="68" fill="#1a1410"/>'
    b += f'<circle cx="{CX+174}" cy="{CY+140}" r="68" fill="none" stroke="url(#rimGrad)" stroke-width="3.5"/>'
    b += f'<circle cx="{CX+174}" cy="{CY+140}" r="53" fill="#8e2622"/>'
    b += f'<ellipse cx="{CX+156}" cy="{CY+122}" rx="21" ry="12" fill="#c0453c" opacity="0.7"/>'
    for _ in range(5):
        b += herb(rng, CX + rng.uniform(-190, 190), CY + rng.uniform(-170, 170), rng.uniform(0.45, 0.7))
    return b


def malawah():
    rng = random.Random(97)
    b = plate() + food_glow(230)
    # stack of thin sweet pancakes
    for i, (dx, dy) in enumerate([(-18, 52), (10, 22), (-8, -8), (6, -40)]):
        cx, cy = CX + dx, CY + dy
        b += (f'<ellipse cx="{cx}" cy="{cy+7}" rx="188" ry="132" fill="#000" opacity="0.3" filter="url(#soft2)"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="188" ry="132" fill="#e9c581"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="188" ry="132" fill="none" stroke="#c69a4f" stroke-width="3" opacity="0.75"/>')
        hr = random.Random(400 + i)
        for _ in range(40):
            t = hr.random() ** 0.5
            a = hr.uniform(0, 2 * math.pi)
            hx = cx + math.cos(a) * 172 * t
            hy = cy + math.sin(a) * 120 * t
            b += (f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{hr.uniform(8,20):.1f}" ry="{hr.uniform(5,11):.1f}" '
                  f'fill="#d7a856" opacity="{hr.uniform(0.25,0.5):.2f}"/>')
    # honey drizzle + dusting
    b += (f'<path d="M{CX-120} {CY-72} q 56 44 118 14 q 52 -26 84 22" fill="none" stroke="#e0a63f" '
          f'stroke-width="14" stroke-linecap="round" opacity="0.9"/>')
    b += f'<ellipse cx="{CX+112}" cy="{CY-30}" rx="40" ry="24" fill="#e0a63f" opacity="0.8"/>'
    for _ in range(60):
        x = CX + rng.uniform(-180, 180)
        y = CY + rng.uniform(-120, 130)
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(1.5,3.2):.1f}" fill="#fff" opacity="{rng.uniform(0.3,0.7):.2f}"/>'
    return b


def xalwo():
    rng = random.Random(113)
    b = plate() + food_glow(220)
    # glossy amber halwa, clustered in a generous mound
    coords = [(CX - 96, CY + 6), (CX + 4, CY + 30), (CX + 106, CY + 4),
              (CX - 50, CY - 66), (CX + 56, CY - 62), (CX + 4, CY - 130)]
    for i, (x, y) in enumerate(coords):
        s = 116 if i % 2 == 0 else 104
        rot = rng.uniform(-16, 16)
        b += (f'<g transform="rotate({rot:.0f} {x} {y})">'
              f'<rect x="{x-s/2}" y="{y-s/2+10}" width="{s}" height="{s}" rx="18" fill="#000" opacity="0.45" filter="url(#soft2)"/>'
              f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="18" fill="#a0331f"/>'
              f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="18" fill="url(#foodGlow)" opacity="0.85"/>'
              # broad glossy sheen — halwa is translucent and wet-looking
              f'<rect x="{x-s/2+9}" y="{y-s/2+9}" width="{s*0.5:.0f}" height="{s*0.34:.0f}" rx="12" fill="#e9944a" opacity="0.6"/>'
              f'<rect x="{x-s/2+13}" y="{y-s/2+13}" width="{s*0.26:.0f}" height="{s*0.15:.0f}" rx="7" fill="#ffd9a6" opacity="0.55"/>'
              f'<rect x="{x-s/2+s*0.5:.0f}" y="{y-s/2+s*0.58:.0f}" width="{s*0.36:.0f}" height="{s*0.26:.0f}" rx="10" '
              f'fill="#6d1f13" opacity="0.45"/>'
              f'<rect x="{x-s/2}" y="{y-s/2}" width="{s}" height="{s}" rx="18" fill="none" stroke="{GOLD}" '
              f'stroke-width="2.2" opacity="0.6"/>')
        # pistachio flecks set into the sweet
        for _ in range(6):
            px = x + rng.uniform(-s * 0.32, s * 0.32)
            py = y + rng.uniform(-s * 0.32, s * 0.32)
            b += (f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{rng.uniform(8,12):.1f}" ry="{rng.uniform(6,9):.1f}" '
                  f'fill="#7f9a4e" opacity="0.95" transform="rotate({rng.uniform(0,180):.0f} {px:.1f} {py:.1f})"/>')
        b += '</g>'
    # cardamom pods scattered on the rim
    for (px, py) in [(CX - 200, CY - 120), (CX + 196, CY + 118), (CX + 150, CY - 150)]:
        b += (f'<ellipse cx="{px}" cy="{py}" rx="17" ry="11" fill="#9aa86a" opacity="0.9" '
              f'transform="rotate({rng.uniform(0,180):.0f} {px} {py})"/>')
    return b


def shaah():
    rng = random.Random(131)
    # a tall tulip tea glass standing on a dark saucer
    base_y = CY + 210            # where the glass foot rests
    top_y = CY - 190             # glass rim
    half_top, half_bot = 116, 74 # tapered body

    b = f'<ellipse cx="{CX}" cy="{base_y+52}" rx="250" ry="40" fill="#000" opacity="0.55" filter="url(#soft)"/>'
    # saucer
    b += f'<ellipse cx="{CX}" cy="{base_y+26}" rx="242" ry="64" fill="url(#plateGrad)"/>'
    b += f'<ellipse cx="{CX}" cy="{base_y+26}" rx="242" ry="64" fill="none" stroke="url(#rimGrad)" stroke-width="4"/>'
    b += f'<ellipse cx="{CX}" cy="{base_y+22}" rx="150" ry="36" fill="#0f0b09" opacity="0.75"/>'

    glass = (f'M{CX-half_top} {top_y} '
             f'L{CX-half_bot} {base_y} Q{CX} {base_y+30} {CX+half_bot} {base_y} '
             f'L{CX+half_top} {top_y} Z')
    # glass body
    b += f'<path d="{glass}" fill="#171310" opacity="0.85"/>'
    # tea, filled to just below the rim
    tea_top = top_y + 54
    ratio = (tea_top - top_y) / (base_y - top_y)
    half_tea = half_top + (half_bot - half_top) * ratio
    b += (f'<path d="M{CX-half_tea:.1f} {tea_top} L{CX-half_bot+6} {base_y-6} '
          f'Q{CX} {base_y+22} {CX+half_bot-6} {base_y-6} L{CX+half_tea:.1f} {tea_top} Z" fill="#a5551f"/>')
    b += (f'<path d="M{CX-half_tea:.1f} {tea_top} L{CX-half_bot+6} {base_y-6} '
          f'Q{CX} {base_y+22} {CX+half_bot-6} {base_y-6} L{CX+half_tea:.1f} {tea_top} Z" '
          f'fill="url(#foodGlow)" opacity="0.95"/>')
    # milk swirling through it
    b += (f'<path d="M{CX-64} {CY-40} q 60 40 130 4" fill="none" stroke="#e9d3ab" stroke-width="18" '
          f'opacity="0.35" stroke-linecap="round"/>')
    b += (f'<path d="M{CX-50} {CY+52} q 52 32 108 2" fill="none" stroke="#e9d3ab" stroke-width="12" '
          f'opacity="0.22" stroke-linecap="round"/>')
    # tea surface
    b += f'<ellipse cx="{CX}" cy="{tea_top}" rx="{half_tea:.1f}" ry="20" fill="#c47b3a"/>'
    b += f'<ellipse cx="{CX}" cy="{tea_top}" rx="{half_tea-10:.1f}" ry="14" fill="#e2a463" opacity="0.65"/>'
    # glass highlights + gold rim
    b += (f'<path d="M{CX-half_top+22} {top_y+80} L{CX-half_bot+26} {base_y-40}" stroke="#fff" stroke-width="10" '
          f'opacity="0.14" stroke-linecap="round"/>')
    b += (f'<path d="M{CX+half_top-26} {top_y+96} L{CX+half_bot-30} {base_y-60}" stroke="#fff" stroke-width="6" '
          f'opacity="0.09" stroke-linecap="round"/>')
    b += f'<path d="{glass}" fill="none" stroke="{GOLD}" stroke-width="2" opacity="0.32"/>'
    b += (f'<ellipse cx="{CX}" cy="{top_y}" rx="{half_top}" ry="22" fill="none" stroke="url(#rimGrad)" '
          f'stroke-width="5"/>')
    # cinnamon stick + cardamom pods on the saucer
    b += (f'<g transform="rotate(-16 {CX+196} {base_y+30})">'
          f'<rect x="{CX+140}" y="{base_y+20}" width="112" height="22" rx="11" fill="#7a4520"/>'
          f'<rect x="{CX+140}" y="{base_y+20}" width="112" height="8" rx="4" fill="#9c5c2c" opacity="0.85"/></g>')
    for (px, py) in [(CX - 176, base_y + 30), (CX - 136, base_y + 44), (CX - 206, base_y + 46)]:
        b += (f'<ellipse cx="{px}" cy="{py}" rx="18" ry="11" fill="#9aa86a" opacity="0.92" '
              f'transform="rotate({rng.uniform(0,180):.0f} {px} {py})"/>')
    b += steam(CX, top_y - 40, 3, 66, op=0.2)
    return b


def muufo():
    rng = random.Random(149)
    b = plate() + food_glow(230)
    # cornmeal flatbread rounds
    for (dx, dy, rr, rad) in [(-40, 30, -10, 168), (34, -18, 8, 176)]:
        cx, cy = CX + dx, CY + dy
        b += (f'<g transform="rotate({rr} {cx} {cy})">'
              f'<ellipse cx="{cx}" cy="{cy+8}" rx="{rad}" ry="{rad*0.8:.0f}" fill="#000" opacity="0.35" filter="url(#soft2)"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="{rad}" ry="{rad*0.8:.0f}" fill="#e0be7e"/>')
        hr = random.Random(700 + int(dx))
        for _ in range(70):
            t = hr.random() ** 0.5
            a = hr.uniform(0, 2 * math.pi)
            hx = cx + math.cos(a) * rad * 0.9 * t
            hy = cy + math.sin(a) * rad * 0.72 * t
            b += (f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{hr.uniform(8,22):.1f}" ry="{hr.uniform(5,13):.1f}" '
                  f'fill="{hr.choice(["#c99a4e","#a97a37","#efd7a3"])}" opacity="{hr.uniform(0.25,0.6):.2f}"/>')
        b += (f'<ellipse cx="{cx}" cy="{cy}" rx="{rad}" ry="{rad*0.8:.0f}" fill="none" stroke="#b98c44" '
              f'stroke-width="4" opacity="0.8"/></g>')
    b += f'<ellipse cx="{CX+30}" cy="{CY-40}" rx="46" ry="26" fill="#e0a63f" opacity="0.75"/>'
    b += steam(CX, CY - 200, 2, 80, op=0.14)
    return b


def basbaas():
    rng = random.Random(163)
    b = plate(bowl=True) + food_glow(200)
    # bright green-chilli & coriander relish
    b += f'<ellipse cx="{CX}" cy="{CY+4}" rx="200" ry="150" fill="#5f7f3c"/>'
    for _ in range(220):
        t = rng.random() ** 0.5
        a = rng.uniform(0, 2 * math.pi)
        x = CX + math.cos(a) * 190 * t
        y = CY + math.sin(a) * 142 * t
        b += (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rng.uniform(5,14):.1f}" ry="{rng.uniform(3,8):.1f}" '
              f'fill="{rng.choice(["#7f9a4e","#496b2e","#94ad5c","#d8d08a"])}" opacity="{rng.uniform(0.5,0.95):.2f}" '
              f'transform="rotate({rng.uniform(0,180):.0f} {x:.1f} {y:.1f})"/>')
    b += f'<ellipse cx="{CX-64}" cy="{CY-50}" rx="70" ry="38" fill="#fff" opacity="0.1" filter="url(#soft2)"/>'
    b += chili(CX + 30, CY - 190, rot=8, col="#6f8f4a")
    b += chili(CX - 90, CY - 176, rot=-16)
    b += lemon_wedge(CX + 190, CY + 140, 44, rot=24)
    return b


DISHES = [
    ("bariis-iskukaris.svg", bariis_iskukaris, "gold"),
    ("hilib-ari.svg", hilib_ari, "red"),
    ("suqaar.svg", suqaar, "red"),
    ("canjeero.svg", canjeero, "gold"),
    ("digaag-qumbe.svg", digaag_qumbe, "gold"),
    ("sambusa.svg", sambusa, "gold"),
    ("malawah.svg", malawah, "gold"),
    ("xalwo.svg", xalwo, "red"),
    ("shaah.svg", shaah, "gold"),
    ("muufo.svg", muufo, "gold"),
    ("basbaas.svg", basbaas, "red"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn, glow in DISHES:
        p = write(name, fn(), glow)
        print(f"{p}  ({os.path.getsize(p)//1024} KB)")
