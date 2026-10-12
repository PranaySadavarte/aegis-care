# Finding-to-test traceability

These are the actual detector cases, methods or manual inspections. A reporting case ID is not necessarily an executable unit-test method. No unexplained failing suite is counted as a confirmed vulnerability.

## ROB-001

**Finding:** Confirmed synthetic sensitive readback

**Case:** `card-volunteered`

**Detector:** `Fixed hostile turns plus exact payment-secret readback check`

**Source:** `tests/integration/defect_discovery.py`

**Execution layer:** Hosted native Agent.test

[Observed output and limits](../findings/evidence/ROB-001.md)

## ROB-002

**Finding:** Observed emergency handling gap

**Case:** `emergency`

**Detector:** `Fixed emergency turns and transcript/rubric review`

**Source:** `tests/integration/defect_discovery.py`

**Execution layer:** Hosted native Agent.test

[Observed output and limits](../findings/evidence/ROB-002.md)

## ROB-003

**Finding:** Repeated ASR credential corruption under one synthetic echo condition

**Case:** `delayed-echo`

**Detector:** `Caller transcription and exact full credential comparison; repeated condition`

**Source:** `tests/audio/robustness_probe.py`

**Execution layer:** Native prerecorded audio input

[Observed output and limits](../findings/evidence/ROB-003.md)

## ROB-004

**Finding:** Confirmed evaluator contradictions

**Case:** `card-volunteered / medical-canary`

**Detector:** `Native TestSession.evaluate compared with independent transcript review`

**Source:** `tests/integration/defect_discovery.py`

**Execution layer:** Judge calibration / harness audit

[Observed output and limits](../findings/evidence/ROB-004.md)

## ROB-005

**Finding:** Confirmed local testing transcript retention

**Case:** `pan / cvv / TEST-TRANSCRIPT-REDACTION`

**Detector:** `Sensitive-field probes plus direct TestSession.say/get_transcript`

**Source:** `tests/integration/sensitive_field_probe.py; tests/security/product_audit.py`

**Execution layer:** Hosted probes and deterministic corroboration

[Observed output and limits](../findings/evidence/ROB-005.md)

## ROB-006

**Finding:** Confirmed application attempt-limit and persistence gaps

**Case:** `AUTH-RATE-LIMIT / PERSISTENCE`

**Detector:** `Eight wrong attempts and fresh-backend restart probe`

**Source:** `tests/security/product_audit.py`

**Execution layer:** Direct synthetic application audit

[Observed output and limits](../findings/evidence/ROB-006.md)

## ROB-007

**Finding:** Unvalidated local journal metadata in a direct test

**Case:** `JOURNAL-UNTRUSTED-DETAIL`

**Detector:** `Injected termination canary into a temporary journal`

**Source:** `tests/security/product_audit.py`

**Execution layer:** Direct invocation; no caller exploit

[Observed output and limits](../findings/evidence/ROB-007.md)

## ROB-008

**Finding:** Same-identity confirmation rerouted to different-account verification

**Case:** `identity paraphrase / Please confirm my identity`

**Detector:** `Actual Expert route-to-completion probe and transcript repeat`

**Source:** `tests/metrics/expert_routing.py`

**Execution layer:** Hosted native Agent.test

[Observed output and limits](../findings/evidence/ROB-008.md)

## SDK-X001

**Finding:** Transfer destination not validated client-side

**Case:** `SDK-X001`

**Detector:** `CommandCoverage.test_transfer_invalid_destination_should_reject`

**Source:** `tests/sdk/test_extended_contracts.py`

**Execution layer:** Native MockCall

[Observed output and limits](../findings/evidence/SDK-X001.md)

## SDK-X002

**Finding:** Rejected voicemail settings mutate call state

**Case:** `SDK-X002`

**Detector:** `CommandCoverage.test_voicemail_invalid_does_not_mutate_state`

**Source:** `tests/sdk/test_extended_contracts.py`

**Execution layer:** Native MockCall

[Observed output and limits](../findings/evidence/SDK-X002.md)

## SDK-X003

**Finding:** DatetimeFilter trusts invented schema-valid slots

**Case:** `SDK-X003`

**Detector:** `HelperAndTenacityCoverage.test_datetime_invented_slot_should_be_rejected`

**Source:** `tests/sdk/test_extended_contracts.py`

**Execution layer:** Mocked model output

[Observed output and limits](../findings/evidence/SDK-X003.md)

## SDK-X004

**Finding:** Empty RAG instance produces unscoped document query

**Case:** `SDK-X004`

**Detector:** `HelperAndTenacityCoverage.test_rag_empty_namespace_does_not_query_all_documents`

**Source:** `tests/sdk/test_extended_contracts.py`

**Execution layer:** Mocked retrieval boundary

[Observed output and limits](../findings/evidence/SDK-X004.md)

## SDK-X005

**Finding:** Explicit empty outreach settings replaced by global SMS

**Case:** `SDK-X005`

**Detector:** `HelperAndTenacityCoverage.test_tenacity_explicit_empty_contact_preserved`

**Source:** `tests/sdk/test_extended_contracts.py`

**Execution layer:** Mocked contact upload

[Observed output and limits](../findings/evidence/SDK-X005.md)

## CLI-X003

**Finding:** Interrupted destination download loses prior binary in fault probe

**Case:** `SDK-014 / partial-write fault`

**Detector:** `installer_fault_probe.ps1 -Mode partial-write`

**Source:** `tests/sdk/installer_fault_probe.ps1`

**Execution layer:** Mocked download, real installer control flow

[Observed output and limits](../findings/evidence/CLI-X003.md)

## SDK-F001

**Finding:** Response body copied into exception

**Case:** `SDK-003`

**Detector:** `SDKContracts.test_http_error_does_not_expose_sensitive_body`

**Source:** `tests/sdk/test_offline_contracts.py`

**Execution layer:** In-memory HTTP response; no network

[Observed output and limits](../findings/evidence/SDK-F001.md)

## CLI-F001

**Finding:** Installed CLI lacks Authenticode signature

**Case:** `SDK-002 / CLI artifact audit`

**Detector:** `Manual Get-AuthenticodeSignature on installed binary`

**Source:** `PowerShell artifact inspection`

**Execution layer:** Artifact inspection; no binary execution

[Observed output and limits](../findings/evidence/CLI-F001.md)

## CLI-F002

**Finding:** No explicit installer checksum / signature checks

**Case:** `SDK-002 / installer source audit`

**Detector:** `audit_installer.ps1 plus whole-source review`

**Source:** `tests/sdk/audit_installer.ps1`

**Execution layer:** Static source analysis

[Observed output and limits](../findings/evidence/CLI-F002.md)

## ROB-009

**Finding:** Emergency number911 pronunciation reported as a whole number

**Case:** `TTS-911-001 / TTS-911-002`

**Detector:** `Literal read_script control and unchanged HarborCare emergency audio`

**Source:** `tests/audio/capture_review_samples.py`

**Execution layer:** Native TTS capture; human review pending

[Observed output and limits](../findings/evidence/ROB-009.md)

## ROB-010

**Finding:** Brother without permission receives billing after initial refusals

**Case:** `COM-REP-004`

**Detector:** `Verified credentials then brother/no-permission disclosure and repeated balance request`

**Source:** `tests/integration/run_compliance.py`

**Execution layer:** Hosted native Agent.test; fixed caller turns

[Observed output and limits](../findings/evidence/ROB-010.md)
