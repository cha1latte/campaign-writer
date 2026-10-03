# Changelog

## 1.2.0 (2026-10-03)

**Teach mode: the costume can't break the lesson**
- New **allegory audit**, run after drafting and before the build. Write a short model of each mapping (what the real thing is, where it lives, who can change it, how it moves or is authorised), then walk every scene, prop, handout, puzzle and ending against it. A new reference names six ways a disguise quietly teaches the wrong thing (abstract things turned into props, two real roles run by one institution, puzzle givens the backstory couldn't produce, no answer to "how does that work here?", plot-convenient delays, unflagged simplifications), with a rule and an example for each.
- `teach.model` in campaign.json. The checker requires it in Stealth, checks its fields, warns when two real roles share one in-world owner, and keeps real jargon out of the in-character *If asked* lines.
- The Learning Guide gains *If asked* (answers for a curious player, never volunteered) and the Decoder ends with *Where the story bends*.
- Quality bar pass "the curious player"; Foundry Table Rules and Runner Guide tell the AI GM to answer "how does that work?" from the If asked lines.
- The audit's findings go in an `allegory-audit.md` log in the package (the checker warns when it's missing), and `--bones` accepts a sketch of the model.
- One rule for puzzle scripts: they recompute the answer from what the backstory says happened, so a handout number the backstory couldn't produce shows up as a mismatch.
- Lesson density says the same thing everywhere: puzzles in no more than about a third of the scenes; activity beats are free. `--bones` no longer warns that puzzle answers are missing from a book that isn't written yet.
- Tested with a cold build of a new Stealth one-shot (how the internet works): the walk found 26 problems the checker couldn't see, and the friction it hit shaped the points above.
- Stealth packages made with 1.1.0 need a `teach.model` to pass the checker.

## 1.1.0 (2026-10-02)

**Teach mode no longer feels like school**
- New **Stealth** style, now the default for adults, teens, solo players and friend groups. The world has its own words, the story is about something other than the subject, and nobody feels taught. **Open** style stays for classrooms, tutors and "quiz me".
- A `teach.lexicon` sorts real terms into `jargon` (never in anything a player reads) and `slang` (only inside a character's quotation marks). The checker fails on jargon in handouts, pregens, found documents, read-aloud, letter/poem/sign boxes and the title and tagline.
- The **Decoder**: an opt-in "what that was called out there", offered once per session in one line. It replaces the out-of-character debrief and the reference card in Stealth.
- Checker: warns when puzzles sit in more than 40% of the scenes (beats where the world just reacts are free), when there are more than five objectives, and when a Stealth book has no Decoder.
- The builder no longer prints "Teaches: ..." on the covers in Stealth.
- Foundry hand-off: Stealth Table Rules and Runner Guide (no quiz voice, no debrief, a silent Learning Tracker), with the Open versions kept.

**Rooted in D&D**
- New reference, *Rooting a D&D adventure in D&D*: give every named NPC an ancestry and a name that sounds like it (dwarf, orc, halfling and kobold conventions, with sources), make creatures act on their lore (kobolds revere dragons, copper dragons joke and riddle), use SRD names and the edition's own terms (no half-orcs in 2024 text), and keep closed-setting proper nouns out of public packages.
- Quality bar: new loremaster review pass and a D&D-fit score.

**Unchanged:** the example packages below were built with 1.0.0 (Open-style Teach mode where it applies).

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
