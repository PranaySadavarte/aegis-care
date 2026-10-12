# SDK-X002: Rejected voicemail settings mutate call state

## In plain language

An invalid voicemail request throws an error after partially changing state. Catching the error does not restore the original call state.

## Which test caught this?

**Case:** `SDK-X002`

**Detector:** `CommandCoverage.test_voicemail_invalid_does_not_mutate_state`

**Source:** `tests/sdk/test_extended_contracts.py`

**Relevant owner:** Guava SDK

**Execution layer:** Native MockCall

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-x002)


**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** Rejected voicemail settings mutate call state. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** SDK command / conversation state. **Owner category:** Guava SDK / installer.

**Problem:** Rejected voicemail settings mutate call state

**Expected:** Rejected configuration leaves prior state/queue unchanged.

**Actual:** Invalid hangup-plus-message raises but sets _voicemail_handler and queues a variable change.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/offline-corrected.txt`; SHA-256: `f77edf221a369c64c5ce55f1a62915dc975852115ef251d018e0cc3f24b163b9`.

```text
FAIL: test_voicemail_invalid_does_not_mutate_state (test_extended_contracts.CommandCoverage.test_voicemail_invalid_does_not_mutate_state)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\prana\aegis-care\tests\sdk\test_extended_contracts.py", line 40, in test_voicemail_invalid_does_not_mutate_state
    self.assertIsNone(c.get_variable('_voicemail_handler'));self.assertEqual(c._command_queue,[])
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'set_voicemail_action' is not None

```

**Proposed owner action / workaround (not applied):** Validate arguments before invoking; isolate retry flow. No SDK code changed.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
