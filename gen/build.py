#!/usr/bin/env python3
"""Assemble and check the Nigeria fact layer."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/mimi/afrifeval")
sys.path.insert(0, "/home/mimi/afrifeval/gen")

import validate_data as V
import part1, part2, part3

DATA = Path("/home/mimi/afrifeval/data/nigeria")

CATS = {
    "fees": (part1.SOURCES, part1.FEES),
    "limits": (part1.SOURCES, part1.LIMITS),
    "kyc": (part1.SOURCES, part1.KYC),
    "regulations": (part2.SOURCES, part2.REGULATIONS),
    "products": (part2.SOURCES, part2.PRODUCTS),
    "interoperability": (part2.SOURCES, part2.INTEROP),
    "cross_border": (part3.SOURCES, part3.CROSS),
    "agent_banking": (part3.SOURCES, part3.AGENT),
    "error_codes": (part3.SOURCES, part3.ERRORS),
    "fraud": (part3.SOURCES, part3.FRAUD),
}

NOTES = {
    "fees": "Tariffs are quoted as the CBN ceiling plus the platform's own published rate. Bank tariffs add VAT on top of the CBN figures. Undated platform pricing pages use the corpus capture date as effective_from.",
    "limits": "Tier caps come from the 2013 three-tiered KYC circular; the scanned circular has no text layer so its OCR text is quoted, including OCR spacing inside numbers. Mobile money wallet caps come from the separate 2021 mobile money framework and differ from the bank-account tiers.",
    "kyc": "The NIN-BVN linkage rule is NOT recorded: no document in this corpus states it, and it is not invented here. Tier 2 caps are quoted from the clean secondary restatement because the circular's table OCR interleaves columns.",
    "regulations": "Payment finality is stated per scheme rather than as a single rule. BDC prohibitions are quoted from the non-permissible activities list.",
    "products": "USSD strings are reproduced with the markdown escaping used in the source file.",
    "interoperability": "NIP has no single system-wide transaction ceiling; the cap is set by CBN regulation and enforced per institution.",
    "cross_border": "The file named cbn_fx_manual_2026 in the corpus is actually the March 2018 revision of the CBN Foreign Exchange Manual; facts are dated 2018-03-01 accordingly and later circulars may have moved the allowances. USD amounts are recorded in USD_cents.",
    "agent_banking": "Limits come from the October 2025 agent banking guidelines as reported by TNP; the CBN's own guideline text is not in the corpus, so confidence is single_source.",
    "error_codes": "Response codes are quoted from the platforms' own developer documentation. A 'pending' code is not a final outcome.",
    "fraud": "Complaint timelines come from Annexure D of the Consumer Protection Regulations, which lists first and second review in working days. The captured Regulations PDF prints no issue date, so entries sourced to it use the publication date of the captured copy (2020-02-01).",
}


def main(write=False):
    bad = []
    total = 0
    for cat, (sources, entries) in CATS.items():
        used = {e["src"] for e in entries}
        src_list = []
        for k in used:
            s = dict(sources[k])
            s["retrieved"] = "2026-11-02"
            src_list.append(s)
        id_by_key = {k: sources[k]["id"] for k in used}
        out_entries = []
        for e in entries:
            e = dict(e)
            e["source_id"] = id_by_key[e.pop("src")]
            e.setdefault("effective_to", None)
            e.setdefault("tolerance", None)
            e.setdefault("notes", "")
            if "value" not in e:
                e["value"] = None
            if "unit" not in e:
                e["unit"] = None
            txt = V.source_text(e["source_path"] if "source_path" in e else sources[[k for k in used if sources[k]["id"] == e["source_id"]][0]]["path"])
            e["source_path"] = sources[[k for k in used if sources[k]["id"] == e["source_id"]][0]]["path"]
            sc = V.quote_score(e["quote"], txt)
            if sc < 0.7:
                bad.append((cat, e["id"], round(sc, 2), e["quote"][:90]))
            out_entries.append(e)
            total += 1
        doc = {
            "country": "Nigeria",
            "regulator": "CBN",
            "category": cat,
            "as_of": "2026-11-02",
            "last_verified": "2026-11-02",
            "sources": src_list,
            "entries": out_entries,
            "notes": NOTES[cat],
        }
        if write:
            DATA.mkdir(parents=True, exist_ok=True)
            (DATA / f"{cat}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"{cat:20s} {len(out_entries):>3} entries, {len(src_list)} sources")

    print(f"\ntotal {total}")
    if bad:
        print(f"\nQUOTE FAILURES {len(bad)}:")
        for b in bad:
            print("  ", b)
    else:
        print("\nall quotes verified")
    return bad


if __name__ == "__main__":
    main(write="--write" in sys.argv)
