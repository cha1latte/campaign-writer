"""Build a campaign folder into a print-ready GM book and player handouts (HTML + PDF).

    python build_book.py <campaign-folder> [--no-pdf] [--no-png] [--a4]

Reads   campaign.json, book/*.md (sorted), handouts/*.md, handouts/found/*.md, pregens/*.md, maps/*.json
Writes  build/<slug>-gm-book.html/.pdf        the GM book
        build/<slug>-handouts.html/.pdf       player-safe from the start: pitch, reference cards, pregens, player maps
        build/<slug>-found-in-play.html/.pdf  in-world clue documents the GM hands over when found (if any)
        build/maps/*                          every map, re-rendered (PNG too, unless --no-png)
Prints  page counts, and WARN lines for anything that needs a look (stray asterisks, handouts spilling over a page).

Markdown subset (full table in references/writing-the-book.md):
  # Chapter            one per book file; starts a new page
  ## Heading {#N3}     anchor id; node headings must carry their node id
  > read-aloud         boxed read-aloud
  ```statblock / ```sidebar Title / ```lesson Title / ```gm Title / ```tip Title / ```write 5
  | tables |, - lists, 1. lists, **bold**, *italic* (works inside formulas: *h* = ½*gt*²), `code`, [links](#N3), \\* for a literal asterisk
  A line starting with **Label** always starts a new paragraph, so field-per-line templates stay readable.
  ![Caption](map:m1){wide}   map across both columns (best at the start of a chapter or after \\pagebreak)
  ![Caption](map:m1){page}   map on its own full page (a plate); text continues on the next page
  \\pagebreak                 new page (columns restart)
  [one-action] [two-actions] [three-actions] [reaction] [free-action]   PF2e action icons
Standard library only.
"""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
TEMPLATES = HERE.parent / "templates"

SYSTEM_NAMES = {"dnd5e-2024": "5E compatible (2024 rules)", "dnd5e-2014": "5E compatible (2014 rules)",
                "pf2e": "Compatible with Pathfinder Second Edition", "other": ""}
BREAK = "\x01BREAK\x01"
PLATE = "\x01PLATE\x01"


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- inline markdown

def _diamond(x, filled=True):
    return (f'<path d="M{x+5},1 L{x+9},5 L{x+5},9 L{x+1},5 Z" fill="{"currentColor" if filled else "none"}" '
            f'stroke="currentColor" stroke-width="1.3"/>')


def _icon(n=1, kind="action"):
    if kind == "reaction":
        body = ('<path d="M2,7 A4,4 0 1 1 8,7" fill="none" stroke="currentColor" stroke-width="1.6"/>'
                '<path d="M6.2,5.2 L8.4,7.6 L10,4.8" fill="none" stroke="currentColor" stroke-width="1.4"/>')
        w = 11
    elif kind == "free":
        body, w = _diamond(0, filled=False), 10
    else:
        body, w = "".join(_diamond(i * 8) for i in range(n)), 8 * n + 2
    return (f'<svg class="act" viewBox="0 0 {w} 10" width="{w * 1.05:.1f}pt" height="10.5pt" aria-hidden="true">{body}</svg>')


ACTION_ICONS = {"[one-action]": _icon(1), "[two-actions]": _icon(2), "[three-actions]": _icon(3),
                "[reaction]": _icon(kind="reaction"), "[free-action]": _icon(kind="free")}


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "section"


def smart_quotes(text):
    """Straight quotes to typographic ones (code spans and tags are handled by the caller)."""
    text = re.sub(r'(^|[\s(\[{\u2014\u2013-])"', "\\1\u201c", text)
    text = text.replace('"', "\u201d")
    text = re.sub(r"(^|[\s(\[{\u2014\u2013-])'", "\\1\u2018", text)
    return text.replace("'", "\u2019")


def inline(text):
    text = text.replace("\\*", "\x02")
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes)-1}\x00"
    text = re.sub(r"`([^`]+)`", keep_code, text)
    links = []

    def keep_link(m):
        links.append(m.group(2))
        return f"[{m.group(1)}](\x03{len(links)-1}\x03)"
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", keep_link, text)
    text = smart_quotes(text)
    text = re.sub(r"\x03(\d+)\x03", lambda m: links[int(m.group(1))], text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: "`" + codes[int(m.group(1))] + "`", text)
    text = html.escape(text, quote=False)
    codes = []

    def keep_code(m):
        codes.append(m.group(1))
        return f"\x00{len(codes)-1}\x00"
    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{html.escape(m.group(2))}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
    # Italic asterisks may touch digits, superscripts and symbols, so formulas like *h* = ½*gt*² work.
    text = re.sub(r"(?<!\*)\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<![\w_])_(?=\S)(.+?)(?<=\S)_(?![\w_])", r"<em>\1</em>", text)
    for k, v in ACTION_ICONS.items():
        text = text.replace(k, v)
    text = text.replace("→", '<span class="sym">→</span>').replace("←", '<span class="sym">←</span>')
    text = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", text)
    return text.replace("\x02", "*")


# ---------------------------------------------------------------- block markdown

class Ctx:
    def __init__(self, root, audience, maps):
        self.root = root            # campaign folder
        self.audience = audience    # "gm" or "player"
        self.maps = maps            # map id -> {"gm": path, "player": path}
        self.toc = []               # (level, id, text)
        self.ids = set()
        self.problems = []


def heading_id(text, ctx):
    m = re.search(r"\s*\{#([A-Za-z0-9_-]+)\}\s*$", text)
    if m:
        hid, text = m.group(1), text[:m.start()]
    else:
        hid = slug(text)
    base, n = hid, 2
    while hid in ctx.ids:
        hid = f"{base}-{n}"
        n += 1
    ctx.ids.add(hid)
    return hid, text.strip()


def image_html(alt, src, mode, ctx, where):
    if src.startswith("map:"):
        mid = src[4:]
        if mid not in ctx.maps:
            ctx.problems.append(f"{where}: map {mid!r} not found in maps/")
            return ""
        path = ctx.maps[mid]["gm" if ctx.audience == "gm" else "player"]
    else:
        path = (ctx.root / src).resolve()
        if not path.exists():
            ctx.problems.append(f"{where}: image {src!r} not found")
            return ""
    cls = {"wide": "fig wide", "page": "fig plate-fig", "": "fig"}[mode]
    return (f'<figure class="{cls}"><img src="{path.as_uri()}" alt="{html.escape(alt)}">'
            f'<figcaption>{inline(alt)}</figcaption></figure>')


def render_table(lines):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    if len(rows) >= 2 and all(re.fullmatch(r":?-{2,}:?", c) for c in rows[1]):
        head, body = rows[0], rows[2:]
    else:
        head, body = None, rows
    out = ["<table>"]
    if head:
        out.append("<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>")
    out.append("<tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c) or '&nbsp;'}</td>" for c in r) + "</tr>" for r in body)
               + "</tbody></table>")
    return "".join(out)


def render_statblock(body, where, ctx):
    lines = [ln.rstrip() for ln in body]
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        ctx.problems.append(f"{where}: empty statblock")
        return ""
    out = ['<div class="statblock">', f'<div class="sb-name">{inline(lines[0].strip())}</div>']
    rest = lines[1:]
    if rest and rest[0].strip() and not rest[0].startswith(("---", "##", "|")):
        out.append(f'<div class="sb-meta">{inline(rest[0].strip())}</div>')
        rest = rest[1:]
    i = 0
    while i < len(rest):
        s = rest[i].strip()
        if not s:
            i += 1
            continue
        if s.startswith("---"):
            out.append('<div class="sb-rule"></div>')
        elif s.startswith("## "):
            out.append(f'<div class="sb-head">{inline(s[3:])}</div>')
        elif s.startswith("|"):
            tbl = []
            while i < len(rest) and rest[i].strip().startswith("|"):
                tbl.append(rest[i])
                i += 1
            out.append(render_table(tbl))
            continue
        else:
            out.append(f"<p>{inline(s)}</p>")
        i += 1
    out.append("</div>")
    return "".join(out)


def keep_with_next(blocks):
    """Wrap each sub-heading with the block after it so a heading never ends a column alone."""
    out = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        label_only = re.fullmatch(r"<p><strong>[^<]{1,60}</strong></p>", b)  # "**What's hidden.**" on its own line
        if ((re.match(r"<h[2-4]\b", b) or label_only) and nxt and not nxt.startswith(("<h", BREAK, PLATE))
                and len(re.sub(r"<[^>]+>", "", nxt)) < 1400):
            out.append(f'<div class="keep">{b}{nxt}</div>')
            i += 2
            continue
        out.append(b)
        i += 1
    return out


def render_blocks(text, ctx, where):
    lines = text.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    para = []

    def flush():
        if para:
            # A line ending in a backslash keeps its line break (verse, letters, addresses).
            joined = ""
            for k, p_ in enumerate(para):
                p_ = p_.strip()
                hard = p_.endswith("\\")
                joined += inline(p_[:-1].rstrip() if hard else p_) + ("<br>" if hard else ("" if k == len(para) - 1 else " "))
            out.append(f"<p>{joined}</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if not s:
            flush()
            i += 1
            continue
        if s.startswith("```"):
            flush()
            info = s[3:].strip()
            kind, _, title = info.partition(" ")
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                ctx.problems.append(f"{where}: unclosed ``` block ({info or 'code'})")
            i += 1
            if kind == "statblock":
                out.append(render_statblock(body, where, ctx))
            elif kind == "write":
                n = int(title) if title.strip().isdigit() else 4
                out.append('<div class="write-lines">' + '<div class="wl"></div>' * n + "</div>")
            elif kind in ("poem", "letter"):
                # Every line kept as written: songs, verse, letters, inscriptions.
                paras, cur = [], []
                for ln_ in body + [""]:
                    if ln_.strip():
                        cur.append(inline(ln_.strip()))
                    elif cur:
                        paras.append("<p>" + "<br>".join(cur) + "</p>")
                        cur = []
                head = f'<div class="box-title">{inline(title)}</div>' if title else ""
                out.append(f'<div class="{kind}">{head}{"".join(paras)}</div>')
            elif kind == "sign":
                inner = "\n".join(render_blocks("\n".join(body), ctx, where))
                head = f'<div class="sign-title">{inline(title)}</div>' if title else ""
                out.append(f'<div class="sign">{head}{inner}</div>')
            elif kind in ("sidebar", "lesson", "gm", "tip"):
                if kind == "gm" and ctx.audience != "gm":
                    continue
                label = {"lesson": "Lesson", "gm": "GM only", "tip": "Tip", "sidebar": ""}[kind]
                inner = "\n".join(render_blocks("\n".join(body), ctx, where))
                head = f'<div class="box-title">{inline(title) if title else label}</div>' if (title or label) else ""
                tag = f'<div class="box-tag">{label}</div>' if label and title else ""
                # Long boxes may split across columns; otherwise they jump whole and leave gaps.
                long_ = " long" if len(re.sub(r"<[^>]+>", "", inner)) > 500 else ""
                out.append(f'<div class="box {kind}{long_}">{tag}{head}{inner}</div>')
            else:
                out.append(f"<pre><code>{html.escape(chr(10).join(body))}</code></pre>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            flush()
            level = len(m.group(1))
            hid, txt = heading_id(m.group(2), ctx)
            if level <= 2:
                ctx.toc.append((level, hid, txt))
            out.append(f'<h{level} id="{hid}">{inline(txt)}</h{level}>')
            i += 1
            continue
        if s in ("\\pagebreak", "<!-- pagebreak -->"):
            flush()
            out.append(BREAK)
            i += 1
            continue
        if re.fullmatch(r"-{3,}|\*{3,}", s):
            flush()
            out.append("<hr>")
            i += 1
            continue
        m = re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)\)(\{(wide|page)\})?", s)
        if m:
            flush()
            mode = m.group(4) or ""
            fig = image_html(m.group(1), m.group(2), mode, ctx, where)
            out.append(PLATE + fig if mode == "page" else fig)
            i += 1
            continue
        if s.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            paras = "\n".join(quote).split("\n\n")
            out.append('<div class="readaloud">' + "".join(f"<p>{inline(' '.join(p.split()))}</p>" for p in paras if p.strip()) + "</div>")
            continue
        if s.startswith("|"):
            flush()
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append(render_table(tbl))
            continue
        if re.match(r"^([-*+]|\d+[.)])\s+", s):
            flush()
            ordered = bool(re.match(r"^\d", s))
            items = []
            base_indent = len(ln) - len(ln.lstrip())
            while i < len(lines) and lines[i].strip():
                cur = lines[i]
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", cur)
                if mm and items and len(mm.group(1)) <= base_indent and bool(re.match(r"\d", mm.group(2))) != ordered:
                    break  # a different kind of list starts here
                if mm:
                    items.append([len(mm.group(1).replace("\t", "    ")), mm.group(3)])
                elif cur.strip().startswith(("**", ">", "```", "#", "|")) and len(cur) - len(cur.lstrip()) <= base_indent:
                    break  # an unindented **Label**, quote, box, heading or table ends the list
                elif items:
                    items[-1][1] += " " + cur.strip()
                i += 1
            first = re.match(r"^\s*(\d+)", ln)
            out.append(render_list(items, ordered, int(first.group(1)) if ordered and first else 1))
            continue
        if s.startswith("<"):
            flush()
            out.append(ln)
            i += 1
            continue
        if s.startswith("**") and para:
            flush()  # a bold label starts its own paragraph
        para.append(ln)
        i += 1
    flush()
    return keep_with_next(out)


def render_list(items, ordered, start=1):
    tag = "ol" if ordered else "ul"
    out = [f'<{tag} start="{start}">' if ordered and start != 1 else f"<{tag}>"]
    base = items[0][0] if items else 0
    i = 0
    while i < len(items):
        indent, txt = items[i]
        sub = []
        j = i + 1
        while j < len(items) and items[j][0] > base:
            sub.append(items[j])
            j += 1
        out.append(f"<li>{inline(txt)}")
        if sub:
            out.append(render_list(sub, False))
        out.append("</li>")
        i = j
    out.append(f"</{tag}>")
    return "".join(out)


def sections(blocks, cls, data):
    """Turn rendered blocks into page sections, splitting at page breaks and full-page plates."""
    out, cur = [], []

    def close():
        if cur:
            out.append(f'<section class="{cls}" data-file="{data}">' + "\n".join(cur) + "</section>")
            cur.clear()
    for b in blocks:
        if b == BREAK:
            close()
        elif b.startswith(PLATE):
            close()
            out.append(f'<section class="plate" data-file="{data}">{b[len(PLATE):]}</section>')
        else:
            cur.append(b)
    close()
    return out


def stray_markup(html_text, where, problems):
    text = re.sub(r"<(pre|code)>.*?</\1>", "", html_text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    for m in re.finditer(r"[^\n]{0,30}(\*\*|(?<=\w)\*|\*(?=\w)|\{#|\]\()[^\n]{0,30}", text):
        problems.append(f"{where}: unrendered markup {m.group(1)!r} near '{' '.join(m.group(0).split())}'")
        break


# ---------------------------------------------------------------- page assembly

def css_text(a4):
    css = (TEMPLATES / "book.css").read_text(encoding="utf-8")
    fonts = (TEMPLATES / "fonts" / "fonts-local.css").read_text(encoding="utf-8")
    fonts = fonts.replace("url('fonts/", f"url('{(TEMPLATES / 'fonts').as_uri()}/")
    if a4:
        css = css.replace("size: letter", "size: A4")
    return fonts + "\n" + css


def cover_html(meta, maps, kind):
    title = html.escape(meta["title"])
    tagline = inline(meta.get("tagline", ""))
    p = meta.get("players", {})
    count, level = p.get("count"), p.get("level")
    if p.get("party_label"):  # systems without levels: "for four investigators"
        who = p["party_label"]
    elif count and level:
        who = (f"a solo adventure for one character of level {level}" if count == 1 else
               f"an adventure for {count} characters of level {level}")
    elif count:
        who = "a solo adventure" if count == 1 else f"an adventure for {count} players"
    else:
        who = ""
    system = SYSTEM_NAMES.get(meta.get("system", ""), "") or meta.get("system_label", "")
    length = meta.get("length", {})
    sessions = length.get("sessions")
    hours = length.get("hours_per_session")
    length_txt = (f"{sessions} session{'s' if sessions != 1 else ''}" + (f" of about {hours} hours" if hours else "")) if sessions else ""
    if length.get("label"):  # e.g. "4 or 5 sessions of about 3 hours"
        length_txt = length["label"]
    teach = meta.get("teach")
    # Stealth style never announces the subject: the cover is the first thing a player sees.
    badge = (f'<div class="cover-teach">Teaches: {html.escape(teach.get("subject", ""))}</div>'
             if meta.get("mode") == "teach" and teach and teach.get("style") != "stealth" else "")
    art = ""
    cover_map = meta.get("cover_map")
    if cover_map and cover_map in maps:
        art = f'<img class="cover-art" src="{maps[cover_map]["player"].as_uri()}" alt="">'
    gm = meta.get("gm_title", "Game Master")  # "Keeper", "Referee", "Narrator"
    label = {"gm": f"{gm}'s Book", "player": "Player Handouts", "found": f"Found in Play: the {gm} hands these out"}[kind]
    facts = " · ".join(x for x in (system, who, length_txt) if x)
    return (f'<section class="cover"><div class="cover-frame">'
            f'<div class="cover-kind">{label}</div><h1 class="cover-title">{title}</h1>'
            f'<div class="cover-tagline">{tagline}</div>{badge}{art}'
            f'<div class="cover-facts">{html.escape(facts)}</div>'
            f'<div class="cover-credit">{html.escape(meta.get("credit", ""))}</div></div></section>')


def toc_html(toc):
    items = []
    for level, hid, txt in toc:
        items.append(f'<li class="toc-{level}"><a href="#{hid}">{inline(txt)}</a></li>')
    return f'<section class="toc"><h1 class="toc-title">Contents</h1><ul>{"".join(items)}</ul></section>'


def page(title, css, body):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f'<style>{css}</style></head><body>{body}</body></html>')


def svg_size(path):
    m = re.search(r'<svg[^>]*width="([\d.]+)"[^>]*height="([\d.]+)"', path.read_text(encoding="utf-8")[:600])
    return (float(m.group(1)), float(m.group(2))) if m else (1, 1)


def render_maps(root, png):
    import map_svg
    maps = {}
    problems = []
    out_dir = root / "build" / "maps"
    for spec in sorted((root / "maps").glob("*.json")) if (root / "maps").exists() else []:
        try:
            rep = map_svg.render(spec, out_dir, png=png)
        except map_svg.SpecError as e:
            problems.append(f"map {spec.name}: {e}")
            continue
        except RuntimeError as e:
            problems.append(f"map {spec.name}: PNG not made ({e}); SVGs are fine")
            rep = map_svg.render(spec, out_dir, png=False)
        maps[rep["id"]] = {"gm": out_dir / f"{rep['id']}-gm.svg", "player": out_dir / f"{rep['id']}-player.svg"}
        for w in rep["warnings"]:
            problems.append(f"map {rep['id']}: {w}")
    return maps, problems


def doc_sections(files, folder, ctx, css_cls):
    out = []
    for f in files:
        blocks = render_blocks(f.read_text(encoding="utf-8"), ctx, f"{folder}/{f.name}")
        out.append(f'<section class="{css_cls}" data-file="{folder}/{f.name}">' + "\n".join(
            b for b in blocks if b != BREAK and not b.startswith(PLATE)) + "</section>")
    return out


def build(root, pdf=True, a4=False, png=True):
    root = Path(root).resolve()
    meta_path = root / "campaign.json"
    if not meta_path.exists():
        raise BuildError(f"{root}: no campaign.json")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for k in ("title", "slug"):
        if not meta.get(k):
            raise BuildError(f"campaign.json: missing '{k}'")
    out = root / "build"
    out.mkdir(exist_ok=True)
    browser = None
    if pdf or png:
        from browser import find_browser
        browser = find_browser()
        if not browser:
            png = False
    maps, problems = render_maps(root, png)
    css = css_text(a4 or meta.get("page_size") == "A4")
    results, expected_pages = {}, {}

    # GM book
    chapters = sorted((root / "book").glob("*.md"))
    if not chapters:
        raise BuildError("book/: no chapter files")
    ctx = Ctx(root, "gm", maps)
    body = []
    for ch in chapters:
        body += sections(render_blocks(ch.read_text(encoding="utf-8"), ctx, ch.name), "chapter", ch.name)
    gm_html = page(f"{meta['title']} (GM Book)", css, cover_html(meta, maps, "gm") + toc_html(ctx.toc) + "".join(body))
    stray_markup(gm_html, "GM book", problems)
    gm_path = out / f"{meta['slug']}-gm-book.html"
    gm_path.write_text(gm_html, encoding="utf-8")
    results["gm_html"] = gm_path
    problems += ctx.problems

    # Player handouts: player-safe from the start (pitch, reference cards, pregens, player maps)
    pctx = Ctx(root, "player", maps)
    hdir = root / "handouts"
    hfiles = sorted(hdir.glob("*.md")) if hdir.exists() else []
    pfiles = sorted((root / "pregens").glob("*.md")) if (root / "pregens").exists() else []
    hbody = doc_sections(hfiles, "handouts", pctx, "handout") + doc_sections(pfiles, "pregens", pctx, "handout pregen")
    for mid in meta.get("player_maps", []):
        if mid not in maps:
            problems.append(f"campaign.json player_maps: no map {mid!r}")
            continue
        w, h = svg_size(maps[mid]["player"])
        orient = "landscape" if w > h * 1.05 else "portrait"
        hbody.append(f'<section class="handout map-handout {orient}"><img src="{maps[mid]["player"].as_uri()}" alt=""></section>')
    if hbody:
        h_html = page(f"{meta['title']} (Player Handouts)", css, cover_html(meta, maps, "player") + "".join(hbody))
        stray_markup(h_html, "handouts", problems)
        h_path = out / f"{meta['slug']}-handouts.html"
        h_path.write_text(h_html, encoding="utf-8")
        results["handouts_html"] = h_path
        expected_pages["handouts_html"] = 1 + len(hbody)

    # Found in play: clue documents the GM hands over at the right moment
    fdir = hdir / "found"
    ffiles = sorted(fdir.glob("*.md")) if fdir.exists() else []
    if ffiles:
        fctx = Ctx(root, "player", maps)
        fbody = doc_sections(ffiles, "handouts/found", fctx, "handout")
        f_html = page(f"{meta['title']} (Found in Play)", css, cover_html(meta, maps, "found") + "".join(fbody))
        stray_markup(f_html, "found-in-play", problems)
        f_path = out / f"{meta['slug']}-found-in-play.html"
        f_path.write_text(f_html, encoding="utf-8")
        results["found_html"] = f_path
        expected_pages["found_html"] = 1 + len(fbody)
        problems += fctx.problems
    problems += pctx.problems

    if pdf:
        from browser import print_pdf
        for key in [k for k in results if k.endswith("_html")]:
            pdf_path = results[key].with_suffix(".pdf")
            try:
                print_pdf(results[key], pdf_path, browser)
            except RuntimeError as e:
                problems.append(f"PDF not made for {results[key].name}: {e}")
                continue
            results[key.replace("html", "pdf")] = pdf_path
            if key in expected_pages:
                got, want = pdf_pages(pdf_path), expected_pages[key]
                if got > want:
                    problems.append(f"{pdf_path.name}: {got} pages for {want - 1} one-page items; "
                                    f"{got - want} spill onto an extra page (preview it and trim)")
    return results, problems


def pdf_pages(path):
    data = Path(path).read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?!s)", data))


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    try:
        results, problems = build(args[0], pdf="--no-pdf" not in argv, a4="--a4" in argv, png="--no-png" not in argv)
    except BuildError as e:
        print(f"ERR  {e}")
        return 1
    for k, v in results.items():
        extra = f" ({pdf_pages(v)} pages)" if k.endswith("pdf") else ""
        print(f"OK   {k}: {v}{extra}")
    for p in problems:
        print(f"WARN {p}")
    return 1 if any(p.startswith("PDF not made") or "not found" in p or "unclosed" in p for p in problems) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
