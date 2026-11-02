# AfriFinEval raw corpus

Raw, unprocessed source material for the four-country fintech truth base.
Nothing here is normalised, extracted, or turned into eval JSON yet. This is
the evidence layer.

## Provenance rule

Every file is either the original bytes served by the source (PDF or HTML) or,
where the origin blocked automated fetch with a bot challenge, a markdown
capture of the rendered page. Each file has a record in `manifest.jsonl`:

```
ts, country, category, name, url, final_url, http_code, content_type,
bytes, sha256, path, source_type, note
```

`source_type` is one of `official`, `regulatory_circular`, `platform_docs`,
`verified_firsthand`. Nothing in this corpus is `verified_firsthand` yet.

## Layout

```
raw/
  manifest.jsonl        one line per capture
  verification.json     content check per file
  pdf_audit.json        page count + text layer per PDF
  INVENTORY.md          generated index with every URL
  <country>/
    <category>/         fees limits kyc regulations products
                        interoperability cross_border agent_banking
                        error_codes fraud
```

## State at pull time

- 219 files, ~164 MB
- 4 countries, all 10 categories populated
- 212 files verified as containing real content
- 10 flagged: 9 scanned PDFs plus one Arabic PDF whose text layer starts after
  page 3 (it does hold 24k chars of selectable text overall)
- 0 empty or truncated files

| country | files |
|---|---|
| nigeria | 70 |
| kenya | 43 |
| south_africa | 51 |
| egypt | 55 |

## Gap status

The seven gaps recorded after the first pull have been worked.

### Closed

**CBN Guide to Charges.** The official PDF (effective 1 Jan 2020) is in
`nigeria/fees/`, recovered from the CBN document host after the old site path
404'd. 12.9k chars of text layer. Added the Stanbic 2026 pricing guide and a
2026 framework analysis as current-period cross-checks.

**Egypt in Arabic.** `cbe_mobile_wallet_rules_ar.pdf` (third edition, April
2021) and the Arabic regulations book 11 are captured. The Arabic pass no
longer blocks regulatory coverage; translation happens at extraction time.

**InstaPay documentation.** No public API docs exist, but the operative
English rules are captured: CBE IPN Services Regulations, the Egyptian Banks
Company IPN page, and Kashier's integration behaviour notes.

### Partial

**NIP response codes.** Interswitch publishes the Nigerian switch response
codes in two documents, both captured. The NIBSS NIP Technical Specification
v7.0 is participant-only. The public preview is saved as
`nibss_nip_spec_preview_partial.md`, explicitly marked partial: section 8
holds the code table at page 25 and is not in the preview.

**PASA return codes.** The canonical list is member-only. Practical coverage
comes from FNB's EFT terms, Standard Bank's electronic banking operational
regulations, and Netcash's unpaid debit order reasons. Treat these as
bank-level behaviour, not the PASA specification.

**CBE Law 18/2022.** No English text of the law itself was located. What is
captured is stronger for grading anyway: CBE Law 194/2020 in English, its
executive regulations, the June 2025 PSO/PSP licensing rules in English, and
the IPN services regulations. The law text itself would have to come from the
Arabic Official Gazette.

### Open, accepted

**Byte-exact archives of bot-blocked origins.** Capitec, FNB, PayShap,
Bankserv, Standard Bank, Fawry, Paystack, PalmPay, Legal500 and SAFLII serve
bot challenges to non-browser clients. Their pages are stored as faithful
markdown captures, not original bytes. Content is complete; byte-exactness is
not.

## OCR (done)

The eight image-only PDFs have been OCR'd. Text is in `ocr/`, one file per
source with page markers. 323 pages, 530,199 characters. Method, quality notes
and the table-reading caveat are in `ocr/README.md`.

## Next step (not done yet)

1. Freeze each source: snapshot hash per entry, not per file.
2. Extract facts into the JSON schema with per-entry `effective_from`,
   `graded_by`, `quote`, and `assertion_type`.
