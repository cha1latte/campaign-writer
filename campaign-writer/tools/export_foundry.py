"""Export a campaign package as Foundry journal pages that read well through Familiar.

    python export_foundry.py <campaign-folder>

Writes foundry/pages.json:
  {"source":   [{"name": "03 N1 The Fallen Lift", "from": "book/02-session-one.md", "html": "..."}],
   "handouts": [...],  "found": [...]}
- one Source page per node heading ({#N…}), plus one for any text before the first node in a file,
  and one per file without node headings; numbered so they sort in book order
- tables become one paragraph per row ("Header: cell; Header: cell"), because Familiar's journal reads
  return plain text and table cells run together
- maps become a one-line pointer ("Map: <caption> (scene image build/maps/<id>-vtt.png)")
- every block tag ends with a line break, so plain-text reads keep headings apart from paragraphs
- pages over 45,000 characters are split (Foundry's page limit is 50,000)
Standard library only. The installing assistant (e.g. the foundry-familiar-campaigns skill) creates the
journals and pushes these pages; this tool never touches Foundry.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_book as bb  # noqa: E402

LIMIT = 45000


def table_to_paras(m):
    rows = re.findall(r"<tr>(.*?)</tr>", m.group(0), re.S)
    head = re.findall(r"<th>(.*?)</th>", rows[0], re.S) if rows and "<th>" in rows[0] else None
    out = []
    for r in rows[1:] if head else rows:
        cells = re.findall(r"<td>(.*?)</td>", r, re.S)
        if head and len(head) == len(cells):
            parts = [f"{h.strip()}: {c.strip()}" if h.strip() else c.strip() for h, c in zip(head, cells)]
        else:
            parts = [c.strip() for c in cells]
        out.append("<p>" + "; ".join(p for p in parts if p and p != "&nbsp;") + "</p>")
    return "\n".join(out)


def foundry_html(blocks):
    html_ = "\n".join(b for b in blocks if b != bb.BREAK)
    html_ = html_.replace(bb.PLATE, "")
    html_ = re.sub(r'<figure[^>]*>.*?<figcaption>(.*?)</figcaption></figure>', lambda m: f"<p><em>Map: {m.group(1)}</em></p>", html_, flags=re.S)
    html_ = re.sub(r"<table>.*?</table>", table_to_paras, html_, flags=re.S)
    html_ = re.sub(r'<svg class="act".*?</svg>', lambda m: "[action]", html_, flags=re.S)
    # Read-aloud boxes lose their styling in a plain-text read, so label where they start and end.
    html_ = re.sub(r'<div class="readaloud">(.*?)</div>',
                   lambda m: m.group(1).replace("<p>", "<p><strong>Read aloud:</strong> ", 1) + "<p><em>(End of read-aloud.)</em></p>",
                   html_, flags=re.S)
    html_ = re.sub(r'<div class="box-tag">(.*?)</div>', r"<p><strong>\1:</strong></p>", html_)
    html_ = re.sub(r'<div class="box-title">(.*?)</div>', r"<h4>\1</h4>", html_)
    html_ = re.sub(r'<div class="(sb-name)">(.*?)</div>', r"<h4>\2</h4>", html_)
    html_ = re.sub(r'<div class="(sb-meta)">(.*?)</div>', r"<p><em>\2</em></p>", html_)
    html_ = re.sub(r'<div class="(sb-head)">(.*?)</div>', r"<p><strong>\2</strong></p>", html_)
    html_ = re.sub(r'<div class="sb-rule"></div>', "", html_)
    html_ = re.sub(r'<div class="write-lines">.*?</div></div>', "", html_)
    html_ = re.sub(r'<span class="sym">(.*?)</span>', r"\1", html_)
    html_ = re.sub(r"</?div[^>]*>", "", html_)
    html_ = re.sub(r'<a href="#[^"]*">(.*?)</a>', r"\1", html_)
    html_ = re.sub(r"(</(h[1-6]|p|li|ul|ol|blockquote)>)", r"\1\n", html_)
    html_ = re.sub(r"\n{2,}", "\n", html_)
    return html_.strip()


def split_long(name, html_):
    if len(html_) <= LIMIT:
        return [(name, html_)]
    parts, cur = [], ""
    for chunk in re.split(r"(?=<h[2-4])", html_):
        if len(cur) + len(chunk) > LIMIT and cur:
            parts.append(cur)
            cur = ""
        cur += chunk
    parts.append(cur)
    return [(f"{name} ({i + 1}/{len(parts)})", p) for i, p in enumerate(parts)]


def node_chunks(text):
    """Split a chapter into (title, markdown) chunks at node headings."""
    lines = text.split("\n")
    chunks, cur, title = [], [], None
    first_h1 = next((ln[2:].strip() for ln in lines if ln.startswith("# ")), None)
    for ln in lines:
        m = re.match(r"^##\s+(.*?)\s*\{#(N\w+)\}\s*$", ln)
        if m:
            if cur and any(x.strip() for x in cur):
                chunks.append((title or first_h1 or "Intro", "\n".join(cur)))
            name = re.sub(r"^[0-9A-Za-z]{1,4}\.\s*", "", m.group(1))  # "1. The Fallen Lift" -> "The Fallen Lift"
            cur, title = [ln], f"{m.group(2)} {name}"
        else:
            cur.append(ln)
    if cur and any(x.strip() for x in cur):
        chunks.append((title or first_h1 or "Intro", "\n".join(cur)))
    return chunks


def export(root):
    root = Path(root).resolve()
    meta = json.loads((root / "campaign.json").read_text(encoding="utf-8"))
    maps = {json.loads(p.read_text(encoding="utf-8"))["id"]: {"gm": p, "player": p}
            for p in (root / "maps").glob("*.json")} if (root / "maps").exists() else {}
    out = {"title": meta["title"], "source": [], "handouts": [], "found": []}
    n = 0
    for ch in sorted((root / "book").glob("*.md")):
        for title, md in node_chunks(ch.read_text(encoding="utf-8")):
            ctx = bb.Ctx(root, "gm", maps)
            html_ = foundry_html(bb.render_blocks(md, ctx, ch.name))
            n += 1
            for name, part in split_long(f"{n:02d} {title}", html_):
                out["source"].append({"name": name, "from": f"book/{ch.name}", "html": part})
    for key, folder in (("handouts", root / "handouts"), ("found", root / "handouts" / "found"), ("handouts", root / "pregens")):
        for f in sorted(folder.glob("*.md")) if folder.exists() else []:
            ctx = bb.Ctx(root, "player", maps)
            text = f.read_text(encoding="utf-8")
            title = next((ln[2:].strip() for ln in text.split("\n") if ln.startswith("# ")), f.stem)
            num = re.match(r"\d+", f.stem)
            name = f"Pregen: {title}" if folder.name == "pregens" else (f"{num.group(0)} {title}" if num else title)
            out[key].append({"name": name, "from": str(f.relative_to(root)).replace("\\", "/"),
                             "html": foundry_html(bb.render_blocks(text, ctx, f.name))})
    dest = root / "foundry"
    dest.mkdir(exist_ok=True)
    (dest / "pages.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return out, dest / "pages.json"


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    out, path = export(argv[0])
    for key in ("source", "handouts", "found"):
        sizes = [len(p["html"]) for p in out[key]]
        if sizes:
            print(f"OK   {key}: {len(sizes)} pages, largest {max(sizes):,} chars")
    tables = sum(p["html"].count("<table") for k in ("source", "handouts", "found") for p in out[k])
    print(f"OK   wrote {path}" + ("" if not tables else f" (WARN {tables} tables left)"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
