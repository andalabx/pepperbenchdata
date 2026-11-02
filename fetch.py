#!/usr/bin/env python3
"""Fetch raw AfriFinEval sources into country/category folders with a manifest.

Usage:
    python3 fetch.py items.json          # download every item in the list
    python3 fetch.py items.json --dry    # resolve only, no writes

Item shape:
    {"country": "nigeria", "category": "fees", "name": "nibss_fee_schedule",
     "url": "https://...", "source_type": "official", "note": ""}

Every attempt appends one JSON line to raw/manifest.jsonl:
    ts, country, category, name, url, final_url, http_code, content_type,
    bytes, sha256, path, source_type, note, error

Re-running is safe: a URL whose sha256 is already on disk for that country/
category is skipped unless --force is passed.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path("/home/mimi/afrifeval/raw")
MANIFEST = ROOT / "manifest.jsonl"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

CT_EXT = {
    "application/pdf": ".pdf",
    "application/json": ".json",
    "application/ld+json": ".json",
    "text/html": ".html",
    "application/xhtml+xml": ".html",
    "text/plain": ".txt",
    "text/csv": ".csv",
    "text/xml": ".xml",
    "application/xml": ".xml",
    "application/msword": ".doc",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "application/vnd.ms-excel": ".xls",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
    "application/zip": ".zip",
}
URL_EXT = (".pdf", ".html", ".htm", ".json", ".txt", ".csv", ".xml",
           ".doc", ".docx", ".xls", ".xlsx", ".zip")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def slug(s: str, limit: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return (s[:limit] or "file").lower()


def pick_ext(ct: str, url: str, head: bytes) -> str:
    if head[:4] == b"%PDF":
        return ".pdf"
    if head[:2] == b"PK":
        return ".docx" if "word" in ct else ".zip"
    base = ct.split(";")[0].strip().lower()
    if base in CT_EXT:
        return CT_EXT[base]
    path = urlparse(url).path.lower()
    for e in URL_EXT:
        if path.endswith(e):
            return (".html" if e == ".htm" else e)
    return ".bin"


def already_have(country: str, category: str, url: str) -> bool:
    if not MANIFEST.exists():
        return False
    with MANIFEST.open() as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            if (r.get("country") == country and r.get("category") == category
                    and r.get("url") == url and not r.get("error")
                    and r.get("bytes", 0) > 512):
                p = ROOT / r.get("path", "")
                if p.is_file() and p.stat().st_size > 512:
                    return True
    return False


def fetch(item: dict, force: bool = False, dry: bool = False) -> dict:
    country = slug(item["country"], 40)
    category = slug(item["category"], 40)
    name = slug(item.get("name") or urlparse(item["url"]).path, 60)
    url = item["url"].strip()

    rec = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "country": country, "category": category, "name": name, "url": url,
        "source_type": item.get("source_type", ""), "note": item.get("note", ""),
        "final_url": "", "http_code": 0, "content_type": "", "bytes": 0,
        "sha256": "", "path": "", "error": "",
    }

    if not force and already_have(country, category, url):
        rec["error"] = "skipped: already downloaded"
        return rec

    outdir = ROOT / country / category
    if not dry:
        outdir.mkdir(parents=True, exist_ok=True)

    # curl writes body + headers so we can see content-type and redirect target
    tmp = Path("/home/mimi/afrifeval/.tmp")
    tmp.mkdir(parents=True, exist_ok=True)
    body = tmp / f"body.{os.getpid()}"
    hdrs = tmp / f"hdr.{os.getpid()}"

    cmd = [
        "curl", "-sS", "-L", "--compressed", "--max-time", "60",
        "--max-filesize", "60000000", "--http1.1",
        "-A", UA,
        "-H", "Accept: text/html,application/pdf,application/json,*/*;q=0.8",
        "-H", "Accept-Language: en-US,en;q=0.9,fr;q=0.8,ar;q=0.7",
        "-D", str(hdrs), "-o", str(body),
        "-w", "%{http_code}|%{url_effective}|%{content_type}",
        url,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        rec["error"] = "timeout"
        return rec

    meta = (p.stdout or "").strip()
    code, final_url, ct = "0", "", ""
    if "|" in meta:
        parts = meta.split("|")
        if len(parts) >= 3:
            code, final_url, ct = parts[0], "|".join(parts[1:-1]), parts[-1]
        elif len(parts) == 2:
            code, final_url = parts
    try:
        rec["http_code"] = int(code)
    except ValueError:
        rec["http_code"] = 0
    rec["final_url"] = final_url
    rec["content_type"] = ct

    data = body.read_bytes() if body.exists() else b""
    if body.exists():
        body.unlink()
    if hdrs.exists():
        hdrs.unlink()

    if not data:
        rec["error"] = rec["error"] or f"empty body (curl rc={p.returncode}) {p.stderr.strip()[:160]}"
        return rec
    if rec["http_code"] >= 400 or rec["http_code"] == 0:
        rec["error"] = f"http {rec['http_code']} {p.stderr.strip()[:120]}"

    ext = pick_ext(ct, final_url or url, data[:8])
    fname = f"{name}{ext}"
    dest = outdir / fname
    n = 2
    while dest.exists() and not force:
        dest = outdir / f"{name}-{n}{ext}"
        n += 1

    rec["bytes"] = len(data)
    rec["sha256"] = sha256_bytes(data)
    if not dry:
        dest.write_bytes(data)
        rec["path"] = str(dest.relative_to(ROOT))
        with MANIFEST.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--only", default="", help="substring filter on country/category")
    args = ap.parse_args()

    items = json.loads(Path(args.items).read_text())
    if args.only:
        items = [i for i in items
                 if args.only in f"{i.get('country')}/{i.get('category')}"]

    ok = bad = skip = 0
    for i, it in enumerate(items, 1):
        r = fetch(it, force=args.force, dry=args.dry)
        if r["error"].startswith("skipped"):
            skip += 1
            flag = "SKIP"
        elif r["error"]:
            bad += 1
            flag = "FAIL"
        else:
            ok += 1
            flag = "OK  "
        print(f"[{i}/{len(items)}] {flag} {r['country']}/{r['category']} "
              f"{r['name']} {r['bytes']}B {r['path'] or r['error'][:90]}")
    print(f"\ndone: ok={ok} fail={bad} skip={skip}")


if __name__ == "__main__":
    main()
