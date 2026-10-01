"""Render campaign maps from a small JSON spec into print-quality SVGs, VTT PNGs and Foundry walls.

    python map_svg.py <campaign>/maps/m1-mill.json [more.json ...] [--png] [--out DIR]

Three kinds of map (see references/maps-and-handouts.md for the full spec):
  dungeon     rooms, corridors and doors on a square grid (buildings, caves, vaults, ships)
  area        an outdoor battle map: trees, rocks, water, cliffs, paths on a square grid
  pointcrawl  a travel map: places joined by paths with travel times

Outputs land in <campaign>/build/maps/ by default:
  <id>-gm.svg      print map with keys, secret doors, traps and GM notes
  <id>-player.svg  print map with all of that removed (safe to show players)
  <id>-vtt.svg/.png  dungeon/area only: exactly cols x rows squares at foundry_px each, player-safe, no frame
  <id>-walls.json  dungeon/area only: Foundry wall data in VTT-image pixels (doors, secret doors, locks)

Standard library only. --png needs Chrome, Edge, Chromium or Brave (see browser.py).
Exit code 1 on any spec error; every error names the map and the field.
"""
import json
import math
import random
import sys
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

INK = "#1d1a17"
PAPER = "#fbf8f1"
FONT = "'Alegreya SC', 'Alegreya', Georgia, 'Times New Roman', serif"
SANS = "'Alegreya Sans', 'Segoe UI', Arial, sans-serif"


class SpecError(Exception):
    pass


VTT_PX = {"foundry": 100, "roll20": 70, "owlbear": 150, "fantasy-grounds": 50}


def vtt_px(spec):
    """Pixels per square for the VTT image: vtt_px, else foundry_px, else the named VTT's default, else 100."""
    if "vtt_px" in spec:
        return int(spec["vtt_px"])
    if "foundry_px" in spec:
        return int(spec["foundry_px"])
    return VTT_PX.get(str(spec.get("vtt", "foundry")).lower(), 100)


def need(spec, key, kind=None, where="map"):
    if key not in spec:
        raise SpecError(f"{where}: missing '{key}'")
    value = spec[key]
    if kind and not isinstance(value, kind):
        raise SpecError(f"{where}: '{key}' should be {kind.__name__ if isinstance(kind, type) else kind}")
    return value


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- shared SVG bits

_FONT_CSS = None


def embedded_fonts():
    """@font-face rules with the bundled fonts inlined, so lettering survives inside <img> and in PNGs."""
    global _FONT_CSS
    if _FONT_CSS is None:
        import base64
        fonts = HERE.parent / "templates" / "fonts"
        rules = []
        for fam, fn, weight in (("Alegreya SC", "AlegreyaSC-400.woff2", 400), ("Alegreya SC", "AlegreyaSC-700.woff2", 700),
                                ("Alegreya Sans", "AlegreyaSans-400.woff2", 400), ("Alegreya", "Alegreya-400i.woff2", 400)):
            path = fonts / fn
            if path.exists():
                data = base64.b64encode(path.read_bytes()).decode("ascii")
                style = "italic" if fn.endswith("i.woff2") else "normal"
                rules.append(f"@font-face{{font-family:'{fam}';font-weight:{weight};font-style:{style};"
                             f"src:url(data:font/woff2;base64,{data}) format('woff2');}}")
        _FONT_CSS = "".join(rules)
    return _FONT_CSS


def svg_open(w, h, extra_defs=""):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{num(w)}" height="{num(h)}" '
            f'viewBox="0 0 {num(w)} {num(h)}">', f"<defs><style>{embedded_fonts()}</style>{extra_defs}</defs>"]


def paper_filter(fid="paper", base="#efe4c8", seed=7):
    return (f'<filter id="{fid}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.012 0.018" numOctaves="4" seed="{seed}" result="n"/>'
            '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.45  0 0 0 0 0.30  0 0 0 0.22 0" result="tint"/>'
            f'<feFlood flood-color="{base}" result="base"/>'
            '<feBlend in="tint" in2="base" mode="multiply"/></filter>')


def ground_filter(fid, color, seed=3, strength=0.18):
    return (f'<filter id="{fid}" x="0" y="0" width="100%" height="100%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="{seed}" result="n"/>'
            f'<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 {strength} 0" result="speck"/>'
            f'<feFlood flood-color="{color}" result="base"/>'
            '<feComposite in="speck" in2="base" operator="over"/></filter>')


def cartouche(title, subtitle, x, y, w, scale_text, gm):
    tag = "GM MAP" if gm else "PLAYER MAP"
    return (f'<g font-family="{FONT}">'
            f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="58" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="{num(x+4)}" y="{num(y+4)}" width="{num(w-8)}" height="50" fill="none" stroke="{INK}" stroke-width="0.8"/>'
            f'<text x="{num(x+16)}" y="{num(y+30)}" font-size="22" fill="{INK}">{escape(title)}</text>'
            f'<text x="{num(x+16)}" y="{num(y+47)}" font-size="12" font-family="{SANS}" fill="#5a4f43">{escape(subtitle)}</text>'
            f'<text x="{num(x+w-16)}" y="{num(y+24)}" font-size="11" font-family="{SANS}" letter-spacing="2" '
            f'text-anchor="end" fill="{"#8b2e1f" if gm else "#2f5d3a"}">{tag}</text>'
            f'<text x="{num(x+w-16)}" y="{num(y+44)}" font-size="12" font-family="{SANS}" text-anchor="end" fill="{INK}">{escape(scale_text)}</text>'
            '</g>')


def compass(cx, cy, r=26):
    return (f'<g transform="translate({num(cx)},{num(cy)})" fill="{INK}" font-family="{FONT}">'
            f'<circle r="{num(r*0.62)}" fill="none" stroke="{INK}" stroke-width="1"/>'
            f'<path d="M0,{-r} L{num(r*0.18)},0 L0,{num(r*0.18)} L{num(-r*0.18)},0 Z"/>'
            f'<path d="M0,{r} L{num(r*0.18)},0 L0,{num(-r*0.18)} L{num(-r*0.18)},0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
            f'<text y="{num(-r-5)}" font-size="13" text-anchor="middle">N</text></g>')


def compass_at(spec, x0, y0, w, h, r=26):
    """Compass rose inside the map frame; spec "compass": true/false or a corner "tl", "tr", "bl", "br"."""
    where = spec.get("compass", "tr")
    if where is False:
        return ""
    if where is True:
        where = "tr"
    if where not in ("tl", "tr", "bl", "br"):
        raise SpecError(f"compass must be true, false, tl, tr, bl or br (got {where!r})")
    cx = x0 + (r + 14 if where[1] == "l" else w - r - 14)
    cy = y0 + (r + 18 if where[0] == "t" else h - r - 10)
    return compass(cx, cy, r)


def map_title(spec, gm):
    return spec.get("title", spec.get("id", "Map")) if gm else spec.get("player_title", spec.get("title", spec.get("id", "Map")))


def hatch_pattern(pid, cell):
    """A Dyson-style hatch tile: clusters of short parallel strokes at varied angles."""
    rnd = random.Random(11)
    size = cell * 2
    strokes = []
    for gx in range(3):
        for gy in range(3):
            cx, cy = (gx + 0.5) * size / 3, (gy + 0.5) * size / 3
            ang = rnd.uniform(0, math.pi)
            dx, dy = math.cos(ang), math.sin(ang)
            px, py = -dy, dx
            length = size / 3 * 0.9
            for k in range(-2, 3):
                ox, oy = cx + px * k * size / 22, cy + py * k * size / 22
                strokes.append(f'M{num(ox-dx*length/2)},{num(oy-dy*length/2)} L{num(ox+dx*length/2)},{num(oy+dy*length/2)}')
    return (f'<pattern id="{pid}" width="{num(size)}" height="{num(size)}" patternUnits="userSpaceOnUse">'
            f'<rect width="{num(size)}" height="{num(size)}" fill="#ffffff"/>'
            f'<path d="{" ".join(strokes)}" stroke="#3b3631" stroke-width="{num(max(1, cell/40))}" stroke-linecap="round"/></pattern>')


# ---------------------------------------------------------------- dungeon

SIDES = {"n": (0, -1), "s": (0, 1), "w": (-1, 0), "e": (1, 0)}
DOOR_TYPES = {"door", "locked", "secret", "open", "portcullis", "barred", "window"}
FEATURES = {"desk", "counter", "radio", "boat", "stairs", "water", "pillar", "rubble", "trap", "statue", "table", "chest", "altar",
            "bed", "well", "barrel", "pit", "brazier", "label", "fire", "crate"}


def edge_key(x, y, side):
    if side == "n":
        return ("h", x, y)
    if side == "s":
        return ("h", x, y + 1)
    if side == "w":
        return ("v", x, y)
    if side == "e":
        return ("v", x + 1, y)
    raise SpecError(f"bad side {side!r}")


def merge_edges(edges):
    """Merge unit edges into long straight segments. Returns [(x1,y1,x2,y2)] in cell units."""
    segs = []
    horiz = sorted((y, x) for (o, x, y) in edges if o == "h")
    vert = sorted((x, y) for (o, x, y) in edges if o == "v")
    run = None
    for y, x in horiz:
        if run and run[1] == y and run[2] == x:
            run[2] = x + 1
        else:
            if run:
                segs.append((run[0], run[1], run[2], run[1]))
            run = [x, y, x + 1]
    if run:
        segs.append((run[0], run[1], run[2], run[1]))
    run = None
    for x, y in vert:
        if run and run[0] == x and run[2] == y:
            run[2] = y + 1
        else:
            if run:
                segs.append((run[0], run[1], run[0], run[2]))
            run = [x, y, y + 1]
    if run:
        segs.append((run[0], run[1], run[0], run[2]))
    return segs


def dungeon_model(spec, name):
    cols, rows = need(spec, "cols", int, name), need(spec, "rows", int, name)
    region = {}
    rooms = spec.get("rooms", [])
    keys_seen = set()
    for i, r in enumerate(rooms):
        where = f"{name} rooms[{i}]"
        for k in ("key", "x", "y", "w", "h"):
            need(r, k, None, where)
        if r["key"] in keys_seen:
            raise SpecError(f"{where}: duplicate room key {r['key']!r}")
        keys_seen.add(r["key"])
        for x in range(r["x"], r["x"] + r["w"]):
            for y in range(r["y"], r["y"] + r["h"]):
                if not (0 <= x < cols and 0 <= y < rows):
                    raise SpecError(f"{where}: cell ({x},{y}) is outside the {cols}x{rows} grid")
                if (x, y) in region:
                    raise SpecError(f"{where}: overlaps room {region[(x, y)][1:]} at ({x},{y})")
                region[(x, y)] = "R" + str(r["key"])
        for (cx, cy) in r.get("extra_cells", []):
            region[(cx, cy)] = "R" + str(r["key"])
    for i, c in enumerate(spec.get("corridors", [])):
        where = f"{name} corridors[{i}]"
        for k in ("x", "y", "w", "h"):
            need(c, k, None, where)
        for x in range(c["x"], c["x"] + c["w"]):
            for y in range(c["y"], c["y"] + c["h"]):
                if not (0 <= x < cols and 0 <= y < rows):
                    raise SpecError(f"{where}: cell ({x},{y}) is outside the grid")
                region.setdefault((x, y), f"C{i}")
    if not region:
        raise SpecError(f"{name}: no rooms or corridors")
    doors = {}
    for i, d in enumerate(spec.get("doors", [])):
        where = f"{name} doors[{i}]"
        for k in ("x", "y", "side"):
            need(d, k, None, where)
        dtype = d.get("type", "door")
        if dtype not in DOOR_TYPES:
            raise SpecError(f"{where}: type {dtype!r} not one of {sorted(DOOR_TYPES)}")
        if (d["x"], d["y"]) not in region:
            raise SpecError(f"{where}: cell ({d['x']},{d['y']}) is not floor; put doors on a floor cell's edge")
        dx, dy = SIDES[d["side"]]
        other = (d["x"] + dx, d["y"] + dy)
        if region.get(other) == region[(d["x"], d["y"])]:
            raise SpecError(f"{where}: edge is inside one room/corridor, not on a wall")
        doors[edge_key(d["x"], d["y"], d["side"])] = dtype
    walls = set()
    for (x, y), reg in region.items():
        for side, (dx, dy) in SIDES.items():
            other = region.get((x + dx, y + dy))
            if other != reg:
                walls.add(edge_key(x, y, side))
    # Connectivity: regions joined by any door type (secret included) or open edges.
    adj = {r: set() for r in set(region.values())}
    for (x, y), reg in region.items():
        for side, (dx, dy) in SIDES.items():
            other = region.get((x + dx, y + dy))
            if other and other != reg and edge_key(x, y, side) in doors:
                adj[reg].add(other)
                adj[other].add(reg)
    start = spec.get("start")
    start_reg = region.get((start["x"], start["y"])) if start else ("R" + str(rooms[0]["key"]) if rooms else next(iter(adj)))
    if start and not start_reg:
        raise SpecError(f"{name}: start ({start['x']},{start['y']}) is not a floor cell")
    # Rooms reached some other way (stairs to another floor, a ladder, a teleport circle) count as entry points.
    roots = [start_reg] + ["R" + str(r["key"]) for r in rooms if r.get("reached_by")]
    seen, todo = set(roots), list(roots)
    while todo:
        cur = todo.pop()
        for nxt in adj[cur]:
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    unreachable = sorted(r for r in adj if r not in seen)
    hidden = {"R" + str(r["key"]) for r in rooms if r.get("hidden")}
    hidden |= {f"C{i}" for i, c in enumerate(spec.get("corridors", [])) if c.get("hidden")}
    return {"cols": cols, "rows": rows, "region": region, "walls": walls, "doors": doors,
            "unreachable": unreachable, "rooms": rooms, "hidden": hidden}


def draw_feature(f, c, gm, where):
    t = f.get("type")
    if t not in FEATURES:
        raise SpecError(f"{where}: feature type {t!r} not one of {sorted(FEATURES)}")
    if f.get("gm") and not gm:
        return ""
    if t == "trap" and not gm:
        return ""
    x, y = f.get("x", 0) * c, f.get("y", 0) * c
    w, h = f.get("w", 1) * c, f.get("h", 1) * c
    out = []
    if t == "stairs":
        n = max(3, int((h if f.get("dir", "n") in "ns" else w) / c * 3))
        out.append(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
        for i in range(1, n):
            if f.get("dir", "n") in "ns":
                yy = y + h * i / n
                out.append(f'<line x1="{num(x)}" y1="{num(yy)}" x2="{num(x+w)}" y2="{num(yy)}" stroke="{INK}" stroke-width="1"/>')
            else:
                xx = x + w * i / n
                out.append(f'<line x1="{num(xx)}" y1="{num(y)}" x2="{num(xx)}" y2="{num(y+h)}" stroke="{INK}" stroke-width="1"/>')
    elif t in ("water", "pit"):
        fill = "#bcd6e8" if t == "water" else "#2b2622"
        out.append(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" fill="{fill}" stroke="{INK}" stroke-width="1"/>')
        if t == "water":
            for i in range(int(h / c * 1.5)):
                for j in range(int(w / c / 1.5)):
                    xx = x + c * (0.2 + j * 1.5 + (0.7 if i % 2 else 0))
                    yy = y + c * 0.45 + i * c / 1.5
                    if xx + c * 0.6 < x + w:
                        out.append(f'<path d="M{num(xx)},{num(yy)} q{num(c*0.15)},{num(-c*0.1)} {num(c*0.3)},0 t{num(c*0.3)},0" '
                                   f'fill="none" stroke="#5f8fb0" stroke-width="1"/>')
    elif t in ("pillar", "well", "brazier", "barrel", "statue", "fire"):
        r = c * (0.32 if t == "pillar" else 0.3)
        cx, cy = x + c / 2, y + c / 2
        fill = {"pillar": INK, "well": "#bcd6e8", "brazier": "#e0a040", "barrel": "#b08a5a",
                "statue": "#d9d4c7", "fire": "#e07a30"}[t]
        out.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(r)}" fill="{fill}" stroke="{INK}" stroke-width="1.4"/>')
        if t == "statue":
            out.append(f'<path d="M{num(cx)},{num(cy-r*0.6)} L{num(cx+r*0.18)},{num(cy-r*0.1)} L{num(cx+r*0.6)},{num(cy)} '
                       f'L{num(cx+r*0.18)},{num(cy+r*0.12)} L{num(cx)},{num(cy+r*0.6)} L{num(cx-r*0.18)},{num(cy+r*0.12)} '
                       f'L{num(cx-r*0.6)},{num(cy)} L{num(cx-r*0.18)},{num(cy-r*0.1)} Z" fill="{INK}"/>')
    elif t == "boat":
        out.append(f'<path d="M{num(x)},{num(y+h/2)} Q{num(x+w*0.15)},{num(y)} {num(x+w*0.5)},{num(y+h*0.08)} '
                   f'L{num(x+w*0.85)},{num(y+h*0.08)} Q{num(x+w)},{num(y+h/2)} {num(x+w*0.85)},{num(y+h*0.92)} '
                   f'L{num(x+w*0.5)},{num(y+h*0.92)} Q{num(x+w*0.15)},{num(y+h)} {num(x)},{num(y+h/2)} Z" '
                   f'fill="#b08655" stroke="{INK}" stroke-width="1.4"/>')
        for k in range(1, max(2, int(w / c))):
            xx = x + w * k / max(2, int(w / c))
            out.append(f'<line x1="{num(xx)}" y1="{num(y+h*0.2)}" x2="{num(xx)}" y2="{num(y+h*0.8)}" stroke="#6e4c2c" stroke-width="1"/>')
    elif t == "radio":
        out.append(f'<rect x="{num(x+c*0.15)}" y="{num(y+c*0.25)}" width="{num(c*0.7)}" height="{num(c*0.5)}" fill="#7a5a3a" '
                   f'stroke="{INK}" stroke-width="1.3"/><circle cx="{num(x+c*0.35)}" cy="{num(y+c*0.5)}" r="{num(c*0.1)}" '
                   f'fill="#e8dcc4" stroke="{INK}"/><line x1="{num(x+c*0.7)}" y1="{num(y+c*0.25)}" x2="{num(x+c*0.85)}" '
                   f'y2="{num(y+c*0.05)}" stroke="{INK}" stroke-width="1.2"/>')
    elif t in ("table", "altar", "bed", "chest", "crate", "desk", "counter"):
        fill = {"table": "#e8dcc4", "altar": "#d9d4c7", "bed": "#efe7d6", "chest": "#c89a5a", "crate": "#d8bf8f",
                "desk": "#c9a77a", "counter": "#b9956a"}[t]
        inset = c * (0.12 if t in ("table", "altar", "bed", "desk", "counter") else 0.25)
        out.append(f'<rect x="{num(x+inset)}" y="{num(y+inset)}" width="{num(w-2*inset)}" height="{num(h-2*inset)}" '
                   f'fill="{fill}" stroke="{INK}" stroke-width="1.3"/>')
        if t == "crate":
            out.append(f'<path d="M{num(x+inset)},{num(y+inset)} L{num(x+w-inset)},{num(y+h-inset)} M{num(x+w-inset)},{num(y+inset)} '
                       f'L{num(x+inset)},{num(y+h-inset)}" stroke="{INK}" stroke-width="0.8"/>')
    elif t == "rubble":
        rnd = random.Random(int(x * 7 + y * 13))
        for _ in range(int(w * h / c / c * 7)):
            px, py = x + rnd.random() * w, y + rnd.random() * h
            s = c * rnd.uniform(0.05, 0.12)
            out.append(f'<path d="M{num(px)},{num(py-s)} L{num(px+s)},{num(py)} L{num(px)},{num(py+s*0.8)} L{num(px-s)},{num(py+s*0.2)} Z" '
                       f'fill="#8a837a" stroke="{INK}" stroke-width="0.6"/>')
    elif t == "trap":
        out.append(f'<rect x="{num(x+c*0.18)}" y="{num(y+c*0.18)}" width="{num(c*0.64)}" height="{num(c*0.64)}" fill="none" '
                   f'stroke="#8b2e1f" stroke-width="1.6" stroke-dasharray="3 2"/>'
                   f'<text x="{num(x+c/2)}" y="{num(y+c*0.66)}" font-family="{SANS}" font-weight="700" font-size="{num(c*0.42)}" '
                   f'text-anchor="middle" fill="#8b2e1f">T</text>')
    if t == "label" or f.get("text"):
        size = c * f.get("size", 0.32)
        out.append(f'<text x="{num(x + c/2)}" y="{num(y + c/2 + size/3)}" font-family="{SANS}" font-size="{num(size)}" '
                   f'text-anchor="middle" fill="{INK}" stroke="#ffffff" stroke-width="{num(max(2, c/14))}" paint-order="stroke" '
                   f'font-style="italic">{escape(f.get("text", ""))}</text>')
    return "".join(out)


def render_dungeon(spec, name, gm, vtt=False):
    m = dungeon_model(spec, name)
    c = vtt_px(spec) if vtt else spec.get("print_px", 32)
    style = spec.get("style", "ink")
    if style not in ("ink", "blueprint"):
        raise SpecError(f"{name}: style must be 'ink' or 'blueprint'")
    cols, rows = m["cols"], m["rows"]
    margin = 0 if vtt else c * 1.2
    foot = 0 if vtt else 74
    W, H = cols * c + 2 * margin, rows * c + 2 * margin + foot
    defs = hatch_pattern("hatch", c)
    parts = svg_open(W, H, defs)
    rock = "#4f7fb4" if style == "blueprint" else "#ffffff"
    surround = spec.get("surround", "rock")  # "rock" (hatched), "water" (a ship at sea, a pier) or "none" (a building on open ground)
    if surround not in ("rock", "water", "none"):
        raise SpecError(f"{name}: surround must be rock, water or none")
    parts.append(f'<rect width="{num(W)}" height="{num(H)}" fill="{PAPER if not vtt and style == "ink" else rock}"/>')
    parts.append(f'<g transform="translate({num(margin)},{num(margin)})">')
    if surround == "water":
        parts.append(f'<rect width="{num(cols*c)}" height="{num(rows*c)}" fill="#8fb5d2"/>')
    elif surround == "none" and vtt:
        parts.append(f'<rect width="{num(cols*c)}" height="{num(rows*c)}" fill="#e9e2d0"/>')
    if style == "blueprint":
        parts.append(f'<rect width="{num(cols*c)}" height="{num(rows*c)}" fill="{rock}"/>')
        grid = "".join(f'<line x1="{i*c}" y1="0" x2="{i*c}" y2="{rows*c}"/>' for i in range(cols + 1))
        grid += "".join(f'<line x1="0" y1="{j*c}" x2="{cols*c}" y2="{j*c}"/>' for j in range(rows + 1))
        parts.append(f'<g stroke="#7fa6d0" stroke-width="1">{grid}</g>')
    # Player and VTT versions: hidden rooms vanish into the rock; secret doors and doors into hidden rooms are plain wall.
    hidden = set() if gm else m["hidden"]
    region = {cell: reg for cell, reg in m["region"].items() if reg not in hidden}

    def cells_of(key):
        o, x, y = key
        return [(x, y - 1), (x, y)] if o == "h" else [(x - 1, y), (x, y)]
    all_edges = set()
    for (x, y), reg in region.items():
        for side, (dx, dy) in SIDES.items():
            if region.get((x + dx, y + dy)) != reg:
                all_edges.add(edge_key(x, y, side))
    visible_doors = {k: v for k, v in m["doors"].items()
                     if (gm or v != "secret") and k in all_edges
                     and not any(m["region"].get(cell) in hidden for cell in cells_of(k))}
    open_edges = {k for k, v in visible_doors.items() if v == "open"}
    if style == "ink" and surround == "rock":
        hatch_path = "".join(
            f'M{x1*c},{y1*c} L{x2*c},{y2*c} ' for (x1, y1, x2, y2) in merge_edges(all_edges - open_edges))
        parts.append(f'<path d="{hatch_path}" stroke="url(#hatch)" stroke-width="{num(c*1.15)}" stroke-linecap="square" fill="none"/>')
    floor = "".join(f'<rect x="{x*c}" y="{y*c}" width="{c}" height="{c}"/>' for (x, y) in region)
    parts.append(f'<g fill="#ffffff" stroke="none" shape-rendering="crispEdges">{floor}</g>')
    grid_color = "#9db9d8" if style == "blueprint" else "#cfc8bd"
    gridlines = "".join(f'<rect x="{x*c}" y="{y*c}" width="{c}" height="{c}"/>' for (x, y) in region)
    parts.append(f'<g fill="none" stroke="{grid_color}" stroke-width="{num(max(0.6, c/60))}">{gridlines}</g>')
    for i, f in enumerate(spec.get("features", [])):
        if m["region"].get((int(f.get("x", 0)), int(f.get("y", 0)))) in hidden:
            continue
        parts.append(draw_feature(f, c, gm, f"{name} features[{i}]"))
    wall_color = "#1f3f66" if style == "blueprint" else INK
    # Secret doors stay drawn as wall on every version; the GM map adds the "S".
    solid = all_edges - {k for k, v in visible_doors.items() if v != "secret"}
    wall_path = "".join(f'M{x1*c},{y1*c} L{x2*c},{y2*c} ' for (x1, y1, x2, y2) in merge_edges(solid))
    parts.append(f'<path d="{wall_path}" stroke="{wall_color}" stroke-width="{num(c*0.14)}" stroke-linecap="square" fill="none"/>')
    for (o, ex, ey), dtype in visible_doors.items():
        parts.append(draw_door(o, ex, ey, dtype, c, wall_color))
    if gm and not vtt:
        for r in m["rooms"]:
            lx, ly = r.get("label_at", [r["x"] + r["w"] / 2 - 0.5, r["y"] + r["h"] / 2 - 0.5])
            cx, cy = (lx + 0.5) * c, (ly + 0.5) * c
            parts.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(c*0.36)}" fill="#ffffff" stroke="{INK}" stroke-width="1.2"/>'
                         f'<text x="{num(cx)}" y="{num(cy + c*0.15)}" font-family="{FONT}" font-weight="700" '
                         f'font-size="{num(c*0.44)}" text-anchor="middle" fill="{INK}">{escape(str(r["key"]))}</text>')
    if not vtt:
        parts.append(f'<rect width="{num(cols*c)}" height="{num(rows*c)}" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append("</g>")
    if not vtt:
        ft = spec.get("feet_per_cell", 5)
        parts.append(cartouche(map_title(spec, gm), spec.get("subtitle", ""), margin,
                               margin + rows * c + 14, cols * c, f"1 square = {ft} ft.", gm))
        parts.append(compass_at(spec, margin, margin, cols * c, rows * c))
    parts.append("</svg>")
    return "\n".join(parts), (W, H), m


def draw_door(o, ex, ey, dtype, c, wall_color):
    if dtype == "open":
        return ""
    if o == "v":
        x, y0 = ex * c, ey * c
        cx, cy, horiz = x, y0 + c / 2, False
    else:
        x0, y = ex * c, ey * c
        cx, cy, horiz = x0 + c / 2, y, True
    long_, short = c * 0.62, c * 0.26
    w, h = (long_, short) if horiz else (short, long_)
    if dtype == "secret":
        return (f'<text x="{num(cx)}" y="{num(cy + c*0.16)}" font-family="{FONT}" font-weight="700" font-size="{num(c*0.46)}" '
                f'text-anchor="middle" fill="#8b2e1f" stroke="#ffffff" stroke-width="{num(c*0.08)}" paint-order="stroke">S</text>')
    if dtype == "window":
        x1, y1 = (cx - c / 2, cy) if horiz else (cx, cy - c / 2)
        x2, y2 = (cx + c / 2, cy) if horiz else (cx, cy + c / 2)
        return (f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#ffffff" stroke-width="{num(c*0.16)}"/>'
                f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="#7fa6c9" stroke-width="{num(c*0.06)}"/>')
    if dtype == "portcullis":
        x1, y1 = (cx - c / 2, cy) if horiz else (cx, cy - c / 2)
        x2, y2 = (cx + c / 2, cy) if horiz else (cx, cy + c / 2)
        return (f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="{wall_color}" '
                f'stroke-width="{num(c*0.1)}" stroke-dasharray="{num(c*0.08)} {num(c*0.08)}"/>')
    out = (f'<rect x="{num(cx-w/2)}" y="{num(cy-h/2)}" width="{num(w)}" height="{num(h)}" fill="#ffffff" '
           f'stroke="{wall_color}" stroke-width="{num(max(1.2, c*0.05))}"/>')
    if dtype == "locked":
        out += f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(c*0.07)}" fill="{wall_color}"/>'
    if dtype == "barred":
        out += (f'<line x1="{num(cx-w/2)}" y1="{num(cy-h/2)}" x2="{num(cx+w/2)}" y2="{num(cy+h/2)}" stroke="{wall_color}" '
                f'stroke-width="{num(max(1, c*0.04))}"/>')
    return out


def dungeon_warnings(spec, m):
    out = []
    cols, rows = m["cols"], m["rows"]
    for d in spec.get("doors", []):
        if d.get("type", "door") != "secret":
            continue  # ordinary doors and windows may open onto the street or the outdoors; a secret door into rock is a bug
        dx, dy = SIDES[d["side"]]
        ox, oy = d["x"] + dx, d["y"] + dy
        inside = 0 <= ox < cols and 0 <= oy < rows
        if inside and (ox, oy) not in m["region"] and not d.get("exterior"):
            out.append(f"door at ({d['x']},{d['y']}) {d['side']} is a secret door into solid rock; move it to a wall between two areas")
    feature_cells = set()
    for f in spec.get("features", []):
        for xx in range(int(f.get("x", 0)), int(f.get("x", 0) + f.get("w", 1))):
            for yy in range(int(f.get("y", 0)), int(f.get("y", 0) + f.get("h", 1))):
                feature_cells.add((xx, yy))
    for r in m["rooms"]:
        lx, ly = r.get("label_at", [r["x"] + r["w"] / 2 - 0.5, r["y"] + r["h"] / 2 - 0.5])
        if (math.floor(lx + 0.5), math.floor(ly + 0.5)) in feature_cells:  # the square under the key circle's centre
            out.append(f"room {r['key']}'s key sits on a feature; set label_at to a clear square")
    return out


def compass_clash(spec, squares):
    """True if any (x, y) square, in map squares, sits under the compass corner."""
    where = spec.get("compass", "tr")
    if where is False:
        return False
    where = "tr" if where is True else where
    cols, rows = spec.get("cols", 0), spec.get("rows", 0)
    xs = range(cols - 3, cols) if where[1] == "r" else range(0, 3)
    ys = range(0, 3) if where[0] == "t" else range(rows - 3, rows)
    return any(int(x) in xs and int(y) in ys for x, y in squares)


def dungeon_walls(spec, m):
    px = vtt_px(spec)
    walls = []
    plain = m["walls"] - set(m["doors"])
    for (x1, y1, x2, y2) in merge_edges(plain):
        walls.append({"c": [x1 * px, y1 * px, x2 * px, y2 * px]})
    for (o, ex, ey), dtype in m["doors"].items():
        if dtype == "open":
            continue
        c = [ex * px, ey * px, (ex + 1) * px, ey * px] if o == "h" else [ex * px, ey * px, ex * px, (ey + 1) * px]
        if dtype == "portcullis":
            walls.append({"c": c, "move": 20, "sight": 0, "light": 0, "sound": 0})
        elif dtype == "window":
            walls.append({"c": c, "preset": "window"})
        else:
            walls.append({"c": c, "door": 2 if dtype == "secret" else 1, "ds": 2 if dtype in ("locked", "barred") else 0})
    return walls


# ---------------------------------------------------------------- area (outdoor battle map)

GROUNDS = {"grass": "#c9d9a6", "snow": "#eef2f5", "stone": "#d6d0c2", "sand": "#e6d6ad",
           "swamp": "#aebd8c", "forest-floor": "#b9c68e", "dirt": "#cdb48c", "cave": "#b7aea0", "wood": "#b99368"}


def poly_points(pts, c):
    return " ".join(f"{num(x*c)},{num(y*c)}" for x, y in pts)


def smooth_path(pts, c, closed=False):
    """Catmull-Rom through points, as cubic Beziers (cell units in, pixels out)."""
    p = [(x * c, y * c) for x, y in pts]
    if len(p) < 3:
        return "M" + " L".join(f"{num(x)},{num(y)}" for x, y in p) + (" Z" if closed else "")
    if closed:
        p = p[-1:] + p + p[:2]
    else:
        p = p[:1] + p + p[-1:]
    d = f"M{num(p[1][0])},{num(p[1][1])}"
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{num(c1[0])},{num(c1[1])} {num(c2[0])},{num(c2[1])} {num(p2[0])},{num(p2[1])}"
    return d + (" Z" if closed else "")


def render_area(spec, name, gm, vtt=False):
    cols, rows = need(spec, "cols", int, name), need(spec, "rows", int, name)
    c = vtt_px(spec) if vtt else spec.get("print_px", 32)
    ground = spec.get("ground", "grass")
    if ground not in GROUNDS:
        raise SpecError(f"{name}: ground {ground!r} not one of {sorted(GROUNDS)}")
    snowy = ground == "snow" or spec.get("snowy", False)
    margin = 0 if vtt else c * 1.2
    foot = 0 if vtt else 74
    W, H = cols * c + 2 * margin, rows * c + 2 * margin + foot
    defs = ground_filter("ground", GROUNDS[ground], seed=spec.get("seed", 5))
    defs += ('<radialGradient id="canopy" cx="40%" cy="38%" r="70%"><stop offset="0" stop-color="#6f9a52"/>'
             '<stop offset="1" stop-color="#2f5a2a"/></radialGradient>'
             '<radialGradient id="pine" cx="40%" cy="38%" r="70%"><stop offset="0" stop-color="#4f7a5a"/>'
             '<stop offset="1" stop-color="#1f3d2e"/></radialGradient>'
             '<radialGradient id="rock" cx="38%" cy="35%" r="75%"><stop offset="0" stop-color="#b9b4ab"/>'
             '<stop offset="1" stop-color="#6d675f"/></radialGradient>')
    parts = svg_open(W, H, defs)
    parts.append(f'<rect width="{num(W)}" height="{num(H)}" fill="{PAPER}"/>')
    parts.append(f'<g transform="translate({num(margin)},{num(margin)})">')
    parts.append(f'<clipPath id="frame"><rect width="{cols*c}" height="{rows*c}"/></clipPath><g clip-path="url(#frame)">')
    parts.append(f'<rect width="{cols*c}" height="{rows*c}" filter="url(#ground)"/>')
    if ground == "wood":
        parts.append('<g stroke="#8a6440" stroke-width="1" opacity="0.6">' + "".join(
            f'<line x1="0" y1="{num(j*c/2)}" x2="{cols*c}" y2="{num(j*c/2)}"/>' for j in range(1, rows * 2)) + "</g>")
    for i, r in enumerate(spec.get("rough", [])):
        parts.append(f'<path d="{smooth_path(need(r, "points", list, f"{name} rough[{i}]"), c, True)}" fill="#8a7a55" '
                     f'fill-opacity="0.25" stroke="#6d5f40" stroke-width="1" stroke-dasharray="4 3"/>')
    for i, w_ in enumerate(spec.get("water", [])):
        pts = need(w_, "points", list, f"{name} water[{i}]")
        deep = w_.get("deep", False)
        fill = "#7fa8c9" if deep else "#a9c8de"
        if snowy and w_.get("frozen"):
            fill = "#d5e6f0"
        shape = smooth_path(pts, c, True) if w_.get("smooth", True) else "M" + " L".join(f"{num(px_*c)},{num(py_*c)}" for px_, py_ in pts) + " Z"
        parts.append(f'<path d="{shape}" fill="{fill}" stroke="#4f7896" stroke-width="{num(max(1.5, c/18))}" stroke-linejoin="round"/>')
        if w_.get("frozen"):
            xs = [x for x, _ in pts]
            ys = [y for _, y in pts]
            rnd = random.Random(i + 3)
            for _ in range(int((max(xs) - min(xs)) * (max(ys) - min(ys)) / 3)):
                px, py = rnd.uniform(min(xs), max(xs)) * c, rnd.uniform(min(ys), max(ys)) * c
                if point_in_poly(px / c, py / c, pts):
                    ang = rnd.uniform(0, math.pi)
                    L = c * rnd.uniform(0.3, 0.8)
                    parts.append(f'<line x1="{num(px)}" y1="{num(py)}" x2="{num(px+math.cos(ang)*L)}" y2="{num(py+math.sin(ang)*L)}" '
                                 f'stroke="#ffffff" stroke-width="1.2" opacity="0.8"/>')
    for i, st in enumerate(spec.get("streams", [])):
        pts = need(st, "points", list, f"{name} streams[{i}]")
        sw = st.get("width", 1.0) * c
        parts.append(f'<path d="{smooth_path(pts, c)}" fill="none" stroke="#4f7896" stroke-width="{num(sw + max(2, c/14))}" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="{smooth_path(pts, c)}" fill="none" stroke="{"#d5e6f0" if st.get("frozen") else "#a9c8de"}" '
                     f'stroke-width="{num(sw)}" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, ch in enumerate(spec.get("chasms", [])):
        pts = need(ch, "points", list, f"{name} chasms[{i}]")
        d = smooth_path(pts, c, True)
        parts.append(f'<path d="{d}" fill="#1c1916"/><path d="{d}" fill="none" stroke="#5d5247" stroke-width="{num(c*0.5)}" '
                     f'stroke-opacity="0.55"/><path d="{d}" fill="none" stroke="#2a2420" stroke-width="{num(max(1.5, c/20))}"/>')
    for i, p in enumerate(spec.get("paths", [])):
        pts = need(p, "points", list, f"{name} paths[{i}]")
        width = p.get("width", 1.2) * c
        edge, mid = ("#b9c4cf", "#d9e0e7") if snowy else ("#a88f68", "#c9b28a")
        parts.append(f'<path d="{smooth_path(pts, c)}" fill="none" stroke="{edge}" stroke-width="{num(width)}" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="0.7"/>'
                     f'<path d="{smooth_path(pts, c)}" fill="none" stroke="{mid}" stroke-width="{num(width*0.72)}" '
                     f'stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>'
                     f'<path d="{smooth_path(pts, c)}" fill="none" stroke="{edge}" stroke-width="{num(max(1, c/30))}" '
                     f'stroke-dasharray="{num(c*0.12)} {num(c*0.35)}" stroke-linecap="round" opacity="0.8"/>')
    for i, br in enumerate(spec.get("bridges", [])):
        pts = need(br, "points", list, f"{name} bridges[{i}]")
        bw = br.get("width", 1.0) * c
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        L = math.hypot(x2 - x1, y2 - y1) * c or 1
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        planks = "".join(f'<line x1="{num(k)}" y1="{num(-bw/2)}" x2="{num(k)}" y2="{num(bw/2)}"/>'
                         for k in [j * c * 0.35 for j in range(1, int(L / (c * 0.35)))])
        parts.append(f'<g transform="translate({num(x1*c)},{num(y1*c)}) rotate({num(ang)})">'
                     f'<rect x="0" y="{num(-bw/2 - c*0.06)}" width="{num(L)}" height="{num(bw + c*0.12)}" fill="#000" opacity="0.25" transform="translate({num(c*0.06)},{num(c*0.08)})"/>'
                     f'<rect x="0" y="{num(-bw/2)}" width="{num(L)}" height="{num(bw)}" fill="#b08655" stroke="#5a3d22" stroke-width="{num(max(1.2, c/30))}"/>'
                     f'<g stroke="#6e4c2c" stroke-width="{num(max(0.8, c/60))}">{planks}</g></g>')
    for i, cl in enumerate(spec.get("cliffs", [])):
        pts = need(cl, "points", list, f"{name} cliffs[{i}]")
        parts.append(cliff_svg(pts, c, cl.get("side", "left")))
    for i, wl in enumerate(spec.get("walls", [])):
        pts = need(wl, "points", list, f"{name} walls[{i}]")
        parts.append(f'<polyline points="{poly_points(pts, c)}" fill="none" stroke="#5b544b" stroke-width="{num(c*0.32)}" '
                     f'stroke-linecap="square" stroke-linejoin="miter"/>'
                     f'<polyline points="{poly_points(pts, c)}" fill="none" stroke="#9a9389" stroke-width="{num(c*0.18)}" '
                     f'stroke-linecap="square" stroke-dasharray="{num(c*0.3)} {num(c*0.06)}"/>')
    for i, rk in enumerate(spec.get("rocks", [])):
        where = f"{name} rocks[{i}]"
        rx, ry, rr = need(rk, "x", None, where), need(rk, "y", None, where), rk.get("r", 0.6)
        parts.append(rock_svg(rx, ry, rr, c, seed=i, snowy=snowy))
    grid = ""
    if not vtt or spec.get("vtt_grid", False):
        grid = "".join(f'<line x1="{i*c}" y1="0" x2="{i*c}" y2="{rows*c}"/>' for i in range(cols + 1))
        grid += "".join(f'<line x1="0" y1="{j*c}" x2="{cols*c}" y2="{j*c}"/>' for j in range(rows + 1))
        parts.append(f'<g stroke="#2a2620" stroke-opacity="0.22" stroke-width="1">{grid}</g>')
    for i, f in enumerate(spec.get("features", [])):
        parts.append(draw_feature(f, c, gm, f"{name} features[{i}]"))
    for i, t in enumerate(spec.get("trees", [])):
        where = f"{name} trees[{i}]"
        tx, ty, tr = need(t, "x", None, where), need(t, "y", None, where), t.get("r", 1.0)
        parts.append(tree_svg(tx, ty, tr, c, t.get("kind", "pine" if snowy else "broadleaf"), snowy, seed=i))
    if gm and not vtt:
        for k in spec.get("keys", []):
            cx, cy = (k["x"] + 0.5) * c, (k["y"] + 0.5) * c
            parts.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(c*0.38)}" fill="#ffffff" stroke="{INK}" stroke-width="1.4"/>'
                         f'<text x="{num(cx)}" y="{num(cy + c*0.15)}" font-family="{FONT}" font-weight="700" '
                         f'font-size="{num(c*0.44)}" text-anchor="middle" fill="{INK}">{escape(str(k["key"]))}</text>')
    parts.append("</g>")  # end of the frame clip
    if not vtt:
        for lab in spec.get("labels", []):
            if lab.get("gm") and not gm:
                continue
            parts.append(f'<text x="{num(lab["x"]*c)}" y="{num(lab["y"]*c)}" font-family="{FONT}" font-size="{num(c*0.5)}" '
                         f'fill="{INK}" stroke="#ffffff" stroke-width="3" paint-order="stroke" font-style="italic">{escape(lab["text"])}</text>')
        parts.append(f'<rect width="{cols*c}" height="{rows*c}" fill="none" stroke="{INK}" stroke-width="2"/>')
    parts.append("</g>")
    if not vtt:
        ft = spec.get("feet_per_cell", 5)
        parts.append(cartouche(map_title(spec, gm), spec.get("subtitle", ""), margin,
                               margin + rows * c + 14, cols * c, f"1 square = {ft} ft.", gm))
        parts.append(compass_at(spec, margin, margin, cols * c, rows * c))
    parts.append("</svg>")
    return "\n".join(parts), (W, H), None


def point_in_poly(x, y, pts):
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-9) + xi:
            inside = not inside
        j = i
    return inside


def cliff_svg(pts, c, side):
    out = [f'<polyline points="{poly_points(pts, c)}" fill="none" stroke="#3d342a" stroke-width="{num(c*0.16)}" '
           f'stroke-linecap="round" stroke-linejoin="round"/>']
    sign = 1 if side == "left" else -1
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        if L == 0:
            continue
        nx, ny = -(y2 - y1) / L * sign, (x2 - x1) / L * sign
        steps = max(1, int(L * 3))
        for k in range(steps):
            t = (k + 0.5) / steps
            px, py = (x1 + (x2 - x1) * t) * c, (y1 + (y2 - y1) * t) * c
            out.append(f'<line x1="{num(px)}" y1="{num(py)}" x2="{num(px + nx*c*0.35)}" y2="{num(py + ny*c*0.35)}" '
                       f'stroke="#3d342a" stroke-width="{num(c*0.06)}" stroke-linecap="round"/>')
    return "".join(out)


def rock_svg(x, y, r, c, seed=0, snowy=False):
    rnd = random.Random(seed * 31 + 7)
    n = 9
    pts = []
    for k in range(n):
        a = 2 * math.pi * k / n
        rr = r * rnd.uniform(0.75, 1.05)
        pts.append(((x + 0.5 + math.cos(a) * rr) * c, (y + 0.5 + math.sin(a) * rr) * c))
    d = "M" + " L".join(f"{num(a)},{num(b)}" for a, b in pts) + " Z"
    out = (f'<path d="{d}" fill="#000" opacity="0.22" transform="translate({num(c*0.08)},{num(c*0.1)})"/>'
           f'<path d="{d}" fill="url(#rock)" stroke="#3f3a34" stroke-width="{num(max(1, c/40))}"/>')
    if snowy:
        top = sorted(pts, key=lambda p: p[1])[:4]
        top = sorted(top, key=lambda p: p[0])
        cap = "M" + " L".join(f"{num(a)},{num(b + c*0.04)}" for a, b in top)
        cap += f" Q{num((x+0.5)*c)},{num((y+0.5-r*0.35)*c)} {num(top[0][0])},{num(top[0][1] + c*0.04)} Z"
        out += f'<path d="{cap}" fill="#ffffff" opacity="0.9"/>'

    return out


def tree_svg(x, y, r, c, kind, snowy, seed=0):
    rnd = random.Random(seed * 17 + 3)
    cx, cy, R = (x + 0.5) * c, (y + 0.5) * c, r * c
    out = [f'<circle cx="{num(cx + R*0.12)}" cy="{num(cy + R*0.15)}" r="{num(R)}" fill="#000" opacity="0.2"/>']
    if kind == "pine":
        for layer, (scale, fill) in enumerate(((1.0, "#1f3d2e"), (0.74, "#2f5640"), (0.46, "#46705a"))):
            spikes = 11 - layer * 2
            pts = []
            rot = rnd.uniform(0, math.pi)
            for k in range(spikes * 2):
                a = rot + math.pi * k / spikes
                rr = R * scale * (1 if k % 2 == 0 else 0.68) * rnd.uniform(0.92, 1.05)
                pts.append(f"{num(cx + math.cos(a)*rr)},{num(cy + math.sin(a)*rr)}")
            out.append(f'<polygon points="{" ".join(pts)}" fill="{fill}" stroke="#13251b" '
                       f'stroke-width="{num(max(0.8, c/60))}" stroke-linejoin="round"/>')
        if snowy:
            for _ in range(5):
                a, d = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.2, 0.75) * R
                out.append(f'<ellipse cx="{num(cx + math.cos(a)*d)}" cy="{num(cy + math.sin(a)*d)}" '
                           f'rx="{num(R*0.16)}" ry="{num(R*0.09)}" fill="#ffffff" opacity="0.85" '
                           f'transform="rotate({num(math.degrees(a))} {num(cx + math.cos(a)*d)} {num(cy + math.sin(a)*d)})"/>')
    else:
        lobes = 7
        d = ""
        for k in range(lobes):
            a = 2 * math.pi * k / lobes + rnd.uniform(-0.1, 0.1)
            d += (f'<circle cx="{num(cx + math.cos(a)*R*0.45)}" cy="{num(cy + math.sin(a)*R*0.45)}" '
                  f'r="{num(R*rnd.uniform(0.5, 0.62))}"/>')
        out.append(f'<g fill="url(#canopy)" stroke="#24461f" stroke-width="{num(max(1, c/45))}">{d}</g>')
        out.append(f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{num(R*0.5)}" fill="url(#canopy)"/>')
        if snowy:
            for _ in range(4):
                a, d = rnd.uniform(0, 2 * math.pi), rnd.uniform(0.1, 0.6) * R
                out.append(f'<circle cx="{num(cx + math.cos(a)*d)}" cy="{num(cy + math.sin(a)*d)}" r="{num(R*0.13)}" '
                           f'fill="#ffffff" opacity="0.8"/>')
    return "".join(out)


def area_walls(spec):
    px = vtt_px(spec)
    walls = []
    for group, note in (("cliffs", "cliff"), ("walls", "wall")):
        for item in spec.get(group, []):
            pts = item["points"]
            for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
                walls.append({"c": [round(x1 * px), round(y1 * px), round(x2 * px), round(y2 * px)]})
    for rk in spec.get("rocks", []):
        if not rk.get("blocks"):
            continue
        r, cx, cy = rk.get("r", 0.6), rk["x"] + 0.5, rk["y"] + 0.5
        ring = [(cx + math.cos(2 * math.pi * k / 8) * r * 0.85, cy + math.sin(2 * math.pi * k / 8) * r * 0.85) for k in range(9)]
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            walls.append({"c": [round(x1 * px), round(y1 * px), round(x2 * px), round(y2 * px)]})
    return walls


# ---------------------------------------------------------------- pointcrawl (travel map)

ICONS = {"village", "town", "camp", "cave", "tower", "ruin", "shrine", "lair", "bridge", "mine",
         "farm", "fort", "grove", "peak", "lake", "ship", "standing-stones", "spot"}
AREA_TYPES = {"forest", "pines", "mountains", "hills", "marsh", "lake", "snowfield", "sea", "town", "land", "fields"}


def icon_svg(icon, x, y, s):
    k = INK
    paper = PAPER
    if icon in ("village", "town", "farm"):
        houses = {"village": [(-0.5, 0.1), (0.15, -0.15), (0.55, 0.25)], "town": [(-0.6, 0.15), (-0.1, -0.2), (0.35, 0.05), (0.7, 0.3)],
                  "farm": [(0, 0)]}[icon]
        out = ""
        for hx, hy in houses:
            bx, by = x + hx * s, y + hy * s
            out += (f'<path d="M{num(bx-s*0.28)},{num(by)} L{num(bx)},{num(by-s*0.3)} L{num(bx+s*0.28)},{num(by)} '
                    f'L{num(bx+s*0.28)},{num(by+s*0.3)} L{num(bx-s*0.28)},{num(by+s*0.3)} Z" fill="{paper}" stroke="{k}" stroke-width="1.6"/>')
        return out
    if icon in ("tower", "fort"):
        w = s * (0.35 if icon == "tower" else 0.8)
        return (f'<path d="M{num(x-w/2)},{num(y+s*0.5)} L{num(x-w/2)},{num(y-s*0.45)} L{num(x-w/2+w*0.25)},{num(y-s*0.45)} '
                f'L{num(x-w/2+w*0.25)},{num(y-s*0.6)} L{num(x+w/2-w*0.25)},{num(y-s*0.6)} L{num(x+w/2-w*0.25)},{num(y-s*0.45)} '
                f'L{num(x+w/2)},{num(y-s*0.45)} L{num(x+w/2)},{num(y+s*0.5)} Z" fill="{paper}" stroke="{k}" stroke-width="1.6"/>')
    if icon in ("cave", "mine", "lair"):
        out = (f'<path d="M{num(x-s*0.7)},{num(y+s*0.4)} Q{num(x-s*0.5)},{num(y-s*0.6)} {num(x)},{num(y-s*0.55)} '
               f'Q{num(x+s*0.5)},{num(y-s*0.6)} {num(x+s*0.7)},{num(y+s*0.4)} Z" fill="#b9ac92" stroke="{k}" stroke-width="1.6"/>'
               f'<path d="M{num(x-s*0.25)},{num(y+s*0.4)} Q{num(x)},{num(y-s*0.2)} {num(x+s*0.25)},{num(y+s*0.4)} Z" fill="{k}"/>')
        if icon == "lair":
            out += (f'<circle cx="{num(x)}" cy="{num(y-s*0.95)}" r="{num(s*0.2)}" fill="#8b2e1f" stroke="{k}" stroke-width="1"/>')
        return out
    if icon in ("ruin", "standing-stones"):
        out = ""
        for i, dx in enumerate((-0.45, -0.1, 0.3)):
            hgt = (0.7, 0.45, 0.6)[i]
            out += (f'<rect x="{num(x+dx*s)}" y="{num(y+s*0.4-hgt*s)}" width="{num(s*0.2)}" height="{num(hgt*s)}" '
                    f'fill="{paper}" stroke="{k}" stroke-width="1.4"/>')
        return out
    if icon == "shrine":
        return (f'<path d="M{num(x-s*0.45)},{num(y+s*0.4)} L{num(x+s*0.45)},{num(y+s*0.4)} M{num(x-s*0.35)},{num(y+s*0.4)} '
                f'L{num(x-s*0.35)},{num(y-s*0.2)} M{num(x+s*0.35)},{num(y+s*0.4)} L{num(x+s*0.35)},{num(y-s*0.2)} '
                f'M{num(x-s*0.55)},{num(y-s*0.2)} L{num(x+s*0.55)},{num(y-s*0.2)} L{num(x)},{num(y-s*0.6)} Z" fill="{paper}" stroke="{k}" stroke-width="1.6"/>')
    if icon == "camp":
        return (f'<path d="M{num(x-s*0.5)},{num(y+s*0.4)} L{num(x)},{num(y-s*0.5)} L{num(x+s*0.5)},{num(y+s*0.4)} Z" fill="{paper}" '
                f'stroke="{k}" stroke-width="1.6"/><path d="M{num(x)},{num(y-s*0.5)} L{num(x)},{num(y+s*0.4)}" stroke="{k}" stroke-width="1.2"/>')
    if icon == "bridge":
        return (f'<path d="M{num(x-s*0.6)},{num(y+s*0.2)} Q{num(x)},{num(y-s*0.4)} {num(x+s*0.6)},{num(y+s*0.2)}" fill="none" '
                f'stroke="{k}" stroke-width="2.4"/><path d="M{num(x-s*0.6)},{num(y+s*0.35)} Q{num(x)},{num(y-s*0.25)} {num(x+s*0.6)},{num(y+s*0.35)}" '
                f'fill="none" stroke="{k}" stroke-width="1.2"/>')
    if icon in ("grove", "peak"):
        if icon == "peak":
            return (f'<path d="M{num(x-s*0.7)},{num(y+s*0.4)} L{num(x)},{num(y-s*0.6)} L{num(x+s*0.7)},{num(y+s*0.4)} Z" fill="{paper}" '
                    f'stroke="{k}" stroke-width="1.6"/><path d="M{num(x-s*0.2)},{num(y-s*0.3)} L{num(x)},{num(y-s*0.6)} L{num(x+s*0.2)},{num(y-s*0.3)} '
                    f'L{num(x+s*0.05)},{num(y-s*0.2)} Z" fill="#ffffff" stroke="{k}" stroke-width="1"/>')
        return "".join(pine_glyph(x + dx * s, y + dy * s, s * 0.55) for dx, dy in ((-0.35, 0.1), (0.3, 0.05), (0, -0.25)))
    if icon == "lake":
        return f'<ellipse cx="{num(x)}" cy="{num(y)}" rx="{num(s*0.7)}" ry="{num(s*0.4)}" fill="#a9c8de" stroke="{k}" stroke-width="1.4"/>'
    if icon == "ship":
        return (f'<path d="M{num(x-s*0.6)},{num(y+s*0.1)} L{num(x+s*0.6)},{num(y+s*0.1)} L{num(x+s*0.4)},{num(y+s*0.4)} '
                f'L{num(x-s*0.4)},{num(y+s*0.4)} Z" fill="{paper}" stroke="{k}" stroke-width="1.5"/>'
                f'<path d="M{num(x)},{num(y+s*0.1)} L{num(x)},{num(y-s*0.6)} L{num(x+s*0.4)},{num(y)} Z" fill="{paper}" stroke="{k}" stroke-width="1.3"/>')
    return f'<circle cx="{num(x)}" cy="{num(y)}" r="{num(s*0.22)}" fill="{k}"/>'


def pine_glyph(x, y, s):
    return (f'<path d="M{num(x)},{num(y-s*0.6)} L{num(x+s*0.32)},{num(y+s*0.25)} L{num(x-s*0.32)},{num(y+s*0.25)} Z" '
            f'fill="#5f7d55" stroke="{INK}" stroke-width="1"/><line x1="{num(x)}" y1="{num(y+s*0.25)}" x2="{num(x)}" '
            f'y2="{num(y+s*0.42)}" stroke="{INK}" stroke-width="1.2"/>')


def area_fill(atype, pts, u, seed, keepout=()):
    path = smooth_path(pts, u, True)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    rnd = random.Random(seed)
    out = []
    if atype in ("town", "land", "fields"):
        fill = {"town": "#d9cdb4", "land": "#e6d9b8", "fields": "#cfd6a3"}[atype]
        out.append(f'<path d="{path}" fill="{fill}" fill-opacity="0.8" stroke="#6b5d45" stroke-width="1" stroke-opacity="0.6"/>')
        if atype in ("town", "fields"):
            rnd2 = random.Random(seed + 101)
            step = 2.2 if atype == "town" else 3.2
            yy = min(ys) + step / 2
            while yy < max(ys):
                xx = min(xs) + step / 2
                while xx < max(xs):
                    if point_in_poly(xx, yy, pts) and all((xx - kx) ** 2 + (yy - ky) ** 2 > kr * kr for kx, ky, kr in keepout):
                        if atype == "town":
                            bw, bh = rnd2.uniform(0.9, 1.6), rnd2.uniform(0.7, 1.3)
                            out.append(f'<rect x="{num((xx-bw/2)*u)}" y="{num((yy-bh/2)*u)}" width="{num(bw*u)}" height="{num(bh*u)}" '
                                       f'fill="#b9a988" stroke="#6b5d45" stroke-width="0.7"/>')
                        else:
                            out.append(f'<path d="M{num((xx-1.2)*u)},{num(yy*u)} L{num((xx+1.2)*u)},{num(yy*u)}" stroke="#8a9a5a" stroke-width="1"/>')
                    xx += step
                yy += step
        return "".join(out)
    base = {"forest": "#9fb487", "pines": "#93ab8c", "mountains": "#cbbfa3", "hills": "#d8cba5", "marsh": "#b5c09a",
            "lake": "#a9c8de", "snowfield": "#f3f5f6", "sea": "#9dbfd8"}[atype]
    out.append(f'<path d="{path}" fill="{base}" fill-opacity="0.55" stroke="#6b5d45" stroke-width="1" stroke-opacity="0.5"/>')
    if atype in ("lake", "sea"):
        out[-1] = f'<path d="{path}" fill="{base}" stroke="#4f7896" stroke-width="1.6"/>'
        return "".join(out)
    spacing = {"forest": 2.4, "pines": 2.4, "mountains": 4.2, "hills": 3.6, "marsh": 3.0, "snowfield": 3.4}[atype]
    y = min(ys) + spacing / 2
    row = 0
    while y < max(ys):
        x = min(xs) + (spacing / 2 if row % 2 else 0) + spacing / 4
        while x < max(xs):
            jx, jy = x + rnd.uniform(-0.6, 0.6), y + rnd.uniform(-0.5, 0.5)
            clear = all((jx - kx) ** 2 + (jy - ky) ** 2 > kr * kr for kx, ky, kr in keepout)
            if clear and point_in_poly(jx, jy, pts):
                X, Y = jx * u, jy * u
                if atype in ("forest", "pines"):
                    out.append(pine_glyph(X, Y, u * 1.5) if atype == "pines" or rnd.random() < 0.3 else
                               f'<circle cx="{num(X)}" cy="{num(Y)}" r="{num(u*0.55)}" fill="#7f9f63" stroke="{INK}" stroke-width="0.9"/>'
                               f'<line x1="{num(X)}" y1="{num(Y+u*0.55)}" x2="{num(X)}" y2="{num(Y+u*0.9)}" stroke="{INK}" stroke-width="1"/>')
                elif atype == "mountains":
                    s = u * rnd.uniform(1.6, 2.3)
                    out.append(f'<path d="M{num(X-s*0.6)},{num(Y+s*0.3)} L{num(X)},{num(Y-s*0.5)} L{num(X+s*0.6)},{num(Y+s*0.3)} Z" '
                               f'fill="{PAPER}" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>'
                               f'<path d="M{num(X)},{num(Y-s*0.5)} L{num(X+s*0.6)},{num(Y+s*0.3)} L{num(X+s*0.12)},{num(Y+s*0.3)} Z" '
                               f'fill="#a8967a" opacity="0.75"/>'
                               f'<path d="M{num(X-s*0.6)},{num(Y+s*0.3)} L{num(X)},{num(Y-s*0.5)} L{num(X+s*0.6)},{num(Y+s*0.3)}" '
                               f'fill="none" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>')
                elif atype == "hills":
                    s = u * rnd.uniform(1.2, 1.7)
                    out.append(f'<path d="M{num(X-s*0.6)},{num(Y+s*0.2)} Q{num(X)},{num(Y-s*0.5)} {num(X+s*0.6)},{num(Y+s*0.2)}" '
                               f'fill="none" stroke="{INK}" stroke-width="1.2"/>')
                elif atype == "marsh":
                    out.append(f'<path d="M{num(X-u*0.6)},{num(Y)} L{num(X+u*0.6)},{num(Y)} M{num(X)},{num(Y)} L{num(X)},{num(Y-u*0.6)} '
                               f'M{num(X-u*0.3)},{num(Y)} L{num(X-u*0.45)},{num(Y-u*0.45)} M{num(X+u*0.3)},{num(Y)} '
                               f'L{num(X+u*0.45)},{num(Y-u*0.45)}" stroke="#4f5f3a" stroke-width="1"/>')
                elif atype == "snowfield":
                    out.append(f'<path d="M{num(X-u*0.5)},{num(Y)} q{num(u*0.25)},{num(-u*0.25)} {num(u*0.5)},0 '
                               f't{num(u*0.5)},0" fill="none" stroke="#9fb3c4" stroke-width="1"/>')
            x += spacing
        y += spacing * 0.8
        row += 1
    return "".join(out)


def area_label_pos(a, shown):
    lx, ly = a.get("label_at", [sum(p[0] for p in a["points"]) / len(a["points"]),
                                sum(p[1] for p in a["points"]) / len(a["points"])])
    if "label_at" not in a:
        for _ in range(6):
            if all(abs(lx - n["x"]) > len(a["label"]) * 0.6 or abs(ly - n["y"]) > 4 for n in shown.values()):
                break
            ly -= 3
    return lx, ly


def render_pointcrawl(spec, name, gm):
    w_units, h_units = spec.get("w", 100), spec.get("h", 70)
    u = spec.get("print_px", 14)
    margin = 34
    foot = 74
    W, H = w_units * u + 2 * margin, h_units * u + 2 * margin + foot
    defs = paper_filter("paper", "#efe4c8", seed=spec.get("seed", 9))
    defs += ('<radialGradient id="vignette" cx="50%" cy="50%" r="75%"><stop offset="0.6" stop-color="#000" stop-opacity="0"/>'
             '<stop offset="1" stop-color="#5a3d1e" stop-opacity="0.35"/></radialGradient>')
    parts = svg_open(W, H, defs)
    parts.append(f'<rect width="{num(W)}" height="{num(H)}" fill="{PAPER}"/>')
    parts.append(f'<g transform="translate({margin},{margin})">')
    parts.append(f'<rect width="{num(w_units*u)}" height="{num(h_units*u)}" filter="url(#paper)"/>')
    parts.append(f'<clipPath id="frame"><rect width="{num(w_units*u)}" height="{num(h_units*u)}"/></clipPath><g clip-path="url(#frame)">')
    # Text scales with the whole map, so labels stay readable when the map is printed at page width.
    WW = w_units * u
    fs_node, fs_edge, fs_area = WW / 58, WW / 82, WW / 48
    nodes = {}
    for i, n in enumerate(need(spec, "nodes", list, name)):
        where = f"{name} nodes[{i}]"
        for k in ("id", "name", "x", "y"):
            need(n, k, None, where)
        if n["id"] in nodes:
            raise SpecError(f"{where}: duplicate id {n['id']!r}")
        if n.get("icon", "spot") not in ICONS:
            raise SpecError(f"{where}: icon {n.get('icon')!r} not one of {sorted(ICONS)}")
        nodes[n["id"]] = n
    keepout = []
    # Only places this version shows may clear terrain; a gap around a hidden place would give it away.
    shown = {k: n for k, n in nodes.items() if gm or not n.get("hidden")}
    for n in shown.values():
        size = max(u * n.get("size", 1.6), WW / 60 * n.get("size", 1.6) / 1.6) / u
        keepout.append((n["x"], n["y"], size * 1.1))
        # the label under the icon: clear its whole width
        label_y = n["y"] + size * 0.55 + fs_node / u * 0.65
        half = len(n["name"]) * fs_node * 0.33 / u + 1
        for k in range(int(-half), int(half) + 1):
            keepout.append((n["x"] + k, label_y, fs_node / u * 0.9))
    for e in spec.get("edges", []):
        if e.get("hidden") and not gm:
            continue
        if e.get("from") in shown and e.get("to") in shown:
            a, b = nodes[e["from"]], nodes[e["to"]]
            L = math.hypot(b["x"] - a["x"], b["y"] - a["y"]) or 1
            bend = e.get("bend", 0.12) * L
            cx = (a["x"] + b["x"]) / 2 - (b["y"] - a["y"]) / L * bend
            cy = (a["y"] + b["y"]) / 2 + (b["x"] - a["x"]) / L * bend
            for k in range(int(L) + 1):
                t = k / max(1, int(L))
                px = (1 - t) ** 2 * a["x"] + 2 * (1 - t) * t * cx + t * t * b["x"]
                py = (1 - t) ** 2 * a["y"] + 2 * (1 - t) * t * cy + t * t * b["y"]
                keepout.append((px, py, 1.4))
    for a in spec.get("areas", []):
        if a.get("label") and a.get("points"):
            lx, ly = area_label_pos(a, shown)
            half = len(a["label"]) * fs_area * 0.36 / u + 1
            for k in range(-int(half), int(half) + 1):
                keepout.append((lx + k, ly - fs_area / u * 0.35, fs_area / u * 0.85))
    for i, a in enumerate(spec.get("areas", [])):
        where = f"{name} areas[{i}]"
        if a.get("type") not in AREA_TYPES:
            raise SpecError(f"{where}: type {a.get('type')!r} not one of {sorted(AREA_TYPES)}")
        parts.append(area_fill(a["type"], need(a, "points", list, where), u, seed=i + 1, keepout=keepout))
        if a.get("label"):
            lx, ly = area_label_pos(a, shown)
            parts.append(f'<text x="{num(lx*u)}" y="{num(ly*u)}" font-family="{FONT}" font-size="{num(fs_area)}" '
                         f'letter-spacing="3" text-anchor="middle" fill="#4a3f30" fill-opacity="0.85" font-style="italic" '
                         f'stroke="#efe4c8" stroke-width="3" paint-order="stroke">{escape(a["label"])}</text>')
    for i, r in enumerate(spec.get("rivers", [])):
        pts = need(r, "points", list, f"{name} rivers[{i}]")
        parts.append(f'<path d="{smooth_path(pts, u)}" fill="none" stroke="#4f7896" stroke-width="{num(r.get("width", 0.5)*u)}" '
                     f'stroke-linecap="round"/>')
    for i, e in enumerate(spec.get("edges", [])):
        where = f"{name} edges[{i}]"
        a, b = need(e, "from", None, where), need(e, "to", None, where)
        if a not in nodes or b not in nodes:
            raise SpecError(f"{where}: unknown node {a if a not in nodes else b!r}")
        hidden_end = nodes[a].get("hidden") or nodes[b].get("hidden")
        hidden = e.get("hidden") or hidden_end
        if not gm and (e.get("hidden") or (nodes[a].get("hidden") and nodes[b].get("hidden"))):
            continue
        if not gm and hidden_end and nodes[a].get("hidden"):
            a, b = b, a  # draw from the visible end
        style = e.get("style", "trail")
        x1, y1, x2, y2 = nodes[a]["x"] * u, nodes[a]["y"] * u, nodes[b]["x"] * u, nodes[b]["y"] * u
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        L = math.hypot(x2 - x1, y2 - y1) or 1
        bend = e.get("bend", 0.12) * L * (-1 if (a, b) != (e["from"], e["to"]) else 1)
        cx, cy = mx - (y2 - y1) / L * bend, my + (x2 - x1) / L * bend
        dash = {"road": "", "trail": f'stroke-dasharray="{num(u*0.7)} {num(u*0.45)}"', "river": "",
                "secret": f'stroke-dasharray="{num(u*0.2)} {num(u*0.4)}"'}.get(style, "")
        color = "#4f7896" if style == "river" else ("#8b2e1f" if hidden and gm else "#5a4630")
        width = u * (0.32 if style == "road" else 0.22)
        if not gm and hidden_end:
            # A public road toward a secret place: show it leaving, then fading out; no label, no destination.
            t = 0.5
            qx1, qy1 = x1 + (cx - x1) * t, y1 + (cy - y1) * t
            qx2, qy2 = cx + (x2 - cx) * t, cy + (y2 - cy) * t
            ex, ey = qx1 + (qx2 - qx1) * t, qy1 + (qy2 - qy1) * t
            gid = f"fade{i}"
            parts.append(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{num(x1)}" y1="{num(y1)}" x2="{num(ex)}" '
                         f'y2="{num(ey)}"><stop offset="0.55" stop-color="{color}"/><stop offset="1" stop-color="{color}" '
                         f'stop-opacity="0"/></linearGradient>')
            parts.append(f'<path d="M{num(x1)},{num(y1)} Q{num(qx1)},{num(qy1)} {num(ex)},{num(ey)}" fill="none" '
                         f'stroke="url(#{gid})" stroke-width="{num(width)}" stroke-linecap="round" {dash}/>')
            continue
        parts.append(f'<path d="M{num(x1)},{num(y1)} Q{num(cx)},{num(cy)} {num(x2)},{num(y2)}" fill="none" stroke="{color}" '
                     f'stroke-width="{num(width)}" stroke-linecap="round" {dash}/>')
        if e.get("label"):
            t_ = float(e.get("label_t", 0.5))  # where along the path the label sits, 0 = start, 1 = end
            lx = (1 - t_) ** 2 * x1 + 2 * (1 - t_) * t_ * cx + t_ * t_ * x2
            ly = (1 - t_) ** 2 * y1 + 2 * (1 - t_) * t_ * cy + t_ * t_ * y2
            off = e.get("label_offset", [0, 0])
            lx, ly = lx + off[0] * u, ly + off[1] * u
            parts.append(f'<text x="{num(lx)}" y="{num(ly - fs_edge*0.45)}" font-family="{SANS}" font-size="{num(fs_edge)}" '
                         f'text-anchor="middle" fill="{color}" stroke="#efe4c8" stroke-width="3" paint-order="stroke">{escape(e["label"])}</text>')
    for n in nodes.values():
        if n.get("hidden") and not gm:
            continue
        X, Y = n["x"] * u, n["y"] * u
        s = max(u * n.get("size", 1.6), WW / 60 * n.get("size", 1.6) / 1.6)
        parts.append(f'<ellipse cx="{num(X)}" cy="{num(Y + s*0.42)}" rx="{num(s*0.75)}" ry="{num(s*0.18)}" fill="#000" opacity="0.12"/>')
        parts.append(icon_svg(n.get("icon", "spot"), X, Y, s))
        label = (f'{n["key"]}. ' if gm and n.get("key") else "") + n["name"]
        anchor = n.get("label_side", "below")
        fsn = fs_node * float(n.get("label_size", 1))
        lx_, ly, ta = X, Y + s * 0.55 + fsn, "middle"
        if anchor == "above":
            ly = Y - s * 0.75
        elif anchor in ("left", "right"):
            lx_, ly, ta = (X - s * 0.9, Y + fsn * 0.35, "end") if anchor == "left" else (X + s * 0.9, Y + fsn * 0.35, "start")
        color = "#8b2e1f" if n.get("hidden") else INK
        parts.append(f'<text x="{num(lx_)}" y="{num(ly)}" font-family="{FONT}" font-size="{num(fsn)}" text-anchor="{ta}" '
                     f'fill="{color}" stroke="#efe4c8" stroke-width="3.5" paint-order="stroke">{escape(label)}</text>')
    for lab in spec.get("labels", []):  # free text: districts, streets, "to Salem"
        if lab.get("gm") and not gm:
            continue
        parts.append(f'<text x="{num(lab["x"]*u)}" y="{num(lab["y"]*u)}" font-family="{FONT}" font-size="{num(fs_node*float(lab.get("size", 0.9)))}" '
                     f'text-anchor="middle" fill="#4a3f30" font-style="italic" stroke="#efe4c8" stroke-width="3" '
                     f'paint-order="stroke">{escape(lab["text"])}</text>')
    parts.append(f'<rect width="{num(w_units*u)}" height="{num(h_units*u)}" fill="url(#vignette)"/>')
    parts.append("</g>")  # end of the frame clip
    parts.append(f'<rect width="{num(w_units*u)}" height="{num(h_units*u)}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    parts.append(f'<rect x="-6" y="-6" width="{num(w_units*u+12)}" height="{num(h_units*u+12)}" fill="none" stroke="{INK}" stroke-width="0.8"/>')
    parts.append(compass_at(spec, 0, 0, w_units * u, h_units * u, 30))
    parts.append("</g>")
    parts.append(cartouche(map_title(spec, gm), spec.get("subtitle", ""), margin, margin + h_units * u + 14,
                           w_units * u, spec.get("scale_text", "Travel times on paths"), gm))
    parts.append("</svg>")
    return "\n".join(parts), (W, H), None


# ---------------------------------------------------------------- driver

def render(spec_path, out_dir=None, png=False):
    spec_path = Path(spec_path)
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SpecError(f"{spec_path.name}: invalid JSON ({e})")
    name = spec_path.name
    mid = need(spec, "id", str, name)
    kind = need(spec, "kind", str, name)
    out_dir = Path(out_dir) if out_dir else spec_path.parent.parent / "build" / "maps"
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {"id": mid, "kind": kind, "files": [], "warnings": []}
    if kind == "dungeon":
        renderer = render_dungeon
    elif kind == "area":
        renderer = render_area
    elif kind == "pointcrawl":
        renderer = None
    else:
        raise SpecError(f"{name}: kind must be dungeon, area or pointcrawl")
    if renderer:
        for label, gm in (("gm", True), ("player", False)):
            svg, size, model = renderer(spec, name, gm)
            p = out_dir / f"{mid}-{label}.svg"
            p.write_text(svg, encoding="utf-8")
            report["files"].append(p.name)
            if png:
                from browser import screenshot
                screenshot(p, p.with_suffix(".png"), int(size[0]), int(size[1]))
                report["files"].append(p.with_suffix(".png").name)
        svg, size, model = renderer(spec, name, False, vtt=True)
        p = out_dir / f"{mid}-vtt.svg"
        p.write_text(svg, encoding="utf-8")
        report["files"].append(p.name)
        if png:
            from browser import screenshot
            screenshot(p, out_dir / f"{mid}-vtt.png", int(size[0]), int(size[1]))
            report["files"].append(f"{mid}-vtt.png")
        if kind == "dungeon":
            report["warnings"] += dungeon_warnings(spec, model)
            if compass_clash(spec, model["region"].keys()):
                report["warnings"].append("the compass sits on floor squares; set \"compass\" to another corner or false")
            walls = dungeon_walls(spec, model)
            if model["unreachable"]:
                report["warnings"].append("unreachable from start (no door/opening joins them): "
                                          + ", ".join(r.replace("R", "room ", 1) if r.startswith("R") else r.replace("C", "corridor ", 1)
                                                      for r in model["unreachable"]))
        else:
            things = [(t["x"], t["y"]) for t in spec.get("trees", []) + spec.get("rocks", []) + spec.get("keys", [])]
            if compass_clash(spec, things):
                report["warnings"].append("the compass sits on a tree, rock or key; set \"compass\" to another corner or false")
            walls = area_walls(spec)
        px = vtt_px(spec)
        wall_doc = {"map": mid, "image": f"{mid}-vtt.png", "grid_px": px,
                    "image_size": [spec["cols"] * px, spec["rows"] * px],
                    "note": "Coordinates are VTT-image pixels. In Foundry add the scene's padding offset "
                            "(sceneX, sceneY) to every x and y before creating walls.",
                    "walls": walls}
        p = out_dir / f"{mid}-walls.json"
        p.write_text(json.dumps(wall_doc, indent=1), encoding="utf-8")
        report["files"].append(p.name)
        png_path = out_dir / f"{mid}-vtt.png"
        if png and png_path.exists():
            p = out_dir / f"{mid}.dd2vtt"
            p.write_text(json.dumps(uvtt(spec, walls, px, png_path)), encoding="utf-8")
            report["files"].append(p.name)
        report["walls"] = len(walls)
    else:
        for label, gm in (("gm", True), ("player", False)):
            svg, size, _ = render_pointcrawl(spec, name, gm)
            p = out_dir / f"{mid}-{label}.svg"
            p.write_text(svg, encoding="utf-8")
            report["files"].append(p.name)
            if png:
                from browser import screenshot
                screenshot(p, p.with_suffix(".png"), int(size[0]), int(size[1]))
                report["files"].append(p.with_suffix(".png").name)
    return report


def uvtt(spec, walls, px, png_path):
    """Universal VTT (format 0.3): image, grid and walls in one file, importable by most VTTs."""
    import base64
    los, portals = [], []
    for w in walls:
        x1, y1, x2, y2 = (v / px for v in w["c"])
        if w.get("door"):
            portals.append({"position": {"x": (x1 + x2) / 2, "y": (y1 + y2) / 2},
                            "bounds": [{"x": x1, "y": y1}, {"x": x2, "y": y2}],
                            "rotation": math.atan2(y2 - y1, x2 - x1), "closed": True, "freestanding": False})
        elif w.get("sight", 20) != 0 and w.get("preset") != "window":
            los.append([{"x": x1, "y": y1}, {"x": x2, "y": y2}])
    return {"format": 0.3, "resolution": {"map_origin": {"x": 0, "y": 0},
                                          "map_size": {"x": spec["cols"], "y": spec["rows"]}, "pixels_per_grid": px},
            "line_of_sight": los, "objects_line_of_sight": [], "portals": portals, "lights": [],
            "environment": {"baked_lighting": False, "ambient_light": "ffffffff"},
            "image": base64.b64encode(png_path.read_bytes()).decode("ascii")}


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    png = "--png" in argv
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
        args.remove(out)
    if not args:
        print(__doc__)
        return 2
    failed = False
    for a in args:
        try:
            r = render(a, out, png)
            extra = f", {r['walls']} walls" if "walls" in r else ""
            print(f"OK   {r['id']} ({r['kind']}): {len(r['files'])} files{extra}")
            for w in r["warnings"]:
                print(f"WARN {r['id']}: {w}")
        except SpecError as e:
            failed = True
            print(f"ERR  {e}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
