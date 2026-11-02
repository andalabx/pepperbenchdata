#!/usr/bin/env python3
"""Check that gap-filling captures actually contain the material they claim."""
import re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path("/home/mimi/afrifeval/raw")


def text(p: Path) -> str:
    if p.suffix.lower() == ".pdf":
        try:
            r = PdfReader(str(p))
            out = []
            for pg in r.pages[:12]:
                try:
                    out.append(pg.extract_text() or "")
                except Exception:
                    pass
            return "\n".join(out)
        except Exception:
            return ""
    s = p.read_text(errors="ignore")
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s)


checks = {
    "nigeria/fees/cbn_guide_to_charges_2020.pdf": ["charge", "%", "transfer"],
    "nigeria/fees/stanbic_pricing_guide_2026.pdf": ["transfer", "charge"],
    "nigeria/error_codes/interswitch_payment_response_codes.md": ["00", "51", "insufficient"],
    "south_africa/error_codes/fnb_eft_terms.pdf": ["return", "reject", "eft"],
    "south_africa/error_codes/standard_bank_operational_regulations.pdf": ["return", "reject"],
    "south_africa/error_codes/netcash_unpaid_debit_orders.html": ["insufficient", "unpaid"],
    "egypt/regulations/cbe_ipn_services_regulations_en.pdf": ["instapay", "limit", "ipn"],
    "egypt/limits/cbe_mobile_wallet_rules_ar.pdf": ["المحفظة", "الحد", "الرصيد"],
    "egypt/regulations/cbe_psp_licensing_rules_en.pdf": ["licen", "payment service"],
    "egypt/error_codes/kashier_instapay_docs.html": ["instapay", "error"],
    "egypt/regulations/cbe_regulations_book_11_ar.html": ["الدفع", "نظم"],
}

for rel, terms in checks.items():
    p = ROOT / rel
    if not p.exists():
        print(f"MISSING  {rel}")
        continue
    t = text(p).lower()
    hits = [x for x in terms if x.lower() in t]
    verdict = "OK" if len(hits) >= max(1, len(terms) - 1) else "WEAK"
    print(f"{verdict:<6} {len(t):>7}c {len(hits)}/{len(terms)} {rel}")
    if verdict == "WEAK":
        print("       missing:", [x for x in terms if x not in hits], "| head:", t[:160])
