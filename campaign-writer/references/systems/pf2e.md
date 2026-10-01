# Pathfinder Second Edition (remaster)

Free rules reference: **Archives of Nethys** (https://2e.aonprd.com), Paizo's official rules site. Pages are script-heavy and some fetch tools summarise or refuse stat blocks; its search API returns full text and is the fastest route:

```text
POST https://elasticsearch.aonprd.com/aon/_search
{"query": {"bool": {"must": [{"match": {"category": "creature"}}, {"match_phrase": {"name": "troll"}}]}},
 "_source": ["name", "level", "weakness_raw", "source_raw", "remaster_id", "text"]}
```

Entries with a `remaster_id` are legacy versions that have a remastered replacement; prefer the remastered one (its `source_raw` names Monster Core, Player Core or GM Core). The remastered core books (Player Core, GM Core, Monster Core) are released under the **ORC License**. Look up every creature, hazard and item on AoN for this job and cite the book and page AoN shows ("Monster Core pg. 337"). Use remaster versions, not legacy (pre-2023) ones, unless the user's table plays legacy.

## Encounter budget (GM Core pp. 75–76)

Budgets assume **four characters**:

| Threat | XP budget | Character adjustment |
|---|---|---|
| Trivial | 40 or less | 10 or less |
| Low | 60 | 20 |
| Moderate | 80 | 20 |
| Severe | 120 | 30 |
| Extreme | 160 | 40 |

For each character beyond four, add the character adjustment. **For each missing character, subtract it.** Creature cost by level relative to the party:

| Creature level | −4 | −3 | −2 | −1 | Party level | +1 | +2 | +3 | +4 |
|---|---|---|---|---|---|---|---|---|---|
| XP | 10 | 15 | 20 | 30 | 40 | 60 | 80 | 120 | 160 |

Keep creatures within −4 to +4 of the party level. Mix threats: a run of moderate fights feels flat; use low and trivial ones to let characters shine and severe ones for big enemies.

Quick structures (GM Core p. 75): Boss and Lackeys (one creature of party level +2 and four of party level −4, 120 XP), Boss and Lieutenant (+2 and party level, 120 XP), Elite Enemies (three of party level, 120 XP), Lieutenant and Lackeys (party level plus four of −4, 80 XP), Mated Pair (two of party level, 80 XP), Troop (party level plus two of −2, 80 XP), Mook Squad (six of −4, 60 XP).

## Solo and duo play

The budget maths gets harsh below four characters. For **one** character the budgets are Trivial 10, Low 0, Moderate 20, Severe 30, Extreme 40, so a single creature of the hero's own level is already an Extreme fight. Pick one of these and state it in *Running this adventure*:

1. **A full companion** the player or GM runs, built as a character of the same level (`counts_as_character: true`). Two characters: Low 20, Moderate 40, Severe 60, Extreme 80. One creature of party level becomes Moderate.
2. **A stronger hero.** Many solo players run their character 1–2 levels above the adventure's assumed level, or use a variant from GM Core (look up the current variant rules on AoN, such as Free Archetype). Budget against the hero's real level.
3. **Weaker foes.** Use creatures 2–4 levels below the hero, and the Weak adjustment where Monster Core provides it. Lean on hazards, terrain, chases and social encounters that don't run on the XP budget at all.

With fewer than four characters some tiers collapse (solo: Low is 0 XP, below Trivial; duo: Low equals Trivial). Label such fights by the tier the checker reports and don't plan "low-threat" fights for one character: use trivial ones, hazards and non-combat challenges instead.

Whatever you pick: make fights puzzles (terrain, weaknesses, preparation), give enemies reasons to flee, capture or bargain, decide what happens at 0 HP (dying rules as normal, or capture/rescue at a cost), and give plenty of healing (potions, a healer NPC, safe rests).

**Worked example (solo troll hunt).** The remastered **Forest Troll** is a level-5 creature (Monster Core pg. 330) with weakness to **electricity and fire**, both of which also switch off its regeneration. A level-5 hero with a level-5 companion (two characters) faces one as a Moderate fight (40 of 40). The same troll against the hero alone is Extreme (40 of 40), and at level 4 or below it's outside the rules (a +1 creature costs 60 XP against a solo Extreme budget of 40). Other trolls differ: in Monster Core 2 the ice troll is weak to fire and sonic and the cavern troll to acid and sonic. **Always read the weaknesses from the creature's own entry**; they're the heart of a monster-hunt adventure.

## Difficulty classes (GM Core pp. 52–53)

**Level-based DCs** (for checks tied to a creature's or hazard's level):

| Level | DC | Level | DC | Level | DC |
|---|---|---|---|---|---|
| 0 | 14 | 7 | 23 | 14 | 32 |
| 1 | 15 | 8 | 24 | 15 | 34 |
| 2 | 16 | 9 | 26 | 16 | 35 |
| 3 | 18 | 10 | 27 | 17 | 36 |
| 4 | 19 | 11 | 28 | 18 | 38 |
| 5 | 20 | 12 | 30 | 19 | 39 |
| 6 | 22 | 13 | 31 | 20 | 40 |

**Simple DCs** (by the proficiency a task needs): untrained 10, trained 15, expert 20, master 30, legendary 40. **Adjustments:** incredibly easy −10, very easy −5, easy −2, hard +2, very hard +5, incredibly hard +10.

Write checks as **DC 20 Survival** or **DC 18 Athletics (Climb)**. Use the four degrees of success: say what a critical success, success, failure and critical failure each do for important checks.

## Creatures and hazards

- Use Monster Core creatures by name with their AoN page. Copy what the GM needs at the table into the Bestiary in PF2e stat block order (name and level, traits, Perception and senses, languages, skills, attributes, items, AC, saves, HP, immunities/weaknesses/resistances, speed, strikes, actions with action icons written as `[one-action]`, `[two-actions]`, `[reaction]`).
- **Custom creatures:** build them with GM Core's *Building Creatures* tables on AoN (they give AC, HP, attack and damage by level and role). Don't guess numbers. Label custom creatures as homebrew in the Bestiary.
- Strip Paizo's proper nouns (named deities, places, characters) from anything you reuse. They're Reserved Material, not ORC content.
- Hazards (traps, haunts, environmental dangers) have levels and XP too (GM Core p. 99): a **complex** hazard costs the same as a creature of its level, a **simple** hazard one fifth (2, 3, 4, 6, 8, 12, 16, 24, 30 XP from −4 to +4). List them under `hazards` in the encounter, not as creatures. They're a good way to add danger in solo play without action-economy problems.

## Pregens

Build them on AoN with Player Core. Checklist:

1. Ancestry (HP, size, speed, boosts and flaw, a level-1 ancestry feat), background (two boosts, a skill and a Lore, a skill feat), class (key attribute boost, HP per level, proficiencies, features, class feats by level).
2. **Attributes:** four free boosts at level 1 plus ancestry and background; at levels 5, 10, 15 and 20 boost four attributes. A boost raises a modifier by 1, or only "partially" (needs two boosts) if it's already +4 or higher.
3. **Proficiency bonus = level + 2 (trained), +4 (expert), +6 (master), +8 (legendary)**; untrained adds nothing.
4. **HP** = ancestry HP + (class HP + Con modifier) × level. **AC** = 10 + Dex (up to the armour's cap) + proficiency + item bonus. **Strikes:** attribute + proficiency + item bonus; damage dice from the weapon (striking runes add dice). **Class DC** = 10 + key attribute + proficiency.
5. Gear by Party Treasure by Level (GM Core); a level-5 character typically has a +1 striking weapon.
6. Write actions with icons (`[one-action]`, `[reaction]`) and keep each pregen to one page.

## Rewards

PF2e expects specific wealth by level (GM Core's *Party Treasure by Level* table on AoN). For one-shots, give consumables (healing potions, elixirs, scrolls, talismans) and one permanent item. Use milestone levelling for short adventures; if using XP, remember awards stay at the four-character values.

## Licence text (required)

Include an ORC Notice in the credits. The ORC AxE (Paizo/Azora's official explainer) gives this shape; fill in what you used:

> **ORC Notice.** This product is licensed under the ORC License held in the Library of Congress at TX 9-307-067 and available online at various locations including www.azoralaw.com/orclicense, www.gencon.com/orclicense and others. All warranties are disclaimed as set forth therein.
>
> **Attribution.** This product is based on the following Licensed Material: *Pathfinder Player Core* © 2023, Paizo Inc.; *Pathfinder GM Core* © 2023, Paizo Inc.; *Pathfinder Monster Core* © 2024, Paizo Inc. (list only the books you used). If you use our Licensed Material in your own published work, please credit us as follows: *<Title>* © <year>, <author>.
>
> **Reserved Material.** Reserved Material elements in this product include, but may not be limited to: <your proper nouns, characters, places and story>.
>
> **Expressly Designated Licensed Material.** <Leave empty, or name anything of yours you want to open up.>

Copy each Paizo book's exact attribution line from its own ORC notice (its legal page, or the AoN source page) when you can; it may list authors. "Pathfinder" is a Paizo trademark and isn't licensed by the ORC. You may say the adventure is "compatible with Pathfinder Second Edition" to identify the game, but don't use Paizo logos or trade dress or imply endorsement. Keep any personal-use package private if the user hasn't checked Paizo's licences for publishing.
