# Maps, handouts and pregens

## Maps

Downloadable adventures ship a map for every key location, in a GM version and a player version, often VTT-ready. `tools/map_svg.py` draws all of that from one small JSON spec per map, so maps match the text exactly and walls come free. `build_book.py` re-renders every map on each build; to iterate on one map, run:

```text
python <skill>/tools/map_svg.py campaigns/<slug>/maps/m2-cellars.json --png
```

Each spec writes to `build/maps/`:

| File | What it is |
|---|---|
| `<id>-gm.svg/.png` | Print map: room keys, secret doors (S), traps (T), hidden rooms and places, GM labels |
| `<id>-player.svg/.png` | The same map with every secret removed. Safe to hand out |
| `<id>-vtt.svg/.png` | Dungeon/area only: exactly `cols × rows` squares at `foundry_px` (default 100) per square, no frame, player-safe |
| `<id>-walls.json` | Dungeon/area only: Foundry walls in VTT-image pixels; doors, secret doors, locks and windows set |
| `<id>.dd2vtt` | Dungeon/area only, with `--png`: Universal VTT file (image, grid, walls, doors in one). Roll20 (with the UniversalVTTImporter API script), Owlbear Rodeo, Foundry (Universal Battlemap Importer), Fantasy Grounds and Arkenforge can import it |

Which locations get a map: anywhere with a fight, a chase, exploration or a puzzle that depends on layout. Social scenes rarely need one. A hunt or journey gets one pointcrawl travel map. Aim for 3–6 maps in a one-shot and 5–12 in a short campaign.

**Look at every PNG.** Check that keys sit inside their rooms, labels don't collide, doors are on walls, nothing important hides under the compass, and the player version gives nothing away. A gap in the terrain where a hidden place sits is a leak, and so is a player-map label that names a place the players haven't heard of yet.

**Everything is clipped to the map frame**, so water, forests and paths can run off the edge: put their points past the border.

**Titles show on player maps.** If the real title is a spoiler ("The Hag's Lair"), add `"player_title": "Sea Cave"`. The checker reads player titles, visible node names, labels and room names for spoiler terms.

**Coordinates.** All maps use squares (pointcrawls use map units), with `x` to the right and `y` down from the top-left corner. Things that *occupy a square* (rooms, corridors, doors, features, trees, rocks, keys) give that square's top-left corner and are drawn inside or centred on it. Lines and shapes (paths, streams, water, cliffs, walls, labels) are on grid lines, so `[0, 5]` is the left edge, five squares down.

**Compass.** `"compass": "tr"` (default), `"tl"`, `"bl"`, `"br"` or `false`. The renderer warns when it lands on floor, trees, rocks or keys.

**Grid size for the VTT image.** `"vtt": "roll20"` (70 px a square), `"foundry"` (100, the default), `"owlbear"` (150) or `"fantasy-grounds"` (50); or set `vtt_px` yourself (`foundry_px` still works). Roll20 can't read `walls.json`: use the `.dd2vtt` file (with Roll20's UniversalVTTImporter API script), or draw Dynamic Lighting by hand. Owlbear Rodeo needs a community extension that imports Universal VTT files plus a fog/lighting extension; otherwise upload the `-vtt.png` and set the grid to the map's squares. VTT images carry no grid lines (the VTT draws its own), so set the grid size to `vtt_px` when you upload.

### Kind 1: dungeon (rooms, corridors, doors)

Rooms and corridors are rectangles. **Different rooms and corridors are walled off from each other unless a door joins them**, and that includes two corridor rectangles that touch. Every connection is a deliberate `doors` entry (`"type": "open"` for an archway or a corridor mouth). The renderer and the checker report any area you can't reach from `start`.

```json
{
  "id": "m2-cellars", "kind": "dungeon", "title": "Mill Cellars", "subtitle": "Beneath the Drowned Mill",
  "cols": 26, "rows": 18, "feet_per_cell": 5, "style": "ink", "foundry_px": 100,
  "rooms": [
    {"key": "1", "x": 2, "y": 2, "w": 7, "h": 5},
    {"key": "2", "x": 12, "y": 2, "w": 5, "h": 4, "label_at": [14, 3]},
    {"key": "3", "x": 20, "y": 2, "w": 4, "h": 4, "hidden": true},
    {"key": "4", "x": 2, "y": 10, "w": 5, "h": 5, "reached_by": "ladder down from area 1"}
  ],
  "corridors": [{"x": 9, "y": 4, "w": 3, "h": 1}, {"x": 17, "y": 3, "w": 3, "h": 1}],
  "doors": [
    {"x": 5, "y": 2, "side": "n", "type": "door"},
    {"x": 9, "y": 4, "side": "w", "type": "open"},
    {"x": 11, "y": 4, "side": "e", "type": "locked"},
    {"x": 17, "y": 3, "side": "w", "type": "open"},
    {"x": 19, "y": 3, "side": "e", "type": "secret"},
    {"x": 2, "y": 3, "side": "w", "type": "window"}
  ],
  "features": [
    {"type": "stairs", "x": 3, "y": 3, "w": 1, "h": 3, "dir": "n"},
    {"type": "trap", "x": 10, "y": 4},
    {"type": "water", "x": 13, "y": 3, "w": 3, "h": 2}
  ],
  "start": {"x": 5, "y": 2}
}
```

- `doors[]`: a floor square and the side of it the door sits on (`n`, `s`, `e`, `w`). Types: `door`, `locked`, `barred`, `secret` (wall to players, `S` on the GM map, a secret door in Foundry), `open`, `portcullis` (blocks movement, not sight), `window` (blocks movement, not sight or light).
- `rooms[].hidden: true`: a secret room. It's drawn on the GM map only; on the player map and the VTT image it's solid rock, and doors into it are plain wall. Its walls still go into `walls.json`.
- `rooms[].reached_by`: for rooms entered some other way (stairs or a ladder to another floor, a trapdoor, a teleport circle). They count as reachable. **Multi-floor buildings:** draw each floor as its own rooms on one map, side by side with a gap, and give the upper floor's first room a `reached_by` naming the stairs. Or make one map per floor.
- `features[]` types: `stairs` (`dir`), `water`, `pit`, `pillar`, `rubble`, `trap` (GM only), `statue`, `table`, `desk`, `counter`, `altar`, `bed`, `chest`, `crate`, `barrel`, `well`, `brazier`, `fire`, `radio`, `boat`, `label` (`text`). The renderer warns when a room key would cover a feature (move it with `label_at`) and when a secret door opens into solid rock. Add `"gm": true` to hide any feature from players. Feature text is small and dark with a white outline; use top-level `labels` (area maps) for bigger place names.
- `rooms[].extra_cells`: `[[x, y], …]` to make a room irregular. `style`: `ink` (hatched, Dyson-like) or `blueprint` (classic blue).
- `surround`: what's outside the rooms. `rock` (default, hatched), `water` (a ship's decks at sea, a pier, a stilt house) or `none` (a building on open ground). **Ships:** draw each deck as rooms (bow, main deck, stern castle, hold), join them with `open` doors and stairs, and set `"surround": "water"`. Use `extra_cells` to taper the bow.
- Other keys: `print_px` (print scale, default 32), `seed` (texture variation), `exterior` is no longer needed.

### Kind 2: area (outdoor or open battle map)

```json
{
  "id": "m3-ridge", "kind": "area", "title": "Ambush at Hollow Ridge", "cols": 24, "rows": 16, "ground": "snow",
  "trees": [{"x": 2, "y": 2, "r": 1.3}, {"x": 19, "y": 12, "r": 1.2, "kind": "broadleaf"}],
  "rocks": [{"x": 10, "y": 4, "r": 0.9, "blocks": true}],
  "water": [{"points": [[14, -1], [17, 1], [18, 4], [16, 6], [14, 5]], "frozen": true}],
  "streams": [{"points": [[3, 17], [5, 13], [9, 12.5], [13, 17]], "width": 0.9}],
  "chasms": [{"points": [[19, 6], [23, 5.5], [25, 8], [22, 9], [19.5, 8.5]]}],
  "bridges": [{"points": [[8.2, 11.4], [8.6, 14.2]], "width": 1.4}],
  "cliffs": [{"points": [[0, 7], [4, 7.5], [9, 8]], "side": "left"}],
  "walls": [{"points": [[3, 12], [8, 12], [8, 15]]}],
  "rough": [{"points": [[5, 1], [9, 1], [9, 3], [5, 3]]}],
  "paths": [{"points": [[-1, 12], [6, 10], [12, 8], [25, 5]], "width": 1.4}],
  "features": [{"type": "fire", "x": 12, "y": 9}, {"type": "crate", "x": 13, "y": 9}],
  "keys": [{"key": "A", "x": 12, "y": 7}],
  "labels": [{"x": 1, "y": 15.4, "text": "to Kettle Hollow"}, {"x": 20, "y": 1, "text": "troll den", "gm": true}],
  "compass": "br"
}
```

- `ground`: `grass`, `snow`, `stone`, `sand`, `swamp`, `forest-floor`, `dirt`, `cave`, `wood` (planks: decks, ship holds, floors).
- Water is smoothed into natural shores; add `"smooth": false` for straight man-made edges (wharves, piers, canals), and `"deep": true` for darker deep water. Overlapping water shapes show a seam where they cross: draw one shape instead. Rough ground under water is hidden (water draws on top).
- Drawing order: ground, rough, water, streams, chasms, paths, bridges, cliffs, walls, rocks, grid, features, trees, keys, labels. A path drawn across water reads as a ford; use a bridge for a deck.
- **Foundry walls** come from `cliffs`, `walls` and rocks with `blocks: true`. Water, chasms, rough ground and trees are terrain, not walls. A cliff is a wall along its whole length, so where a bridge, stair or path crosses a cliff, **split the cliff into two lines** with a gap there.
- `features[]` work here too (fires, crates, altars, statues, tables, wells…). Keys and `gm` labels appear on the GM map only.

### Kind 3: pointcrawl (travel map)

Coordinates in map units (default 100 × 70). Text scales with the map, so it stays legible at page width.

```json
{
  "id": "m1-valley", "kind": "pointcrawl", "title": "The Grimwater Valley", "w": 100, "h": 64,
  "areas": [{"type": "pines", "points": [[5, 8], [30, 4], [38, 18], [26, 30], [8, 26]], "label": "The Needlewood"}],
  "rivers": [{"points": [[-2, 36], [40, 34], [102, 38]], "width": 0.7}],
  "nodes": [
    {"id": "N1", "key": "1", "name": "Kettle Hollow", "x": 14, "y": 46, "icon": "village"},
    {"id": "N6", "key": "6", "name": "The Gnawing Cave", "x": 82, "y": 16, "icon": "lair", "hidden": true}
  ],
  "edges": [{"from": "N1", "to": "N6", "label": "2 hrs", "style": "trail"}]
}
```

Area types: `forest`, `pines`, `mountains`, `hills`, `marsh`, `lake`, `snowfield`, `sea`, and for towns and farmland `town` (street blocks), `fields`, `land` (plain ground). Free text goes in `labels` (`x`, `y`, `text`, optional `size`, `gm`): districts, streets, "to Salem". Icons: `village`, `town`, `farm`, `camp`, `cave`, `mine`, `lair`, `tower`, `fort`, `ruin`, `standing-stones`, `shrine`, `bridge`, `grove`, `peak`, `lake`, `ship`, `spot`. Edge styles: `road`, `trail`, `river`, `secret`; `bend` (default 0.12, negative bends the other way) shapes the curve. A travel map has **no grid**: give distances as travel times on the paths, and set the footer with `scale_text` ("Travel times by longboat").

**Hidden places:** a `hidden` node appears only on the GM map. An edge to it that isn't itself `hidden` shows on the player map as a road that leaves the known place and fades out, with no label: players know the trail goes somewhere. Mark the edge `hidden` too if even the trail is secret. Use the node ids from `campaign.json` so map and book agree. Move a crowded label with `label_side` (`below`, `above`, `left`, `right`) or a smaller `label_size` (0.8) on a node, `label_t` (0 to 1 along the path) or `label_offset` (`[dx, dy]` in map units) on an edge, and `label_at` on an area. City investigations with many sites: map the districts and landmarks, and list the individual addresses in the book.

### In the book and in Foundry

- `![Map 2: Mill Cellars](map:m2-cellars){page}` puts a battle map on its own page; `{wide}` spans both columns (best at the top of a chapter). The book shows the GM version; the handouts PDF shows the player version of maps listed in `player_maps` (landscape maps get a landscape page).
- For Foundry: upload `<id>-vtt.png`, set the scene grid to `foundry_px` (default 100) and the size to `cols × foundry_px` by `rows × foundry_px`, then create the walls from `<id>-walls.json`, adding the scene's padding offset to every coordinate. See the [Foundry hand-off](foundry-handoff.md).

## Handouts

Two folders, two PDFs:

| Folder | Builds into | Holds | Who sees it when |
|---|---|---|---|
| `handouts/` | `<slug>-handouts.pdf` (with pregens and `player_maps`) | `00-pitch.md` (always), reference cards, a field notebook, safety-tool sheet | The players, before the first session |
| `handouts/found/` | `<slug>-found-in-play.pdf` | In-world documents that carry clues: letters, ledgers, notices, a map scrap, a wanted poster | The GM hands each one over when it's found |

The checker scans `handouts/` and `pregens/` for `spoiler_terms`. Found documents may carry clues, since that's their job, but shouldn't give away more than the moment calls for. In the book, name the node that hands each one out. GM notes for a handout go in a ```` ```gm ```` box in the book or in the handout file; they're dropped from every player PDF.

- Write documents in the character's voice, in a ```` ```letter ```` box or as plain paragraphs (not `>`, which is the small italic read-aloud style), and make the clue findable: plain enough that a player who reads it carefully gets it.
- Teach mode: a **reference card** (formulas, units, a worked example in the setting's voice, a glossary) and, if wanted, a **field notebook** page with ```` ```write 6 ```` lines for predictions. One page each.
- One handout per file; each prints on its own page. The build warns if one spills onto a second page.
- **Signs, posters and charts:** use a ```` ```sign Title ```` box for big lettering, or a markdown table for a chart. If you draw an SVG diagram for a handout, give its text a common font (Georgia, Arial): the bundled fonts don't reach images. Printable manipulatives (fraction strips, cut-out cards, a dial) work well as tables or simple SVGs.

## Pregens

Don't put GM ids (N3, C1, E2) in anything players see; the checker flags them. Put ready-to-play characters in `pregens/` (one file each) for one-shots and whenever the user has no character. Each one: name, ancestry or species, class and level, a one-line concept, the full numbers by the system's own rules (abilities, AC, HP, attacks with bonuses and damage, saves, skills, spells or features), equipment, and **a personal hook into this adventure** plus a bond that pays off in play. Pregens are player material: check each bond for indirect spoilers. For a solo game, offer two or three so the player can choose.

Check pregen maths with the system file's build checklist ([D&D 5e](systems/dnd5e.md#pregens-2024-rules), [Pathfinder 2e](systems/pf2e.md#pregens)). A wrong pregen is the first thing a player notices. Keep each to one page: the build warns when one spills over. A short level-1 sheet can use the spare space for a "how to play this character" box or ```` ```write 6 ```` notes lines.
