#!/usr/bin/env python3
"""Build raw/INVENTORY.md from files on disk, enriched from manifest.jsonl."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path("/home/mimi/afrifeval/raw")
CATS = ["fees", "limits", "kyc", "regulations", "products",
        "interoperability", "cross_border", "agent_banking",
        "error_codes", "fraud"]
COUNTRIES = ["nigeria", "kenya", "south_africa", "egypt"]

# manifest: last record per path wins
meta = {}
if (ROOT / "manifest.jsonl").exists():
    for line in (ROOT / "manifest.jsonl").read_text().splitlines():
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("path") and not r.get("error"):
            meta[r["path"]] = r

ocr = {}
if (ROOT / "pdf_audit.json").exists():
    for r in json.loads((ROOT / "pdf_audit.json").read_text()):
        ocr[r["path"]] = r["kind"]

rows = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.name in ("manifest.jsonl", "verification.json",
                                     "pdf_audit.json", "INVENTORY.md"):
        continue
    rel = str(p.relative_to(ROOT))
    parts = rel.split("/")
    if len(parts) < 3:
        continue
    country, cat = parts[0], parts[1]
    m = meta.get(rel, {})
    rows.append({
        "country": country, "category": cat, "path": rel,
        "bytes": p.stat().st_size,
        "source_type": m.get("source_type", "?"),
        "url": m.get("url", ""),
        "note": ocr.get(rel, ""),
    })

by = defaultdict(list)
for r in rows:
    by[(r["country"], r["category"])].append(r)

out = ["# AfriFinEval raw source corpus", "",
       f"Files: {len(rows)}  |  Size: {sum(r['bytes'] for r in rows)/1e6:.1f} MB  |  "
       "Layout: raw/<country>/<category>/<name>.<ext>", "",
       "Every file is an original capture (PDF/HTML) or, where the origin blocked "
       "automated fetch, a markdown capture of the page. Provenance for each file is "
       "in `manifest.jsonl` (url, http_code, content_type, sha256, retrieved_at).", "",
       "## Coverage", "",
       "| country | " + " | ".join(CATS) + " |",
       "|---" * (len(CATS) + 1) + "|"]
for c in COUNTRIES:
    cells = []
    for cat in CATS:
        n = len(by.get((c, cat), []))
        cells.append(str(n) if n else "-")
    out.append(f"| {c} | " + " | ".join(cells) + " |")

for c in COUNTRIES:
    out += ["", f"## {c}", ""]
    for cat in CATS:
        items = by.get((c, cat), [])
        if not items:
            continue
        out.append(f"### {cat} ({len(items)})")
        for r in sorted(items, key=lambda x: x["path"]):
            flags = []
            if r["note"] in ("scanned", "sparse"):
                flags.append(f"**{r['note'].upper()}**")
            out.append(f"- `{r['path'].split('/')[-1]}` "
                       f"({r['bytes']/1024:.0f} KB, {r['source_type']})"
                       + (" " + " ".join(flags) if flags else ""))
            if r["url"]:
                out.append(f"  - {r['url']}")
        out.append("")

(ROOT / "INVENTORY.md").write_text("\n".join(out))
print(f"wrote INVENTORY.md: {len(rows)} files, "
      f"{sum(r['bytes'] for r in rows)/1e6:.1f} MB")
for c in COUNTRIES:
    n = sum(len(by.get((c, k), [])) for k in CATS)
    cats = sum(1 for k in CATS if by.get((c, k)))
    print(f"  {c:<14} {n:>3} files across {cats}/10 categories")
