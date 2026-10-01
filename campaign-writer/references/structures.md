# Structures, engines and clues

Reviewers praise adventures with great locations, freedom inside a clear goal, and NPCs with conflicting motives. They complain about linear railroads, twists that weren't earned, "mysteries" with no detective work, and adventures that are padded or rushed for their length. Design against that list.

## 1. Pick a structure

| Wish sounds like | Structure | Shape in `campaign.json` |
|---|---|---|
| "a one-shot", "a quick adventure", a convention game | **Five-scene one-shot**: hook, obstacle, twist or complication, climax, aftermath | 5–7 nodes, mostly `leads_to`, one optional side node |
| "hunt", "track", "explore the wilds", "survive the winter" | **Pointcrawl with a clock**: a map of places joined by paths; the quarry or threat moves on a schedule | 6–10 nodes, `structure: "pointcrawl"`, clues pointing to the lair, a travel-time pointcrawl map |
| "mystery", "who killed", "investigate", "heist planning" | **Node-based**: places, people and events that each hold clues to the others; the solution is a conclusion | `structure: "node"`, conclusions with three clues each, several entry points |
| "dungeon", "tomb", "the old mine" | **Keyed location**: a map with numbered areas, loops and more than one way to the goal | Nodes per area or area group, a dungeon map, `structure: "dungeon"` |
| "campaign", "a few sessions", "an arc" | **Linked adventures under a front**: 3–5 adventures, each one of the above, tied together by one threat that escalates between them | One node per adventure's main beats; the threat's timeline as a clock |
| "sandbox", "let me roam", "open world" | **Small sandbox**: 6–12 sites, 3 factions, rumours that point between sites | `structure: "sandbox"`, clues as rumours |

Keep loops and choices even in linear shapes: two ways into the climax, a side node that pays off later, an optional ally.

## 2. Find the engine

Every adventure runs on these five. Write them in `book/01-overview.md` under *What's really going on*:

1. **Want.** What the antagonist (a person, a monster, a disaster) is trying to achieve, in one sentence.
2. **Obstacle.** Why they can't just have it, and why that puts them in the heroes' path.
3. **Clock.** What happens next if nobody interferes, in 3–6 steps with triggers ("Day 2: the trolls take the mill. Day 4: they cross the bridge"). The clock is how the world moves when the players don't.
4. **Choice.** A real decision near the end with no right answer: spare the troll mother or end the line, save the town or the prisoners, keep the artifact or destroy it.
5. **Hook.** Why the heroes care today. Give three: one personal, one paid, one moral. For a solo hero, tie at least one to that character's own sheet or background if you have it.

**Make the antagonist a person, even if it's a monster.** It wants something, fears something, and changes plans when the heroes hurt it. Monsters that regenerate, hunt, retreat and lay traps are more fun than monsters that wait in room 7.

**Twists must be earned.** If there's a reveal, plant three clues before it, and make sure the story still works for a group that guesses early. Avoid the stock reveals (the quest-giver was the villain, it was all a dream, the mentor dies to motivate you) unless you can make them surprising *and* fair.

## 3. Clues and information

- **Three Clue Rule.** For every conclusion the players must reach, include at least three clues in at least two places. Players miss clues; three gives them a fair chance.
- **Node-based design.** In a mystery or pointcrawl, every place should point to at least two other places, and every place reached only by clues needs three clues pointing to it. That's how you avoid dead ends without railroading.
- **Clues are things, not rolls.** "A muddy boot print, too big for a human, pointing toward the fen" is a clue. "Make an Investigation check" is a way to find one. A failed roll should cost time or attract attention, not lose the clue: give the information and make it cost something.
- **Write clues as GM-ready lines** in the book: *what they find → what it means → where it points*.
- **Say when a conclusion counts as proved** ("any two of these four clues prove C1") and what changes in the world when it is (the Council delays its vote, the villain moves early). An AI GM can't run the consequences of a fact it doesn't know is established.

In `campaign.json`, a clue `points_to` either a node (a place to go) or a conclusion (a fact to work out). The checker counts them.

## 4. Encounters with purpose

Every fight, trap or social challenge should change something: reveal a clue, cost a resource, show the threat, or force a choice. Give each one:

- **Why it's here** and **what the enemy wants** (most enemies want to win cheaply, not to die). Morale: when they flee, surrender or bargain.
- **Terrain** that matters (ice, a ledge, a rope bridge, a fire).
- **A way to avoid or end it** without killing everyone (stealth, talk, trickery, a deal), unless the fiction truly allows none.
- **Scaling notes** for a weaker or stronger party.
- **Difficulty from the system's own maths** (see the system files). Mix difficulties across a session: mostly low and moderate, one high at the climax.

## 5. Pace sessions

For each session, aim for: a strong start that's already in motion, two or three scenes, one fight or tense challenge, one decision, and a cliffhanger or a satisfying stop. Mark session breaks in the book (`### Ending the session here`), with a one-paragraph recap the GM can read out next time.

## 6. Endings

Write at least three in *Endings*: **success**, **partial** (they win at a cost), and **failure-forward** (they lose, and the world changes in a way that's still fun to play: the town falls but the survivors rally, the troll king gets his bridge but now owes you). Then *What's next*: two hooks for further adventures.

## 7. Solo design (one player)

- **Agency carries the game.** The hero needs a reason to act alone, or an NPC companion who's useful but never the star (they don't solve puzzles or land the killing blow).
- **Encounters as puzzles.** A lone character dies to action economy. Prefer fewer, smarter enemies; terrain, tricks and preparation that let one hero win; and enemies that capture, bargain or retreat instead of killing.
- **Set lethality explicitly** in the running guide: what happens at 0 HP (captured, rescued, wakes at the river's edge with a cost) so the GM never has to choose between killing the only player and cheating.
- **Rest and healing.** Give safe places to recover, and potions or a healer companion on the map.
- **GM-less play** (no GM at all): add an oracle table (yes/no with "and/but" results), random-event tables per location and clear "if you do X, turn to Y" guidance. Make sure clue placement still works without a GM to improvise.

## 8. Campaigns

A campaign is a front: one threat, its escalating clock across adventures, and 3–5 adventures that each resolve something while the big threat grows. Each adventure gets its own nodes, encounters and ending, and a *Between adventures* section: what changed, what the villain does next, downtime and levelling. Level up at milestones you name ("after the bridge falls, reach level 4").
