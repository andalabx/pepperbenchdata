#!/usr/bin/env python3
"""Verify that downloaded raw files actually contain the source, not a block page.

Writes raw/verification.json and prints a compact table of anything suspect.
Exit code 1 if any file is flagged.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path("/home/mimi/afrifeval/raw")
BAD_TITLES = re.compile(
    r"(404|not found|403|forbidden|access denied|just a moment|attention required|"
    r"are you a robot|security check|domain not found|page not found|error)",
    re.I,
)
BAD_TEXT = re.compile(
    r"(enable javascript|checking your browser|verify you are human|"
    r"cf-browser-verification|access to this page has been denied)", re.I
)


def pdf_text(p: Path, pages: int = 3) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        r = PdfReader(str(p))
        out = []
        for pg in r.pages[:pages]:
            out.append(pg.extract_text() or "")
        return "\n".join(out)
    except Exception as e:
        return f"__PDF_ERROR__ {e}"


def html_text(s: str) -> tuple[str, str]:
    t = re.search(r"<title[^>]*>(.*?)</title>", s, re.S | re.I)
    title = re.sub(r"\s+", " ", t.group(1)).strip() if t else ""
    s = re.sub(r"<script.*?</script>|<style.*?</style>|<!--.*?-->", " ", s,
               flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&nbsp;?", " ", s)
    s = re.sub(r"\s+", " ", s)
    return title, s.strip()


def check(p: Path) -> dict:
    rec = {"path": str(p.relative_to(ROOT)), "bytes": p.stat().st_size,
           "kind": p.suffix.lstrip("."), "title": "", "text_chars": 0,
           "flags": []}
    raw = p.read_bytes()[:8]
    if raw[:4] == b"%PDF" or p.suffix.lower() == ".pdf":
        text = pdf_text(p)
        if text.startswith("__PDF_ERROR__"):
            rec["flags"].append(text)
            return rec
        rec["text_chars"] = len(text)
        if len(text) < 400:
            rec["flags"].append("pdf:little-text (scanned?)")
    elif p.suffix.lower() in (".html", ".htm"):
        title, text = html_text(p.read_text(errors="ignore"))
        rec["title"] = title
        rec["text_chars"] = len(text)
        if BAD_TITLES.search(title):
            rec["flags"].append(f"html:bad-title:{title[:60]}")
        if BAD_TEXT.search(text[:4000]):
            rec["flags"].append("html:block-page")
        if len(text) < 600:
            rec["flags"].append("html:thin")
    else:
        rec["text_chars"] = -1
    return rec


def main():
    recs = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and p.name not in ("manifest.jsonl", "verification.json"):
            recs.append(check(p))
    (ROOT / "verification.json").write_text(json.dumps(recs, indent=1))

    flagged = [r for r in recs if r["flags"]]
    ok = [r for r in recs if not r["flags"]]
    print(f"files={len(recs)} clean={len(ok)} flagged={len(flagged)}\n")
    for r in sorted(flagged, key=lambda x: -x["bytes"]):
        print(f"FLAG {r['path']}\n     {r['bytes']}B text={r['text_chars']} "
              f"title={r['title'][:70]!r} {r['flags']}")
    print("\n-- largest clean files --")
    for r in sorted(ok, key=lambda x: -x["bytes"])[:8]:
        print(f"      {r['bytes']:>9}B text={r['text_chars']:>7} {r['path']}")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
