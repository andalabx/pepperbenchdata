#!/usr/bin/env python3
"""OCR the scanned PDFs in the AfriFinEval corpus with tesseract.

Renders each page with pymupdf at 300 dpi, runs tesseract, writes one text file
per source under ocr/<same relative path>.txt with page markers.

Usage:
    python3 ocr.py                # all known scanned PDFs
    python3 ocr.py --dpi 400 --jobs 4
    python3 ocr.py path/to/a.pdf  # specific files
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pymupdf

RAW = Path(os.environ.get("AFRI_RAW", "/home/mimi/afrifeval/raw"))
OUT = Path(os.environ.get("AFRI_OUT", "/home/mimi/afrifeval/ocr"))

TARGETS = [
    "nigeria/kyc/cbn_3_tiered_kyc_requirements.pdf",
    "nigeria/cross_border/cbn_fx_manual_2026.pdf",
    "nigeria/kyc/nibss_bvn_circular_2026.pdf",
    "nigeria/kyc/nfiu_cbn_kyc_doc.pdf",
    "nigeria/kyc/doa_kyc_fintechs_2024.pdf",
    "nigeria/regulations/cbn_bdc_guidelines_2024.pdf",
    "nigeria/regulations/cbn_statements_payment_finality.pdf",
    "nigeria/fraud/cbn_time_bar_disputes.pdf",
]


def ocr_page(args):
    pdf_path, page_no, dpi = args
    doc = pymupdf.open(str(pdf_path))
    page = doc.load_page(page_no)
    pix = page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    fd, img = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        pix.save(img)
        p = subprocess.run(
            ["tesseract", img, "stdout", "-l", "eng", "--psm", "3"],
            capture_output=True, text=True, timeout=180,
        )
        txt = (p.stdout or "").strip()
        return page_no, txt, (p.stderr or "").strip()[:200]
    finally:
        try:
            os.unlink(img)
        except OSError:
            pass


def ocr_pdf(rel: str, dpi: int, jobs: int) -> dict:
    src = RAW / rel
    dest = (OUT / rel).with_suffix(".txt")
    dest.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    if dest.exists() and dest.stat().st_size > 500:
        return {"path": rel, "pages": -1, "chars": dest.stat().st_size,
                "seconds": 0.0, "status": "skipped (exists)"}

    doc = pymupdf.open(str(src))
    n = len(doc)
    doc.close()

    results = {}
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        futures = [ex.submit(ocr_page, (src, i, dpi)) for i in range(n)]
        for k, f in enumerate(futures, 1):
            pg, txt, err = f.result()
            results[pg] = txt
            print(f"    {rel} page {k}/{n} ({len(txt)}c)"
                  + (f" ERR {err}" if err else ""), flush=True)

    chunks = []
    for i in range(n):
        t = results.get(i, "")
        if t:
            chunks.append(f"=== page {i+1} ===\n{t}")
    body = "\n\n".join(chunks)
    dest.write_text(body)
    dt = time.time() - t0
    print(f"  DONE {rel}: {n}p {len(body)}c in {dt:.1f}s", flush=True)
    return {"path": rel, "pages": n, "chars": len(body),
            "seconds": round(dt, 1), "status": "ok"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", default=None)
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    targets = args.files or TARGETS
    summary = []
    for rel in targets:
        if not (RAW / rel).exists():
            print(f"MISSING {rel}", flush=True)
            continue
        print(f"OCR {rel}", flush=True)
        summary.append(ocr_pdf(rel, args.dpi, args.jobs))

    out = OUT / "ocr_summary.json"
    prev = json.loads(out.read_text()) if out.exists() else []
    merged = {r["path"]: r for r in prev}
    for r in summary:
        merged[r["path"]] = r
    out.write_text(json.dumps(list(merged.values()), indent=1))
    total = sum(r["chars"] for r in summary)
    print(f"\nOCR complete: {len(summary)} documents, {total} chars", flush=True)


if __name__ == "__main__":
    main()
