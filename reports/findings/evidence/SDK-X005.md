# SDK-X005: Explicit empty outreach settings replaced by global SMS

**Current step:** SDK and unchanged Expert adversarial evaluation.

**Status and scope:** Explicit empty outreach settings replaced by global SMS. Confirmed client behavior; downstream impact limited or unverified.

**Stage:** Campaign / telephony preparation. **Owner category:** Guava SDK / installer.

**Problem:** Explicit empty outreach settings replaced by global SMS

**Expected:** An explicitly supplied per-contact setting follows documented precedence.

**Actual:** Mocked upload replaced contact outreach_modalities=[] with global[sms]. No SMS sent. Empty-list opt-out semantics need vendor clarification.

**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.

- Local path: `evidence/2026-10-11/extended-sdk/offline-corrected.txt`; SHA-256: `f77edf221a369c64c5ce55f1a62915dc975852115ef251d018e0cc3f24b163b9`.

```text
test_action_callback_executed (test_extended_contracts.CallbackCoverage.test_action_callback_executed) ... ok
test_action_request_callback_suggestions (test_extended_contracts.CallbackCoverage.test_action_request_callback_suggestions) ... ok
test_agent_dtmf_callback (test_extended_contracts.CallbackCoverage.test_agent_dtmf_callback) ... ok
test_agent_speech_interruption_flag (test_extended_contracts.CallbackCoverage.test_agent_speech_interruption_flag) ... ok
test_caller_dtmf_callback (test_extended_contracts.CallbackCoverage.test_caller_dtmf_callback) ... ok
test_caller_speech_revisions_have_same_id (test_extended_contracts.CallbackCoverage.test_caller_speech_revisions_have_same_id) ... ok
test_escalate_callback (test_extended_contracts.CallbackCoverage.test_escalate_callback) ... ok
test_invalid_dtmf_event_rejected (test_extended_contracts.CallbackCoverage.test_invalid_dtmf_event_rejected) ... ok
test_question_callback_answer_correlated (test_extended_contracts.CallbackCoverage.test_question_callback_answer_correlated) ... ok
test_question_failure_uses_safe_fallback (test_extended_contracts.CallbackCoverage.test_question_failure_uses_safe_fallback) ... ok
test_session_end_callback (test_extended_contracts.CallbackCoverage.test_session_end_callback) ... ok
test_task_callback_failure_informs_dialog (test_extended_contracts.CallbackCoverage.test_task_callback_failure_informs_dialog) ... ok
test_task_complete_callback_executed (test_extended_contracts.CallbackCoverage.test_task_complete_callback_executed) ... ok
test_add_info_uses_variable_namespace (test_extended_contracts.C
```

**Proposed owner action / workaround (not applied):** Clarify empty versus unset semantics; do not assume[]disables outreach when global SMS is enabled.

**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.

**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.
