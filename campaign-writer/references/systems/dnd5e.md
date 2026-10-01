# D&D 5th edition (2024 and 2014)

Free rules reference: **SRD 5.2.1** (2024 rules), CC-BY-4.0, from https://www.dndbeyond.com/srd. It includes about 330 monster stat blocks (pp. 254–364), magic items (from p. 209), spells, classes and the encounter rules below. For 2014 games, SRD 5.1 is the equivalent. Look rules up in the SRD for this job rather than trusting memory; stat blocks changed between editions.

## Encounter budget (SRD 5.2.1, "Combat Encounters", p. 202)

1. Choose a difficulty: **Low** (one or two scary moments, no casualties), **Moderate** (could go badly; weaker characters might drop), **High** (could be lethal; needs smart tactics and luck).
2. Budget = the table value × the number of characters.
3. Spend it on creatures by their XP. Spend as much as you can without going over.

| Level | Low | Moderate | High | | Level | Low | Moderate | High |
|---|---|---|---|---|---|---|---|---|
| 1 | 50 | 75 | 100 | | 11 | 1,900 | 2,900 | 4,100 |
| 2 | 100 | 150 | 200 | | 12 | 2,200 | 3,700 | 4,700 |
| 3 | 150 | 225 | 400 | | 13 | 2,600 | 4,200 | 5,400 |
| 4 | 250 | 375 | 500 | | 14 | 2,900 | 4,900 | 6,200 |
| 5 | 500 | 750 | 1,100 | | 15 | 3,300 | 5,400 | 7,800 |
| 6 | 600 | 1,000 | 1,400 | | 16 | 3,800 | 6,100 | 9,800 |
| 7 | 750 | 1,300 | 1,700 | | 17 | 4,500 | 7,200 | 11,700 |
| 8 | 1,000 | 1,700 | 2,100 | | 18 | 5,000 | 8,700 | 14,200 |
| 9 | 1,300 | 2,000 | 2,600 | | 19 | 5,500 | 10,700 | 17,200 |
| 10 | 1,600 | 2,300 | 3,100 | | 20 | 6,400 | 13,200 | 22,000 |

**XP by CR** (p. 256): 0 → 0 or 10 · 1/8 → 25 · 1/4 → 50 · 1/2 → 100 · 1 → 200 · 2 → 450 · 3 → 700 · 4 → 1,100 · 5 → 1,800 · 6 → 2,300 · 7 → 2,900 · 8 → 3,900 · 9 → 5,000 · 10 → 5,900 · 11 → 7,200 · 12 → 8,400 · 13 → 10,000 · 14 → 11,500 · 15 → 13,000 · 16 → 15,000 · 17 → 18,000 · 18 → 20,000 · 19 → 22,000 · 20 → 25,000 · 21 → 33,000 · 22 → 41,000 · 23 → 50,000 · 24 → 62,000 · 25 → 75,000 · 26 → 90,000 · 27 → 105,000 · 28 → 120,000 · 29 → 135,000 · 30 → 155,000.

**The SRD's own warnings** (p. 203), which the checker repeats:
- More than two creatures per character → include fragile ones that drop fast, especially at levels 1–2.
- A creature whose CR is above the party's level can take a character out with one action (an ogre can kill a level-1 wizard with one blow).
- More than two or three different stat blocks in one fight is hard to run.
- Adjust on the fly: creatures flee to make it easier, reinforcements arrive to make it harder.

The 2014 rules used thresholds and multipliers instead. This skill uses the 2024 budget for both editions, because XP by CR is identical and the 2024 method is the free, current one. Say so in *Running this adventure* for a 2014 game.

**Worked example (solo).** One level-3 character: Low 150, Moderate 225, High 400. A single CR 1 creature (200 XP) is a Moderate fight. A CR 2 (450) is beyond High for one character. The SRD troll (CR 9, 5,000 XP) is a High fight only for one character of level 13+, or four of level 5–6 (High budget 1,100 × 4 = 4,400 at level 5 is not enough; 1,400 × 4 = 5,600 at level 6 is).

## Difficulty classes (p. 6)

Very easy 5 · Easy 10 · Medium 15 · Hard 20 · Very hard 25 · Nearly impossible 30. Most checks in an adventure are 10–15; use 20 for things only specialists should manage. Write checks as **DC 13 Wisdom (Survival)**.

## Monsters

- **Use SRD creatures by name** and cite the page: "1 **Troll** (SRD 5.2.1 p. 333)". Copy the stat block into the Bestiary for the creatures the GM needs at hand; the CC-BY licence allows it with the attribution.
- **Reskin before you invent.** Need a "bog lurker" at CR 2? Take an SRD creature of CR 2 with the right shape (an Ogre for a brute, a Giant Constrictor Snake for a grappler), keep its numbers, and change the name, the description and at most two traits, each swapped for one of similar strength (Darkvision plus Sunlight Sensitivity for a kobold boss is fine). Label it in the Bestiary: *"Bog lurker (uses the Ogre stat block, SRD 5.2.1 p. 312, with Swamp Camouflage)"*.
- **Scaling a monster down** (e.g. a troll whelp for low levels): base it on an SRD creature of the target CR for AC, HP, attack bonus and damage, then add the signature trait in a weakened form. Mark it homebrew and say what it's based on. Don't invent numbers from scratch; CR guidance for building monsters is in the Dungeon Master's Guide, which isn't free, so anchor to an SRD creature at the target CR instead.
- Never paste stat blocks from non-SRD books (Monster Manual creatures not in the SRD, named NPCs from published adventures).
- Familiar's Foundry tools can build SRD monsters straight from the dnd5e compendium; mention which ones in the [Foundry hand-off](../foundry-handoff.md).

## Solo and small groups

- Budget for one character as written (budget × 1). Most solo fights should be **Low**, with one **Moderate** or **High** set piece and a way out.
- One enemy with the right trick beats a crowd: action economy kills solo heroes. Prefer enemies that grab, push, flee, bargain or take prisoners.
- A companion who fights at full strength counts toward the budget (`counts_as_character: true`). A sidekick-style helper usually doesn't. Use an SRD NPC stat block (Guard, Scout, Priest Acolyte, Warrior Infantry) for a companion and keep them a helper, not the hero.
- Give generous healing: potions of healing in the first treasure, a safe rest point per session.
- State what 0 HP means in this adventure (death saves as normal; captured; rescued at a cost).

## Pregens (2024 rules)

From SRD 5.2.1 pp. 19–23 ("Character Creation"). Check every pregen against this list:

1. **Class** → hit die, saving throws, skills (choose the listed number), weapon and armour training, level-1 features, Weapon Mastery where the class has it.
2. **Background** (SRD 5.2.1 has four: Acolyte, Criminal, Sage, Soldier) → **+2 to one and +1 to another of its three listed abilities, or +1 to all three** (no score above 20), its **Origin feat**, two skill proficiencies, one tool, starting gear. The SRD has no rule for overlapping proficiencies (skills or tools, e.g. Criminal and Rogue both give Thieves' Tools): pick a background or class options that don't overlap. Check every option exists in SRD 5.2.1 (it has only some Fighting Styles and feats; Dueling, for example, isn't there).
3. **Species** (Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling) → size, Speed, traits. **Languages:** Common plus two.
4. **Ability scores:** standard array 15, 14, 13, 12, 10, 8 (or 27-point buy), then the background increases.
5. **Numbers:** proficiency bonus +2 (levels 1–4), +3 (5–8), +4 (9–12). **HP** at level 1 = maximum hit die + Con modifier; each later level adds the fixed value (Barbarian 7; Fighter, Paladin, Ranger 6; Bard, Cleric, Druid, Monk, Rogue, Warlock 5; Sorcerer, Wizard 4) + Con modifier. **AC** 10 + Dex without armour, otherwise by the armour table. **Attack** = Str (melee) or Dex (ranged/finesse) + proficiency. **Spell save DC** = 8 + ability + proficiency; **spell attack** = ability + proficiency. Passive Perception = 10 + Wisdom (Perception).
6. **Level 4** brings an Ability Score Improvement or feat; **level 3** most subclasses.
7. **Spells with costly components** (a diamond, a pearl) need that component on the sheet; starting gear rarely covers it. Give it as part of the hook, or pick another spell.
8. **New or young players:** choose a class with few options (Fighter, Barbarian, Rogue; or a caster with its spell list cut to 4–6 favourites) and put a one-line "on your turn you can…" summary at the top of the sheet.

The SRD's PDF page numbers match its printed page numbers. It's two-column, so extract text by column (or search the PDF for the exact heading) rather than reading a plain text dump.

## Rewards

- Milestone levelling is simplest: name the milestones ("reach level 4 after the bridge"). For XP, award each creature's XP to the party, split evenly.
- Treasure: coins and story items in most areas, one or two permanent magic items per few sessions at low levels, consumables (potions, scrolls) more often. Use SRD magic items by name. Tie at least one reward to the theme (a fire-forged axe in a troll hunt).

## Licence text (required)

Any package that uses SRD 5.2.1 material (rules text, stat blocks, spell or item text) must carry this **verbatim** in the credits:

> This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

The SRD asks for no other attribution to Wizards of the Coast. You may describe the product as "compatible with fifth edition" or "5E compatible". Don't call it an official D&D product or use D&D logos or trade dress.

For 2014 (SRD 5.1):

> This work includes material taken from the System Reference Document 5.1 ("SRD 5.1") by Wizards of the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at https://creativecommons.org/licenses/by/4.0/legalcode.
