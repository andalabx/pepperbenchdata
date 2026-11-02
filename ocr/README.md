# OCR output

Text extracted from the eight image-only PDFs in `raw/`. One `.txt` per source,
mirroring the raw path, with `=== page N ===` markers.

Method: pymupdf renders each page at 300 dpi greyscale, tesseract 5.3.4
(`--psm 3`, `eng`, `OMP_THREAD_LIMIT=1`) reads it, four pages in parallel.

Run executed on the second host (45.85.250.43) because this machine was under a
load average of 11 from unrelated services.

| file | pages | chars |
|---|---|---|
| cross_border/cbn_fx_manual_2026.txt | 170 | 213,446 |
| kyc/nfiu_cbn_kyc_doc.txt | 81 | 200,199 |
| regulations/cbn_bdc_guidelines_2024.txt | 52 | 88,538 |
| kyc/cbn_3_tiered_kyc_requirements.txt | 7 | 12,353 |
| kyc/doa_kyc_fintechs_2024.txt | 8 | 7,684 |
| regulations/cbn_statements_payment_finality.txt | 3 | 4,156 |
| kyc/nibss_bvn_circular_2026.txt | 1 | 1,920 |
| fraud/cbn_time_bar_disputes.txt | 1 | 1,903 |

Total: 323 pages, 530,199 characters.

## Quality

Prose pages read cleanly. The tier limits in the KYC circular came through with
every figure intact (Level 1: N20,000 single deposit, N200,000 balance,
N3,000/N30,000 mobile; Level 2: N50,000, N400,000, N10,000/N100,000;
Level 3: no balance cap, N100,000/N1,000,000 mobile).

Table pages are the weak point. Columns interleave, so a row that reads
"Maximum single deposit of N50,000 and a maximum cumulative balance of
N400,000" can appear split across lines. The numbers survive; the reading order
does not. Every figure must be checked against the page image before it enters
the fact layer.

Pages with little text: FX manual 138, 146, 150, 170; BDC guidelines 47;
DoA KYC page 1 (cover page). These are blank or signature pages, not failures.
