"""Render PDF pages to PNG so you can look at them: contact sheets for the whole book, single pages up close.

    python preview_pdf.py <file.pdf> [--pages 1,5-7] [--sheet] [--per 6] [--out DIR] [--scale 1.3]

  --sheet    contact sheets (default when no --pages is given); --per sets pages per sheet (default 6, readable)
  --pages    render these pages at full size instead (1-based, ranges allowed)
Writes PNGs to <pdf folder>/preview/ by default and prints their paths.

Needs one PDF renderer: `pip install pypdfium2 pillow` (preferred) or `pip install pymupdf`.
"""
import sys
from pathlib import Path


def parse_pages(spec, n):
    pages = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            pages += range(int(a), int(b) + 1)
        elif part.strip():
            pages.append(int(part))
    return [p for p in pages if 1 <= p <= n]


def open_renderer(pdf_path):
    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(pdf_path))
        return len(doc), lambda i, scale: doc[i].render(scale=scale).to_pil()
    except ImportError:
        pass
    try:
        import fitz  # PyMuPDF
        from PIL import Image
        doc = fitz.open(str(pdf_path))

        def render(i, scale):
            pix = doc[i].get_pixmap(matrix=fitz.Matrix(scale, scale))
            return Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        return len(doc), render
    except ImportError:
        raise SystemExit("No PDF renderer found. Install one:  pip install pypdfium2 pillow   (or: pip install pymupdf)")


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    pdf = Path(args[0]).resolve()

    def opt(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    out = Path(opt("--out", pdf.parent / "preview"))
    out.mkdir(parents=True, exist_ok=True)
    scale = float(opt("--scale", "1.3"))
    n, render = open_renderer(pdf)
    for old in out.glob(f"{pdf.stem}-*.png"):  # stale renders from an earlier build mislead
        old.unlink()
    written = []
    if "--pages" in argv:
        for p in parse_pages(opt("--pages"), n):
            path = out / f"{pdf.stem}-p{p:02d}.png"
            render(p - 1, scale).save(path)
            written.append(path)
    if "--sheet" in argv or "--pages" not in argv:
        from PIL import Image
        per = int(opt("--per", "6"))
        cols = 3 if per <= 6 else 4
        thumbs = [render(i, 0.62 if per <= 6 else 0.42) for i in range(n)]
        w, h = max(t.width for t in thumbs), max(t.height for t in thumbs)
        for s in range(0, n, per):
            chunk = thumbs[s:s + per]
            rows = (len(chunk) + cols - 1) // cols
            sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 12) + 12), (90, 90, 90))
            for k, t in enumerate(chunk):
                sheet.paste(t, (12 + (k % cols) * (w + 12), 12 + (k // cols) * (h + 12)))
            path = out / f"{pdf.stem}-sheet-{s // per + 1}.png"
            sheet.save(path)
            written.append(path)
    print(f"{pdf.name}: {n} pages")
    for p in written:
        print(p)
    for line in ([] if pdf.stem.endswith(("-handouts", "-found-in-play")) else find_gaps(pdf)):
        print(line)
    return 0


def find_gaps(pdf_path):
    """Pages where a text column ends high up while the other runs on: likely a box or map that jumped. pypdfium2 only."""
    try:
        import pypdfium2 as pdfium
    except ImportError:
        return []
    out = []
    doc = pdfium.PdfDocument(str(pdf_path))
    for i in range(len(doc)):
        page = doc[i]
        w, h = page.get_size()
        if any(obj.type == 3 for obj in page.get_objects()):  # pages with images (maps, plates, cover) are laid out by hand
            continue
        tp = page.get_textpage()
        lowest = {0: h, 1: h}  # PDF y grows upwards: track the lowest text bottom per column
        found = {0: False, 1: False}
        for k in range(tp.count_chars()):
            box = tp.get_charbox(k)
            if not box or box[1] < h * 0.08:  # skip the page number
                continue
            col = 0 if (box[0] + box[2]) / 2 < w / 2 else 1
            lowest[col] = min(lowest[col], box[1])
            found[col] = True
        if not (found[0] or found[1]):
            continue
        used = {c: (h - lowest[c]) / h for c in (0, 1) if found[c]}
        empty = [c for c in (0, 1) if not found[c] or used.get(c, 0) < 0.5]
        if i < len(doc) - 1 and empty and max(used.values()) > 0.85:
            side = "left" if empty == [0] else "right" if empty == [1] else "both"
            short = min(used.get(c, 0.0) for c in empty)
            out.append(f"GAP  page {i + 1}: the {side} column stops early ({short:.0%} of its height used); "
                       "fine at a chapter's end, otherwise look at it")
        elif i < len(doc) - 1 and max(used.values()) < 0.35 and not doc[i + 1].get_textpage().get_text_range()[:40].strip() == "":
            out.append(f"GAP  page {i + 1}: only {max(used.values()):.0%} of the page has text; if it isn't a chapter's last page, look at it")
    return out


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
