#!/usr/bin/env python3
import json
from pathlib import Path
from pypdf import PdfReader

ROOT = Path("/home/mimi/afrifeval/raw")
rows = []
for p in sorted(ROOT.rglob("*.pdf")):
    rel = str(p.relative_to(ROOT))
    try:
        r = PdfReader(str(p))
        n = len(r.pages)
        chars = 0
        for pg in r.pages[:8]:
            try:
                chars += len(pg.extract_text() or "")
            except Exception:
                pass
    except Exception:
        rows.append({"path": rel, "pages": -1, "text_chars": 0, "kind": "unreadable"})
        continue
    kind = "text" if chars > 1000 else ("sparse" if chars > 200 else "scanned")
    rows.append({"path": rel, "pages": n, "text_chars": chars, "kind": kind})

json.dump(rows, open(ROOT / "pdf_audit.json", "w"), indent=1)
print(f"{len(rows)} pdfs")
for k in ("scanned", "sparse", "unreadable"):
    sub = [r for r in rows if r["kind"] == k]
    print(f"\n== {k} ({len(sub)}) ==")
    for r in sub:
        print(f"  {r['pages']:>4}p {r['text_chars']:>7}c {r['path']}")
