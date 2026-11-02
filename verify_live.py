#!/usr/bin/env python3
"""Firsthand verification harness for AfriFinEval provider facts.

Read-only sandbox checks. Never moves money. Never prints a key.

Credentials are read from /home/mimi/afrifeval/.secrets.env (chmod 600):
    PAYSTACK_SECRET_KEY=sk_test_...
    MONNIFY_API_KEY=...
    MONNIFY_SECRET_KEY=...
    DARAJA_CONSUMER_KEY=...
    DARAJA_CONSUMER_SECRET=...
    DARAJA_PASSKEY=...

Run:
    python3 verify_live.py            # all providers with keys present
    python3 verify_live.py paystack   # one provider
"""
import base64
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/home/mimi/afrifeval/verified")
SECRETS = Path("/home/mimi/afrifeval/.secrets.env")
UA = "AfriFinEval/0.1 (+verification harness)"
CTX = ssl.create_default_context()


def load_secrets() -> dict:
    env = {}
    if SECRETS.exists():
        for line in SECRETS.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def call(method: str, url: str, headers: dict | None = None,
         body: dict | None = None, timeout: int = 30) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    h = {"User-Agent": UA, "Accept": "application/json"}
    if data:
        h["Content-Type"] = "application/json"
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            raw = r.read()
            return {"status": r.status, "body": _parse(raw),
                    "content_type": r.headers.get("Content-Type", "")}
    except urllib.error.HTTPError as e:
        raw = e.read()
        return {"status": e.code, "body": _parse(raw),
                "content_type": e.headers.get("Content-Type", "")}
    except Exception as e:
        return {"status": 0, "body": {"error": f"{type(e).__name__}: {e}"},
                "content_type": ""}


def _parse(raw: bytes):
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return {"raw_head": raw[:300].decode("utf-8", "replace")}


def record(provider: str, checks: list) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc)
    doc = {
        "provider": provider,
        "environment": "sandbox/test",
        "verified_at": ts.isoformat(timespec="seconds"),
        "harness": "verify_live.py",
        "checks": checks,
    }
    p = OUT / f"{provider}-{ts.strftime('%Y%m%dT%H%M%SZ')}.json"
    p.write_text(json.dumps(doc, indent=1))
    return p


def paystack(env):
    key = env.get("PAYSTACK_SECRET_KEY", "")
    checks = []
    checks.append({"fact": "signup requires a secret key; unauthenticated calls are rejected",
                   **call("GET", "https://api.paystack.co/bank?country=nigeria")})
    if key:
        auth = {"Authorization": f"Bearer {key}"}
        r = call("GET", "https://api.paystack.co/bank?country=nigeria&perPage=100", auth)
        banks = (r.get("body") or {}).get("data") or []
        checks.append({"fact": f"nigeria bank list reachable, {len(banks)} banks returned",
                       "status": r["status"], "sample": banks[:3]})
    return checks


def monnify(env):
    api_key = env.get("MONNIFY_API_KEY", "")
    secret = env.get("MONNIFY_SECRET_KEY", "")
    checks = []
    checks.append({"fact": "sandbox login endpoint exists and rejects missing credentials",
                   **call("POST", "https://sandbox.monnify.com/api/v1/auth/login")})
    if api_key and secret:
        token = base64.b64encode(f"{api_key}:{secret}".encode()).decode()
        r = call("POST", "https://sandbox.monnify.com/api/v1/auth/login",
                 {"Authorization": f"Basic {token}"})
        body = r.get("body") or {}
        tok = (body.get("responseBody") or {}).get("accessToken")
        checks.append({"fact": "basic auth returns an access token",
                       "status": r["status"], "token_present": bool(tok)})
        if tok:
            h = {"Authorization": f"Bearer {tok}"}
            b = call("GET", "https://sandbox.monnify.com/api/v1/banks", h)
            banks = (b.get("body") or {}).get("responseBody") or []
            checks.append({"fact": f"sandbox bank list reachable, {len(banks)} banks returned",
                           "status": b["status"], "sample": banks[:3]})
    return checks


def daraja(env):
    key = env.get("DARAJA_CONSUMER_KEY", "")
    secret = env.get("DARAJA_CONSUMER_SECRET", "")
    checks = []
    checks.append({"fact": "oauth endpoint exists and rejects missing credentials",
                   **call("GET", "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials")})
    if key and secret:
        token = base64.b64encode(f"{key}:{secret}".encode()).decode()
        r = call("GET", "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
                 {"Authorization": f"Basic {token}"})
        tok = (r.get("body") or {}).get("access_token")
        checks.append({"fact": "consumer key/secret returns an access token",
                       "status": r["status"], "token_present": bool(tok)})
    return checks


PROVIDERS = {"paystack": paystack, "monnify": monnify, "daraja": daraja}


def main():
    env = load_secrets()
    want = sys.argv[1:] or list(PROVIDERS)
    for name in want:
        fn = PROVIDERS.get(name)
        if not fn:
            print(f"unknown provider {name}")
            continue
        checks = fn(env)
        p = record(name, checks)
        print(f"{name}: {len(checks)} checks -> {p}")
        for c in checks:
            print(f"   {c['status']}  {c['fact'][:70]}")


if __name__ == "__main__":
    main()
