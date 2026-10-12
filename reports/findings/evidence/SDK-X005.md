# SDK-X005: Explicit empty outreach settings replaced by global SMS

## In plain language

A contact with an empty outreach list inherits the campaign SMS setting. If your app uses an empty list to mean do not contact, this could defeat that intention. Guava must clarify the intended meaning; our upload was mocked and sent no message.

## Which test caught this?

**Case:** `SDK-X005`

**Detector:** `HelperAndTenacityCoverage.test_tenacity_explicit_empty_contact_preserved`

**Source:** `tests/sdk/test_extended_contracts.py`

**Relevant owner:** Guava SDK

**Execution layer:** Mocked contact upload

[Finding-to-test traceability](../../test-plans/finding-to-test-map.md#sdk-x005)


## Expected input and what could happen

Outreach modalities are ways a campaign may contact someone, such as SMS. This is a campaign-upload test, not a feature used by our inbound HarborCare calls.

**Actual tested input:** one synthetic contact with `outreach_modalities=[]`, uploaded into a campaign whose global setting was `outreach_modalities=["sms"]`. The HTTP upload was mocked; no contact was uploaded and no SMS was sent.

```json
{
  "contact_setting_before_upload": [],
  "campaign_default": ["sms"],
  "contact_setting_in_mocked_upload": ["sms"]
}
```

**Our test expectation:** preserve the explicitly supplied empty per-contact list rather than silently replacing it. A nonempty per-contact override worked in another control test.

**Meaning still to clarify:** does Guava define an empty list as no outreach, inherit defaults, or an invalid setting? We have not established that the public contract promises an opt-out through this field. The test is a safety expectation, not proof of a documented-contract breach.

**Possible consequence:** an application that interprets `[]` as do not contact could prepare an SMS-capable contact despite that intention. Whether a message actually sends also depends on server settings, campaign state and consent checks. No unwanted message or legal breach was demonstrated.

**Safe proposed workaround:** do not treat `[]` as a verified opt-out. Exclude contacts without permission from uploads, or use an explicitly documented suppression mechanism after Guava confirms it. A clear API could distinguish omitted/inherit from empty/none; that is a recommendation, not a documented current guarantee.


**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** Explicit empty outreach settings replaced by global SMS. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** Campaign / telephony preparation. **Owner category:** Guava SDK / installer.

**Problem:** Explicit empty outreach settings replaced by global SMS

**Expected:** An explicitly supplied per-contact setting follows documented precedence.

**Actual:** Mocked upload replaced contact outreach_modalities=[] with global [sms]. No SMS sent. Empty-list opt-out semantics need vendor clarification.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/offline-corrected.txt`; SHA-256: `f77edf221a369c64c5ce55f1a62915dc975852115ef251d018e0cc3f24b163b9`.

```text
FAIL: test_tenacity_explicit_empty_contact_preserved (test_extended_contracts.HelperAndTenacityCoverage.test_tenacity_explicit_empty_contact_preserved)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\prana\aegis-care\tests\sdk\test_extended_contracts.py", line 120, in test_tenacity_explicit_empty_contact_preserved
    campaign.upload_contacts([contact],outreach_modalities=['sms']);self.assertEqual(post.call_args.kwargs['json']['contacts'][0]['outreach_modalities'],[])
                                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['sms'] != []

First list contains 1 additional elements.
First extra element 0:
'sms'

- ['sms']
+ []

```

**Proposed owner action / workaround (not applied):** Clarify empty versus unset semantics; do not assume[]disables outreach when global SMS is enabled.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
