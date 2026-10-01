# Teach mode

"Teach me Physics I through D&D." The adventure has to be fun on its own *and* leave the player able to do something they couldn't do before. Get either half wrong and it fails: a quiz with dice is homework, and a romp with a physics word in it teaches nothing.

## The principles

1. **The concept is the verb.** Players succeed *by using the idea*: predicting where the boulder lands, timing the rope cut, balancing the drawbridge. Educational games that build the content into the core mechanic teach more than ones that bolt quiz questions onto play (Habgood & Ainsworth's "intrinsic integration" studies; the bolted-on kind is nicknamed "chocolate-covered broccoli"). If a puzzle would work the same with the subject swapped for trivia, redesign it.
2. **Dice never replace thinking.** A roll can buy a hint, save time or soften a mistake. It never produces the answer. An Intelligence check can reveal the next hint rung; the player still does the reasoning.
3. **Predict, then watch, then explain.** Misconceptions survive lectures and die to surprises. Have the player commit to a prediction, show the world doing the real thing, then ask why. This is the core loop for any concept with a common wrong intuition.
4. **Mistakes cost something in the fiction, never the game.** A wrong answer cracks the floor, wakes the guard or costs an hour. It never kills the character or locks the adventure. Every puzzle has a way forward after a miss, often a second attempt with what they learned.
5. **Little and often.** Each objective appears at least three times: introduced, practised, assessed, ideally in different sessions and mixed with older ideas (spaced and interleaved practice).
6. **Correct, sourced and checked.** Every fact, formula and constant comes from a source you looked up for this job, not from memory. Every numeric answer is recomputed by a script. Wrong content is worse than none.
7. **Fun first.** Learning beats take at most about 40% of play. The rest is the adventure: characters, danger, choices.

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

### 4. Build each puzzle

Write it in `teach.puzzles` and in the book:

- **The question in the world's words**, with every given number printed where the player can see it (a sign, an NPC's line, the reference card). Units always. Givens that are *clues* go in `handouts/found/`, never in the player's own handouts.
- **The answer** exactly as the GM will see it, with units and an acceptable range (`tolerance`). Accept equivalent reasoning, not just one method.
- **A script** (`puzzles/pN_name.py`) that recomputes numeric answers from the printed givens. The checker runs it.
- **A three-rung hint ladder**: (1) a nudge to what matters ("what do you know about the bell?"), (2) the strategy ("which equation links distance and time from rest?"), (3) a worked step that still leaves the last step to them. A hint costs a little in the fiction (time, noise) or a roll can buy it.
- **What happens in the fiction** on a right answer and on a wrong one (`in_world_consequence`), and how they can try again. Write it in two steps: a **soft** consequence for a first wrong answer (someone reacts, time passes, a small cost) followed by a retry, and the **full** consequence only when the player *acts on* a wrong answer (they sign the report, pull the lever, throw the float). Say so in the puzzle text, so a GM knows which one fires.
- **Common wrong answers**, each with a diagnostic question ("what unit does *g* × *t* come out in?"). These nudges point at the slip; they don't count as hint rungs and never contain the answer.
- **The worked solution** in the Learning Guide, step by step, in plain language.

Friendly numbers for younger players (*g* = 10 m/s², whole-number answers); realistic ones for older (*g* = 9.8 m/s², a calculator allowed). Say which in the reference card.

### 5. Assess in play

- **Practice** beats are low-stakes and repeatable.
- The **assessment** beat comes later and combines objectives in a new situation, ideally the climax ("the bridge is collapsing: where do you stand, and when do you jump?"). Success is visible in the fiction.
- In the Learning Guide, add a **debrief**, tagged by the beats each question needs ("after P2") so a GM can ask only what's been played (3–5 out-of-character questions for the end of each session: "what surprised you?", "explain to Pim why the bell and the anvil landed together") and an optional **check** (3–5 short questions, answers given) to run before and after.

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

## Debrief questions
## Before and after check (optional)
## Sources
```

Put a short `lesson` box in the node itself wherever a beat happens, pointing to the full solution in the guide, so the GM sees it in the moment.

### 7. Check accuracy

- Every formula, constant, date and definition is traceable to `teach.sources`.
- Every numeric answer is recomputed by its script (the checker fails on a mismatch).
- Re-read each puzzle as a student: are all the givens printed? Is the question unambiguous? Could a correct but different method give a different answer? (Then widen the tolerance or tighten the question.)
- State simplifications out loud ("ignore air resistance", "treat the rope as massless") in the puzzle text and the reference card.

## For a parent or tutor

The likeliest Teach-mode GM is a parent running it for their child. Write the Learning Guide for a non-teacher: what the idea is in one plain paragraph, what the child should be able to do by the end, the exact words for each hint, what a common wrong answer tells you, and "if they're tired or frustrated, end the scene on a win and come back to it". Keep sessions to 60–120 minutes for children.

## For a classroom

If the user is a teacher: add a one-page lesson plan to the Learning Guide (subject and standards, time, materials, group roles, how to run it with 4–6 players per table, assessment rubric, accommodations), keep sessions to class length, and include safety tools. Keep names and situations school-appropriate.

## For an AI GM

An AI GM will happily solve the puzzle for the player unless told not to. The [Foundry hand-off](foundry-handoff.md#3-teach-mode-rules-for-the-ai-gm) has the Table Rules lines and a *Learning Tracker* page that keep it honest: ask, wait, hint by the ladder, never give the answer first, accept answers within the printed range, and debrief at the end of each session.
