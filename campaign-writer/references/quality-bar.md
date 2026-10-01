# Quality bar

The checker proves the structure; it can't prove the adventure is good. Before hand-over, do these review passes, then score each part out of 10. Fix every part under 8 and score it again. Report the final scores honestly, including anything you couldn't check.

## Review passes

Do each pass as a different reader, re-reading the actual files rather than recalling what you meant to write.

1. **The GM at the table.** Open the PDF at a random node. Can you find, in five seconds, what's here, what's hidden, what happens if the players do nothing, and every number you need? Is any key fact (DC, distance, time, who knows what) only in prose three paragraphs down?
2. **The player who goes off-script.** Pick three unexpected but reasonable choices (skip the hook, attack the quest-giver, go straight to the lair). Does the book tell the GM what happens? Is there a dead end, an unwinnable fight or a clue only one NPC holds?
3. **The rules lawyer.** Recalculate two encounters and one pregen by hand. Check that stat blocks match their source, that DCs follow the system's table, and that treasure fits the level.
4. **The editor.** Read two chapters aloud in your head. Cut stock phrasing, repeated sentence shapes, filler adjectives and read-aloud that tells players what they feel. Check names: easy to say, distinct first letters, no generator clichés.
5. **The spoiler hunter** (when the requester plays). Re-read the handouts, pregens, player maps and your own chat messages. Search for every spoiler term, then for **indirect** giveaways the checker can't see: a pregen whose bond names the villain's sister, a map label "Ambush Point", a road label naming a hidden place, or two harmless facts that solve the mystery together (a date on the reference card plus a date in the pitch). Clue documents belong in `handouts/found/`.
6. **Teach mode: the student and the teacher.** Solve every puzzle from the printed givens only. Is it solvable and unambiguous? Does the answer match the script and the solution page? Is each objective really practised by *doing*, or just mentioned? Would a teacher sign off on the accuracy?
7. **The layout check.** Look at the PDF pages and every map PNG: no overlapping labels, no orphaned headings at the foot of a column, stat blocks not split, maps legible at print size, handouts one per page.

## Score sheet

| Part | 10 looks like |
|---|---|
| **Fit to the wish** | Exactly what was asked (system, players, length, tone); every assumption stated in the README |
| **Premise and engine** | A want, an obstacle, a clock and a real choice; an antagonist who acts; a hook that bites in the first five minutes |
| **Structure and clues** | Checker clean; three clues per conclusion; no dead ends; more than one way through; off-script choices answered |
| **Encounters** | Budgeted by the system's maths; varied; terrain and tactics; ways to avoid or end them; scaling notes |
| **NPCs** | Every one has a want; key ones know and hide something; voices are distinct and quotable |
| **Writing** | Clear, concrete, specific; short read-aloud; numbers inline; no stock AI phrasing; reads like a published module |
| **Maps** | Every key location; GM and player versions; legible, attractive, consistent with the text; VTT images and walls |
| **Handouts and pregens** | Player pitch plus in-world handouts that carry clues; pregens with correct maths and personal hooks |
| **Rules accuracy** | Stat blocks, DCs, budgets and rewards match the system; sources cited; licence text present |
| **Teach mode** (if used) | Objectives measurable and sourced; each one introduced, practised and assessed by *doing*; answers script-checked; hint ladders; debrief; fun stands on its own |
| **Spoiler safety** (if the requester plays) | Nothing in chat or player files gives away the plot; checker clean |
| **Package** | README, GM book PDF, handouts PDF, maps, `campaign.json`; builds from scratch with one command; looks professional |

**Score from evidence, not from intent.** A 9 needs something you can point to (a checker line, a page you looked at, a puzzle you solved, a rule you looked up). If you can't name the evidence, score it 7 and say what's unverified. Common reasons for a 6: a premise that's just "monsters attack the village", read-aloud over 90 words, NPCs who only give quests, fights that are all moderate, a mystery whose answer sits with one NPC, a lesson that's a quiz with a fantasy wrapper, a map with labels on top of each other.

Record the final scores in the package README and the receipt's *Scores* line.

## Honest reporting

In the hand-over, separate what you **verified** (checker output, built PDFs and their page counts, pages and maps you looked at, puzzles you solved) from what you **didn't** (playtesting with real people, rules you couldn't look up, a browser that wasn't available for PDFs). Never say "playtested" for something you only read.
