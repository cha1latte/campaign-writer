"""Check a campaign folder for the problems that ruin published adventures.

    python check_campaign.py <campaign-folder> [--bones] [--json]

--bones checks only the skeleton in campaign.json (structure, clues, encounters, Teach alignment, puzzle
scripts), for use before the chapters exist. Run it without --bones before hand-over.

ERR lines must be fixed. WARN lines need a decision (fix it, or say in the hand-over why it stays).
Exit code 1 if any ERR. Standard library only.

What it checks (see references/quality-bar.md for why):
  structure   ids, start node, every node reachable, every node has a heading in the book
  clues       three-clue rule for required conclusions and for nodes reached only by clues
  encounters  XP budget maths for D&D 5e (SRD 5.2.1) and Pathfinder 2e (GM Core), CR/XP and level ranges
  teach       every objective introduced, practised and assessed; hint ladders; answers recomputed by script; sources;
              Stealth style: lesson density, a Decoder, and a lexicon that keeps real jargon out of player text
  spoilers    spoiler terms absent from handouts, pregens, the player pitch and player maps
  writing     placeholders, read-aloud length, stock AI phrasing, licence/attribution text
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# D&D 5e 2024: SRD 5.2.1 p.202, "XP Budget per Character" (Low, Moderate, High)
DND_BUDGET = {
    1: (50, 75, 100), 2: (100, 150, 200), 3: (150, 225, 400), 4: (250, 375, 500), 5: (500, 750, 1100),
    6: (600, 1000, 1400), 7: (750, 1300, 1700), 8: (1000, 1700, 2100), 9: (1300, 2000, 2600), 10: (1600, 2300, 3100),
    11: (1900, 2900, 4100), 12: (2200, 3700, 4700), 13: (2600, 4200, 5400), 14: (2900, 4900, 6200),
    15: (3300, 5400, 7800), 16: (3800, 6100, 9800), 17: (4500, 7200, 11700), 18: (5000, 8700, 14200),
    19: (5500, 10700, 17200), 20: (6400, 13200, 22000),
}
DND_TIERS = ("low", "moderate", "high")
# SRD 5.2.1 p.256, "Experience Points by Challenge Rating"
CR_XP = {"0": (0, 10), "1/8": (25,), "1/4": (50,), "1/2": (100,), "1": (200,), "2": (450,), "3": (700,), "4": (1100,),
         "5": (1800,), "6": (2300,), "7": (2900,), "8": (3900,), "9": (5000,), "10": (5900,), "11": (7200,),
         "12": (8400,), "13": (10000,), "14": (11500,), "15": (13000,), "16": (15000,), "17": (18000,),
         "18": (20000,), "19": (22000,), "20": (25000,), "21": (33000,), "22": (41000,), "23": (50000,),
         "24": (62000,), "25": (75000,), "26": (90000,), "27": (105000,), "28": (120000,), "29": (135000,),
         "30": (155000,)}
# Pathfinder 2e: GM Core p.75-76 (Encounter Budget; Creature XP and Role; Different Party Sizes)
PF_TIERS = ("trivial", "low", "moderate", "severe", "extreme")
PF_BUDGET = {"trivial": 40, "low": 60, "moderate": 80, "severe": 120, "extreme": 160}
PF_ADJUST = {"trivial": 10, "low": 20, "moderate": 20, "severe": 30, "extreme": 40}
PF_CREATURE_XP = {-4: 10, -3: 15, -2: 20, -1: 30, 0: 40, 1: 60, 2: 80, 3: 120, 4: 160}
# GM Core p.99, Table 10-14: Hazard XP (simple, complex)
PF_HAZARD_XP = {-4: (2, 10), -3: (3, 15), -2: (4, 20), -1: (6, 30), 0: (8, 40), 1: (12, 60), 2: (16, 80), 3: (24, 120), 4: (30, 150)}

SYSTEMS = {"dnd5e-2024", "dnd5e-2014", "pf2e", "other"}
NODE_STRUCTURES = {"node", "pointcrawl", "sandbox", "mystery", "hexcrawl"}
PLACEHOLDERS = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|XXX)\b|\[insert|\[name\]|\[placeholder", re.I)
STOCK_PHRASES = ["a testament to", "tapestry", "delve into", "palpable", "unbeknownst", "little do they know",
                 "little did they know", "ancient evil", "embark on", "nestled", "bustling", "shadowy figure",
                 "eldoria", "whispering woods", "the air is thick with", "sends shivers down", "a sense of foreboding",
                 "hauntingly beautiful", "steeped in", "rich tapestry", "in the heart of", "the fate of the realm",
                 "dark forces", "mysterious stranger", "eerie silence", "ominous", "otherworldly glow", "brimming with"]
SRD_ATTRIBUTION = ["System Reference Document 5.2.1", "creativecommons.org/licenses/by/4.0"]
SRD51_ATTRIBUTION = ["System Reference Document 5.1", "creativecommons.org/licenses/by/4.0"]
ORC_MARKERS = ["ORC License"]


BONES = False  # set by --bones: skip everything that needs written chapters, handouts or maps


class Report:
    def __init__(self):
        self.items = []

    def err(self, area, msg):
        self.items.append(("ERR", area, msg))

    def warn(self, area, msg):
        self.items.append(("WARN", area, msg))

    def ok(self, area, msg):
        self.items.append(("OK", area, msg))

    @property
    def errors(self):
        return [i for i in self.items if i[0] == "ERR"]


def load(root, rep):
    path = root / "campaign.json"
    if not path.exists():
        rep.err("structure", "campaign.json is missing")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        rep.err("structure", f"campaign.json is not valid JSON: {e}")
        return None


def read_dir(root, folder):
    d = root / folder
    return {f"{folder}/{p.name}": p.read_text(encoding="utf-8") for p in sorted(d.glob("*.md"))} if d.exists() else {}


def ids_unique(items, label, rep, area):
    seen = set()
    for it in items:
        i = it.get("id")
        if not i:
            rep.err(area, f"a {label} has no id: {json.dumps(it)[:80]}")
        elif i in seen:
            rep.err(area, f"duplicate {label} id {i!r}")
        seen.add(i)
    return seen


def party_size(c):
    p = c.get("players", {})
    n = p.get("count", 0)
    n += sum(1 for comp in p.get("companions", []) if comp.get("counts_as_character"))
    return n


# ---------------------------------------------------------------- sections

def check_basics(c, root, book, rep):
    for k in ("title", "slug", "system", "players", "nodes"):
        if k not in c:
            rep.err("structure", f"campaign.json: missing '{k}'")
    if c.get("system") not in SYSTEMS:
        rep.err("structure", f"system {c.get('system')!r} must be one of {sorted(SYSTEMS)}")
    p = c.get("players", {})
    if not isinstance(p.get("count"), int) or p.get("count", 0) < 1:
        rep.err("structure", "players.count must be a whole number of 1 or more")
    if not isinstance(p.get("level"), int) and c.get("system") != "other":
        rep.err("structure", "players.level must be a whole number (systems without levels: use system 'other' and players.party_label)")
    if c.get("mode", "standard") not in ("standard", "teach"):
        rep.err("structure", "mode must be 'standard' or 'teach'")
    if not book and not BONES:
        rep.err("structure", "book/ has no chapter files")


def check_graph(c, book_text, rep):
    nodes = c.get("nodes", [])
    node_ids = ids_unique(nodes, "node", rep, "structure")
    conclusions = c.get("conclusions", [])
    concl_ids = ids_unique(conclusions, "conclusion", rep, "clues")
    clues = c.get("clues", [])
    ids_unique(clues, "clue", rep, "clues")
    starts = [n["id"] for n in nodes if n.get("start")]
    if not starts:
        rep.err("structure", "no node has \"start\": true")
    edges = {n.get("id"): set() for n in nodes}
    incoming_lead = {n.get("id"): 0 for n in nodes}
    for n in nodes:
        for t in n.get("leads_to", []):
            if t not in node_ids:
                rep.err("structure", f"node {n['id']} leads_to unknown node {t!r}")
            else:
                edges[n["id"]].add(t)
                incoming_lead[t] += 1
        anchor = "{#" + str(n.get("id")) + "}"
        if anchor not in book_text and not BONES:
            rep.err("structure", f"node {n.get('id')} ({n.get('name', '?')}) has no heading with {anchor} in book/")
    incoming_clues = {nid: [] for nid in node_ids}
    concl_clues = {cid: [] for cid in concl_ids}
    for k in clues:
        where, target = k.get("in"), k.get("points_to")
        if where not in node_ids:
            rep.err("clues", f"clue {k.get('id')} is in unknown node {where!r}")
            continue
        if target in node_ids:
            incoming_clues[target].append(k)
            edges[where].add(target)
        elif target in concl_ids:
            concl_clues[target].append(k)
        else:
            rep.err("clues", f"clue {k.get('id')} points_to unknown node/conclusion {target!r}")
        if not k.get("text"):
            rep.warn("clues", f"clue {k.get('id')} has no text")
    seen, todo = set(starts), list(starts)
    while todo:
        cur = todo.pop()
        for nxt in edges.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    unreachable = [n for n in node_ids if n not in seen]
    if unreachable:
        rep.err("structure", "nodes nobody can reach from a start node: " + ", ".join(sorted(unreachable)))
    elif nodes:
        rep.ok("structure", f"{len(nodes)} nodes, all reachable from {', '.join(starts)}")
    for cid, ks in concl_clues.items():
        concl = next(x for x in conclusions if x.get("id") == cid)
        places = {k["in"] for k in ks}
        if concl.get("required", True):
            if len(ks) < 2:
                rep.err("clues", f"required conclusion {cid} has {len(ks)} clue(s); give it at least three (Three Clue Rule)")
            elif len(ks) < 3:
                rep.warn("clues", f"required conclusion {cid} has only 2 clues; aim for three")
            if len(places) < 2 and ks:
                rep.warn("clues", f"all clues for {cid} sit in one node ({next(iter(places))}); spread them out")
    structure = c.get("structure", "linear")
    if structure in NODE_STRUCTURES:
        known = {n["id"] for n in nodes if n.get("known")}
        for nid in node_ids:
            if nid in starts or nid in known:
                continue
            ways = incoming_lead.get(nid, 0) + len(incoming_clues[nid])
            if ways < 3:
                rep.warn("clues", f"node {nid} has {ways} way(s) in (leads plus clues); node-based design wants three. "
                                  "If the heroes simply know the place (their base, the town square), mark it \"known\": true")
    if conclusions:
        rep.ok("clues", f"{len(clues)} clues for {len(conclusions)} conclusions")
    endings = c.get("endings", [])
    if len(endings) < 2:
        rep.warn("structure", f"{len(endings)} ending(s) described; give at least a success and a failure/partial outcome")
    return node_ids


def usable_tiers(budgets, tiers):
    """Tiers whose budget rises above the previous one. Small PF2e parties lose some (solo Low is 0 XP)."""
    out, last = [], -1
    for t in tiers:
        if budgets[t] > last:
            out.append(t)
            last = budgets[t]
    return tuple(out)


def tier_for(total, budgets, tiers):
    for t in tiers:
        if total <= budgets[t]:
            return t
    return "beyond " + tiers[-1]


def check_encounters(c, node_ids, rep):
    system = c.get("system")
    level = c.get("players", {}).get("level")
    chars = party_size(c)
    encounters = c.get("encounters", [])
    ids_unique(encounters, "encounter", rep, "encounters")
    if not encounters:
        rep.warn("encounters", "no encounters listed; fine for a pure mystery or social game, otherwise add them")
        return
    base_level = level
    for e in encounters:
        eid = e.get("id", "?")
        level = e.get("party_level", base_level)
        if e.get("node") not in node_ids:
            rep.err("encounters", f"{eid}: node {e.get('node')!r} unknown")
        creatures = e.get("creatures", [])
        if not creatures and not e.get("hazards"):
            rep.err("encounters", f"{eid}: no creatures or hazards listed")
            continue
        n_chars = chars + e.get("allies_count", 0)
        claimed = str(e.get("difficulty", "")).lower()
        if system in ("dnd5e-2024", "dnd5e-2014"):
            if level not in DND_BUDGET:
                rep.err("encounters", f"party level {level} outside 1-20")
                return
            budgets = {t: DND_BUDGET[level][i] * n_chars for i, t in enumerate(DND_TIERS)}
            total, count = 0, 0
            for cr in creatures:
                crs, xp, k = str(cr.get("cr", "")), cr.get("xp"), cr.get("count", 1)
                if crs not in CR_XP:
                    rep.err("encounters", f"{eid}: {cr.get('name')} has CR {crs!r}, not a valid CR")
                    continue
                if xp is None:
                    xp = CR_XP[crs][-1]
                elif xp not in CR_XP[crs]:
                    rep.err("encounters", f"{eid}: {cr.get('name')} CR {crs} is worth {CR_XP[crs][-1]} XP, not {xp}")
                total += xp * k
                count += k
                if crs not in ("0", "1/8", "1/4", "1/2") and int(crs) > level:
                    rep.warn("encounters", f"{eid}: {cr.get('name')} (CR {crs}) is above party level {level}; "
                                           "SRD warns it can drop a character in one action")
            band = tier_for(total, budgets, DND_TIERS)
            if total < budgets["low"] / 2:
                rep.warn("encounters", f"{eid}: {total} XP is under half the Low budget ({budgets['low']}); "
                                       "likely trivial. Fine for a speed bump, otherwise add a creature or a twist")
            if count > 2 * n_chars and level <= 2:
                rep.warn("encounters", f"{eid}: {count} creatures vs {n_chars} level-{level} characters; use fragile creatures")
            if len({cr.get('name') for cr in creatures}) > 3:
                rep.warn("encounters", f"{eid}: more than three different stat blocks in one fight is hard to run")
            check_band(eid, claimed, band, total, budgets, DND_TIERS, e, rep)
        elif system == "pf2e":
            budgets = {t: PF_BUDGET[t] + PF_ADJUST[t] * (n_chars - 4) for t in PF_TIERS}
            tiers = usable_tiers(budgets, PF_TIERS)
            total = 0
            for hz in e.get("hazards", []):
                lvl, k = hz.get("level"), hz.get("count", 1)
                if not isinstance(lvl, int):
                    rep.err("encounters", f"{eid}: hazard {hz.get('name')} needs an integer 'level'")
                    continue
                diff = lvl - level
                if diff < -4:
                    continue  # GM Core: trivial, no XP
                if diff > 4:
                    rep.err("encounters", f"{eid}: hazard {hz.get('name')} is {diff:+d} vs the party; keep hazards within +4")
                    continue
                complex_ = hz.get("complexity", "simple") == "complex"
                total += PF_HAZARD_XP[diff][1 if complex_ else 0] * k
            for cr in creatures:
                lvl, k = cr.get("level"), cr.get("count", 1)
                if not isinstance(lvl, int):
                    rep.err("encounters", f"{eid}: {cr.get('name')} needs an integer 'level'")
                    continue
                diff = lvl - level
                if diff not in PF_CREATURE_XP:
                    rep.err("encounters", f"{eid}: {cr.get('name')} is level {lvl}, {diff:+d} vs the party; "
                                          "GM Core keeps creatures within -4..+4")
                    continue
                total += PF_CREATURE_XP[diff] * k
            band = tier_for(total, budgets, tiers)
            if claimed in PF_TIERS and claimed not in tiers:
                rep.warn("encounters", f"{eid}: labelled {claimed!r}, but for {n_chars} character(s) GM Core's "
                                       f"{claimed} budget ({budgets[claimed]}) isn't above the tier below it; "
                                       f"use one of: {', '.join(tiers)}")
                claimed = band
            check_band(eid, claimed, band, total, budgets, tiers, e, rep)
        else:
            if not claimed:
                rep.warn("encounters", f"{eid}: say how hard it is meant to be ('difficulty')")


def check_band(eid, claimed, band, total, budgets, tiers, e, rep):
    budget_txt = ", ".join(f"{t} {budgets[t]}" for t in tiers)
    msg = f"{eid}: {total} XP vs budgets ({budget_txt}) = {band}"
    if band.startswith("beyond"):
        if e.get("over_budget_reason"):
            rep.warn("encounters", msg + f"; over budget on purpose: {e['over_budget_reason']}")
        else:
            rep.err("encounters", msg + "; cut creatures, or add over_budget_reason and an escape route in the text")
    elif claimed and claimed != band:
        rep.warn("encounters", msg + f", but it is labelled {claimed!r}")
    else:
        rep.ok("encounters", msg)


def check_teach(c, root, node_ids, book_text, rep):
    t = c.get("teach")
    if not t:
        rep.err("teach", "mode is 'teach' but campaign.json has no 'teach' block")
        return
    if not t.get("subject"):
        rep.err("teach", "teach.subject is missing")
    objectives = t.get("objectives", [])
    obj_ids = ids_unique(objectives, "objective", rep, "teach")
    style = t.get("style")
    if style not in ("stealth", "open"):
        if style is not None:
            rep.err("teach", f"teach.style must be 'stealth' or 'open', not {style!r}")
        else:
            rep.warn("teach", "teach.style isn't set; choose 'stealth' (learning hidden in play, the default) or 'open' "
                              "(classroom, tutor, quiz me). Treating it as open")
        style = "open"
    stealth = style == "stealth"
    if stealth:
        if not 2 <= len(objectives) <= 5:
            rep.warn("teach", f"{len(objectives)} objectives; Stealth wants 2-5 in total. More is a syllabus: cut some or save them for a sequel")
    elif not 2 <= len(objectives) <= 8:
        rep.warn("teach", f"{len(objectives)} objectives; aim for 2-4 in a one-shot, 3-6 over a few sessions, up to 8 in a campaign")
    beats = t.get("beats", [])
    puzzles = t.get("puzzles", [])
    puzzle_ids = ids_unique(puzzles, "puzzle", rep, "teach")
    kinds = {o: set() for o in obj_ids}
    for b in beats:
        if b.get("objective") not in obj_ids:
            rep.err("teach", f"beat {b.get('id')} names unknown objective {b.get('objective')!r}")
            continue
        if b.get("node") not in node_ids:
            rep.err("teach", f"beat {b.get('id')} is in unknown node {b.get('node')!r}")
        if b.get("kind") not in ("introduce", "practice", "assess"):
            rep.err("teach", f"beat {b.get('id')} kind must be introduce, practice or assess")
        if b.get("puzzle") and b["puzzle"] not in puzzle_ids:
            rep.err("teach", f"beat {b.get('id')} names unknown puzzle {b['puzzle']!r}")
        if b.get("kind") in ("practice", "assess") and not b.get("puzzle") and not b.get("activity"):
            rep.warn("teach", f"beat {b.get('id')} ({b.get('kind')}) has no puzzle or activity; practice and assessment "
                              "should be something the player does (add \"puzzle\" or describe it in \"activity\")")
        kinds[b["objective"]].add(b.get("kind"))
    for o in objectives:
        missing = {"introduce", "practice", "assess"} - kinds.get(o.get("id"), set())
        if missing:
            rep.err("teach", f"objective {o.get('id')} is never {', '.join(sorted(missing))}d in play")
        if not o.get("misconception"):
            rep.warn("teach", f"objective {o.get('id')} names no misconception to provoke and correct")
    for p in puzzles:
        pid = p.get("id")
        if p.get("node") not in node_ids:
            rep.err("teach", f"puzzle {pid} is in unknown node {p.get('node')!r}")
        hints = p.get("hints", [])
        if len(hints) < 3:
            rep.err("teach", f"puzzle {pid} has {len(hints)} hints; write a three-step hint ladder")
        if not p.get("answer"):
            rep.err("teach", f"puzzle {pid} has no answer")
        elif plain(p["answer"]) not in plain(book_text):
            rep.warn("teach", f"puzzle {pid}: answer {p['answer']!r} doesn't appear word for word in the book (GM can't check it)")
        if "value" in p:
            if not p.get("script"):
                rep.warn("teach", f"puzzle {pid}: answer not recomputed by a script")
            else:
                check_script(root, p, rep)
        if p.get("in_world_consequence") is None:
            rep.warn("teach", f"puzzle {pid}: say what happens in the fiction on a wrong answer (in_world_consequence)")
    if stealth and node_ids:
        # Only beats with a puzzle count: a puzzle is the part that feels like homework. Activity beats (the world
        # reacts to what the hero does) are free.
        lesson_nodes = {b.get("node") for b in beats if b.get("puzzle") and b.get("node") in node_ids}
        share = len(lesson_nodes) / len(node_ids)
        if share > 0.4 + 1e-9:
            rep.warn("teach", f"puzzles sit in {len(lesson_nodes)} of {len(node_ids)} nodes ({share:.0%}); Stealth wants "
                              "about a third, and warns above 40%. Turn some into activity beats (the world reacts, no "
                              "question), fold them into scenes that already hold one, or add adventure scenes")
        if not BONES and not re.search(r"^#{1,4}\s+.*\bdecoder\b", book_text, re.I | re.M):
            rep.err("teach", "Stealth style needs a 'Decoder' section in the Learning Guide (what the player did, and what it's "
                             "really called, one block per session)")
        if not t.get("lexicon"):
            rep.warn("teach", "Stealth style but no teach.lexicon; list the real jargon and slang so the checker can keep it "
                              "out of what the player reads")
    elif not stealth and not BONES and not re.search(r"^#{1,4}\s+.*\bdebrief\b", book_text, re.I | re.M):
        rep.warn("teach", "Open style: add debrief questions to the Learning Guide")
    check_lexicon_fields(t, node_ids, rep)
    sources = t.get("sources", [])
    covered = set()
    for s in sources:
        if not s.get("url") and not s.get("citation"):
            rep.err("teach", f"source {s.get('title')!r} has no url or citation")
        covered |= set(s.get("covers", []))
    for o in obj_ids - covered:
        rep.err("teach", f"objective {o} has no source in teach.sources[].covers")
    if not kinds or all(not v for v in kinds.values()):
        return
    rep.ok("teach", f"{len(objectives)} objectives, {len(beats)} beats, {len(puzzles)} puzzles, {len(sources)} sources")


LEX_KINDS = ("jargon", "slang")
PLAYER_BOXES = re.compile(r"^```(?:letter|poem|sign)\b[^\n]*\n(.*?)^```", re.S | re.M)
QUOTED = re.compile(r'"[^"\n]*"|\u201c[^\u201d]*\u201d')


def check_lexicon_fields(t, node_ids, rep):
    seen = set()
    for i, e in enumerate(t.get("lexicon", [])):
        real = (e.get("real") or "").strip()
        if not real:
            rep.err("teach", f"lexicon entry {i + 1} has no 'real' term")
            continue
        if real.lower() in seen:
            rep.warn("teach", f"lexicon lists {real!r} twice")
        seen.add(real.lower())
        if e.get("kind") not in LEX_KINDS:
            rep.err("teach", f"lexicon entry {real!r}: kind must be 'jargon' or 'slang'")
        if e.get("first_node") and e["first_node"] not in node_ids:
            rep.err("teach", f"lexicon entry {real!r}: first_node {e['first_node']!r} is not a node")


def player_text_of_book(book):
    """What a player reads inside the GM book: read-aloud (> lines) and letter, poem and sign boxes."""
    out = {}
    for name, text in book.items():
        parts = [m.group(1) for m in PLAYER_BOXES.finditer(text)]
        text = PLAYER_BOXES.sub("", text)
        parts += [ln.strip()[1:] for ln in text.splitlines() if ln.strip().startswith(">")]
        if parts:
            out[name + " (read-aloud and boxed documents)"] = "\n".join(parts)
    return out


def check_lexicon(c, book, player_docs, found, rep):
    t = c.get("teach") or {}
    if t.get("style") != "stealth":
        return
    entries = [e for e in t.get("lexicon", []) if (e.get("real") or "").strip() and e.get("kind") in LEX_KINDS]
    if not entries:
        return
    docs = {}
    for name, text in {**player_docs, **found}.items():
        if "decoder" in name.lower():  # the opt-in Decoder handout is the one player document allowed the real terms
            continue
        docs[name] = re.sub(r"```gm.*?```", "", text, flags=re.S)
    docs.update(player_text_of_book(book))
    docs["the title and tagline (they are printed on every cover)"] = " ".join([c.get("title", ""), c.get("tagline", "")])
    bad = 0
    for name, text in docs.items():
        unquoted = QUOTED.sub(" ", text)
        for e in entries:
            term = e["real"].strip()
            pat = re.compile(r"(?<![\w])" + re.escape(term) + r"(?:s|es)?(?![\w])", re.I)
            hay = text if e["kind"] == "jargon" else unquoted
            m = pat.search(hay)
            if m:
                where = "anywhere" if e["kind"] == "jargon" else "outside quotation marks"
                fix = ("use the world's word " + repr(e["world"])) if e.get("world") else (
                    "give it a world word in teach.lexicon and use that" if e["kind"] == "jargon"
                    else "only a character may say it, inside quotation marks")
                rep.err("teach", f"{name} uses the real term {term!r} ({where}); in Stealth style, {fix}")
                bad += 1
    if not bad:
        rep.ok("teach", f"lexicon: {len(entries)} real terms kept out of {len(docs)} player-facing texts")


def plain(text):
    """Text without markdown emphasis, with collapsed spaces and straight quotes, for answer matching."""
    text = re.sub(r"[*_`]", "", text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return " ".join(text.split()).lower()


def check_script(root, p, rep):
    script = root / p["script"]
    if not script.exists():
        rep.err("teach", f"puzzle {p['id']}: script {p['script']} not found")
        return
    try:
        res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        rep.err("teach", f"puzzle {p['id']}: script timed out")
        return
    lines = [ln for ln in res.stdout.strip().splitlines() if ln.strip()]
    if res.returncode != 0 or not lines:
        rep.err("teach", f"puzzle {p['id']}: script failed: {res.stderr.strip()[-300:]}")
        return
    from fractions import Fraction
    value = p["value"]
    if isinstance(value, str):
        last = lines[-1].strip()
        try:  # a fraction like "1/3" is compared exactly
            ok = Fraction(value.strip()) == Fraction(last.split()[0])
        except (ValueError, ZeroDivisionError):
            ok = plain(last) == plain(value)
        if ok:
            rep.ok("teach", f"puzzle {p['id']}: answer {value!r} recomputed exactly")
        else:
            rep.err("teach", f"puzzle {p['id']}: book says {value!r}, script prints {last!r}")
        return
    try:
        got = float(lines[-1].split()[0])
    except ValueError:
        rep.err("teach", f"puzzle {p['id']}: script's last line should start with the number, got {lines[-1]!r}")
        return
    want = float(value)
    if "tolerance_abs" in p:
        slack = float(p["tolerance_abs"])
    else:
        slack = abs(want) * float(p.get("tolerance", 0.02))
    lo, hi = want - slack, want + slack
    if not lo - 1e-9 <= got <= hi + 1e-9:
        rep.err("teach", f"puzzle {p['id']}: book says {want}, script computes {got:g} (accepted range {lo:g} to {hi:g})")
    else:
        rep.ok("teach", f"puzzle {p['id']}: answer {want:g} recomputed as {got:g}; accept {lo:.3g} to {hi:.3g}")


def check_spoilers(c, root, player_docs, rep):
    terms = [t for t in c.get("spoiler_terms", []) if t.strip()]
    if not terms:
        aud = c.get("audience", {})
        if aud.get("requester_plays") or aud.get("protect_players") or c.get("mode") == "teach":
            rep.err("spoilers", "players must be protected (requester plays, protect_players or Teach mode), but spoiler_terms "
                                "is empty; list the secrets and answers to keep out of player material")
        else:
            rep.warn("spoilers", "spoiler_terms is empty; list the twist names/secrets so player material can be checked")
        return
    leaks = 0
    for name, text in player_docs.items():
        low = text.lower()
        for t in terms:
            if t.lower() in low:
                rep.err("spoilers", f"{name} contains spoiler term {t!r}")
                leaks += 1
    for spec_path in sorted((root / "maps").glob("*.json")) if (root / "maps").exists() else []:
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        visible = [spec.get("player_title", spec.get("title", "")), spec.get("subtitle", "")]
        visible += [n.get("name", "") for n in spec.get("nodes", []) if not n.get("hidden")]
        visible += [r.get("name", "") for r in spec.get("rooms", []) if not r.get("hidden")]
        visible += [e.get("label", "") for e in spec.get("edges", []) if not e.get("hidden")]
        visible += [lab.get("text", "") for lab in spec.get("labels", []) if not lab.get("gm")]
        visible += [a.get("label", "") for a in spec.get("areas", [])]
        visible += [f.get("text", "") for f in spec.get("features", []) if not f.get("gm") and f.get("type") != "trap"]
        for t in terms:
            if any(t.lower() in v.lower() for v in visible if v):
                rep.err("spoilers", f"player map {spec_path.name} shows spoiler term {t!r}")
                leaks += 1
    if not leaks:
        rep.ok("spoilers", f"{len(terms)} spoiler terms absent from {len(player_docs)} player documents and player maps")


def check_writing(c, book, all_docs, rep):
    for name, text in all_docs.items():
        for m in PLACEHOLDERS.finditer(text):
            rep.err("writing", f"{name}: placeholder text {m.group(0)!r}")
    long_reads = 0
    for name, text in book.items():
        block = []
        for ln in text.splitlines() + [""]:
            if ln.strip().startswith(">"):
                block.append(ln.strip()[1:])
            elif block:
                words = len(" ".join(block).split())
                if words > 90:
                    long_reads += 1
                    rep.warn("writing", f"{name}: read-aloud of {words} words ('{' '.join(block)[:50].strip()}...'); keep it under 90")
                block = []
    joined = "\n".join(all_docs.values()).lower()
    hits = {p: joined.count(p) for p in STOCK_PHRASES if p in joined}
    total = sum(hits.values())
    if total >= 4:
        rep.warn("writing", f"stock phrasing {total} times: " + ", ".join(f"{k} x{v}" for k, v in sorted(hits.items(), key=lambda x: -x[1])))
    # Prose words: skip tables, stat blocks and the Learning Guide; count "1/8" as one word.
    prose = []
    for name, text in book.items():
        if re.search(r"^#\s+Learning Guide", text, re.M):
            continue
        text = re.sub(r"```statblock.*?```", "", text, flags=re.S)
        prose.append("\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("|")))
    words = len(re.findall(r"[\w/'.-]+", "\n".join(prose)))
    sessions = c.get("length", {}).get("sessions") or 1
    guide = 10000 if sessions == 1 else 5000 * sessions
    rep.ok("writing", f"book prose is about {words:,} words (tables, stat blocks and Learning Guide excluded); "
                      f"{long_reads} long read-aloud blocks")
    if words < guide * 0.4:
        rep.warn("writing", f"{words:,} words of prose for {sessions} session(s) looks thin (guide about {guide:,}); "
                            "check every node has what's here, what's hidden and what happens")
    if words > guide * 1.25:
        rep.warn("writing", f"{words:,} words of prose for {sessions} session(s); the guide is up to about {guide:,}. "
                            "Cut repetition, or say in the README why it's longer")
    system = c.get("system")
    text = "\n".join(all_docs.values())
    if system == "dnd5e-2024" and c.get("uses_srd", True):
        if not all(s in text for s in SRD_ATTRIBUTION):
            rep.err("writing", "uses SRD 5.2.1 content but the credits lack the required attribution statement (see systems/dnd5e.md)")
    if system == "dnd5e-2014" and c.get("uses_srd", True):
        if not all(s in text for s in SRD51_ATTRIBUTION):
            rep.err("writing", "uses SRD 5.1 content but the credits lack the CC-BY-4.0 attribution (see systems/dnd5e.md)")
    if system == "pf2e" and c.get("uses_srd", True):
        if not all(s in text for s in ORC_MARKERS):
            rep.err("writing", "uses Pathfinder rules content but the credits lack the ORC License notice (see systems/pf2e.md)")
    marker = c.get("licence_marker")
    if marker and marker not in text:
        rep.err("writing", f"licence_marker {marker!r} (the required notice) doesn't appear in the credits")


def check_crossrefs(c, book_text, player_docs, rep):
    """Encounter creatures named in the book; GM ids (N3, C1, E2) kept out of player material."""
    low = book_text.lower()
    for e in c.get("encounters", []):
        for cr in e.get("creatures", []) + e.get("hazards", []):
            name = str(cr.get("name", ""))
            # "Zombie (the drowned)" or "Hester Vane (Pirate Captain)": either part named in the book is enough
            parts = [name] + [p_.strip() for p_ in re.split(r"[()]", name) if p_.strip()]
            parts += [re.sub(r"^(the|a|an)\s+", "", p_, flags=re.I) for p_ in parts]
            if name and not any(p_.lower() in low for p_ in parts if len(p_) > 2):
                rep.warn("encounters", f"{e.get('id')}: {name!r} is in campaign.json but never named in the book (stat block?)")
    ids = [x.get("id") for key in ("nodes", "conclusions", "encounters", "clues") for x in c.get(key, []) if x.get("id")]
    if ids:
        pat = re.compile(r"\b(" + "|".join(re.escape(i) for i in sorted(set(ids), key=len, reverse=True)) + r")\b")
        for name, text in player_docs.items():
            text = re.sub(r"```gm.*?```", "", text, flags=re.S)  # GM boxes never reach players
            m = pat.search(text)
            if m:
                rep.warn("spoilers", f"{name} mentions the GM id {m.group(1)!r}; ids mean nothing to players, use names")


def check_maps(c, root, book_text, rep):
    import map_svg
    specs = sorted((root / "maps").glob("*.json")) if (root / "maps").exists() else []
    for sp in specs:
        try:
            spec = json.loads(sp.read_text(encoding="utf-8"))
            if spec.get("kind") == "dungeon":
                m = map_svg.dungeon_model(spec, sp.name)
                if m["unreachable"]:
                    rep.err("maps", f"{sp.name}: areas with no door or opening to the start: {', '.join(m['unreachable'])}")
            mid = spec.get("id")
            if mid and f"map:{mid}" not in book_text and not BONES:
                rep.warn("maps", f"{sp.name}: map {mid} is never shown in the book (![caption](map:{mid}){{wide}})")
        except (json.JSONDecodeError, map_svg.SpecError) as e:
            rep.err("maps", f"{sp.name}: {e}")
    ids = set()
    for sp in specs:
        try:
            ids.add(json.loads(sp.read_text(encoding="utf-8")).get("id"))
        except json.JSONDecodeError:
            pass
    refs = ([c["cover_map"]] if c.get("cover_map") else []) + list(c.get("player_maps", [])) + list(c.get("maps", []))
    for ref in dict.fromkeys(refs):
        if ref not in ids and not BONES:
            rep.err("maps", f"campaign.json names map {ref!r}, but no maps/*.json has that id")
    if specs:
        rep.ok("maps", f"{len(specs)} map specs")
    elif c.get("table", {}).get("maps", True) and not BONES:
        rep.warn("maps", "no maps; add at least the key locations unless the table plays theatre-of-the-mind")


def check_npcs(c, node_ids, book_text, rep):
    npcs = c.get("npcs", [])
    ids_unique(npcs, "npc", rep, "structure")
    for n in npcs:
        for a in n.get("appears", []):
            if a not in node_ids:
                rep.err("structure", f"npc {n.get('id')} appears in unknown node {a!r}")
        if n.get("name") and n["name"] not in book_text and not BONES:
            rep.warn("structure", f"npc {n['name']} is listed but never named in the book")
        if not n.get("wants"):
            rep.warn("structure", f"npc {n.get('name', n.get('id'))} has no 'wants'; give every NPC a goal")


def run(root):
    root = Path(root).resolve()
    rep = Report()
    c = load(root, rep)
    if c is None:
        return rep
    book = read_dir(root, "book")
    handouts = read_dir(root, "handouts")
    found = read_dir(root, "handouts/found")
    pregens = read_dir(root, "pregens")
    book_text = "\n".join(book.values())
    check_basics(c, root, book, rep)
    node_ids = check_graph(c, book_text, rep)
    check_npcs(c, node_ids, book_text, rep)
    check_encounters(c, node_ids, rep)
    if c.get("mode") == "teach":
        check_teach(c, root, node_ids, book_text, rep)
    player_docs = dict(handouts)
    player_docs.update(pregens)
    if BONES:
        check_maps(c, root, book_text, rep)
        rep.ok("structure", "--bones: chapters, handouts, licence and spoiler checks skipped; run without --bones before hand-over")
        return rep
    if not handouts:
        rep.warn("writing", "no handouts/; published adventures ship at least a player pitch or one handout")
    check_spoilers(c, root, player_docs, rep)
    if c.get("mode") == "teach":
        check_lexicon(c, book, player_docs, found, rep)
    all_docs = dict(book)
    all_docs.update(player_docs)
    all_docs.update(found)  # found-in-play documents: placeholder and phrasing checks, not spoiler checks
    check_crossrefs(c, book_text, {**player_docs, **found}, rep)
    check_writing(c, book, all_docs, rep)
    check_maps(c, root, book_text, rep)
    return rep


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    global BONES
    BONES = "--bones" in argv
    rep = run(args[0])
    if "--json" in argv:
        print(json.dumps([{"level": l, "area": a, "message": m} for l, a, m in rep.items], indent=1))
    else:
        order = {"ERR": 0, "WARN": 1, "OK": 2}
        for level, area, msg in sorted(rep.items, key=lambda x: order[x[0]]):
            print(f"{level:<4} [{area}] {msg}")
        n_err = len(rep.errors)
        n_warn = sum(1 for i in rep.items if i[0] == "WARN")
        print(f"\n{n_err} error(s), {n_warn} warning(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
