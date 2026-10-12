# SDK-F001: Response body included in exception

## In plain language

An error copies the whole server response into its exception message. If a response contains private data, copying it into logs/support tickets could expose it. We demonstrated a synthetic marker, not a production leak.

## Which test caught this?

**Case:** `SDK-003`

**Detector:** `SDKContracts.test_http_error_does_not_expose_sensitive_body`

**Source:** `tests/sdk/test_offline_contracts.py`

**Relevant owner:** Guava SDK and downstream application logging

**Execution layer:** In-memory HTTP response; no network

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-f001)


Actual exception, reproduced with a synthetic in-memory response (no HTTP request):

```text
HTTP 401 Unauthorized for url 'https://offline.invalid/', Body: synthetic-sensitive-marker
```

Proposed default message, not applied:

```text
HTTP 401 Unauthorized for url https://offline.invalid/; response body omitted
```

The body marker must not appear in the default exception. Real response bodies may contain credentials, patient details, payment values or internal diagnostics; none should be copied wholesale into shared exceptions/logs. Request identifiers may be included only when present and allowlisted. URL query strings also need redaction when sensitive.

Reproduce: `python -m unittest discover -s tests/sdk -p test_offline_contracts.py -v`. Original source: `guava/utils.py:check_response`, SDK0.47.0; this is independent of uv installation. Raw suite output is preserved under `evidence/2026-10-11/suite-runs/`. No production secret leak is claimed.
