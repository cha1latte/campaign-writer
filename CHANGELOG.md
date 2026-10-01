# Changelog

## 1.0.0 (2026-10-01)

First release.

**Writes the whole package from one sentence**
- GM book, player handouts and found-in-play PDFs, built by a headless browser with a bundled book style (Alegreya, OFL).
- Maps from small JSON specs: dungeons (rooms, doors, secret doors, traps, hidden rooms, multiple floors, ships on water), outdoor battle maps and pointcrawl travel maps. Each map comes in GM, player and VTT versions, with Foundry walls and a Universal VTT (.dd2vtt) file. Roll20, Owlbear Rodeo and Fantasy Grounds grid presets.
- Pregens built by the system's own rules, with personal hooks.

**Teach mode**
- Learning objectives with the misconception each one targets, puzzles whose answer comes from the concept, three-rung hint ladders, soft and full consequences, debrief questions, and sources.
- Every puzzle answer (numbers, fractions, choices) is recomputed by a script.
- Rules for an AI game master to teach without giving answers away, tested live in Foundry.

**Checks before you see it** (`check_campaign.py`, with `--bones` for the skeleton)
- Reachability, the Three Clue Rule, node-based ways in.
- Encounter budgets: D&D 5e 2024 (SRD 5.2.1) and Pathfinder 2e (GM Core), including small parties and hazards.
- Spoiler terms and GM ids kept out of player material; licence notices present; stock AI phrasing; read-aloud length; book length.

**Foundry hand-off**
- `export_foundry.py` turns the book into journal pages that read cleanly through Familiar.
- A hand-off file for Familiar Campaign Prep, including Teach-mode Table Rules and a Learning Tracker page.

**Systems:** D&D 5e (2024 and 2014), Pathfinder 2e remaster, Call of Cthulhu 7e, plus guidance for other families.

**Tested:** six campaigns written cold by fresh AIs across three systems, with fixes after each round; played live in Foundry VTT 14 with Familiar 2.25 by an outside AI GM and by Familiar's own AI GM.
