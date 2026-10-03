---
name: campaign-writer
description: Use when someone wants an original tabletop RPG adventure or campaign written from a rough idea, such as "give me a solo Pathfinder campaign where I hunt trolls", "a spooky one-shot for four level-3 players" or "teach me Physics I through D&D". Produces the package people expect from a downloadable adventure (GM book PDF, keyed GM and player maps, VTT map images with walls, handouts, pregens, stat blocks checked against the system's encounter maths) plus an optional Foundry/Familiar hand-off. Teach mode builds a real subject into play. Not for running a live session, importing a published adventure (use foundry-familiar-campaigns), or a quick rules question.
---

# Campaign Writer

Turn a one-line wish into the kind of adventure people buy and actually run: a GM book that works at the table, maps for print and VTT, player handouts, and numbers that hold up. In **Teach mode** the subject *is* the gameplay: players learn physics by predicting where the boulder lands, not by answering a quiz to open a door. By default the learning stays hidden (**Stealth**): the world has its own words, the story is about something else, and nobody feels taught.

Five rules shape everything:

1. **Wish in, product out, with the fewest questions.** Infer what you can. Ask one short round only when the answer changes the build (system, who plays, how long).
2. **Bones before prose.** Design the adventure as data in `campaign.json` (places, clues, NPCs, fights, lessons), run the checker, and only then write chapters. Structural mistakes are cheap to fix in data and expensive in a 12,000-word book.
3. **Runnable at the table.** A GM glancing at a page mid-game finds what's here, what's hidden, what happens next and every number they need. Read-aloud stays short. Nothing important is buried in a paragraph.
4. **Protect the player's surprise.** If the person asking will *play* it, never put the plot, twists, monsters, clue answers or puzzle solutions in chat. They get a back-cover pitch and a file path.
5. **Prove it.** The checker passes, the PDF builds, and you've looked at the pages and maps. Report what you verified and what you didn't.

## 0. Before you start

- The tools need **Python 3.9+** (standard library only). PDFs and PNG maps also need Chrome, Edge, Chromium or Brave. Check with `python <skill>/tools/browser.py`. Without a browser you still get HTML and SVG; say so in the hand-over.
- To *look* at the PDFs you need page images. If your file reader can't show PDFs, install a renderer once (`pip install pypdfium2 pillow`) and use `tools/preview_pdf.py`. If you can't install anything, say the pages weren't inspected.
- Write the package to `campaigns/<slug>/` in the working directory unless the user names a place. If that folder exists, read it first: you may be continuing someone's work.
- Long job? Work in this order and save as you go: `campaign.json` → checker → chapters → maps → handouts → allegory audit (Teach) → build → look → fix.

## 1. Read the wish

Turn the request into a brief: system, players and level, solo or group, length, tone and limits, mode (standard or Teach), who will run it (a human GM, an AI GM in Foundry/Familiar, or GM-less), and whether the requester will play. Fill gaps with the defaults in [Brief intake](references/brief-intake.md). Ask only if a missing answer would change the whole build. "Teach me physics through D&D" is enough to start. Who runs it comes from what the user says, not from which tools happen to be connected.

## 2. Design the bones in `campaign.json`

1. **Pick a structure** that fits the wish ([Structures](references/structures.md)). A monster hunt is a pointcrawl with a tracking clock. A mystery is node-based. A one-shot is five scenes. A campaign is three to five linked adventures under one threat.
2. **Find the engine.** One antagonist or force with a goal, a timeline that advances whether or not the heroes act, and a real choice at the end. Avoid stock twists (the quest-giver was the villain all along) unless the clues earn them.
3. **Root it in the game.** For D&D, give every named NPC an ancestry, then a name that sounds like it, and make creatures act on their lore (kobolds revere dragons; copper dragons joke and riddle). See [Rooting a D&D adventure in D&D](references/dnd-lore.md).
4. **Lay out** nodes, clues (three per conclusion), NPCs (want, know, hide), encounters (budgeted with [D&D 5e](references/systems/dnd5e.md), [Pathfinder 2e](references/systems/pf2e.md) or [another system](references/systems/other.md)), rewards and at least three endings. Field reference: [campaign.json](references/campaign-json.md).
5. **Teach mode:** pick the style (Stealth by default, Open for classrooms and tutors), set two to five learning objectives, the misconception each one provokes, puzzles whose *answer comes from the concept*, three-step hint ladders, scripts that recompute every numeric answer, and the sources you checked. In Stealth, also design the disguise: an analogy world rather than a rename, a story about something else, and a `lexicon` that keeps real jargon out of anything the player reads. Puzzles go in no more than about a third of the scenes (activity beats, where the world just reacts, are free). Write `teach.model` now too: for each real thing or role the world stands in for, what it is, where it lives, who can change it and how it moves (the checker requires it in Stealth; step 5 uses it). See [Teach mode](references/teach-mode.md).
6. Run `python <skill>/tools/check_campaign.py campaigns/<slug> --bones`. It checks only the skeleton (reachability, clues, encounter budgets, Teach alignment, puzzle scripts). Fix every error before you write prose.

## 3. Write the book

Write `book/NN-name.md` chapters in the order and format in [Writing the book](references/writing-the-book.md). Size it to the table: about 3,000–5,000 words of book per session of play (a one-shot is 6,000–10,000), not counting stat blocks. Write: overview and running guide, the adventure itself (one heading per node, tagged `{#id}`), NPCs, bestiary, rewards and endings, appendices, credits. Teach mode adds a Learning Guide with objectives, worked solutions and debrief questions.

Write like a good published module, not like a chatbot: concrete nouns, short read-aloud, mechanics inline ("**DC 13 Wisdom (Survival)**: the tracks are a day old"), and every NPC with a voice and a want. The checker flags stock AI phrasing. Rewrite those lines; don't just swap synonyms.

## 4. Maps, handouts and pregens

- **Maps:** write a small JSON spec per key location (`maps/<id>.json`): a *dungeon* (rooms, corridors, doors, secret doors, traps), an *area* battle map (trees, rocks, water, cliffs, paths) or a *pointcrawl* travel map (places, paths, travel times, hidden sites). One spec renders a GM map with keys and secrets, a player map without them, a VTT image at Foundry's grid size and a Foundry walls file. See [Maps and handouts](references/maps-and-handouts.md). Don't use AI image generation unless the user asks: many players dislike AI art, and it costs their credit.
- **Handouts**: `handouts/` holds what players may read **before** play (the pitch, reference cards, the player travel map). `handouts/found/` holds in-world clue documents (letters, ledgers, notices) that the GM hands over when they're found. They build into separate PDFs, so a player who opens their own PDF early spoils nothing.
- **Pregens** (`pregens/`): ready-to-play characters with a hook into this adventure, for one-shots and whenever the user has no character yet. Build them by the system's own rules.

## 5. Teach mode: audit the allegory

After the chapters, handouts, pregens and maps are drafted and before the build, whenever the world stands in for the subject (always in Stealth). The checker keeps real words out; it can't see the scenery breaking the real mechanism: energy sold in jars, one guild doing two real jobs, a handout whose numbers the backstory couldn't produce. Players learn from the props as much as from the puzzles.

1. **Finish the model.** Each `teach.model` entry says what the real thing **is**, where it **lives**, who **can change it** and how it **moves or is authorised**, with in-character *if asked* lines and any deliberate simplification.
2. **Walk the package against it:** every scene, NPC job, prop, handout, found document, pregen, puzzle and ending. Fix contradictions in the story itself, not in a footnote, and log each one in `allegory-audit.md` in the package root.
3. **Write it up:** the *If asked* lines go in the Learning Guide (answers when a player asks, never volunteered) and a *Where the story bends* block ends the Decoder.

The six failure classes, their rules and an example of each: [Teach-mode allegory audit](references/teach-allegory-audit.md).

## 6. Build, check and look

```text
python <skill>/tools/check_campaign.py campaigns/<slug>      # must end with 0 errors
python <skill>/tools/build_book.py campaigns/<slug>          # GM book + handouts, HTML and PDF
```

The build also re-renders every map (SVG and PNG) and warns about unrendered markdown and handouts that spill onto a second page. Then **look**: `python <skill>/tools/preview_pdf.py build/<slug>-gm-book.pdf` makes contact sheets (6 pages each) and `--pages 5,9` renders single pages up close. Look at every contact sheet (handout PDFs are skipped for gaps: their pages are short by design), a few pages at full size, every map PNG in `build/maps/`, and the handouts. The preview also prints `GAP` lines for pages where a column stops early; check each one (a chapter's last page is fine). Fix overflow, gaps, collisions and anything a reader would trip on. Then run the review passes and the score sheet in [Quality bar](references/quality-bar.md), and fix any part scoring under 8.

## 7. Hand over

Write `README.md` in the package (what's inside, how to run it, licence). Then give the user a short receipt in chat:

```text
Ready:     <title>, <system>, <players/level>, <sessions>; start by reading <file/section>
Package:   GM book (N pages), handouts (N pages), N maps (GM/player/VTT), N pregens
Verified:  checker 0 errors / N warnings kept (why); PDFs built and inspected; maps inspected; Teach: allegory audit, N fixes
Scores:    the quality-bar parts out of 10 (also in the README)
Not done:  anything skipped or unverified
Next:      the one next step (e.g. "install in Foundry with foundry-familiar-campaigns")
```

If the requester is the GM, add the GM pitch (a few lines: what's really going on and the big choice) after the receipt. If the requester will play, the receipt names files and counts but **no plot**. Don't summarise the story, villain, twist or answers. Tell them which files are GM-only.

**Foundry + Familiar:** if they play in Foundry with Familiar's AI GM, follow [Foundry hand-off](references/foundry-handoff.md): `tools/export_foundry.py` turns the book into Foundry-ready journal pages, and `foundry/handoff.md` tells the installer the rest. It prepares the package so the companion skill `foundry-familiar-campaigns` can install it, including Teach-mode rules for the AI GM. If that skill isn't installed, tell the user where to get it (github.com/cha1latte/familiar-campaign-prep) instead of improvising an install.

## References

| File | Read when |
|---|---|
| [brief-intake.md](references/brief-intake.md) | Always, at the start: defaults, questions, spoiler-safe pitch |
| [structures.md](references/structures.md) | Designing the adventure: structures, engine, clues, endings |
| [campaign-json.md](references/campaign-json.md) | Writing or fixing `campaign.json` |
| [writing-the-book.md](references/writing-the-book.md) | Writing chapters: outline, templates, style, markdown |
| [maps-and-handouts.md](references/maps-and-handouts.md) | Map specs, handouts, pregens |
| [teach-mode.md](references/teach-mode.md) | Any educational request |
| [teach-allegory-audit.md](references/teach-allegory-audit.md) | Teach mode, after drafting: the model, the walk, six failure classes |
| [dnd-lore.md](references/dnd-lore.md) | Any D&D adventure: species, names, creature lore, system names |
| [systems/dnd5e.md](references/systems/dnd5e.md) | D&D 5e (2024 or 2014) |
| [systems/pf2e.md](references/systems/pf2e.md) | Pathfinder 2e (remaster) |
| [systems/other.md](references/systems/other.md) | Any other system |
| [quality-bar.md](references/quality-bar.md) | Before hand-over: review passes and score sheet |
| [foundry-handoff.md](references/foundry-handoff.md) | The table plays in Foundry, especially with Familiar |
