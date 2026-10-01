# Brief intake

The user gives you a sentence. You need a brief. Infer most of it, ask only what changes the build, and never stall a clear request with a questionnaire.

## Read the wish

Pull these out of the request, the conversation and the user's environment (an open Foundry world, character sheets in the folder, earlier campaigns in `campaigns/`):

| Field | Look for | Default if nothing says otherwise |
|---|---|---|
| System | "D&D", "5e", "Pathfinder", "PF2e", a named game; the Foundry world's system | D&D 5e, **2024 rules** (SRD 5.2.1) |
| Players | "solo", "just me", "for my group of 5" | 4 players; "solo"/"I hunt" → 1 |
| Level | "level 3", "new characters", an existing sheet | Level 3 (enough options to be fun, low enough to be scary), **unless the wish names a foe**: then pick the lowest level at which that foe fits the system's budget for this party (a solo PF2e troll hunt needs a level-5 hero plus a companion; see the system file) and say why |
| Length | "one-shot", "campaign", "a few sessions" | "one-shot" → 1 session of about 4 hours; "campaign" → 4 sessions of about 3 hours; nothing → 2–3 sessions |
| Tone and limits | "spooky", "for kids", "grimdark", "no spiders" | Adventurous and PG-13. Name the content in the running guide so the table can adjust |
| Mode | "teach me", "learn", "for my class", a subject name | Standard. Any learning request → Teach (see [Teach mode](teach-mode.md)) |
| Who runs it | "I'll DM", "AI GM", "Familiar", "solo with an oracle" | Group and they say "my players": the requester is the GM. Requester plays solo and names no GM: write for **an AI GM or a friend** (both read the same book) and add the [Foundry hand-off](foundry-handoff.md) if they play in Foundry. Connected Foundry/Familiar tools only tell you Foundry is available; they don't say who runs the game |
| Requester plays? | "I hunt trolls", "for me to play", "solo", "my players" | **Yes** if they say *I*/*me* about the hero or it's solo; **no** if they say *my players/group* |
| Table style | "theatre of the mind", "VTT", "minis" | Maps for key locations, usable in print and VTT |
| Ages | "my 10-year-old", "class of 9th graders", "college" | Adult/teen. Children → no gore, gentler peril, shorter sessions (60–120 minutes), simpler sentences, big-print handouts, simple pregens (see the system file) |
| Experience | "never played", "new to D&D", "veterans" | New players → level 1–3 with low-option classes and a one-page "how to play" handout; veterans → whatever the story needs |

**Other games:** use the current edition unless they say otherwise (Call of Cthulhu 7th, Pathfinder 2e remaster, Shadowdark, Blades in the Dark). Systems without levels skip the Level row; say how experienced the characters are instead.

**Edition note.** "D&D" with nothing else means the 2024 rules, because SRD 5.2.1 is the current free reference. If the user's world or sheets are 2014, use 2014 (SRD 5.1); monster XP by CR is the same in both.

## When to ask

Ask one short round (up to three questions, with your default stated so they can just say "go") only if:

- the system is truly unknown *and* matters (they named no game and nothing in their environment says);
- you can't tell whether they'll play or run it, and it decides what you show them;
- Teach mode: the level of the subject is unclear in a way that changes the content ("physics" for a 12-year-old vs. a college Physics I course). "Physics I" means an introductory algebra-based or calculus-based mechanics course; default to algebra-based.

Otherwise state your assumptions in one line and start. Example: *"Going with D&D 5e (2024), one level-3 character, about three sessions, PG-13. Say if you want any of that changed."*

## Two kinds of requester

**Someone else plays it** (a parent running it for a child, a teacher for a class): treat the requester as the GM, but the players still need protecting. Set `audience.protect_players: true`, fill `spoiler_terms`, and keep clue documents in `handouts/found/`.

**They'll run it (GM).** Show the full pitch before or after the build: premise, structure, villain, twist, sample encounter. They need it to decide.

**They'll play it.** Treat everything past the back cover as a spoiler:

- In chat, show only the **player pitch**: a back-cover blurb (what the hero knows at the start, the tone, the promise), and practical facts (system, level, sessions, what to bring).
- Never mention villains, twists, monster names (beyond what the pitch reveals), clue answers, puzzle solutions, endings or secret rooms. Not in chat, not in file names, not in progress updates ("Writing the betrayal scene…" is a spoiler).
- Keep progress updates neutral: "Designing the structure", "Writing chapter 3 of 6", "Drawing maps".
- Name the GM-only files ("`*-gm-book.pdf`, `*-found-in-play.pdf`, `book/`, `campaign.json`, `puzzles/` and the `*-gm` maps are for the GM; the handouts PDF is yours") and put the same warning in the package README.
- In-world clue documents go in `handouts/found/` (their own PDF, handed over when found), never in the player's own handouts PDF.
- Fill `spoiler_terms` in `campaign.json` and let the checker prove the player material is clean.
- If they ask a question that would need a spoiler to answer ("is there a dragon?"), say it's in the GM book and offer to answer only if they want to know.

If they're playing with an AI GM (Familiar), the AI GM is the reader of the GM book. The player still never needs to see it.

## The pitch formats

**Player pitch** (`handouts/00-pitch.md`, also the chat summary for players):

```text
# <Title>
<Two to four sentences: who you are, what just happened, what you want, what stands in the way. Present tense, second person. Ends on a hook, not a twist.>
- System: <system and level>   - Players: <solo / N>   - Length: <sessions>
- Tone: <three words>          - Content: <anything the player should know, e.g. "body horror, mild">
```

**GM pitch** (top of `book/01-overview.md`, and the chat summary for GMs): logline, what's really going on, structure in one line, the big choice at the end, and why it's fun ("the trolls regenerate unless you burn them, so every fight is about fire and terrain").

## Write it down

Put the brief into `campaign.json` (system, players, length, mode, audience, table) and add a **Brief** section to the package `README.md` with the original wish quoted word for word and every assumption you made. That's how the user, or the next assistant, can see why it came out this way.
