# Rooting a D&D adventure in D&D

For D&D (any edition), the adventure should read as if it belongs in the game: creatures act the way their lore says, people carry their people's history, and names sound like the folk they belong to. A kobold called Bartholomew or a dwarf called Gwendolyn breaks the spell before anyone has rolled a die. So does a dwarf who could be a human with a beard.

Use this file while writing the NPC list in `campaign.json` (the `lore` field, see [npcs.md](npcs.md)) and again in the quality-bar loremaster pass.

Facts below were looked up in October and November 2026; sources at the end. **For any species, creature or god not covered here, look it up before using it.** Don't guess from the stat block alone, and say in the hand-over what you looked up and what you didn't.

## 1. Species: what the lore gives a character

Give every named NPC an ancestry before a name. Then use the ancestry's lore for something concrete: what they believe, what they remember, what their people expect of them, what they've rejected. The point is behaviour at the table, not a paragraph of history.

**Rules edition.** The 2024 Player's Handbook has ten species: aasimar, dragonborn, dwarf, elf, gnome, goliath, halfling, human, orc and tiefling. Half-elf and half-orc are gone; for a 2024 table describe such NPCs as human, elf or orc, or "of mixed heritage". 2014 and Pathfinder tables can keep half-species. In the 2024 rules most species live about 80 years and all come of age at about the same time; the exceptions are below.

| Species | What the 2024 lore says | What it can give an NPC |
|---|---|---|
| **Dwarf** | Raised from the earth by a forge god (Moradin, or another name on other worlds). Live about 350 years. Cities carved into mountains and underground; their oldest stories are wars with giants and Underdark horrors; their songs praise the small beating the mighty. Hill and mountain dwarves. | A memory longer than the town's; a record or grudge kept for centuries; pride in craft; old enmity with giants. |
| **Elf** | Made by Corellon. The first elves could change shape; Corellon took that away after some plotted with Lolth, and most were forgiven when Lolth was cast into the Abyss. Came from the Feywild. Live about 750 years and trance instead of sleeping. Lineages: drow (shaped by the Underdark), high elves (Feywild crossings), wood elves (old forests). | Patience that maddens humans; grief for people who died "recently" (a century ago); a drow who renounced Lolth, or didn't; Feywild manners. |
| **Gnome** | Made by gods of invention, illusion and life underground. The first gnomes were secretive forest and burrow folk who built traps and maze-tunnels and learned magic from gods who visited in disguise (Garl Glittergold, Baervan Wildwanderer, Baravar Cloakshadow). Forest and rock gnomes. Live about 425 years. Like a roof overhead, even a hat. | A trick for every problem; a workshop or burrow full of traps; delight in illusion and secrets. |
| **Halfling** | Cherished by gods of life, home and hearth (Yondalla, Brandobaris, Charmalaine) and credited with luck. Live about 150 years. Communities differ a lot: quiet shires, crime families, territorial gangs. Stouts underground; lightfoots nomadic or living among taller folk. | Luck they half believe in; a big extended family; home-loving or restless, and the family's opinion about which. |
| **Human** | Everywhere, ambitious, as varied as people on Earth, with many gods. One story places the first gathering in Sigil, the City of Doors, where Common began. | The default, so make them specific: region, trade, faith, class, language. |
| **Orc** | Made by Gruumsh, who gave them endurance, determination and darkvision; orcs keep those gifts even when they worship other gods. Some grow up on stories of their ancestors and wonder whether Gruumsh will call them and if they'd be worthy; others leave the stories behind. **Not evil by species in 2024**: play them as people. | Waiting for a call that may never come; a choice of gods; a family's travel-stories. |
| **Dragonborn** | Hatched from eggs of chromatic and metallic dragons, blessed by Bahamut and Tiamat (or made by dragons without the gods' blessing, depending who tells it). Colour and breath follow the dragon ancestor. | A dragon ancestor to live up to or live down; which origin story their family tells. |
| **Goliath** | Distant descendants of giants, carrying gifts of the first giants (one is growing for a moment). Looks echo cloud, fire, frost, hill, stone or storm giant kin. They've forged their own path away from the giants' feuds and look for heights beyond their ancestors. | Pushing their limits; a giant lineage that shows; deliberately staying out of old giant feuds. |
| **Tiefling** | Born of the Lower Planes or with a fiend in the bloodline. The legacy gives power but **doesn't decide morals**; a tiefling embraces it or regrets it. Abyssal (demon blood: horns, fur, tusks), Chthonic (Carceri, Gehenna, Hades: some look corpse-like), Infernal (devil blood: horns, tails, golden eyes, a smell of sulphur). | How strangers treat them; whether they lean into the legacy or away; which plane, and what that looks like. |
| **Aasimar** | Mortals with a link to the Upper Planes. *Not verified in this pass: look up their origin and guides before writing one.* | |

### Names

The 2024 Player's Handbook has **no name lists or naming conventions**. The rules below are the older books' patterns, written as sounds, not names to copy. Never reuse the example names printed in any rulebook; they're the first thing an experienced player recognises. (The checker warns on the classic ones.)

| Ancestry | How names work |
|---|---|
| **Dwarf** | A given name plus a clan name. Given names are short and hard (two syllables, stops and *-a/-ek/-in/-dra* endings). Clan names are compounds of stone, metal, fire or craft words. |
| **Orc** | One or two syllables, blunt, heavy consonants (*g, k, r, z, th*). Usually no surname; a deed or place can be added. |
| **Halfling** | A melodic, often three-syllable given name plus a homely compound family name made of everyday things (food, plants, hearth, the burrow). |
| **Kobold** | Short and sharp, one or two syllables, with clicks and hisses. Named by the warren for what they do or have done, and they add to or change the name after an event. |
| **Dragon** | A long, grand Draconic name with rolling consonants. Mortals use a shortened or mangled form, which is a story in itself. |
| **Elf, gnome, dragonborn, tiefling, goliath, aasimar** | Not verified in this pass. Look up the older books' conventions, then invent from the pattern. |
| **Human** | No single convention. Decide per region in `campaign.json` `naming` (see [npcs.md](npcs.md)), and make two regions sound different. |

**Don't reuse one name style for everyone.** If every NPC has an English-village name, the table can't tell a dwarf from a dockhand. Humans in a port or crossroads can mix; other peoples shouldn't.

## 2. Creatures behave like their lore

A stat block gives numbers. The lore gives motives. Use the motive, and turn the stat block's signature traits into behaviour the players see before the fight: a creature that regenerates is careless with its body, a shapechanger is hiding in plain sight, a creature that flees at half hit points has an escape route ready.

- **Kobolds.** In the 2024 Monster Manual kobolds are Dragons, not humanoids: small draconic cousins who serve dragons and in some lands worship them. Their scales echo the dragons near their warren. Zealous and ingenious, cowardly in a fair fight and brave in a trap; they pledge themselves to dragons in rites of passage and do anything a dragon asks. A kobold meeting a dragon is awestruck, not casual.
- **Goblins, hobgoblins, bugbears.** **Fey** in the 2024 Monster Manual: they came from the Feywild. A 5e telling has the god Maglubiyet conquering them and corrupting an original fae form; he isn't their ancestor. Goblin tribes are run by the strongest, often a non-goblin using them as expendable troops, and ride wolves or worgs. Hobgoblins are militaristic and close-knit, and can be negotiated with. Bugbears ambush and, in 2024, abduct. Bugbears were written as inherently evil only before 5e.
- **Hags.** **Fey** in 2024. Hags work alone or in a **coven** (the stat blocks carry Coven Magic) and hide behind illusions; a sea hag has an illusory appearance, a vile true appearance and a death glare, and lives on coasts and under the sea. Hags are known for deals and trickery; look up a hag's lore before writing her scene. Play the stat block as behaviour: she keeps the illusion up as long as it pays, and when it drops, the vile appearance and the glare are how she fights.
- **Gnolls.** Hyena-headed; in D&D they worship the demon lord Yeenoghu. Look up the 5e details before writing them as anything more than raiders.
- **Trolls.** Regenerate; only fire or acid stops it, and a severed limb or head can regrow. Speak Giant, often worship Vaprak, live in cold mountains. A smart table burns them; a smart troll fears torches.
- **Giants.** Each kind has a temperament: hill giants dim and greedy, stone giants reclusive artists who leave you alone if you leave them alone, frost giants respect only strength, fire giants are organised smiths and soldiers, cloud giants proud, storm giants isolated seers. Old enemies of dwarves.
- **Vampires.** Keep the alignment and personality they had in life; drain blood, charm with a gaze, command rats, bats and wolves. Their spawn are made by their bite and serve their maker.
- **Liches.** Wizards who cheat death by hiding the soul in a phylactery; in 5e they feed it captured souls. Destroying the body only sends the soul back. They keep their memories and personality, and their phylactery is the plot.
- **Mind flayers.** Believe they are the rightful masters of everything; take thralls, eat brains, and reproduce by implanting larvae (ceremorphosis). Patient schemers, not brutes.
- **Beholders.** Paranoid and xenophobic, even towards beholders that look different. Lairs full of guards and traps.
- **Yuan-ti.** Snake-people cults working through infiltration, not open war; purebloods pass as human and serve as spies and diplomats, and the castes look down on each other.
- **Kenku.** Cursed to speak only in mimicry. Thieves and spies in urban flocks; they fool people with copied voices.
- **Owlbears.** Hungry, territorial animals. Some remote places try to tame them; it goes badly.
- **Dragons.** All collect treasure; all are patient planners. Chromatic dragons scheme and dominate (a green dragon lies and pretends to agree; a red one is pure arrogance); metallic dragons often take mortal shapes to watch over people. Copper dragons are pranksters and riddlers, sociable, sulky when their joke dies, lairing in dry rocky uplands behind hidden entrances in maze-like tunnels.
- **Any other creature:** check its temperament, society, gods and attitude to lesser creatures before writing its scene.

If the adventure needs a creature to act against its lore, say why in the text (a curse, a bargain, a trick). Otherwise follow the lore.

## 3. Faith

The 2024 Player's Handbook doesn't give a pantheon; the 2024 Dungeon Master's Guide reportedly uses Greyhawk's as its sample. Gods appear in the species lore above (Moradin, Corellon, Lolth, Gruumsh, Bahamut, Tiamat, Yondalla and others).

- **In a package meant to be shared**, don't use a published world's gods by name (see section 5). Invent a small faith instead, and make it something people *do*: a daily rite, a food rule, a holy day, a saying, a shrine at the crossroads, a priest people argue with. One concrete practice beats a page of theology.
- **For a private table**, the user may want canon gods: look them up, use them accurately, and say in the README what's canon and what's invented.
- **Faith is a character tool.** Who prays, who stopped, who prays to the wrong god, who uses the temple for business. A god's name on an NPC card means nothing unless it changes what they do.

## 4. Use the system's own names

- Use SRD stat block names exactly (Goblin Minion, Kobold Warrior, Animated Rug of Smothering, Tough Boss, Swarm of Ravens). Rename tokens, not stat blocks.
- Use the system's own coins, languages, conditions and item names: "gold piece", "copper piece", "Draconic", "Dwarvish", "potion of healing".
- Page numbers and stat blocks come from the SRD in front of you, not memory.

## 5. Settings and proper nouns

Named settings, gods, cities and NPCs from published worlds (Forgotten Realms, Eberron and so on) are not in the SRD. Don't put them in a package that will be shared publicly. For a private table the user can ask for them: then use only what you can look up, and say in the README which parts are canon and which are invented. An invented city in an unnamed world is fine; it still follows everything above.

## Checking it

In the quality-bar loremaster pass, list every named NPC and creature with its ancestry, the reason its name fits, and the piece of lore that shapes it (`lore` in `campaign.json`). Reread each creature's scene against its lore. Fix any mismatch, and report what you looked up and what you didn't.

## Sources

Looked up November 2026 unless noted.

- Species lore and lifespans: D&D Beyond, *Basic Rules (2024): Character Origins* (dndbeyond.com/sources/dnd/free-rules/character-origins). Nine species there; aasimar isn't in the free text and wasn't checked.
- The ten 2024 species and the removal of half-elf and half-orc: D&D Beyond, *The 10 Species in the 2024 Player's Handbook* (dndbeyond.com/posts/1783), and thegamer.com's 2024 Player's Handbook FAQ (October 2026).
- Name patterns: the 2014 Player's Handbook chapter 2 name tables for dwarf, half-orc and halfling, as reproduced on dndbeyond.com/species (October 2026); kobold names from Volo's Guide to Monsters as reproduced at nerdsandscoundrels.com/kobold-names.
- Goblinoids as Fey in 2024: dungeonmister.com, *All the monsters changing monster type in D&D 2024*; Gaming Nexus on the 2024 Monster Manual's fey. Maglubiyet, goblin society and gods: Wikipedia, *Goblin (Dungeons & Dragons)*.
- Kobolds: 2024 Monster Manual summaries (belloflostsouls.net; Dump Stat Adventures, October 2026) and Wikipedia, *Kobold (Dungeons & Dragons)*.
- Hags: the SRD 5.2.1 Sea Hag, Green Hag and Night Hag stat blocks (Fey; Coven Magic; Illusory Appearance; Vile Appearance; coastal and underwater habitat for the sea hag).
- Trolls, giants, vampires, liches, beholders, yuan-ti, kenku, owlbears, dragons: the matching Wikipedia articles (*Troll (Dungeons & Dragons)*, *Giant (Dungeons & Dragons)*, *Vampire (Dungeons & Dragons)*, *Lich (Dungeons & Dragons)*, *Beholder (Dungeons & Dragons)*, *Yuan-ti*, *Kenku*, *Owlbear*, *Dragon (Dungeons & Dragons)*); mind flayers: Wikipedia, *Illithid*. Gnolls and Yeenoghu: Wikipedia, *List of hybrid creatures in folklore* (thin; look up more before use).
- Copper dragons (October 2026): Bell of Lost Souls, *D&D Monster Spotlight: If You Can't Take a Joke, Beware the Copper Dragon*; the D&D Homebrew Wiki copper dragon page.
- The 2024 Dungeon Master's Guide using Greyhawk's pantheon: EN World forum summaries of the book (secondhand).
