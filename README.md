# AfriFinEval

Machine-checkable ground truth for African fintech and payment rails. Built to
grade models, not to be read by them.

435 assertions covering Nigeria, Kenya, South Africa and Egypt, ten categories
per country, each one tied to a source document in this repository by a verbatim
quote.

## Why it exists

Published fee schedules, regulator caps and platform rules are prose. A grader
cannot score against prose without a second model in the loop, and then the
second model becomes the ground truth. This repository turns the prose into
atomic assertions with a fixed answer, a unit, a validity date and a quote that
a machine can find in the cited file.

## What is here

| Layer | Path | Contents |
|---|---|---|
| Evidence | `raw/` | 64 PDFs, 116 HTML captures, 42 markdown captures, 163 MB. Every file has a manifest record with URL, HTTP status, content type, sha256 and capture time. |
| OCR | `ocr/` | 8 text files, 323 pages, 530k characters, covering the scanned PDFs only. |
| Facts | `data/` | 40 JSON files, 435 assertions, 10 categories per country. |
| Firsthand | `verified/` | 9 timestamped records of live sandbox calls to Monnify, Paystack, Mono and Daraja. |

## Counts

| country | fees | limits | kyc | regulations | products | interoperability | cross_border | agent_banking | error_codes | fraud | total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Nigeria | 13 | 12 | 13 | 12 | 10 | 12 | 15 | 11 | 11 | 11 | 120 |
| Kenya | 12 | 10 | 8 | 10 | 10 | 8 | 9 | 9 | 10 | 11 | 97 |
| South Africa | 12 | 11 | 11 | 12 | 12 | 11 | 11 | 7 | 12 | 9 | 108 |
| Egypt | 11 | 12 | 11 | 12 | 10 | 11 | 10 | 9 | 12 | 12 | 110 |

Confidence: 321 `confirmed_primary`, 85 `single_source`, 29 `corroborated`.

Grading modes: 204 `numeric_exact`, 156 `judge_with_quote`, 50 `enum_match`,
18 `boolean`, 7 `numeric_tolerance`.

## Guarantees

- Every entry cites a file that exists in `raw/` and carries a verbatim quote.
- `validate_data.py` re-extracts the text of every cited file and searches it
  for that quote, after whitespace and ligature normalisation. An unquotable
  fact is a hard failure. Current state: 40 files, 435 entries, 0 issues.
- Money is stored in minor units, never as a formatted string. `1000` with
  `NGN_minor` is ₦10.
- Every entry carries `effective_from`, a `confidence` grade and a `graded_by`
  mode, so a grader knows whether to compare a number, match an enum, or abstain.
- Live values (FX rates, campaigns) are excluded by construction.

## Quick start

```bash
python3 -m pip install pypdf
python3 validate_data.py
```

Exit code 0 means every quote in every file was found in the source it cites.

## What was verified by execution, and what was not

`VERIFICATION.md` separates two different claims:

- **Verified capture**: the bytes in `raw/` came from the recorded URL, with a
  sha256 in `manifest.jsonl`.
- **Verified firsthand**: we called the live system. Only 9 records qualify, and
  they cover API mechanics and error contracts, not commercial rules.

Sandbox APIs never charge a fee, enforce a KYC tier or apply a transaction cap.
Those facts are document-sourced and graded accordingly. The distinction is kept
visible rather than smoothed over.

## Known gaps

Recorded in `data/README.md` and in per-file notes rather than filled in:

- The NIN-BVN linkage rule is not in this corpus. No KYC entry asserts it.
- The 4th Edition CBN FX Manual does not restate a Business Travel Allowance
  figure, so the 2018 US$5,000 entry carries an end date.
- No Egypt-specific source cites Law 18/2022; the corpus supports Law 194/2020
  plus the June 2025 PSO/PSP licensing rules.
- Fawry consumer fee amounts, Daraja result codes, RTC decline codes and South
  African agent-banking detail are absent from the captures.
- NIBSS NIP response codes and PASA return codes are membership-only documents.

## Layout

```
SCHEMA.md              entry contract: fields, units, grading modes, confidence
validate_data.py       the enforcer
validation_report.json last run
raw/                   evidence corpus, index and manifest
ocr/                   text of the scanned PDFs
data/                  the fact layer
verified/              live sandbox records
fetch.py               refetch the corpus from its manifest
verify.py              capture audit
audit_pdfs.py          page and text-layer audit
ocr.py                 OCR pipeline
verify_live.py         read-only sandbox harness
make_inventory.py      regenerate the corpus index
```

## Provenance

Corpus captured 2026-11-02. Source precedence where documents conflict:
regulator over bank over platform FAQ, and newer over older. Conflicts that
could not be resolved are flagged in entry notes, not silently resolved.

No credentials are stored in this repository. The sandbox harness reads
`.secrets.env`, which is gitignored.

Proprietary. AndaLabX.
