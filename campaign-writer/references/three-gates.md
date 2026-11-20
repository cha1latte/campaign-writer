# The gates

A campaign ships only when it passes every gate at **8.5 out of 10 or better**:

1. **Is it fun?**
2. **Is it D&D?** (or, for another system: does it play like a good session of *that* game?)
3. **Does it really teach what it set out to teach?** (Teach mode only)
4. **Is it easy to follow?** Breezy for the player at the table, beginner or not.

(The file keeps its old name, three-gates.md, so links still work.)

The gates are scored from the **player's chair**, not the author's: what the player sees, hears, decides and feels, minute by minute. A book that reads well but plays like homework fails. They sit on top of the part-by-part score sheet in [quality-bar.md](quality-bar.md): the score sheet asks "is this a well-made package?", the gates ask "will these people have a great time playing, and come away knowing the thing?" Both must pass.

Why they exist: a Teach campaign once passed every structural check and scored 8.5 or better on every part of the score sheet, and its real player quit after one session. Their words: too many words and money talk, didn't know what to do or why, not enough D&D, felt like school. Cold judges scored it Fun 3.6, D&D 3.7, Teaches 4.0. Nothing on the old score sheet could see that.

## How to score

0. **Calibrate the judges first** when the table has a real session log, above all one the player didn't enjoy. Score it cold with the same judges and rubric. If they don't rank the session the player hated clearly low, fix the rubric before trusting any simulated score. (In the run that added Gate 4, the scales were fine on real play; the earlier, too-high scores came from a simulation that was too polite.)
1. **Score a playthrough, never just the book.** Best: a real session (its chat log). Next best: a simulated session (below). A book-only score is capped at **7** on every gate: nobody knows yet how it plays.
2. **Score cold.** Each gate gets its own judge who didn't write the campaign and hasn't seen the author's reasoning: a subagent, a second model, a friend. Give them this file, the transcript and the GM book, and ask for one gate only. One judge looking hard at one thing finds what three glances miss.
3. **Every criterion 0 to 10, with evidence.** Quote the transcript line or name the book section. A criterion with no evidence scores 6 at most.
4. **Gate score = the average of its criteria, then the caps.** A cap is a hard ceiling: hit one and the gate can't pass, whatever the average.
5. **Fix at the root, then re-run.** Fix the lowest criterion first, in the design (the scene, the encounter, the beat), not by telling the GM to deliver it better. Re-run the playthrough for what changed and re-score with **fresh** judges. Repeat until every gate is 8.5+. Two or three rounds is normal.
6. **Never round up.** 8.4 is a fail.
7. **Real players overrule judges.** If the real player says it wasn't fun, it wasn't, whatever the scores said. Find the moment in their session log where it went wrong and score from that moment.

### Simulated playthrough

Two separate agents, so the player can't have read the book:

- **GM agent.** Gets the GM book for the session (plus the overview, NPC, bestiary and learning chapters) and **the real live setup**: the table rules as installed, the AI GM's own play rules (its skill or system prompt) and the campaign's runner guide. It runs the session the way the real GM (human or AI) will, *not* "faithfully, adding nothing": the real GM improvises when the player goes off the page, and that is where sessions break. Run the GM on the same model the real table uses. If the live setup enforces something (a reply-length cap, a hook), enforce it in the relay too.
- **Player agent.** Gets only what a player has: the pitch, the pre-play handouts, the character sheet, and a **player profile** written from the real player if you have one, built from their **latest** real session (how they talk, what they ask, what bores them, the off-book plans they reach for, the words they ask about, when they skip time, how much they already know of the subject). Never the book. It plays in character and, after every line, adds an honest bracketed feeling tag (`[OOC: lost, too many new words]`, `[OOC: laughing]`). For a Teach campaign it's a **beginner**: it may only use what the game has shown it, and reasons the way a newcomer does, wrong intuitions included.
- **Dice:** give each side a tray of real random numbers with every message. Models asked to "roll" don't.
- **Relay:** a small script passes messages between the two and writes the transcript to a file. Keep it out of any chat the real player can see.
- **Coverage:** at least the first session and the session with the heaviest lesson load, and every **assessed** moment (Teach): a gate can't pass on an objective nobody played. Sessions run long in play: one book session can take 80 exchanges.
- **Segment it, and watch the cost.** One relay that resends the whole book to a top model every turn is very expensive (a single session cost about $200 at API prices in the rework that produced this file). Keep **one persistent player agent** (so its learning carries over) and start a **fresh GM agent per segment** with only that chapter, the overview, NPCs, bestiary and Learning Guide, plus a short "story so far". A cheaper model is fine for both sides once the method works. Put a cost cap in the relay.
- **Beat checklist.** At the end of each segment ask the GM agent to list every Learning Guide beat it delivered, quoting its line, and every one it skipped. Judges then know whether a failure was the design or the GM dropping a line. (In testing, the GM agent dropped a required line, and the player got lost in exactly the place it would have helped.) A line the GM must never drop goes in read-aloud.
- **Debrief:** after each segment ask the player agent, out of character: what were you trying to do, did you always know what to do next, best and worst moment, fun and D&D out of 10, when were you lost or bored, did it feel like school. **Teach:** "Without using anything the game didn't show you, explain to a friend how this works."
- **Quiz, four ways (Teach).** A short real-world quiz on every objective, taken by: (1) a fresh beginner agent before any play, (2) a fresh agent that only reads the Decoder (the control), (3) the played agent before the Decoder, (4) the played agent after it. The bar is 80% for (4), clearly above (1) and (2). A model can't fully forget what it knows, so (1) runs high; the judge also checks that every right answer in (3) is backed by a moment in the transcript.

A simulated player is evidence, not proof. Say which you have. Three things learned the hard way:
- **It plateaus.** A model playing a player rates almost every scene about 8/10 whatever happens. Its numbers stop carrying information after the first round or two; read its feeling tags and debriefs for *what* worked and didn't.
- **Check coverage from the GM checklists, not your plan.** Segments run out of turns before their last scenes; an evidence index that says "played N12" when the run stopped at the door misleads every judge after it. List what was actually reached.
- **It can't clear the last half-point.** Simulation is good for finding and fixing design faults (it took a rebuilt campaign from about 4 to about 8 on every gate). The final call on fun, and on "it felt like school", belongs to the real player.

## Gate 1: Is it fun?

| # | Criterion | 10 looks like | 5 looks like |
|---|---|---|---|
| F1 | **Hook in five minutes** | The first scene is action, mystery or a person in trouble the hero cares about. By minute five the player has done something and wants something. | The hero arrives and is told things. The first "why" comes from an NPC's explanation. |
| F2 | **Always knows what to do and why** | At every scene's end the player can name a goal and a way to chase it without asking the GM. Goals come from people and danger, not from a job sheet. | The player asks "what am I supposed to do?", "who am I and why am I here?" or "what can I do from here?" more than once a session. |
| F3 | **The player drives** | Every scene hands the player a real choice with a visible result. NPCs react to the hero; the hero never watches an NPC do the interesting thing. | Scenes where an NPC demonstrates, explains or does the task while the hero watches. |
| F4 | **Light load** | At most one new invented word or system per scene, and only when the player needs it to act. Read-aloud under 90 words. Admin (shopping, sums, bookkeeping) under five minutes a session and always under pressure. | A pile of new terms in one scene; a bill to read; arithmetic before anything exciting has happened. |
| F5 | **Payoffs and surprise** | Clever play gets a visible, satisfying reward soon. At least one twist a session. Every session ends on a hook. Wins feel earned; losses feel fair. | Easy wins ("that was it?"), rewards that land as numbers on a page, no reversal. |
| F6 | **The hero matters** | The hero's backstory, companions and class features change scenes. Their people are in the story, in danger, or in the way. | The hero could be anyone; their companion is a tool; their class never comes up. |
| F7 | **Variety and pace** | Each session mixes danger, discovery, talk and laughs, with no stretch longer than about 20 minutes of one kind of scene. | One long run of talk-and-numbers, or one long run of corridors. |
| F8 | **The world pushes back** | NPCs and threats act on their own clock without waiting for the hero. The main danger stays visible and moves. The player feels time pressure inside the fiction, not from GM notes. | The world waits politely. The villain's big move happens in the background while the hero does something else. "Take your time, nothing will happen." |
| F9 | **The main line pulls** | The player chases the adventure because they want to. Detours are short, or cost something, and the main hook comes back to them in the fiction. | An improvised detour eats most of the session. The player asks "what should I do?" or skips time because nothing is pulling them. |

**Caps (any one caps Gate 1 at 6):** the first 15 minutes of session 1 explain how the world's systems work; the player (real or simulated) says they're lost, bored or overwhelmed and the book's design, not the GM's delivery, caused it; a required sum or form stands between the hero and the first exciting thing; the player skips time ("fast forward", "let a few days pass") twice or more with nothing at stake in between; the GM tells the player nothing will happen while they think.

## Gate 2: Is it D&D?

| # | Criterion | 10 looks like | 5 looks like |
|---|---|---|---|
| D1 | **The three pillars, every session** | Every session has real exploration (a place with secrets to poke at), combat that matters, and social play with stakes. The adventure is the main course. | One pillar carries a session; the rest is a non-D&D activity in costume. |
| D2 | **Danger is real** | Fights are budgeted for the **actual party** (hero, companions, sidekicks, class-feature combatants), and each session has at least one that could drop the hero if they play it badly. Traps and hazards cost something. Clever bypasses exist and are earned (a hard check, a resource, a risk), never free. | Fights built for one hero when the hero brings a steel defender or an animal companion; every guardian skipped by one easy check; "that was really easy". |
| D3 | **The class sheet gets used** | Scenes that reward the hero's class, subclass, tools, languages and companion: things only this hero could do, or do best. | Generic checks only; the hero's best tricks never come up. |
| D4 | **Treasure and growth** | Loot that's fun to find (magic items at the edition's rate, odd salvage, keys to other places), levels at the promised beats, power the player can feel. | Coin only, or rewards that are mostly numbers in a ledger. |
| D5 | **It feels like fantasy** | Dungeons, monsters acting on their lore, magic, ruins, rivals; people whose ancestry, faith and history show in what they do. A special system (a market, a court, a lab) sits inside a fantasy world, not instead of one. | A fantasy-costumed office, market or classroom; NPCs who are stock types with fantasy names. |
| D6 | **Rules hold up** | Stat blocks, DCs, budgets and rewards match the edition; the GM never has to invent a rule mid-scene to make the design work. Hidden things have DCs above the party's passive scores unless you want them found. | Missing DCs, wrong budgets, rules the GM must improvise. |
| D7 | **Honest difficulty for the player's own plans** | When the hero invents a plan, the real rules resolve it: the right checks, several steps for a big job (a skill challenge), real cost (spell slots, time, gold, HP), and a real chance to fail or to get a complication. Something NPCs called near-impossible stays hard. The book has an "off the page" box for the detours a player is likely to try. | A big invented plan succeeds on one check with no complication; a "season's work" is done in an afternoon; a ruling quietly removes the danger; an off-book job pays more than the main line. |
| D8 | **Rules used correctly** | Spells, rests, conditions, skills, DCs and companion rules match the edition as written. When the GM improvises a ruling, it's stated plainly, once, and is fair both ways. | Spells do more than they should (a cantrip used as a weapon), checks use the wrong ability, rests or prep skip their real cost, improvised rulings always favour the player or get reversed mid-scene. |

**Caps (any one caps Gate 2 at 6):** a session spends more than about 40% of its play time on something that isn't adventuring (trading, accounting, shopping, lectures); session 1 has no fight or real hazard in its first half; encounters were never re-budgeted after the party changed (a pet, a sidekick, a player's own character); any session (or a long scene, when scoring a stretch) with no fight AND no hazard that could actually cost the hero HP, resources or something they care about.

For another system, read "D&D" as that game: Gate 2 asks whether it plays like the game the table chose (investigation and dread in Call of Cthulhu, the three-action economy in Pathfinder), not like a different activity wearing its rules.

## Gate 3: Does it really teach what it set out to? (Teach mode)

| # | Criterion | 10 looks like | 5 looks like |
|---|---|---|---|
| T1 | **Learned by doing** | The player does the reasoning that matters: decides, predicts, argues, catches the lie. Arithmetic can be handed to a tool or a companion; the *choice of what to work out* stays with the player. | NPCs explain or demonstrate the idea; the player watches, or answers a quiz in costume. |
| T2 | **Shown before tested** | Each objective is met once, working, small, with nothing at stake, before any choice that costs something hangs on it. Every given is said plainly before the player commits. | The first contact is a test; key facts only come "if asked". |
| T3 | **Felt, not told** | The misconception behind each objective gets a moment where acting on it visibly hurts someone the player cares about (or tempts them hard), and the right idea visibly works. | Misconceptions corrected in an NPC's words. |
| T4 | **Comes back** | Each objective returns at least three times, in different situations, getting harder. | Met once, then never used again. |
| T5 | **True and transferable** | The allegory obeys the real mechanism ([allegory audit](teach-allegory-audit.md) done). The Decoder bridges every world word to the real one. A simulated beginner who read the Decoder scores at least 80% on a short real-world quiz, well above their score before playing. No invented word is a false friend for a different real term. | The world's version breaks the real rule; nothing ties it back to the real world; the quiz score barely moves. |
| T6 | **Invisible while it works** (Stealth) | The player never feels taught: no lesson talk, no "let me explain", no obvious question with a right answer. They'd describe the campaign by its plot. | "It felt like school"; the player names the lesson in the first hour. |

**Caps (any one caps Gate 3 at 6):** an objective has no assessed moment the player actually plays; the simulated quiz after the Decoder is under 70%; the real player said it felt like school.

**Show, don't pitch.** In a Teach campaign the "shown" beat for an objective is an event, not a speech: two otherwise identical things diverge in front of the player (the same coin under two keepers over a few winters), and the loss lands on someone they care about. Three NPCs explaining three systems back to back reads as school however short each line is.

**Is it the right subject?** Before scoring, check the objectives against the wish. A plot rule the story runs on (who controls a vote, how a lock works) is not automatically something the player asked to learn. If an objective is only there because the plot needs it, demote it to plot: state it plainly in play, let a companion do its sums, and don't assess it.

## Gate 4: Is it easy to follow?

Scored from the player's chair, as a beginner would sit in it. A game can be fun, real D&D and true, and still lose its player in a pile of names.

| # | Criterion | 10 looks like | 5 looks like |
|---|---|---|---|
| E1 | **Short replies** | Most GM replies read in under 30 seconds (about 120 words or less), one beat at a time, then the player acts. | Long blocks; several beats in one reply; the player has to read a wall before acting. |
| E2 | **One thing at a time** | New people and threads arrive one per beat. The player never has to track more than about three open threads. | Several arrivals in one reply; the player loses track of who wants what. |
| E3 | **Plain words** | New world words come one at a time, in plain English, only when the player needs them. Nothing assumes the player remembers names or jargon from an earlier session. | A pile of names, places and invented terms; old-session jargon assumed. |
| E4 | **No recap needed** | The player follows without asking "who is X / what is Y / remind me". The story itself carries the information. | Several "what's a ___ / who is ___ / remind me" questions; OOC recaps needed to keep going. |
| E5 | **Numbers are easy** | Any number is small, said once, plainly, in the same coin when two are compared; a companion can do the sums; the player only decides. | The player has to convert coins or do multi-step sums to follow what happened. |
| E6 | **Light out-of-character load** | OOC explanations and rulings are rare and short. | Frequent OOC lists, recaps, rulings and "where things stand" blocks. |

**Caps (any one caps Gate 4 at 6):** the player says they're confused, lost or overwhelmed; more than three "who/what is X / remind me" questions in the first hour of play.

**Design for it.** A scene introduces at most one new named person per beat; everyone else is "the crew", "the holders". Each returning name gets a few plain words the first time per session. A scene that carries a chase, a mystery and a lesson is three scenes. Written length rules alone don't hold an AI GM to short replies (in testing, 48 to 82% of replies ran long with the rule in its instructions): cut what the book asks the GM to say per beat, and enforce a cap in the live setup if you can.

## The fixes that usually move the needle

From the rework that produced this file, roughly in order of how much they moved the scores:

- **Open on a person in trouble**, tied to the hero's own backstory, with danger in the first ten minutes. Move the "how this world works" material after the first fight, and make most of it unnecessary.
- **Replace every NPC demonstration** with an event that happens to the hero (the price halves in front of them; the thief profits from their deed).
- **Cut the invented words** to the few that name things the player handles. Say everything else in plain English. Prices, sides of a trade and fees don't need fantasy names.
- **Give the arithmetic to a companion** and keep the decision with the player.
- **Re-budget for the real party**, put one fight per session that can't be skipped for free, and make every bypass cost something.
- **Write one class-spotlight moment per session**: a machine only an Artificer can fix, a lock for the rogue, a ward for the wizard.
- **Pay out loot, not ledger lines.**
- **Split an overstuffed scene.** One scene, one job: the chase, the mystery and the lesson each get their own.
- **Write "off the page" boxes** for the detours this player is likely to try (from their real sessions), with a skill challenge, a cost, honest pay and the clock still running.
- **Keep the clock visible in the fiction**: someone says the deadline out loud, and when it fires the hero sees it.

## The log

Keep `gates-log.md` in the package root: each round's three gate scores, every criterion with its evidence, the caps hit, what changed and why. End it with one line the checker reads:

```text
Final: Fun 8.7 / D&D 8.9 / Easy 8.6 / Teaches 8.6 (round 3, simulated playthrough of sessions 1-2; real play: not yet)
```

Use `Teaches n/a` for a standard campaign. `Easy` is required for every campaign. The README's *Scores* table gets a row per gate with the final number and what it rests on (real play, simulated, or book only).
