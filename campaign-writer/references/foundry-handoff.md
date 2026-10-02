# Foundry hand-off

Campaign Writer writes the adventure. Installing it in Foundry VTT, so that Familiar's AI GM can run it faithfully session after session, is the job of the companion skill **foundry-familiar-campaigns** (github.com/cha1latte/familiar-campaign-prep). Your job here is to leave a package that skill can install without guessing.

Do this when the user says they play in Foundry, and always when `table.runner` is `familiar`. Familiar's tools being connected to *you* only means Foundry is available; ask or follow the brief, and don't use those tools during writing.

## 1. Export the pages

```text
python <skill>/tools/export_foundry.py campaigns/<slug>
```

This writes `foundry/pages.json`: one Source page per node (plus intros and whole-file chapters), the handouts and found-in-play documents, all in HTML that survives Familiar's plain-text reads. Tables become one line per row, read-aloud is labelled "Read aloud: … (End of read-aloud.)", maps become a pointer to their scene image, and nothing exceeds Foundry's page limit. The installer pushes these pages as they are; nobody retypes the book. (Tested live: Familiar's `get-journal-page` returned the Learning Guide's tables as clean "Objective: …; Introduced: …" lines.)

## 2. Write `foundry/handoff.md`

One file in the package, written for the preparing assistant that will install it. Use this template and fill every field with real names, ids and paths:

```markdown
# Foundry hand-off: <Title>

Source type: original adventure written with Campaign Writer (homebrew). The book chapters in book/ are the
authoritative text; treat them as the Source. Nothing here is copied from a published adventure.
System: <dnd5e 2024 | pf2e | …>. Players: <count> at level <level>. Mode: <standard | teach: subject>.
Requester plays: <yes/no>. If yes, keep everything below out of their sight.

## Source pages (GM-only "<Title>: Source" journal)
From foundry/pages.json ("source"), in order. Page name, then the file and heading it comes from:
- 01 Overview: book/01-overview.md (whole file)
- 02 N1 The Tilting Tower: book/02-act-one.md, "## 1. The Tilting Tower {#N1}"
- …
- 20 Learning Guide: book/09-learning-guide.md (Teach mode)

## Start Here seeds
- Pickup (opening): <where the hero starts, the first decision, what's already happened>
- Table Profile: <tone, content notes, lethality rule, hint level, solo/party>
- Trackers: <clocks with their steps>
- Learning Tracker (Teach mode): its own Start Here page, "6 Learning Tracker", so logging attempts never rewrites the clocks. In Stealth it is GM-side bookkeeping the player is never shown or told about
- Runner Guide additions: <Teach-mode procedure below, any adventure-specific procedure>

## Scenes (one per map)
| Scene | Image | Grid | Size | Walls | Light | Node |
|---|---|---|---|---|---|---|
| Hollow Ridge | build/maps/m3-ridge-vtt.png | 100 px, 5 ft | 2400 × 1600 | build/maps/m3-ridge-walls.json (19) | daylight | N4 |
| Grimwater Valley (travel) | build/maps/m1-valley-player.png | none (travel map) | image size | none | n/a | N1–N8 |

Token positions per encounter (in map squares from the top-left; convert to pixels with the grid size,
then add the scene padding): E2: troll whelp at (20, 10); hero arrives on the path at (1, 12).

## Actors
- From the system compendium: Troll (SRD 5.2.1), Guard ×2 …
- Custom (build from the Bestiary page, then read the computed sheet back): Troll Whelp …
- Pregens / player character: pregens/01-…md

## Handouts journal (player-safe, GM shares by hand)
handouts/00-pitch.md, handouts/01-…md
## Found-in-play journal (GM-only until found; the runner shows each page when its node says so)
handouts/found/01-…md (given out in N3), …

## Table Rules lines to merge
<the block below, filled in>
```

## 3. Teach-mode rules for the AI GM

An AI GM's instinct is to be helpful, which means solving the puzzle for the player. These lines stop that. They're short because Familiar's Table Rules cap is 3,000 characters for everything; the full procedure lives in the Runner Guide.

**Table Rules lines, Stealth** (about 800 characters, filled in; this is the default):

```text
TEACH MODE, STEALTH (<subject>): the player must never feel taught. Lesson beats are marked in the Source pages and solved in the "Learning Guide" page.
- Never say lesson, quiz, puzzle, objective, "as you learned". Speak the world's words. Real <subject> terms only from characters who'd say them (Lexicon), never defined in narration.
- At a lesson beat, read its puzzle in the Learning Guide BEFORE narrating. Pose a situation with a want and a cost, give numbers only through the world, then STOP. Never state or hint the answer first.
- Stuck or wrong: the world reacts (soft consequence); an ally gives the next hint rung in character.
- Log attempts silently on the Learning Tracker. No out-of-character debrief. At session end offer the Decoder once, in one line, and only give it if asked.
```

**Table Rules lines, Open** (about 600 characters, filled in; classrooms, tutors, "quiz me"):

```text
TEACH MODE (<subject>): lesson beats are marked in the Source pages and solved in the "Learning Guide" page.
- At a lesson beat, read its puzzle in the Learning Guide BEFORE narrating it. Pose it in the world, then STOP and wait.
- Never state or hint the answer before the player tries. Stuck or wrong: give only the next hint rung.
- Accept any valid method within the printed range; ask "how did you get that?" A roll can buy a hint, never the answer.
- Log every attempt on the Learning Tracker page. At session end, ask the debrief questions out of character.
```

**Runner Guide section, Stealth** (full procedure, in the Start Here journal):

```text
TEACH MODE PROCEDURE (STEALTH)
1. Before a lesson beat: get-journal-page on the Learning Guide; find the puzzle (givens, answer range, hint ladder,
   in-world consequence) and the Lexicon.
2. Narrate in the world's words. Give the numbers through things the hero can see, hear or ask about, not as a list.
   Never write "hint:", never announce a challenge. A real <subject> term appears only in the mouth of a character the
   Lexicon allows, as slang, and is never explained by the narrator.
3. When the player acts or answers:
   - inside the range: show it working in the fiction. If a character would want to know why, let them ask in character;
   - outside it: the soft consequence fires, an ally (in character) offers the next hint rung when asked or when the
     player stalls. The full consequence fires only when they act on a wrong answer;
   - "I don't know" / "help": the next rung only, spoken by an ally.
4. Misconception moments: let them act on the wrong idea, show what really happens, let a character react. Never lecture.
5. Log on the "6 Learning Tracker" page, one line per attempt: date, beat or puzzle id, first answer, hints, result.
6. Session end (before Closeout): one line, "Want the decoder for tonight?" Give the Decoder block for the beats actually
   played only if they say yes. Otherwise move on. Put "Learning so far" in the Pickup.
```

**Runner Guide section, Open** (full procedure, in the Start Here journal):

```text
TEACH MODE PROCEDURE
1. Before a lesson beat: get-journal-page on the Learning Guide; find the puzzle (question, givens, answer range,
   hint ladder, in-world consequence).
2. Narrate the situation and give every number the player needs, in the world's words. Ask for a prediction or
   an answer. Stop. Do not add "hint:" lines.
3. If they answer:
   - inside the range: show it working in the fiction, then ask them to explain their reasoning in one line;
   - outside it: if it's a common wrong answer, ask its diagnostic question; show the soft consequence; offer to try
     again (hint rung 1 if they want it). The full consequence fires only when they act on a wrong answer;
   - "I don't know" / "help": give the next hint rung only (1, then 2, then 3).
4. Misconception moments: let them commit to the wrong prediction, then show what really happens and ask why.
   Don't lecture first.
5. Log: on the "6 Learning Tracker" page, one line per attempt: date, beat or puzzle id, first answer, hints used, result.
   For an introduce beat, log the prediction, then add the player's "why" to the same line.
6. Session end (before Closeout): ask only the debrief questions for beats actually played (a real-world session
   often stops partway through an adventure session), write the answers on the Learning Tracker page, and
   include "Learning so far" in the Pickup. If the player has to leave at once, write the Pickup first with
   "debrief pending", and ask the questions at the start of next session.
```

**Learning Tracker** (its own Start Here page, `6 Learning Tracker`; `update-journal-page` replaces a whole page, so keeping it separate stops a log write from clobbering the clocks):

```text
LEARNING TRACKER: <subject>
Objectives: LO1 <text> | LO2 <text> | …
Attempts (newest last):
- <date> P1 (LO1): first answer "3 s", hints 1, final "2 s" correct
Debrief notes:
- <date>: <what they explained in their own words>
Status: LO1 practised 1/2, assessed no; LO2 not yet met
```

## 4. Prepare files Foundry can load

- VTT images are `build/maps/<id>-vtt.png`: exactly `cols × foundry_px` by `rows × foundry_px` pixels. Foundry needs them under its own **Data** folder (for example `Data/campaign-writer/<slug>/`), not a local path elsewhere. Tell the installing assistant or the GM to copy `build/maps/*-vtt.png` there.
- Walls are in `build/maps/<id>-walls.json`, in image pixels, already in the shape Familiar's `create-walls` takes: `c` is `[x1, y1, x2, y2]`; `door: 1` is a door, `door: 2` a secret door; `ds: 2` is locked; `preset: "window"` is a window; the portcullis entry blocks movement but not sight. Add the scene's padding offset (Foundry's `sceneX`, `sceneY`) to every coordinate, and send at most 100 walls per call.
- Familiar's canvas tools (walls, lights, tokens) act on the **active** scene only, so the installer stages scenes carefully. Don't activate scenes yourself during writing.

## 5. Hand over

In the receipt, say: "Foundry hand-off ready in `foundry/handoff.md`. Next: ask your assistant to install it with foundry-familiar-campaigns." Add these two notes to `handoff.md` for the installer:

- **Share the player handouts.** Familiar can't change journal ownership, so the GM shares the player-safe pages (pitch, reference card, notebook) by hand, and the found-in-play pages when each is found. Say which pages are which by their numbers.
- **Give each campaign its own world if you can.** Familiar feeds its AI GM the world's campaign memories and its table-chat history. Tested live in a world that already held another campaign: after the Table Rules were switched, table chat kept answering as the old campaign ("this chat is currently hosting <old campaign>"). Neither the GM panel's *New chat* nor a player's `@familiar /new` resets table chat. What worked: **switch Table Chat off and on** in Familiar's settings (that clears table-chat turn histories) and **start the Table Rules with an explicit line**: `ACTIVE CAMPAIGN in this world: <Title>. The solo player is "<user>", playing <PC>. <Other campaign> is PAUSED: never read its journals, never mention it, ignore its campaign memories and old chat.` After that, Familiar's own AI GM read the right Start Here, recapped from the Pickup and ran the next lesson beat.
