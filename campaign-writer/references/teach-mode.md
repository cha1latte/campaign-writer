# Teach mode

"Teach me Physics I through D&D." The adventure has to be fun on its own *and* leave the player able to do something they couldn't do before. Get either half wrong and it fails: a quiz with dice is homework, and a romp with a physics word in it teaches nothing.

There is a third way to fail, and it is the commonest: **the lesson shows**. A world where every coin, ledger and shop is a one-word rename of the real subject, where NPCs explain terms, and where nearly every scene ends in a question with a right answer, is a lecture in a costume. Players feel it in the first ten minutes and the fun drains out. The more obvious the learning, the less fun it is. Everything below is built to stop that.

## Pick the teaching style first

| Style | Use when | What it means |
|---|---|---|
| **Stealth** (default) | The learner is an adult or teenager who wants a good game, "sneak it in", a solo player, a friend group | The narration never names the subject. The world has its own words. Learning is judged by what the world does, not by questions. No quiz voice, no out-of-character debrief. An optional **Decoder** maps the world's words to the real ones, only when the player asks. |
| **Open** | A classroom, a parent or tutor running it for a child, someone who said "quiz me" or "I want to practise" | The subject can be named, there is a reference card, and the debrief and check run as written. Everything else in this file still applies: fun first, concept as the verb, little and often. |

Set `teach.style` in `campaign.json`. If the request doesn't say, use Stealth.

## The principles

1. **The concept is the verb.** Players succeed *by using the idea*: predicting where the boulder lands, timing the rope cut, balancing the drawbridge. Educational games that build the content into the core mechanic teach more than ones that bolt quiz questions onto play (Habgood & Ainsworth's "intrinsic integration" studies; the bolted-on kind is nicknamed "chocolate-covered broccoli"). If a puzzle would work the same with the subject swapped for trivia, redesign it.
2. **Dice never replace thinking.** A roll can buy a hint, save time or soften a mistake. It never produces the answer. An Intelligence check can reveal the next hint rung; the player still does the reasoning.
3. **Predict, then watch, then explain.** Misconceptions survive lectures and die to surprises. Have the player commit to a prediction, show the world doing the real thing, then ask why. This is the core loop for any concept with a common wrong intuition. In Stealth the prediction is a *choice with a stake* (place the bet, pick the door, set the weight), the world shows the result, and the "why" comes from a character who wants to know, never from the GM stepping outside the story.
4. **Mistakes cost something in the fiction, never the game.** A wrong answer cracks the floor, wakes the guard or costs an hour. It never kills the character or locks the adventure. Every puzzle has a way forward after a miss, often a second attempt with what they learned.
5. **Little and often.** Each objective appears at least three times: introduced, practised, assessed, ideally in different sessions and mixed with older ideas (spaced and interleaved practice).
6. **Correct, sourced and checked.** Every fact, formula and constant comes from a source you looked up for this job, not from memory. Every numeric answer is recomputed by a script. Wrong content is worse than none.
7. **Fun first.** In Stealth, learning beats take about 15–20% of play and put puzzles in no more than about a third of the scenes (the checker warns above 40%; Open style: no limit beyond the time share). Activity beats, where the world reacts to what the hero does and nobody asks a question, are free and are the better default (Open: up to about 40% of play). The rest is the adventure: characters, danger, choices. If every scene carries a lesson, you have written a syllabus. Cut objectives, or save the rest for a sequel.
8. **Hide the subject.** In Stealth the player can't tell what is being taught from the pitch, the names, the props or the scene dressing. Run three tests on the draft:
   - **The friend test.** Explain the plot to a friend without naming the subject. If you can't, the story is the lesson. Rewrite the story around a person, a want and a fear, and let the concept be the terrain they cross.
   - **The rename test.** If every invented noun maps to one real noun (the Glint is Bitcoin, the Gilded Tally is an exchange, the Ledger is the blockchain), you have a costume, not a world. Build a world with its own economy, craft or law that shares the *mechanism*, then let the mapping be discovered by playing.
   - **The glossary test.** No scene hands the player a definition. NPCs talk in the world's words, the way people do. Nobody explains what their own trade's word means to someone who lives there.
9. **Earn the real word.** The player meets the thing first, uses it, and only later learns what the real world calls it. See *Vocabulary* below.

## Step by step

### 1. Scope

Work out the course and level from the wish ("Physics I" = intro mechanics; "for my 10-year-old" = upper-primary maths), then choose **two to four objectives** for a one-shot, **three to six** over a few sessions, or up to **eight** across a campaign. Write each with a measurable verb and a context:

- Good: "Predict the fall time of a dropped object from its height, ignoring air resistance." "Explain why both carts move after a collision, using conservation of momentum."
- Weak: "Understand gravity." "Learn about momentum."

Order them so later ones build on earlier ones. For each, note the **misconception** it targets (for physics, the Force Concept Inventory literature names the classics: heavier things fall faster; motion needs a constant force; the bigger object pushes harder in a collision; zero velocity means zero acceleration).

### 2. Research

Find two or three authoritative, preferably open sources and record them in `teach.sources` with the objectives they cover:

- Open textbooks and courses: OpenStax (physics, chemistry, biology, maths, economics, history), LibreTexts, MIT OpenCourseWare, Khan Academy.
- Official curricula and standards when the user mentions a class (state standards, AP course descriptions, the national curriculum).
- Primary sources for history; reputable dictionaries and grammars for languages.

Use them for definitions, formulas, constants, worked examples and misconceptions. If sources disagree, use the one that matches the user's course level and say so in the Learning Guide.

### 3. Turn each concept into a mechanic

| Pattern | In play | Fits |
|---|---|---|
| **Predict and test** | Commit to a prediction, then the world shows the truth | Physics, chemistry, biology, probability |
| **Calculate to act** | The number decides an action: when to cut the rope, how much counterweight, how many rations | Maths, physics, chemistry, economics |
| **Explain to persuade** | An NPC (a sceptical guildmaster, a judge) only moves if the argument uses the concept correctly | History, science, ethics, economics |
| **Diagnose the fault** | Find what's wrong with a machine, a spell formula, a forged ledger, a liar's story | Engineering, programming, logic, accounting |
| **Decode and translate** | Runes, ciphers or a foreign tongue map to the target language or notation | Languages, notation, cryptography |
| **Classify and identify** | Sort reagents, creatures or artefacts by real properties to use them | Biology, chemistry, geology, art history |
| **Sequence and model** | Put a process in order or build a working model (an aqueduct, a trap, a treaty) | History, chemistry, engineering, civics |

**Physics I example map** (algebra-based mechanics):

| Concept | Adventure moment |
|---|---|
| Free fall, *h* = ½*gt*² | Count the seconds a stone takes to hit the bottom of a well to find its depth; time a drop to land on a moving cart |
| Projectile motion | Aim a catapult or a grappling line across a chasm; range at a given angle and speed |
| Newton's first and second laws | A sled on frictionless ice keeps sliding; how hard must the troll push to stop the cart (*F* = *ma*)? |
| Friction | Will the crate slide down the ramp? Coefficients on stone, ice and wood |
| Newton's third law | Push off a raft, recoil from a cannon; the misconception that the bigger body pushes harder |
| Work and energy | A pendulum blade's speed at the bottom from its height; a spring trap's stored energy |
| Momentum and collisions | A battering ram meets a door; two carts collide in the mine |
| Torque and levers | Balance the drawbridge, lift the portcullis with a lever, the seesaw lock |

**Beyond physics** (same patterns, other subjects):

| Subject and level | Adventure moment |
|---|---|
| Fractions (grade 3–5) | A candle clock burns in eighths; share a dragon's hoard fairly; a villain's "fair-share chart" cheats with bigger denominators |
| Ratios and percentages | Mix a potion at the right ratio; a merchant's "50% off then 50% more" |
| Chemistry (intro) | Balance a reaction to forge an alloy; acids and bases as rival guilds |
| History | Persuade a council using real causes of an event; spot the anachronism in a forged chronicle |
| A language | Ruins whose inscriptions are the target language; an NPC who only speaks it |
| Programming / logic | Golems that run instructions literally; debug the gate's rune sequence |

**Printable props help younger players**: fraction strips, pie circles, a number line, a candle or water clock to colour in. Put them in `handouts/` and tell the GM when to hand each out.

Keep the magic out of the concept's way. A world where magic changes how gravity works breaks the lesson unless you frame it as a deliberate contrast ("in the Fey realm, things fall upward; predict where").

### 3b. Disguise the subject (Stealth)

1. **Choose an analogy world, not a translation.** Ask what the *mechanism* looks like in a place where it grows naturally: guild debts and sealed registers for money systems, tides and ferries for logistics, a bell-tower for signals. The player should feel "oh, it works like that" only after they have used it. If the fantasy version has the same villains, the same jargon and the same twist as the news story, start again.
2. **Make the story about something else.** The engine is a person's want (an aunt's rent, a rival's pride, a missing friend), with the concept as the terrain, the tools and the traps. The subject is never the plot; it is how the plot is solved or lost.
3. **Spread the givens through the world.** A number the puzzle needs is on a board, in an overheard grumble, in a ledger the player has to ask to see. Not on a card handed over with the question. Don't announce a puzzle; pose a situation with a want and a cost.
4. **Allies give hints, in character.** The hint ladder is spoken by the companion or a mentor in their own voice, one rung at a time ("Is that the whole price, though?"), never as a line marked *Hint*.
5. **No reference card or glossary in the player's pre-play handouts.** Use in-world props instead: a price board, a ready-reckoner stamped with the guild's seal, a tutor's chalk notes. The pitch sells the story, the stakes and the tone. It doesn't define or even name the subject.

### Vocabulary: earn the real word

Real subject terms are what make a game feel like a lesson. Sort every important term into the `teach.lexicon` table in `campaign.json`:

| Kind | Meaning | Where it may appear |
|---|---|---|
| `jargon` | A textbook or professional term | Nowhere a player reads (read-aloud, handouts, pregens, found documents). GM-facing pages and the Decoder use it freely. |
| `slang` | A term people really say casually | Only inside quotation marks, spoken by a character who would say it (the very online sidekick, the scammer's pitch, a show-off rival). Never as narration, never defined in the scene. |
| *(not listed)* | The world's own word | Anywhere |

Each entry: `real` (the term), `world` (what the fiction says instead, or empty for slang that is simply used), `kind`, and `first_node` (where the player first meets the thing). In Stealth the checker fails when a `jargon` term, or a `slang` term outside quotation marks, shows up in player-facing text.

The **Decoder** is an appendix in the Learning Guide, one block per session or act: "what you did, and what it's called out there", written to the player in a friendly voice. It is **opt-in**: the GM offers it once at the end of a session, in one line, and gives it only if the player says yes. It is the only place the real vocabulary is gathered, so a player who wants the proper names can have them and a player who doesn't never feels taught.

### 4. Build each puzzle

Write it in `teach.puzzles` and in the book:

- **The situation in the world's words**, with every given number printed *somewhere the player can find it in the fiction* (a sign, an NPC's line, an item). In Open style a reference card is fine. In Stealth, scatter the givens (see 3b) and make sure none is only discoverable by luck. Units always. Givens that are *clues* go in `handouts/found/`, never in the player's own handouts.
- **The answer** exactly as the GM will see it, with units and an acceptable range (`tolerance`). Accept equivalent reasoning, not just one method.
- **A script** (`puzzles/pN_name.py`) that recomputes numeric answers from the printed givens. The checker runs it.
- **A three-rung hint ladder**: (1) a nudge to what matters ("what do you know about the bell?"), (2) the strategy ("which equation links distance and time from rest?"), (3) a worked step that still leaves the last step to them. A hint costs a little in the fiction (time, noise) or a roll can buy it. In Stealth, write each rung as a line an ally would say.
- **What happens in the fiction** on a right answer and on a wrong one (`in_world_consequence`), and how they can try again. Write it in two steps: a **soft** consequence for a first wrong answer (someone reacts, time passes, a small cost) followed by a retry, and the **full** consequence only when the player *acts on* a wrong answer (they sign the report, pull the lever, throw the float). Say so in the puzzle text, so a GM knows which one fires.
- **Common wrong answers**, each with a diagnostic question ("what unit does *g* × *t* come out in?"). These nudges point at the slip; they don't count as hint rungs and never contain the answer.
- **The worked solution** in the Learning Guide, step by step, in plain language.

Friendly numbers for younger players (*g* = 10 m/s², whole-number answers); realistic ones for older (*g* = 9.8 m/s², a calculator allowed). Say which in the reference card.

### 5. Assess in play

- **Practice** beats are low-stakes and repeatable.
- The **assessment** beat comes later and combines objectives in a new situation, ideally the climax ("the bridge is collapsing: where do you stand, and when do you jump?"). Success is visible in the fiction.
- **Open style:** in the Learning Guide, add a **debrief**, tagged by the beats each question needs ("after P2") so a GM can ask only what's been played (3–5 out-of-character questions for the end of each session: "what surprised you?", "explain to Pim why the bell and the anvil landed together") and an optional **check** (3–5 short questions, answers given) to run before and after.
- **Stealth style:** no out-of-character debrief and no check. Understanding shows up in the fiction: a character who wants to know asks the hero to explain the plan ("walk me through why you waited"), the world rewards or punishes the choice, and a later scene needs the idea again in a new disguise. The GM watches silently and logs on the Learning Tracker. The only out-of-character moment is the one-line Decoder offer at the end of a session.

### 6. Write the Learning Guide chapter

```markdown
# Learning Guide

## What this adventure teaches {#learning}
| Objective | Introduced | Practised | Assessed |
|---|---|---|---|
| LO1 Predict fall time from height | The Tilting Tower (N1) | The Drop Gallery (N2) | The Provost's Study (N4) |

## Running the lessons
How to pace them; when to give hints; accepting approximate answers; what to do if the player is stuck or races ahead.

## Puzzle solutions
### P1. The falling bell (N2)
Question, givens, worked solution, accepted range, hint ladder, common wrong answers and what they reveal.

## Misconceptions to listen for
"The anvil will land first": heavier-falls-faster. Don't correct in words; drop both.

## Lexicon
Every real term, the world's word for it, and where it may appear (see *Vocabulary*).

## Debrief questions (Open style)
## Before and after check (Open style, optional)
## Decoder (Stealth style)
One short block per session: what the player did, what it is really called, in a friendly voice.
## Sources
```

Put a short `lesson` box in the node itself wherever a beat happens, pointing to the full solution in the guide, so the GM sees it in the moment.

### 7. Check accuracy

- Every formula, constant, date and definition is traceable to `teach.sources`.
- Every numeric answer is recomputed by its script (the checker fails on a mismatch).
- Re-read each puzzle as a student: are all the givens printed? Is the question unambiguous? Could a correct but different method give a different answer? (Then widen the tolerance or tighten the question.)
- State simplifications out loud ("ignore air resistance", "treat the rope as massless") in the puzzle text and the reference card. In Stealth, say them in the world ("the tally-house rounds to the nearest whole mark") and put the real simplification in the Learning Guide.
- Run the **friend, rename and glossary tests** from principle 8 on the finished pitch, handouts and read-aloud. Re-read them *as the player who was never told the subject*.

## For a parent or tutor

The likeliest Teach-mode GM is a parent running it for their child. Write the Learning Guide for a non-teacher: what the idea is in one plain paragraph, what the child should be able to do by the end, the exact words for each hint, what a common wrong answer tells you, and "if they're tired or frustrated, end the scene on a win and come back to it". Keep sessions to 60–120 minutes for children.

## For a classroom

If the user is a teacher: add a one-page lesson plan to the Learning Guide (subject and standards, time, materials, group roles, how to run it with 4–6 players per table, assessment rubric, accommodations), keep sessions to class length, and include safety tools. Keep names and situations school-appropriate.

## For an AI GM

An AI GM has two instincts that spoil Teach mode: it solves the puzzle for the player, and it explains. Both turn a game into a tutorial. The [Foundry hand-off](foundry-handoff.md#3-teach-mode-rules-for-the-ai-gm) has the Table Rules lines and a *Learning Tracker* page that keep it honest: pose the situation in the world's words, wait, hint by the ladder through an ally, never give the answer first, accept answers within the printed range, never define a term in narration, and (Stealth) never mention lessons, puzzles or objectives. Open style adds the debrief at the end of each session.
