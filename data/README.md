# AfriFinEval fact layer

435 machine-checkable assertions across 4 countries and 10 categories, built from the `raw/` corpus and validated by `validate_data.py`.

## Entries per category

| country | fees | limits | kyc | regulations | products | interoperability | cross_border | agent_banking | error_codes | fraud | total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| nigeria | 13 | 12 | 13 | 12 | 10 | 12 | 15 | 11 | 11 | 11 | 120 |
| kenya | 12 | 10 | 8 | 10 | 10 | 8 | 9 | 9 | 10 | 11 | 97 |
| south_africa | 12 | 11 | 11 | 12 | 12 | 11 | 11 | 7 | 12 | 9 | 108 |
| egypt | 11 | 12 | 11 | 12 | 10 | 11 | 10 | 9 | 12 | 12 | 110 |

Confidence: confirmed_primary 321, single_source 85, corroborated 29.

## How these were checked

`validate_data.py` re-extracts the text of every cited file and searches it for the entry's quote, after whitespace and ligature normalisation. An entry whose quote cannot be found in the file it cites is a hard failure. Current state: 40 files, 435 entries, 0 issues.

It does not check that the number in `value` matches the number in the quote. That was spot-checked by hand, including the M-Pesa KSh 500,000 daily and KSh 250,000 per-transaction limits and the InstaPay EGP 120,000 daily cap.

## Known gaps, recorded rather than invented

Nigeria
- The NIN-BVN linkage rule is not in this corpus. No KYC entry asserts it.
- The 4th Edition FX Manual does not restate a BTA figure. The US$5,000 entry carries `effective_to: 2026-05-15`.
- The file originally captured as `cbn_fx_manual_2026.pdf` was the March 2018 revision. It is renamed `cbn_fx_manual_2018_rev.pdf`; the real 4th Edition was fetched separately and supports six cross-border entries.

Kenya
- Nothing supports Huduma Namba, SIM registration rules, agent-level cash caps or minimum float.
- Daraja timeout, insufficient-float and reversal result codes are absent, so `error_codes` covers published contract codes only.
- PesaLink pricing is bank-specific, not a scheme tariff, and is recorded that way.

South Africa
- `agent_banking` is thin: the captured Post Office page is postal-only, and GoTyme does not name host retailers.
- FNB eWallet pricing was not in the capture, so no eWallet fee is asserted.
- No RTC decline-code table exists in the corpus.

Egypt
- No document states the 14-digit length of the national ID.
- No Egypt-specific source cites Law 18/2022; the corpus supports Law 194/2020 plus the June 2025 PSO/PSP rules.
- Fawry consumer fee amounts are absent.
- No PAPSS document states Egypt's participation, so no Egypt-to-Nigeria route is asserted.
- Two conflicts are flagged, not resolved: CBE's 30k/day wallet cap versus Vodafone Cash's 60k/day, and a 10 EGP versus 15 EGP cap on other-wallet transfers.
