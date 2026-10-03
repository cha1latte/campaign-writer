# Teach mode: the allegory audit

In Stealth Teach mode the subject wears a costume: a world whose trade, law or craft works the way the real thing works. The checker keeps the real words out of the player's text. It can't tell when the costume quietly breaks the real mechanism, and that happens more often than wrong answers do: the puzzle teaches the idea correctly while the props, institutions and timings around it teach something false. Players learn from the scenery as much as from the puzzles, so a wrong prop is a wrong lesson.

This audit catches that. It is about meaning, so you do it by reading, not by running a script.

**When:** every Teach package whose world stands in for the subject (every Stealth package, and any Open one built on an analogy world). Sketch the model with the bones, then walk the package against it after the chapters, handouts, pregens and maps are drafted and before the build.

## 1. Write the model

One entry in `teach.model` for every real thing or role the story leans on: the thing that moves, **and** the places it starts and ends (the endpoints, the users) and every institution that touches it. Missing endpoints are the commonest gap, and they surface later as merged roles. Answer four questions about the **real** thing, not the fictional one:

| Field | The question |
|---|---|
| `real` | What is the real thing or role? |
| `world` | What stands in for it? One in-world owner per real role |
| `is` | What kind of thing is it: an object, a record, a quantity, a relationship, a role, a process? |
| `lives` | Where does it exist? |
| `changed_by` | Who or what can change it, and who can't? |
| `moves` | How does it move, or how is a change authorised? |
| `if_asked` | One to three in-character lines a character says if a player asks how it works (see class 4) |
| `bends` | The deliberate simplification, if any (see class 6) |

The model is one-to-one on purpose, and that doesn't fail the [rename test](teach-mode.md): the rename test is about the surface (every invented noun is a thin label for a real brand or term, in a world with nothing else in it). The model is about the mechanism, inside a world that has its own people, trade and trouble.

The checker requires `real`, `world`, `is`, `lives`, `changed_by` and `moves` in Stealth (in `--bones` a missing field is only a warning, so a sketch passes), warns when an entry has no `if_asked` line or two entries share an owner, checks that every `if_asked` line is in the book, and warns when the package has no `allegory-audit.md` log. It can't check that the story obeys the model. That is the walk.

```json
{"teach": {"model": [
  {"real": "electric charge in a circuit", "world": "the water in the Lockhouse pipes",
   "is": "a substance already filling the whole loop; the lamps use its push, not the water itself",
   "lives": "inside the closed pipes, all the way round",
   "changed_by": "nobody adds or removes water; the pump only pushes it",
   "moves": "drifts slowly round the loop, while the push reaches the far end almost at once",
   "if_asked": ["\"The pipes are always full, love. Push at one end and the far end spills at once. The water you pushed won't get there till Tuesday.\""],
   "bends": "Real charge drifts through a wire at a fraction of a millimetre per second; the pipes show the idea, not the speed."},
  {"real": "a battery", "world": "the treadmill pump",
   "is": "a source of push (energy per unit of charge), not a store of water",
   "lives": "in the loop, at one place",
   "changed_by": "whoever walks the treadmill; it slows as they tire",
   "moves": "it doesn't move; it raises the pressure of water passing through it",
   "if_asked": ["\"The pump doesn't make water. It makes the water want to go somewhere.\""]}
]}}
```

## 2. Walk the package against the model

Re-read the actual files, not your memory of them: every scene (read-aloud and GM text), every NPC's job, every item, treasure and piece of pregen gear, every handout and found document, every puzzle's givens and every ending. Wherever a modelled thing appears, ask the four questions. Is it treated as what it **is**? Is it where it **lives**? Does only its **changed_by** change it? Does it **move** the way the real thing moves?

Plenty of what the walk finds is a plain mechanism error that fits none of the classes below (the thing moves wrong, a lesson box gets the order of steps wrong). Fix those too and log them as *mechanism*.

Also check **the world's own words**: a world word reused in another sense (the word for the network's address also used for a scratch on a coin) teaches the wrong meaning. Give the other sense a different word.

Fix failures in the story, not in a footnote. The Decoder may explain a deliberate simplification, never an accident. Keep a short log at `allegory-audit.md` in the package root (GM-only, not built into any PDF): each finding with its class, where it was and the fix, plus what you deliberately left as a simplification. Put the count in the hand-over's *Verified* line. Re-walk the parts you touch whenever a later edit changes a modelled thing.

## 3. The six failure classes

### 1. The abstract thing becomes a prop

**Rule:** if the real thing is a record, a quantity or a relationship, it never appears as an object someone can carry, hide or hand over. The only physical props allowed are what holds it or grants access to it: a key, a seal, a password, a wound spring, a raised weight.

**Example (physics, energy).** In a mill town the Heft stands in for energy. *Wrong:* a thief runs off with "a jar of Heft" drawn from the millrace. That teaches energy as a fluid you can bottle, the mistake of the old caloric theory of heat. *Fixed:* the thief lets the mill's counterweights down in the night, or steals the wound mainspring. Heft is only ever *in* something: a raised weight, a spinning wheel, a hot kettle.

### 2. Two real roles merged into one owner

**Rule:** map every real role to its own in-world owner, and let each owner do only what its real counterpart can do. If one institution starts doing a second job because the plot needs it, the plot needs a second institution. The exception is a real counterpart that really does hold several roles (a big organisation that runs two of the services itself): then keep them in one institution, with a different desk or person for each job, and let each desk do only its own.

**Example (biology, immunity).** The Wall Wardens stand in for skin and mucous membranes. *Wrong:* in act two the same Wardens chase a spy through the alleys and keep a book of every face they have seen. Barriers block; they don't hunt intruders inside the body or remember them. *Fixed:* the Wardens only turn strangers away at the gate; the Lamplighters (the white cells that hunt) chase whatever gets in; the Portrait Hall (memory cells) remembers faces. The chase now needs the Lamplighters, which also gives the story a second faction to deal with.

### 3. Puzzle givens the backstory couldn't produce

**Rule:** trace every puzzle's givens back through the backstory, run the real mechanism forward from what happened, and make sure the numbers on the page are the numbers it produces. The puzzle script should start from the backstory's numbers, not from the handout.

**Example (physics, momentum).** Backstory: a runaway 400 kg ore cart rolling at 3 m/s hit a parked 200 kg cart and the two coupled. *Wrong:* the foreman's chalk log, a found handout, says "both rolled on together at 3 m/s". Momentum gives 400 × 3 = 600 × *v*, so *v* = 2 m/s. A player who checks the log against what they've learned either decides the rule is wrong or decides the foreman is lying, and neither is what you meant. *Fixed:* the log says 2 m/s. If you *want* a lying log, make the lie a clue, say so in the GM text, and make sure the real figure is findable.

### 4. No answer to "how does that work here?"

**Rule:** for each core mechanism, write one to three short in-character lines a character would say if a player asks how it works. They are answers, not exposition: nobody volunteers them, they are never read-aloud, and they use the world's words. Put them in `teach.model[].if_asked` and in the Learning Guide under *If asked*.

**Example (physics, circuits).** The Lockhouse pipes above. A curious player asks: "If the water crawls, why does the lamp across town light the moment the sluice opens?" With no line ready, the GM either says "magic" (and the model breaks) or explains with real jargon (and the disguise breaks). With one, the lock-keeper answers in a breath: "The pipes are always full, love. Push at one end and the far end spills at once."

### 5. Timing that suits the plot and teaches the wrong lesson

**Rule:** every delay, grace period or deadline either has a believable in-world reason that matches the real behaviour, or it goes. If you kept a timing that bends reality, the Decoder says what really happens. If the fixed timing already *is* the real behaviour, a Decoder line is optional (it often makes a good one).

**Example (biology, infection).** The plot needs a week for the heroes to investigate. *Wrong:* invaders slip into the city and sit unnoticed for seven quiet days, then the alarm sounds. The body's first defenders react within hours (fever, swelling); what takes days is a specific response to a germ it has never met. *Fixed:* the week is loud. The Lamplighters fight in the streets from the first night while the Portrait Hall slowly draws the invader's face, and the heroes' week *is* that lag. Decoder: "Your first defenders start within hours. A targeted response to something new takes one to two weeks to build; the second time, it comes much faster."

### 6. Simplifications nobody flags

**Rule:** every deliberate simplification goes in the Decoder under a short *Where the story bends* block, one line each: what the story does, and what is really true. A simplification nobody names becomes a fact the player believes. Look for convenient labels, instant signals, missing friction or drag, and anything that pauses when the plot doesn't need it.

**Example (physics, motion).**

```text
Where the story bends
- Arrows here fly with no air drag. Real ones fall short of the textbook range, more so the faster they go.
- The Fall pulls the same on every tower and in every cellar. Really it weakens with height, too little to notice on a tower.
- Across the valley you see the cannon flash and hear the boom together. Real sound takes about three seconds to cross a kilometre.
```

## After the audit

- `teach.model` matches what the book now says, and `allegory-audit.md` lists every finding.
- The Learning Guide has an *If asked* section with every `if_asked` line, by mechanism.
- The Decoder ends with *Where the story bends*.
- Re-run the checker: the lexicon check catches jargon a fix may have let in.
