# Firsthand verification

Facts confirmed by calling a live system, not by reading a document. Records in
`verified/`, one JSON per provider and run. No secret is stored in any record.

## Monnify sandbox

Run against `sandbox.monnify.com` with a sandbox API key pair.

Confirmed:

- `POST /api/v1/auth/login` with `Basic base64(apiKey:secretKey)` returns
  `accessToken`. `expiresIn` was 3584 seconds, consistent with the documented
  1-hour token and its refresh pattern.
- Unauthenticated login returns 401,
  `"Unauthorized, supply authorization header"`.
- `GET /api/v1/banks` returns 200 with 374 Nigerian institutions, each carrying
  `name`, `code` and `nipBankCode`. Saved to `verified/monnify-banks-*.json`.
- `GET /api/v1/disbursements/account/validate` returns 422 with an explicit
  deprecation notice pointing at `/api/v2/disbursements/account/validate`.
- The v2 account validate method is **GET**, not POST. POST returns 405.
- An unknown account on v2 returns 404, `"Invalid account details supplied"`.
- Wallet balance returns 400,
  `"You're not permitted to access this functionality"`. The key is not
  provisioned for disbursements, which is the documented default state.

After the contract code and merchant wallet were supplied, three more checks ran:

- `GET /api/v2/disbursements/wallet-balance?accountNumber=` returns 200 with
  `availableBalance` and `ledgerBalance`. The hyphenated path is correct;
  `/wallet/balance` returns 404.
- A single transfer without `destinationAccountName` fails with *422,
  responseCode D01, "destination account name is required"*. The mandatory-field
  claim is confirmed.
- Reserved account creation returned 200 with a set of virtual accounts even
  with *no BVN or NIN* in the payload, using `getAllAvailableBanks: true`. This
  contradicts the earlier belief that BVN/NIN is mandatory, at least at the
  sandbox API layer. Live enforcement and per-contract settings are still
  unproven.

Not confirmed:

- Fee amounts, transaction caps and KYC tiers. Sandbox never charges a fee or
  enforces a tier, so these cannot be verified this way at all.
- Live-mode differences for any of the above.

Side effect: one sandbox reserved account was created under reference
`AFEVAL1793614737`. Harmless test resource, but it exists.

## Mono (not Monnify)

A separate test key (`test_s…`) exists in `/home/mimi/pepper-api.env` for Mono,
the open-banking aggregator.

- `GET /v2/accounts` authenticates with the `mono-sec-key` header and returned
  200 with 10 sandbox accounts.
- Bearer auth with the same key returns 403; the header name is load-bearing.
- Response fields per account: `id`, `name`, `account_number`, `balance`,
  `currency`, `institution`, `bvn`, `customer`, `type`, `status`, `auth_method`.
- Records in `verified/mono-*.json` hold only the field list and counts. Account
  data is PII and was not persisted.

## Coverage statement

Document-sourced facts remain the base layer. Firsthand verification currently
covers provider mechanics and error contracts only. No tariff, limit or KYC fact
has been confirmed against a live system, and none can be without a funded
production account.

## Credentials

`/home/mimi/afrifeval/.secrets.env`, mode 600. Monnify sandbox only. Values are
never written to verification records or logs. Rotate the key pair once this
verification round is closed.
