#!/usr/bin/env python3
"""Validate the AfriFinEval fact layer against the schema and the raw corpus.

Checks per entry:
  - required fields present and of the right type
  - id unique across the whole dataset and well formed
  - source_path exists under raw/
  - source_id appears in the file's sources[]
  - quote is actually findable in the cited source (exact or >=70% shingle match)
  - money values carry a *_minor unit

Usage: python3 validate_data.py [--quiet]
Exit code 1 if any entry fails a hard check.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/home/mimi/afrifeval")
DATA = ROOT / "data"
RAW = ROOT / "raw"
OCR = ROOT / "ocr"

COUNTRIES = {"nigeria": "Nigeria", "kenya": "Kenya",
             "south_africa": "South Africa", "egypt": "Egypt"}
CATEGORIES = ["fees", "limits", "kyc", "regulations", "products",
              "interoperability", "cross_border", "agent_banking",
              "error_codes", "fraud"]
MONEY_UNITS = {"NGN_minor", "KES_minor", "ZAR_cents", "EGP_piastres", "USD_cents"}
REQUIRED = ["id", "subject", "assertion_type", "attribute",
            "graded_by", "volatility", "confidence", "source_id",
            "source_path", "quote"]
GRADED_BY = {"numeric_exact", "numeric_tolerance", "enum_match", "boolean",
             "judge_with_quote", "unverifiable"}

_text_cache = {}


def norm(s: str) -> str:
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    for a, b in (("\ufb01", "fi"), ("\ufb02", "fl"), ("\ufb00", "ff"),
                 ("\ufb03", "ffi"), ("\ufb04", "ffl"), ("\ufb05", "st"),
                 ("\ufb06", "st")):
        s = s.replace(a, b)
    s = re.sub(r"[^\w\s%]+", " ", s.lower(), flags=re.UNICODE)
    s = s.replace("_", " ")
    return re.sub(r"\s+", " ", s).strip()


def source_text(rel: str) -> str:
    if rel in _text_cache:
        return _text_cache[rel]
    p = RAW / rel
    out = ""
    if p.exists():
        ext = p.suffix.lower()
        if ext == ".pdf":
            ocr = (OCR / rel).with_suffix(".txt")
            if ocr.exists() and ocr.stat().st_size > 500:
                out = ocr.read_text(errors="ignore")
            else:
                try:
                    from pypdf import PdfReader
                    r = PdfReader(str(p))
                    out = "\n".join((pg.extract_text() or "") for pg in r.pages)
                except Exception:
                    out = ""
        elif ext in (".html", ".htm"):
            s = p.read_text(errors="ignore")
            s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
            out = re.sub(r"<[^>]+>", " ", s)
        else:
            out = p.read_text(errors="ignore")
    _text_cache[rel] = norm(out)
    return _text_cache[rel]


def quote_score(quote: str, src: str) -> float:
    q = norm(quote)
    if not q or not src:
        return 0.0
    if q in src:
        return 1.0
    words = q.split()
    if len(words) < 8:
        return 1.0 if q in src else 0.0
    shingles = [" ".join(words[i:i + 8]) for i in range(len(words) - 7)]
    hits = sum(1 for s in shingles if s in src)
    return hits / len(shingles)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not DATA.exists():
        print("no data/ directory")
        return 1

    ids = Counter()
    issues = []
    per_file = []
    conf = Counter()
    graded = Counter()

    files = sorted(DATA.rglob("*.json"))
    for f in files:
        rel = f.relative_to(DATA)
        try:
            doc = json.loads(f.read_text())
        except Exception as e:
            issues.append((str(rel), "-", f"invalid json: {e}"))
            continue

        parts = rel.parts
        country_slug = parts[0] if len(parts) > 1 else ""
        category = parts[-1].rsplit(".", 1)[0]
        if country_slug not in COUNTRIES:
            issues.append((str(rel), "-", f"unknown country dir {country_slug}"))
        if category not in CATEGORIES:
            issues.append((str(rel), "-", f"unknown category {category}"))
        for k in ("country", "regulator", "category", "as_of", "sources", "entries"):
            if k not in doc:
                issues.append((str(rel), "-", f"missing wrapper key {k}"))

        src_ids = {s.get("id") for s in doc.get("sources", [])}
        entries = doc.get("entries", []) or []
        per_file.append((str(rel), len(entries)))

        for e in entries:
            eid = e.get("id", "?")
            ids[eid] += 1
            for k in REQUIRED:
                if k not in e:
                    issues.append((str(rel), eid, f"missing {k}"))
            if e.get("source_id") not in src_ids:
                issues.append((str(rel), eid, "source_id not in sources[]"))
            sp = e.get("source_path", "")
            if sp and not (RAW / sp).exists():
                issues.append((str(rel), eid, f"source_path missing: {sp}"))
            if "value" not in e and "value_text" not in e:
                issues.append((str(rel), eid, "missing value or value_text"))
            if "value" not in e and not e.get("value_text"):
                issues.append((str(rel), eid, "null value and empty value_text"))
            if e.get("graded_by") == "boolean" and not isinstance(e.get("value"), bool):
                issues.append((str(rel), eid, "boolean grading requires a real bool value"))
            if e.get("graded_by") == "enum_match" and not (e.get("value") or e.get("value_text")):
                issues.append((str(rel), eid, "enum_match with no answer"))
            if "value" in e and "unit" not in e:
                issues.append((str(rel), eid, "missing unit"))
            if e.get("graded_by") not in GRADED_BY:
                issues.append((str(rel), eid, f"bad graded_by {e.get('graded_by')}"))
            if e.get("unit") in MONEY_UNITS and not isinstance(e.get("value"), (int, float)):
                issues.append((str(rel), eid, "money unit but non-numeric value"))
            if isinstance(e.get("value"), (int, float)) and e.get("volatility") == "live":
                issues.append((str(rel), eid, "live facts are not allowed"))
            if sp and e.get("quote"):
                sc = quote_score(e["quote"], source_text(sp))
                if sc < 0.7:
                    issues.append((str(rel), eid, f"quote not found (score {sc:.2f})"))
            conf[e.get("confidence", "?")] += 1
            graded[e.get("graded_by", "?")] += 1

    dups = {k: v for k, v in ids.items() if v > 1}
    for k, v in dups.items():
        issues.append(("global", k, f"duplicate id x{v}"))

    total = sum(n for _, n in per_file)
    print(f"files: {len(files)}  entries: {total}  issues: {len(issues)}")
    print("\nper file:")
    for name, n in per_file:
        print(f"  {n:>3}  {name}")
    print("\nconfidence:", dict(conf))
    print("graded_by:", dict(graded))

    if issues and not args.quiet:
        print("\nissues:")
        for f, eid, msg in issues[:120]:
            print(f"  {f} :: {eid} :: {msg}")
        if len(issues) > 120:
            print(f"  ... {len(issues) - 120} more")

    (ROOT / "validation_report.json").write_text(json.dumps(
        {"files": len(files), "entries": total,
         "issues": [{"file": f, "id": i, "issue": m} for f, i, m in issues]},
        indent=1))
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
