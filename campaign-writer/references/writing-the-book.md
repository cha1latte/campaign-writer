# Writing the book

The GM book is the product. Someone runs it with friends watching, flips to a page mid-game and needs the answer in five seconds. Write for that moment.

## Chapter plan

One file per chapter in `book/`, numbered so they sort. Use this order and drop what doesn't apply:

| File | Contents |
|---|---|
| `01-overview.md` | **Adventure overview**: GM pitch; *What's really going on* (want, obstacle, clock, choice); *Adventure at a glance* (structure in a list or table, one line per node); *Hooks* (three); *Running this adventure* (tone, content and safety notes, solo or party scaling, lethality, what to do if the players skip something); session plan (what fits in each session) |
| `02-…` to `0N-…` | **The adventure**, one chapter per act, region or session. One `##` heading per node, tagged with its id: `## 3. The Old Toll Bridge {#N3}` |
| next | **Non-player characters**: an NPC card for everyone with lines |
| next | **Bestiary**: stat blocks, or references plus changes (see the system file) |
| next | **Rewards, advancement and endings**: treasure table, milestones, the three endings, what's next |
| campaigns | **Between adventures** after each adventure's chapter: what changed, what the villain does next, downtime, levelling |
| next | **Appendix**: random tables (encounters, rumours, names, weather), a timeline or clock tracker, quick-reference sheet |
| Teach mode | **Learning guide**: objectives, where each is taught, practised and assessed; worked solutions; hint ladders; misconceptions to watch for; debrief questions; sources |
| last | **Credits and licence**: author line, tools, licence and attribution text (verbatim from the system file), and the font credit: *Set in Alegreya, Alegreya SC and Alegreya Sans by Huerta Tipográfica (SIL Open Font License 1.1).* |

## The node template

Every place, scene or event gets the same shape, so the GM always knows where to look:

```markdown
## 4. The Broken Watch {#N4}

*Two hours from the bridge, on the ridge road. Day 2 or later.*

> Three walls of a watchtower still stand, black with old fire. Snow has drifted against the
> doorway, and something has dug through it from inside.

**What's here.** The tower's ground floor (area 4a) and a collapsed stair to a roof platform (4b).
The trolls used it as a waystation two nights ago.

**What's hidden.**
- **Gnawed antlers** under the snow (DC 12 Wisdom (Perception), or automatically if they dig): the trolls ate here → they're heading for the high pass (**N5**).
- **A soldier's tally stick** with eleven notches, the last three fresh → the garrison's missing patrol (**C2**).

**What happens.** If the heroes arrive after Day 3, two trolls are sleeping off a meal here (**E3**). Otherwise it's empty and makes a safe camp.

**Leads.** The ridge road continues to the pass (**N5**, 3 hours). The tally stick points to the garrison (**N2**).
```

Rules for nodes:

- **Read-aloud: one to three sentences, under 90 words.** What the senses notice first. No feelings for the players ("you feel uneasy"), no actions for them, no hidden facts. Many areas need none.
- **Bold the first mention** of anything the GM must find on the page: NPCs, creatures, items, clues, DCs.
- **Numbers inline**: DC, distance, time, quantity, damage. Never "a difficult check" or "a while".
- **Every clue says where it points** (→ node or conclusion id in bold) so the GM can steer.
- **Say what happens if the players do nothing** and if they fail.
- **Give people who come and go a schedule**: "Fenn leaves 30 minutes after the heroes arrive, or at once if accused". Say whether the heroes can stop them and what that changes.
- **Mark what's public**: read-aloud and obvious details versus GM-only facts. An AI GM reads every word and needs to know which ones it may say.
- Use `###` for sub-areas (4a, 4b) and `####` for small labels.
- Each **Label.** line starts its own paragraph, so you can write one field per line as in the templates.

## NPC cards

```markdown
### Marta Grell, the toll-keeper {#marta}

*Sixty, broad as a door, a sealskin coat over a smith's apron.* **Voice:** slow, says "aye" before bad news.
**Wants:** to keep the bridge open so the village doesn't starve. **Fears:** the trolls coming back for the debt.
**Knows:** the trolls came from the Grey Teeth (→ **N5**); her husband paid them in salted fish for twenty years.
**Hides:** she still owes them, and the payment is due on Day 4 (→ **C1**).
**If pushed:** lies once, then cries and tells the truth.
```

Give every named NPC a want. Give the important ones something they know, something they hide, and a line of dialogue. Make voices distinct: different rhythms and word choices, not just accents.

## Encounter blocks

```markdown
### Encounter: Ambush at Hollow Ridge (E2)

**Difficulty:** moderate for one level-3 character (budget 225 XP; 200 XP spent).
**Enemies:** 1 **troll whelp** (see Bestiary). **Terrain:** knee-deep snow (difficult terrain off the path), a frozen pond (DC 10 Dexterity (Acrobatics) to cross at full speed), two boulders (half cover).
**Tactics:** it charges from the pines at the first person on the path, drags them toward the pond, and flees at half HP to the cave (**N6**), leaving a blood trail.
**Avoid it:** a hero who spots the tracks (DC 13 Wisdom (Survival)) can circle the ridge and lose 1 hour instead.
**Scaling:** weaker hero: the whelp starts wounded (half HP). Stronger: add a second whelp at round 2.
**Aftermath:** a torn satchel holding the patrol's map (→ **N4**).

![Map 3: Hollow Ridge](map:m3-ridge){wide}
```

## Style

- Write in a clear, warm, practical voice. Present tense for what's there, second person ("you") only in read-aloud and handouts.
- Short paragraphs, lists for anything the GM scans, tables for anything with columns.
- Concrete beats atmospheric: "the snow is pink around the stump" beats "an aura of menace".
- The checker flags stock AI phrasing (tapestry, testament, delve, nestled, bustling, palpable, ominous, shadowy figure). Replace each one with a concrete detail.
- **Names.** Fit the setting's sound, make them easy to say aloud, start important names with different letters, and avoid fantasy-generator clichés (Eldoria, Shadowmere, the Whispering Woods). Test by saying them aloud.
- **Original.** Don't copy text, named characters or settings from published adventures. Reuse public rules (SRD, ORC) and credit them. Familiar tropes are fine if you give them a turn.
- **Inclusive and table-safe.** Varied people in every role. Flag intense content (gore, body horror, harm to children or animals) in *Running this adventure* so the table can set lines and veils.

## Markdown the builder understands

| Write | Gets |
|---|---|
| `# Chapter` (once per file) | Chapter title on a new page |
| `## Name {#N3}` | Section heading with an anchor id (required for nodes) |
| `> text` | Read-aloud box |
| ```` ```sidebar Title ```` … ```` ``` ```` | Sidebar box (advice, variants) |
| ```` ```gm Title ```` … | GM-only box (in the GM book; dropped from handouts) |
| ```` ```lesson Title ```` … | Lesson box (Teach mode) |
| ```` ```tip Title ```` … | Tip box |
| ```` ```statblock ```` … | Stat block (see the system file for the layout) |
| `![Caption](map:m1-mill){page}` | Rendered map on its own full page (a plate). Best for battle maps: no half-empty columns |
| `![Caption](map:m1-mill){wide}` | Rendered map across both columns. Put it right after the chapter title or a `\pagebreak`, or Chrome leaves a gap above it |
| `![Caption](map:m1-mill)` | Map in one column: only for small, simple maps (labels shrink to about 4 pt) |
| `![Caption](images/x.png)` | An image from the package folder |
| `\pagebreak` | New page; the two columns restart |
| a line ending in `\` | Keeps its line break (addresses, short verse) |
| ```` ```poem Title ```` … | Every line kept as written: songs, verse, inscriptions |
| ```` ```letter Title ```` … | A letter or diary page in plain, larger type, line breaks kept. Use it for found documents; `>` is for read-aloud only |
| ```` ```write 6 ```` … ```` ``` ```` | Six ruled writing lines (field notebooks, prediction sheets) |
| `[one-action]`, `[two-actions]`, `[three-actions]`, `[reaction]`, `[free-action]` | Pathfinder action icons |
| `*h* = ½*gt*²` | Italics work inside formulas; write `\*` for a literal asterisk |
| `[text](#N3)` | Link (works inside the PDF) |

Bold inside italic works (the bold italic face is bundled). A numbered list that resumes after a table keeps counting from its first number. Tables, lists (one nesting level), `**bold**`, `*italic*` and `` `code` `` work as usual, inside boxes too: a box body follows the same paragraph rules (single line breaks join; a blank line or a **Label** starts a new paragraph). Quotes and apostrophes are printed curly. ```` ```sign Title ```` makes a big-lettered notice (a sign, a poster, a chart for young readers). A heading always stays with the block that follows it; long lesson boxes may split across columns. The build warns about markdown that didn't render (stray `*`, `{#`, `](`).

**Where maps go.** The pattern that lays out cleanly: `\pagebreak`, then the map with `{wide}`, then the node heading and its text. A map can also go in a *Maps* appendix as `{page}` plates, linked from the node. A `\pagebreak` before a map can leave the end of the previous page short; that's acceptable at the end of a section, and the alternative is the appendix. Avoid a `{page}` plate straight after a heading (the heading is left alone at the foot of a page) and an unbreakable sidebar straight after a `{wide}` map. Travel maps: `{wide}` at the start of the chapter that uses them. Every map PNG is also in `build/maps/` for screens and VTTs.

**Statblock layout.** First line: the name. Second line: the type line (rendered italic). `---` draws a rule. `## Actions` makes a section header. A pipe table renders as the ability row. Everything else is a paragraph, so write bold labels yourself:

````markdown
```statblock
Troll Whelp
Large Giant, Chaotic Evil
---
**AC** 13 **Initiative** +1 (11)
**HP** 45 (6d10 + 12)
**Speed** 30 ft.
| STR | DEX | CON | INT | WIS | CHA |
|---|---|---|---|---|---|
| 16 (+3) | 12 (+1) | 15 (+2) | 6 (−2) | 9 (−1) | 7 (−2) |
---
**Senses** Darkvision 60 ft.; Passive Perception 9
**CR** 1 (XP 200; PB +2)
## Traits
**Regeneration.** The whelp regains 5 Hit Points at the start of each of its turns. If it takes Acid or Fire damage, this trait doesn't function on its next turn. It dies only if it starts its turn with 0 Hit Points and doesn't regenerate.
## Actions
**Rend.** *Melee Attack Roll:* +5, reach 5 ft. *Hit:* 7 (1d8 + 3) Slashing damage.
```
````

(That whelp is a homebrew reskin; the system file explains how to build one and how to label it.)

**D&D 2024 layout.** The 2024 books print a modifier and a saving throw for each ability. Use two rows of three:

```markdown
| | | MOD | SAVE | | | MOD | SAVE | | | MOD | SAVE |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Str** | 16 | +3 | +3 | **Dex** | 12 | +1 | +1 | **Con** | 15 | +2 | +2 |
| **Int** | 6 | −2 | −2 | **Wis** | 9 | −1 | −1 | **Cha** | 7 | −2 | −2 |
```

**Call of Cthulhu and other percentile games.** Characteristics as a table with full, half and fifth values, then derived stats:

````markdown
```statblock
Owen Hale, ex-Navy radioman
Age 48, human
---
| STR | CON | SIZ | DEX | INT | POW |
|---|---|---|---|---|---|
| 55 (27/11) | 60 (30/12) | 65 (32/13) | 50 (25/10) | 75 (37/15) | 80 (40/16) |
---
**HP** 12 **DB** +1D4 **Build** 1 **Move** 7 **MP** 16
**Combat** Fighting (Brawl) 45% (22/9), damage 1D3 + DB; .38 revolver 40% (20/8), damage 1D10
**Skills** Electrical Repair 70%, Radio 75%, Persuade 50%, Spot Hidden 55%
**Sanity loss** to see what he tunes in: 0/1D6
```
````

**Pathfinder 2e layout.**

````markdown
```statblock
Forest Troll Pup
Creature 2 · Large, Giant, Troll
---
**Perception** +8; darkvision
**Skills** Athletics +9, Intimidation +6
**Str** +4, **Dex** +1, **Con** +3, **Int** −2, **Wis** +0, **Cha** −1
---
**AC** 17; **Fort** +11, **Ref** +6, **Will** +6
**HP** 40, regeneration 5 (deactivated by electricity or fire); **Weaknesses** electricity 5, fire 5
**Speed** 30 feet
---
**Melee** [one-action] jaws +10, **Damage** 1d10+4 piercing
**Rend** [one-action] claw. If the pup hit the same creature with two claw Strikes this turn, it deals 1d6+2 slashing damage.
```
````

(Also homebrew: label it in the Bestiary and build it from GM Core's *Building Creatures* tables.)
