# Writing NPCs: people, not plot parts

A card that says only what an NPC wants, knows and hides tells the GM what the character *does for the plot*. It doesn't say who they are, so at the table they come out as a type: the gruff dwarf, the nervous scholar, the kindly grandmother. This file is how to get from a plot part to a person: one the players remember, who sounds like nobody else, and who could only exist in this world.

Do it in two places: in `campaign.json` while designing (the fields below), and in the NPC chapter while writing (the card format at the end).

## 1. Major and minor

- **Major NPCs** carry scenes: anyone in two or more nodes, every antagonist, every companion, anyone the hero must talk round. Give them the full person pass (section 2). Mark them `"major": true`.
- **Minor NPCs** pass through: a ferryman, a guard, a witness. Give them a name, an ancestry, one want, **one specific detail** (an object, a habit, a wound, a joke) and one line. Two sentences on the page is plenty.

Depth comes from specifics, not length. A major card is about 120-200 words, not a page of backstory.

## 2. The person pass (major NPCs)

Answer each of these in one concrete sentence. If a sentence would fit any NPC in any adventure, it's not done yet.

| Field | The question | Weak | Strong |
|---|---|---|---|
| `life` | What were they doing on an ordinary day before the heroes arrived: work, place, routine? | "Runs the inn." | "Opens the tally-house at first bell, counts barges until noon, then naps in the toll-booth with the door wedged." |
| `loves` | What do they care about that isn't the plot: a person, a thing, a habit, a place? | "Her family." | "A bad-tempered goat called Second Opinion, and the smell of new paper." |
| `contradiction` | Which two true things about them pull against each other? | "Brave but scared." | "Believes every debt must be paid, and has been quietly forgiving the poorest families' tolls for six years." |
| `lore` | What concrete piece of this world's lore shapes them: their people's history, their faith, a creature's nature? (See [dnd-lore.md](dnd-lore.md).) | "She's a dwarf." | "Dwarves keep records and grudges and live about 350 years; she's older than the town, and her clan's grudge-book names the giants whose bones lie in the ford." |
| `lore`, all-human casts | In a cast of one people, the lore comes from region, trade, faith and local belief, not the species tag. "Human" alone is not lore. | "She's human." | "Harbour law says a search lasts three tides; she called it after one, and everyone in the village knows it." |
| `ties` | Who else in this adventure do they have **history** with, and what happened? | "Knows the mayor." | "Taught the reeve to read when he was a stable boy; he repays her by never auditing her books." |
| `without_heroes` | What will they do if nobody steps in? | "Waits for help." | "On the third night she pays the bandits' toll out of the forgiven money and ruins herself." |
| `wants` / `knows` / `secret` | As before: a goal, what they can tell, what they won't. | | |

**The trope test.** Write `trope`: the stock character this NPC is closest to ("gruff dwarf", "corrupt official", "wise old mentor"). Then write `twist`: at least two changes that show up **at the table**, in what they want, what they do under pressure, or how they talk. Changing a hat or a hair colour doesn't count. If you can't name a trope, it may be fine; if you can, and the twist is cosmetic, rework the NPC. Apply it hardest to the NPC at the centre of the plot: the plot leans on their type (the grieving father, the scheming vizier), so they're the one most likely to stay stock. Keep the type's plot job and change the person doing it.

**Ties make a cast.** Every major NPC has at least one `ties` entry pointing at another NPC (`"npc": "P3"`). A web of old favours, grudges and debts is what makes a village feel lived in, and it gives the players levers the plot didn't plan for.

**Let them be wrong, and let them change.** People believe things that aren't true, want two incompatible things, and change their minds when something happens to them. Write at least one belief a major NPC holds that the adventure can prove wrong, and what they do when it is (optional field `wrong_about`).

**Don't make everyone nice or everyone suspicious.** A cast needs people the heroes like who are no help, people who are useful and unpleasant, and at least one who simply doesn't care about the plot.

## 3. Names

Most generated names come from the same small shelf. Players notice when the third campaign in a row has a Tamsin. Do this before naming anyone:

1. **Decide how each people in the setting names itself**, and write it in `campaign.json` under `naming` (one entry per people or region: `people`, `style`, `sounds`). Example: `{"people": "river-town humans", "style": "short given name + the parent's trade", "sounds": "soft consonants, -an/-el endings"}`. Two regions of humans should not sound alike. Follow [dnd-lore.md](dnd-lore.md) for the species conventions.
2. **Make up names from the rule**; don't pick them from a list. Every example name in this skill is an example of a rule, not a name to reuse.
3. **Reject a name if:** it's on the overused list below; it already belongs to an NPC in another campaign in the same folder (the checker looks); it shares its first three letters with another NPC in this adventure (Cadrin and Cadric blur together at the table); or it's a famous name from a published setting in a package meant to be shared.
4. **Let names carry story:** a nickname the town uses, a title they earned or lost, a name a mortal can't pronounce and has mangled, a name they changed.

**Overused names** (the checker warns on these; avoid them unless the user asks): Elara, Lyra, Kael, Thorne, Seraphina, Aldric, Elowen, Vex, Silas, Zephyr, Isolde, Ysolde, Tamsin, Odile, Osric, Pell, Wick, Hesketh, Jory, Brask, Fisk, Quill, Ashby, Hale, Dunmore, Ambrose, Oriel, Morwen, Corvin, Rowan.

Intentional reuse is fine: a sequel that brings back its cast sets `"series"` to the same value in both packages, and the checker stops warning between them.

## 4. The card in the book

The NPC chapter turns the fields into a card a GM can read mid-scene. The person pass doesn't all go on the card: `life`, `loves` and `contradiction` become two or three sentences of description; the rest stays in `campaign.json` unless a GM needs it in play.

**Card layout, one field per line, in this order**, so a GM finds each thing in the same place on every card:

1. *Italic look* (ancestry, age, one thing you'd notice), then two or three sentences of life, love and contradiction.
2. **Voice:** and **Lines:** (rhythm, then two or three things they'd say in different moods, so a GM hears the voice and not one catchphrase; a voice habit should show in at least one line).
3. **Wants:**
4. **Knows:** (with → links to the clues and nodes it feeds)
5. **Hides:**
6. **If pushed:** what they do when cornered, and the line they say when they break. This is the line a GM needs most at the climax; never drop it from a major NPC. For a monster or caster, say how its signature abilities show up when it's pushed (when the disguise drops, what it uses on whom).
7. **Ties:** history with another NPC in the cast.
8. **Wrong about:** (optional) a belief the adventure can prove false, and what they do when it is.
9. **If nobody comes:** what they'll do if the heroes don't step in.

Never run Wants, Knows and Hides together on one line: a GM scanning mid-scene misses whatever is in the middle.

**Every card reads on its own.** A GM opens the NPC chapter mid-scene, not the chapter where a detail was set up. Anything a card mentions that isn't explained on the card (a person, an object, an event, a custom) gets a few words of what it is or a → link to where it is: "the dropped shutters (→ **N3**)", "Sennen, the net-mender". If neither fits, cut it.

Use these as patterns for **shape and specificity only**. Don't reuse their names, phrases or details; the checker flags phrases copied from this skill's examples.

```markdown
### Hulda Slagmantle, keeper of the tally-house {#hulda}

*Dwarf, two hundred and twelve, ink under every nail, a brass hearing-horn she claims is for show.* Counts barges at Durrow Ford from first bell to noon, then naps in the toll-booth with the door wedged. Keeps a goat called Second Opinion. Every evening she rewrites one page of her clan's grudge-book from memory, because the original burned.
**Voice:** answers a question with the date it was last asked; wants everything in writing. **Lines:** "Write it down and I'll believe you. Say it and I'll only remember you said it." / "Third of Thawmonth, you asked me that. I said no then too." / "Sit. The goat doesn't bite. Much."
**Wants:** the bandits gone without the town learning what she's done.
**Knows:** every barge's cargo for forty years, and which ones stopped coming (→ **C2**).
**Hides:** for six years she's forgiven the poorest families' tolls, a debt she'd call theft in anyone else.
**If pushed:** produces a ledger for everything except the forgiven tolls; shown one of the families, she closes the book. "I wrote every one of them down. I just never added them up."
**Ties:** taught Reeve Ambo to read (→ **ambo**); he has never audited her books.
**If nobody comes:** on the third night she pays the bandits from the forgiven money and ruins herself.
```

```markdown
### Uzka, the hedge-priest at the crossroads shrine {#uzka}

*Orc, about thirty, a grey cloak patched with twelve different cloths, one for each family who gave her one.* She was raised on stories of the One-Eyed's call and is still waiting to hear it. Meanwhile she tends a roadside shrine to the harvest saint the farmers pray to, because somebody has to.
**Voice:** blunt, kind, says the worst thing first and the comfort second. **Lines:** "Your brother's dead. Sit down; I've got soup." / "Pray if you like. I'll keep digging." / "That's not a sign. That's a crow."
**Wants:** a sign, any sign, that she's where she's meant to be.
**Knows:** who has been leaving offerings at night, and that the offerings are stolen (→ **N4**).
**Hides:** she has started answering the farmers' prayers herself, with her own coin.
**If pushed:** lies badly, then laughs at herself. "Fine. The saint's been a bit short. I've been covering."
**Ties:** the miller's daughter is the only one who knows, and is blackmailing her gently, for apples.
**Wrong about:** thinks a god's call would be loud. When the heroes need her, she has to decide whether that counts.
**If nobody comes:** she follows the thief into the marsh alone, sure this is the call.
```

```markdown
**Ilo Bastide**, nine, human, the ferry-boy. Wants a real knife. Keeps a dead beetle in a matchbox and introduces it to strangers. "Say hello to Captain."
```

**Voice notes are seasoning.** Write "says X a lot", never "says X every sentence" or "after everything": an AI GM obeys that literally and the NPC turns into a caricature. The sample line shows rhythm; it isn't a script.

## 5. Check yourself

Before moving on, read the cast list top to bottom and ask:

- Could two of these NPCs swap names without anyone noticing? Then one of them isn't a person yet.
- Does every major NPC have a contradiction, a tie with history, and a piece of real lore that changes what they do?
- Is any of them only there to give a quest, explain something, or be rescued? Give them a want of their own that isn't about the heroes.
- Do the voices differ in rhythm and word choice, not just accent?
- Are the names from the naming rules in `campaign.json`, none on the overused list, none shared with another campaign?
- **Does every new detail agree with the rest of the book?** Each person, object or event you add to deepen an NPC (a whistle, a son, an old wreck) must match what the other chapters already say. Search the book for it. A son who is the wrong age, an object that belongs to someone else, or a reference to a person who never appears trips a GM mid-scene.
- **Does every thread you add go somewhere?** A detail a GM will be asked about (a second son, an object someone wants back, an old debt) needs one more clause saying where it leads, or it goes. Check timelines too: when you write "one more night" or "since the wreck", count the nights against the adventure's clock.
- **Is each secret still secret?** If a custom or event you added would make the village know the "hidden" thing, change one of them.
- Does every major card still carry **If pushed** with the line they say when they break?
