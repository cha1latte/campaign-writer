# Other systems

The skill works for any game. The book structure, clue design, maps, handouts and Teach mode don't change. What changes is the maths and the licence.

## Before writing

1. **Find the system's own free reference** and use it for this job: an SRD, a free quickstart, the publisher's open licence page (Creative Commons, ORC or a third-party licence) or the user's own rulebook if they point you to it. Note the edition.
2. **Find its difficulty guidance**: how it sets target numbers, how it balances fights or threats (budgets, threat levels, clocks, "danger" ratings), and how characters advance.
3. Set `"system": "other"` and `"system_label": "<Game and edition>"` in `campaign.json`. Encounter maths can't be checked by the tool, so write each encounter's difficulty in the system's own terms and **show the working** in the encounter block ("Threat 3 of 5, per Core p. 112: two soldiers equal one trained PC").

## Common families

| Family | Examples | How difficulty works | Adventure tips |
|---|---|---|---|
| OSR / old-school D&D-likes | Old-School Essentials, Shadowdark, Knave, Cairn | Monster HD versus party level; reaction and morale rolls; random encounters as a clock | Lethal by design. Telegraph danger, reward clever play, and make treasure the XP engine. Keyed dungeon maps shine here |
| Powered by the Apocalypse | Dungeon World, Monster of the Week, Masks | No balance maths: fronts, clocks and GM moves | Write fronts with grim portents, custom moves for set pieces, and questions instead of answers |
| Forged in the Dark | Blades in the Dark, Scum and Villainy | Position and effect; clocks for everything | Write factions with tiered clocks, scores with several approaches, and engagement complications |
| Investigation | Call of Cthulhu, Delta Green, GUMSHOE | Skill percentages or spends; sanity and stress | Node-based structure; core clues that can't be missed (GUMSHOE) plus three clues per conclusion |
| Narrative / generic | Fate, Cypher, Savage Worlds, GURPS | Each system's own difficulty ladder | Use the ladder by name and give aspects or complications to every scene |

## Call of Cthulhu 7th edition

- **Free reference:** Chaosium's *Call of Cthulhu Quick-Start Rules* (free on chaosium.com) covers characteristics, skills, combat, Sanity and chases. Default to 7th edition; ask only if they mention 6th.
- **No levels.** Set `players.count`, leave out `level`, and set `players.party_label` ("for four investigators") and `gm_title: "Keeper"`. Investigators are built by characteristic rolls or point-buy plus occupation and personal-interest skill points; check pregen totals with a small script.
- **Difficulty in its own terms:** Regular, Hard or Extreme rolls; opposed rolls; a fight's danger is the enemy's damage and Build against the investigators' HP. Write it in the encounter block ("Difficulty: Regular; two thugs, 1D6+DB each, the investigators should talk or run").
- **Conventions:** Sanity loss as `0/1D6` (success/failure); chases with locations, hazards and Move; core clues an investigator gets automatically if they look in the right place, plus three clues per conclusion. Pushed rolls: say what the cost of failing a pushed roll is.
- **Licence:** for free fan material, Chaosium's Fan Material Policy requires this notice, verbatim, in plain sight (set `licence_marker: "Fan Material Policy"`): *"This [adventure] uses trademarks and/or copyrights owned by Chaosium Inc/Moon Design Publications LLC, which are used under Chaosium Inc's Fan Material Policy. We are expressly prohibited from charging you to use or access this content. This [adventure] is not published, endorsed, or specifically approved by Chaosium Inc. For more information about Chaosium Inc's products, please visit www.chaosium.com."* No Chaosium logos; free only. Selling it needs Chaosium's community-content programme or a licence.

## Licence

Only reuse rules text that the system's licence allows, and copy its required notice verbatim into the credits (Creative Commons attribution, ORC notice, or the publisher's third-party licence terms). If there's no open licence, refer to rules by name and page ("see Core p. 40") instead of reprinting them, and keep the package for personal use. Set `"uses_srd": false` in `campaign.json` when you reprint no rules text (the name is historical: it means "reprints licensed rules text"). Put a distinctive phrase from the required notice in `licence_marker` so the checker can confirm the credits carry it.
