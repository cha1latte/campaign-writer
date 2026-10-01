# campaign.json

The adventure's skeleton as data. The checker reads it to prove the structure works; the book builder reads it for the cover. Write it first, keep it in sync with the book, and keep IDs stable once chapters reference them.

## Example (a small, valid file)

```json
{
  "title": "The Weight of Falling Things",
  "slug": "weight-of-falling-things",
  "tagline": "The Clockwork Academy's tower is tilting, and only you can read why.",
  "system": "dnd5e-2024",
  "mode": "teach",
  "players": {"count": 1, "level": 3, "solo": true,
              "companions": [{"name": "Pim, apprentice artificer", "counts_as_character": false}]},
  "length": {"sessions": 3, "hours_per_session": 2},
  "audience": {"requester_plays": true, "ages": "16+"},
  "table": {"runner": "familiar", "maps": true},
  "structure": "node",
  "credit": "Written with Campaign Writer",
  "cover_map": "m1-academy",
  "player_maps": ["m1-academy"],
  "spoiler_terms": ["Provost Varne", "counterweight sabotage"],

  "nodes": [
    {"id": "N1", "name": "The Tilting Tower", "start": true, "leads_to": ["N2", "N3"]},
    {"id": "N2", "name": "The Drop Gallery", "leads_to": ["N4"]},
    {"id": "N3", "name": "The Counterweight Shaft", "leads_to": ["N4"]},
    {"id": "N4", "name": "The Provost's Study", "leads_to": []}
  ],
  "conclusions": [
    {"id": "C1", "text": "Someone cut the counterweight cables on purpose", "required": true}
  ],
  "clues": [
    {"id": "K1", "in": "N1", "points_to": "C1", "text": "Clean cut ends on the snapped cable"},
    {"id": "K2", "in": "N3", "points_to": "C1", "text": "Fresh tool marks on the pulley housing"},
    {"id": "K3", "in": "N2", "points_to": "C1", "text": "The tower tilts toward the side with the missing weights"}
  ],
  "npcs": [
    {"id": "P1", "name": "Pim", "appears": ["N1", "N2"], "wants": "to prove apprentices can fix the tower",
     "secret": "dropped a cable cutter near the shaft in a panic"}
  ],
  "encounters": [
    {"id": "E1", "node": "N3", "name": "Brass guardians", "difficulty": "moderate",
     "creatures": [{"name": "Animated Armor", "cr": "1", "xp": 200, "count": 1, "source": "SRD 5.2.1"}],
     "avoidable": true}
  ],
  "endings": [
    {"id": "X1", "text": "Tower saved, saboteur exposed"},
    {"id": "X2", "text": "Tower saved, saboteur escapes"},
    {"id": "X3", "text": "Tower falls; the Academy relocates and blames the apprentices"}
  ],
  "teach": {
    "subject": "Physics I: free fall and torque",
    "level": "intro algebra-based",
    "objectives": [
      {"id": "LO1", "text": "Predict fall time from height using h = 1/2 g t^2", "bloom": "apply",
       "misconception": "Heavier objects fall faster"}
    ],
    "beats": [
      {"id": "B1", "objective": "LO1", "node": "N1", "kind": "introduce"},
      {"id": "B2", "objective": "LO1", "node": "N2", "kind": "practice", "puzzle": "P1"},
      {"id": "B3", "objective": "LO1", "node": "N4", "kind": "assess"}
    ],
    "puzzles": [
      {"id": "P1", "node": "N2", "objective": "LO1",
       "question": "How long does a bell dropped from the 20 m gallery take to hit the floor?",
       "answer": "about 2.0 seconds", "value": 2.02, "tolerance": 0.05, "script": "puzzles/p1_fall_time.py",
       "hints": ["What do you know: height, and that it starts at rest.",
                 "Which equation links distance and time when starting from rest?",
                 "h = 1/2 g t^2, so t = sqrt(2h/g). Put in h = 20 m and g = 9.8 m/s^2."],
       "in_world_consequence": "A wrong count means the counterweight lands early and the gallery floor cracks (DC 12 Dex save or 1d6 damage)"}
    ],
    "sources": [
      {"title": "OpenStax College Physics 2e, 2.7 Falling Objects", "url": "https://openstax.org/books/college-physics-2e/pages/2-7-falling-objects",
       "covers": ["LO1"]}
    ]
  },
  "maps": ["m1-academy"]
}
```

## Fields

**Top level**

| Field | Required | Notes |
|---|---|---|
| `title`, `slug`, `tagline` | title, slug | `slug` names the output files: lowercase, hyphens |
| `system` | yes | `dnd5e-2024`, `dnd5e-2014`, `pf2e` or `other` (then set `system_label`, e.g. "Mothership 1e") |
| `mode` | no | `standard` (default) or `teach` |
| `players` | yes | `count`, `level` (not needed for systems without levels), `party_label` (cover text such as "for four investigators"), `solo`, `companions[]` (`counts_as_character: true` for a full-strength ally that should count toward encounter budgets) |
| `gm_title` | no | What this game calls the GM: "Keeper", "Referee", "Narrator". Used on the covers |
| `licence_marker` | no | A phrase from the licence notice this game requires (e.g. "Fan Material Policy"); the checker fails if the credits lack it |
| `length` | no | `sessions` (a number; the checker sizes the book by it), `hours_per_session`, `label` (cover text such as "4 or 5 sessions of about 3 hours") |
| `audience` | no | `requester_plays` or `protect_players` (either makes empty `spoiler_terms` an error; Teach mode does too), `ages` |
| `table` | no | `runner` (`human`, `familiar`, `none`), `maps` (false for theatre-of-the-mind), `vtt` (`foundry`, `roll20`, `owlbear`, `fantasy-grounds`, or none) |
| `structure` | no | `linear`, `node`, `mystery`, `pointcrawl`, `hexcrawl`, `dungeon`, `sandbox`. The node-like ones get the stricter clue check |
| `uses_srd` | no | default true. Set false only if you use no rules text or stat blocks from the SRD/ORC material (the licence check then skips) |
| `cover_map`, `player_maps`, `maps` | no | map ids: the cover art (drawn from the player version), maps to include in the handouts PDF, and the list of all maps. The checker confirms each id exists in `maps/` |
| `spoiler_terms` | when the requester plays | Exact phrases that must not appear in handouts, pregens or player maps: the villain's name, the twist, the secret location |

**Nodes** are places, scenes or events. `id` (N1, N2…), `name`, `start` (at least one), `leads_to` (obvious next nodes), `known` (true for places the heroes know without being told: their base, the town square). Every node needs a book heading ending in `{#N1}`. In node-based structures the checker wants three ways into every node that isn't a start or `known` (each `leads_to` and each clue pointing at it counts once).

**Conclusions** are facts the players must work out (`required: true`) or may work out (`false`). **Clues** live `in` a node and `points_to` a node id or a conclusion id.

**NPCs:** `id`, `name` (must appear in the book), `appears` (node ids), `wants`, `knows`, `secret`.

**Encounters:** `id`, `node`, `name`, `difficulty`, `creatures[]`, `hazards[]`, `allies_count` (extra allied combatants for this fight only), `party_level` (when the party has levelled since the start, e.g. in part 3 of a campaign), `avoidable`, `over_budget_reason` (only for deliberate set pieces, with an escape route written in the text). The checker also warns when a fight is under half the Low budget (5e): probably trivial.
- D&D 5e creature: `name`, `cr` as a string (`"1/4"`, `"9"`), `xp` (checked against the CR), `count`, `source`.
- Pathfinder 2e creature: `name`, `level` (integer), `count`, `source`. Hazard: `name`, `level`, `complexity` (`simple` = 1/5 the XP, or `complex`), `count`, `source`.
- A companion built as a full character (PF2e or 5e) belongs in `players.companions` with `counts_as_character: true`, not in encounters.
- Other systems: `name`, `count`, and `difficulty` in the system's own terms.

**Endings:** at least three (success, partial, failure-forward).

**Teach** (Teach mode only): `subject`, `level`, `objectives[]` (`id`, `text` with a measurable verb, `bloom`, `misconception`), `beats[]` (`objective`, `node`, `kind`: introduce / practice / assess, optional `puzzle`), `puzzles[]` (`question`, `answer`, `value`, `tolerance` or `tolerance_abs`, `script`, three `hints`, `in_world_consequence`), `sources[]` (`title`, `url` or `citation`, `covers` objective ids).
- `bloom`: the thinking level the objective asks for, from Bloom's taxonomy: remember, understand, apply, analyze, evaluate, create. Most adventure puzzles are *apply* or *analyze*.
- `value` can be a number, a fraction string (`"1/3"`, compared exactly), or any other string (the script's last line must match it, ignoring case) for choices and sequences (`"left, right, middle"`).
- `answer` is the text the GM will see, and the checker wants it **word for word** somewhere in the book (the Learning Guide's solution is the natural place).
- `tolerance` is a **fraction** of the value (0.05 = ±5%; default 0.02). `tolerance_abs` is an absolute margin in the answer's units (0.1 = ±0.1 s). Print the same accepted range in the solution. The checker prints the range it accepts.
- One puzzle can serve two objectives: add a beat for each objective that names the same puzzle.

## Puzzle scripts

Every numeric answer gets a tiny script in `puzzles/` that recomputes it from the numbers printed in the puzzle. The last line of output must start with the answer. The checker runs it and compares it with `value`.

```python
# puzzles/p1_fall_time.py: bell dropped from the 20 m gallery
import math
g = 9.8      # m/s^2, as stated in the handout
h = 20.0     # m, as printed in N2
t = math.sqrt(2 * h / g)
print(f"{t:.2f} s")
```

If the book's numbers change, the script changes with them. That's the point: the book can't silently drift away from the maths.

Watch floating point when an answer rounds: `math.ceil(1200 / 0.3 / 1000)` gives 5, not 4, because `1200 / 0.3` is 4000.0000000000005. For counts ("how many weights?") use whole-number or `fractions.Fraction` arithmetic, or round to a sensible precision before `ceil`/`floor`.
