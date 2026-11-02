# Fact schema

Every category file is one JSON object:

```json
{
  "country": "Nigeria",
  "regulator": "CBN",
  "category": "fees",
  "as_of": "2026-11-02",
  "last_verified": "2026-11-02",
  "sources": [
    {
      "id": "src_ng_nibss_epc_2023",
      "name": "NIBSS Approved Guidelines on Operations of Electronic Payment Channels",
      "url": "https://nibss-plc.com.ng/wp-content/uploads/2023/03/Approved-Guidelines-on-Operations-of-Electronic-Payment-Channels-in-Nige1.pdf",
      "path": "nigeria/fees/nibss_electronic_payment_channels_guidelines.pdf",
      "retrieved": "2026-11-02"
    }
  ],
  "entries": [
    {
      "id": "ng_fee_nibss_2023_01",
      "subject": "nip_transfer_fee",
      "assertion_type": "conditional",
      "conditions": {"channel": "bank_transfer", "amount_ngn": {"min": 0, "max": 5000}},
      "attribute": "fee",
      "value": 1000,
      "unit": "NGN_minor",
      "display": "\u20a610 for transfers up to \u20a65,000",
      "graded_by": "numeric_exact",
      "tolerance": null,
      "effective_from": "2020-01-01",
      "effective_to": null,
      "volatility": "periodic",
      "confidence": "confirmed_primary",
      "source_id": "src_ng_nibss_epc_2023",
      "source_path": "nigeria/fees/nibss_electronic_payment_channels_guidelines.pdf",
      "quote": "exact sentence copied from the source",
      "notes": ""
    }
  ]
}
```

## Field rules

`id` — `<country2>_<category3>_<source-short>_<year>_<nn>`. Unique across the
whole dataset. Example: `ke_lim_saf_2026_03`.

`assertion_type` — `positive`, `negative`, `conditional`, `unverifiable`.
Use `negative` for facts like "there is no direct settlement path between X and
Y". Use `unverifiable` only when the fact is genuinely not public.

`conditions` — flat object. Recognised keys: `channel` (ussd, app, api, agent,
pos, bank_transfer, merchant), `actor` (consumer, business, agent), `kyc_tier`,
`amount_<ccy>`, `corridor`, `account_type`. Omit when unconditional.

`value` — number for anything comparable. **Money is always in minor units**
and `unit` says which: `NGN_minor`, `KES_minor`, `ZAR_cents`, `EGP_piastres`.
Percentages use `unit: "percent"` and the number as written (1.5 means 1.5%).
Non-numeric answers use `value_text` instead of `value`.

`display` — the human form, for reviewers. Not used by the grader.

`graded_by` — how a grader decides a model is right:
- `numeric_exact` — one exact number
- `numeric_tolerance` — number within `tolerance` (set it, e.g. 0.01)
- `enum_match` — one of a closed set, listed in `notes`
- `boolean` — true/false
- `judge_with_quote` — needs a judge because the answer is textual
- `unverifiable` — grader must abstain

`effective_from` / `effective_to` — ISO dates. Use the date the source states.
If the source has no date, use the publication date. Never leave both null and
also claim `confidence` above `single_source`.

`volatility` — `static` (law, definitions), `periodic` (tariffs, limits),
`live` (FX rates, current campaigns). Do not create facts of type `live`.

`confidence` —
- `confirmed_primary` — regulator or platform's own document states it and the
  quote is verbatim
- `corroborated` — two independent sources in this corpus agree
- `single_source` — one document, nothing else to check it against
- `unverifiable` — not publicly determinable

`quote` — verbatim from the cited file. Must be findable by a checker after
whitespace normalisation. For OCR'd PDFs, copy the OCR text as-is, including its
artifacts. Never paraphrase, never merge two sentences, never invent. If the
figures sit in a table whose columns interleaved during OCR, quote the raw OCR
line and put the cleaned reading in `display`.

`source_path` — path relative to `raw/`. Must exist.

## Quality bar

- One fact per entry. Do not bundle "fee and limit" into one entry.
- Prefer 8 solid entries to 20 padded ones. Never invent to fill a category.
- If the material does not support a category, write the file with an empty
  `entries` array and say why in the wrapper's `notes`.
- Every numeric fact needs a quote containing the number.
