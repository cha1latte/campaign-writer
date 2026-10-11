# Changelog

## 1.4.0 (2026-10-11)

**Teach mode: teach before you test. Dialogue: offers and voices that sound like people**
- Teach before test: the first time players meet an idea is never a bet, a choice with a stake or a puzzle. The *Introduced* beat shows the idea working once with nothing riding on it (a character does it out loud with small numbers, or the world does it in plain view); the predict-with-a-stake moment moves to *Practised*. Show-then-try inside one scene is fine.
- `shows` on introduce beats in campaign.json: who shows the idea and how. The checker errors when an introduce beat carries a puzzle and warns when it has no `shows`.
- Fair givens: every number a puzzle needs is said in play before the players commit. A fact they can't know to ask about (the world's calendar, what "let it ride" does) is never left to an *if asked* answer. The student pass in the quality bar now solves puzzles only from what the scene actually puts in front of the players.
- If players say they weren't taught something, the AI GM fixes it in the fiction (a character shows the idea, no stakes) and never explains it out of character; a loss that came from missing givens is undone in-world for a reason that fits a character.
- NPC voices: a **Voice** note is seasoning, not a rule for every line. Never write "says X every sentence" (an AI GM obeys it and the NPC turns into a caricature); the sample line shows rhythm, it isn't a script.
- Foundry hand-off: the Runner Guide tells the AI GM to talk like people (one or two sentences a line, answer what was asked, catchphrases once or twice a scene) and to keep actions out of voiced quotes, because the voice reads everything inside them.
- Foundry hand-off: after AI-painting a map, check every entrance the book names against the painting and fix the book or the walls to match; generate a music bed per scene if the world has no playlists, and recommend Dice So Nice.
- Found in live play: a group lost their first wages on a bet about an idea nobody had shown them, with one key fact only available "if asked", and said the puzzle felt unfair.

## 1.3.0 (2026-10-10)

**Teach mode: onboard, don't flood**
- New principle: an invented world is its own jargon. The heroes are newcomers, and locals explain their own words to newcomers, in half a breath and in their own voice. A friendly gloss of the *world's* word is fine; a definition of the *real* term still isn't.
- New **word ladder**, `teach.words` in campaign.json: every world word a player has to learn (money words and setting names), with a plain `gloss` and the node where it first lands. At most three new words per node, fewer in the opening scene, and named characters introduced one or two at a time instead of as a roll-call.
- Checker: warns when a node introduces more than three new world words, when a word has no gloss, and when lexicon world words aren't on the ladder. Stealth packages without a ladder get a warning, not an error.
- New **newcomer test** in the accuracy pass and the quality bar: read the opening aloud as someone who's never seen the setting and count what they'd have to ask about.
- Players may get one in-world word list that starts empty and grows as they meet words (a list chalked inside a cupboard door), never a pre-play glossary.
- Foundry hand-off: the AI GM's Table Rules and Runner Guide introduce world words in ladder order, glossed on first use, and answer "what does X mean?" in one plain line.
- Found in live play: an opening scene with ten new words and seven characters read as "a lot of jargon, intimidating to get started".

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
