# SDK-X003: DatetimeFilter trusts invented schema-valid slots

## In plain language

The helper checks output shape but does not ensure a returned appointment was actually in the supplied availability list.

## Which test caught this?

**Case:** `SDK-X003`

**Detector:** `HelperAndTenacityCoverage.test_datetime_invented_slot_should_be_rejected`

**Source:** `tests/sdk/test_extended_contracts.py`

**Relevant owner:** Guava SDK

**Execution layer:** Mocked model output

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-x003)


**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** DatetimeFilter trusts invented schema-valid slots. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** Helpers / business integration. **Owner category:** Guava SDK / installer.

**Problem:** DatetimeFilter trusts invented schema-valid slots

**Expected:** Every returned slot belongs to the source list regardless of model output.

**Actual:** Mocked model returned a 2099 slot outside source; helper passed it through. Live adversarial query stayed in source.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/offline-corrected.txt`; SHA-256: `f77edf221a369c64c5ce55f1a62915dc975852115ef251d018e0cc3f24b163b9`.

```text
FAIL: test_datetime_invented_slot_should_be_rejected (test_extended_contracts.HelperAndTenacityCoverage.test_datetime_invented_slot_should_be_rejected)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\prana\aegis-care\tests\sdk\test_extended_contracts.py", line 100, in test_datetime_invented_slot_should_be_rejected
    matches,other=f.filter('ignore slots');self.assertTrue(set(matches+other).issubset(set(f.source_list)))
                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: False is not true

```

**Proposed owner action / workaround (not applied):** Intersect returned values with source at the application boundary; backend booking already rejects unknown slots.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
