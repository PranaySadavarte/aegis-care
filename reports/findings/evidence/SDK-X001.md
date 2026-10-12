# SDK-X001: Transfer destination not validated client-side

## In plain language

The SDK accepts a badly formatted transfer destination into its outgoing command queue. A developer gets no early rejection; the call could fail later. We did not make a transfer or prove it reaches the wrong person.

## Which test caught this?

**Case:** `SDK-X001`

**Detector:** `CommandCoverage.test_transfer_invalid_destination_should_reject`

**Source:** `tests/sdk/test_extended_contracts.py`

**Relevant owner:** Guava SDK

**Execution layer:** Native MockCall

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-x001)


**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** Transfer destination not validated client-side. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** SDK command / telephony. **Owner category:** Guava SDK / installer.

**Problem:** Transfer destination not validated client-side

**Expected:** Reject malformed phone/SIP destinations before queuing.

**Actual:** Invalid destination string queued; no actual carrier transfer attempted.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/offline-corrected.txt`; SHA-256: `f77edf221a369c64c5ce55f1a62915dc975852115ef251d018e0cc3f24b163b9`.

```text
FAIL: test_transfer_invalid_destination_should_reject (test_extended_contracts.CommandCoverage.test_transfer_invalid_destination_should_reject)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\prana\aegis-care\tests\sdk\test_extended_contracts.py", line 26, in test_transfer_invalid_destination_should_reject
    with self.assertRaises(ValueError):MockCall().transfer('not a phone number or SIP URI')
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: ValueError not raised

```

**Proposed owner action / workaround (not applied):** Validate at the application boundary; verify server rejection separately.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
