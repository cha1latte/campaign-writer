"""Find a Chromium-family browser and use it headless for PDF printing and PNG screenshots.

Standard library only. Set CAMPAIGN_BROWSER to a browser executable to override detection.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CANDIDATES = {
    "win32": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    ],
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ],
    "linux": [],
}
PATH_NAMES = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
              "microsoft-edge", "microsoft-edge-stable", "brave-browser", "chrome", "msedge"]


def find_browser():
    env = os.environ.get("CAMPAIGN_BROWSER")
    if env:
        if Path(env).exists():
            return env
        raise SystemExit(f"CAMPAIGN_BROWSER points to a missing file: {env}")
    local = os.environ.get("LOCALAPPDATA")
    extra = [str(Path(local) / "Google/Chrome/Application/chrome.exe")] if local else []
    for path in CANDIDATES.get(sys.platform, []) + extra:
        if Path(path).exists():
            return path
    for name in PATH_NAMES:
        found = shutil.which(name)
        if found:
            return found
    return None


def _run(browser, args, timeout=180):
    profile = tempfile.mkdtemp(prefix="cw-browser-")
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run",
           "--no-default-browser-check", "--hide-scrollbars", "--allow-file-access-from-files",
           f"--user-data-dir={profile}", "--virtual-time-budget=8000"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    shutil.rmtree(profile, ignore_errors=True)
    return result


def print_pdf(html_path, pdf_path, browser=None):
    """Print an HTML file to PDF. Returns the PDF path, or raises with the browser's stderr."""
    browser = browser or find_browser()
    if not browser:
        raise RuntimeError("no Chromium-family browser found (Chrome, Edge, Chromium or Brave); "
                           "set CAMPAIGN_BROWSER, or open the HTML and use Print > Save as PDF")
    pdf_path = Path(pdf_path).resolve()
    if pdf_path.exists():
        pdf_path.unlink()
    result = _run(browser, ["--no-pdf-header-footer", "--print-to-pdf-no-header", "--generate-pdf-document-outline",
                            f"--print-to-pdf={pdf_path}", Path(html_path).resolve().as_uri()])
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"PDF not written. Browser said:\n{result.stderr[-2000:]}")
    return pdf_path


def screenshot(src_path, png_path, width, height, browser=None):
    """Render an SVG or HTML file to a PNG of exactly width x height CSS pixels."""
    browser = browser or find_browser()
    if not browser:
        raise RuntimeError("no Chromium-family browser found; PNG export needs one (SVG files are still usable)")
    png_path = Path(png_path).resolve()
    if png_path.exists():
        png_path.unlink()
    src = Path(src_path).resolve()
    if src.suffix.lower() == ".svg":
        # Wrap the SVG so the page has no margin and exactly the map's size.
        wrapper = src.with_suffix(".shot.html")
        wrapper.write_text(
            "<!doctype html><html><head><style>html,body{margin:0;padding:0;background:#fff}"
            "img{display:block}</style></head><body>"
            f'<img src="{src.name}" width="{width}" height="{height}"></body></html>',
            encoding="utf-8")
        target = wrapper
    else:
        target = src
    result = _run(browser, [f"--screenshot={png_path}", f"--window-size={width},{height}",
                            "--force-device-scale-factor=1", target.as_uri()])
    if src.suffix.lower() == ".svg":
        wrapper.unlink(missing_ok=True)
    if not png_path.exists() or png_path.stat().st_size == 0:
        raise RuntimeError(f"PNG not written. Browser said:\n{result.stderr[-2000:]}")
    return png_path


if __name__ == "__main__":
    print(find_browser() or "no browser found")
