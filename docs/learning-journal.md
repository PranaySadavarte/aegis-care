# Learning journal
Earlier entries: journal/learning-journal.md.
## 2026-10-11 — Coverage and layered testing
No SDK vulnerabilities have been independently confirmed; coverage areas are hypotheses until tested.
Learned: verification is a backend authorization decision, not field extraction. Payment redaction does not authorize access to billing data. Disconnect recovery requires idempotency and reconciliation to avoid duplicate transactions.
VAD/endpointing controls when speech is considered started/finished; ASR converts speech to text; TTS converts response text to audio. Their quality must be measured separately from business outcomes.
Next: exact-version baseline, then offline SDK contracts and documented live test capabilities. No security/behavior tests ran this milestone.

## 2026-10-11 — First executed SDK contracts
Established exact SDK 0.47.0 environment using working bundled Python 3.12.14; executed eight offline tests (seven passes, one failure).
Learned: MockCall isolates handler state but does not emulate server authorization or lifecycle. Agent.patch copies callback maps without changing the original. The Client constructor can perform a deprecation request; offline tests must prevent network side effects.
An exception is a data sink: HTTP response content may become exception text and later logs or telemetry. Reproducing synthetic marker inclusion confirms that behavior, but not an actual production breach.
Official agent-testing guide separates offline MockCall from live scripted/roleplay sessions. Next extend mock-backed SDK fault/security tests and complete CLI identification.

## 2026-10-11 — Coverage correction
Testing a Python SDK package does not validate the Windows CLI installer. A binary may be signed while its installer never checks that signature; computing a hash alone does not verify it against a trusted expected value.
Eight categories require separate evidence and completion criteria. Added missing detailed cases; no new runtime tests performed.

## 2026-10-11 — Installer verification
Direct path execution verified CLI 0.47.0 even though this process cannot resolve guava on PATH. Authenticode reports NotSigned for the installed binary.
Read-only installer audit found no explicit checksum/signature enforcement in current official script. HTTPS, checksums and publisher signatures address different trust boundaries; a recorded local hash preserves identity but does not authenticate the publisher.
Direct downloads over the destination raise a failure-recovery question, not a proven rollback defect. Next use isolated/mocked failure paths before drawing behavioral conclusions.

## 2026-10-11 — Installation methods
uv manages Python package/environment installation here. irm retrieves the Windows installer script; iex executes it, and that script installs the CLI binary. Route labels distinguish supply-chain/setup tests from SDK runtime tests.
A defect observed after uv installation is not automatically caused by uv. Controlled comparisons require matching versions, runtime and transitive artifacts.

## 2026-10-11 — Online and KPI transition
Offline contracts isolate Expert SDK logic; hosted text tests exercise live dialog/state without validating actual phone transport. Native reach_person and event decoding used for outbound subchecks, not replaced with custom logic.
A 15/16 test pass count is a regression metric, not a 93.75% voice-agent success rate. Field sensitive serialization is not proof of hosted redaction.
DocumentQA server mode uploads documents and concurrent instances need namespaces. Full SDK review still in progress.

Hosted Agent.test now executed successfully; added stable extracted-field and termination assertions. Text testing can validate a live dialog/Expert interaction without registering a phone number listener. Actual phone readiness still needs a separate listener/routing test.

## 2026-10-11 — Results dashboard
A test pass count is not a count of resolved findings. Static installer observations, hypotheses and unexecuted coverage require separate views. A snapshot dashboard must label freshness and cannot imply continuous monitoring.

## 2026-10-11 — HarborCare and stage-specific evaluation
A backend authorization gate checks the verified session subject before every sensitive read or mutation; model field extraction does not itself grant access.
Payment idempotency needs both a stable key and matching request fingerprint. The synthetic ledger implements this in process memory, not durable production storage.
Native Agent.test exercised six happy workflows and a wrong-code denial. Test harness errors must be preserved and separated from SDK/application defects.
ASR RTF requires isolated recognition processing duration; total agent runtime cannot substitute. Model confidence and rubric pass are different concepts. BERT/ROUGE names remain provisional pending user confirmation.

## 2026-10-11 — Approved inbound registration
The local Expert registered with Guava via native listen_phone. Registration confirms an available listener but does not establish PSTN/audio quality or successful caller workflow.
Startup deprecation warnings require tracking independently of actual failures; do not promote them into vulnerabilities.
User confirmed BERTScore and ROUGE. Scores remain unmeasured.

## 2026-10-11 — Voice-friendly credentials
Text correctness and spoken usability differ. Defined format normalization is safer than fuzzy credential matching; wrong digits still reject. Logs without entered values protect privacy but limit ASR root-cause attribution.
call_local means local microphone/speakers with hosted WebRTC, not local model inference or necessarily free usage. Offline backend tests are the known no-hosted-call path.

## 2026-10-11 — Call outcomes versus test grades
A completed call or transcript denial is an observation. Pass/fail requires a known expected scenario: rejecting a wrong code may be correct, while rejecting a correct code is a defect.
Native conversation records can reconstruct past calls, but precise application outcomes are easier to capture at the Expert callback. Mask identifiers and omit credentials; retain raw originals locally for attribution.

## 2026-10-11 — Background evaluation versus regression
HarborCare is the caller-facing service; AEGIS Care evaluates it. Do not narrate test internals during every call.
Each call can receive scoped observation checks without launching unrelated regressions. Full suites are explicit operator actions. No test result means inconclusive, not pass.
Native SDK semantic rubric evaluation complements deterministic backend checks but does not produce calibrated confidence or acoustic metrics.
Preserve transcript before asserting outcomes so failed hosted cases remain diagnosable. Malformed code and valid-format wrong code test different boundaries.

## 2026-10-11 � layered text and audio evidence
A text chat mode does not exercise microphones or speakers. Browser playback, native output capture, microphone permission, transport registration and successful speech recognition are different observations. Test each boundary separately. Native Agent.test_audio and on_caller_speech avoid inventing a parallel transport; Jiwer supplies standard WER/CER. Spoken digit words versus numeric transcripts can inflate literal errors even when identity values survive. Report normalization and sample scope. IntentRecognizer in installed0.47.0 returns SuggestedAction lists; read the pinned implementation when current documentation examples differ. Clear authorization before changing identity and collect fresh fields. Assert exact business values/actions and semantic safety; allow natural paraphrases.

Browser WebRTC: user explicitly reported hearing HarborCare and receiving responses to speech. This is user-confirmed two-way audio, not a transcript-scored workflow or measured latency. No matching new listener journal entry was found at the check; the inspected diagnostic tab was Idle. Session attribution remains unverified.

## October11,2026 — defect finding and evaluation calibration
Passing unit tests do not establish conversation safety: the backend rejects negative integers but the dialog may extract a different positive amount. A native model judge can produce incorrect PASS/FAIL; pair it with independent exact readback/authorization/action invariants and preserve disagreements. A complete digit match differs from substring presence; trailing echo digits must fail entity scoring. Sensitive field collection, caller transcript retention, spoken readback, recordings and diagnostics are separate sinks. NumPy seeded noise and SoundFilePCM fixtures provide repeatability; delayed caller copy and prerecorded speech overlap are not real acoustic echo cancellation or live interruption tests. AEC needs time-aligned speaker reference and microphone signals; indiscriminate transcript deduplication can suppress legitimate repeated consent. QA SQLite indexes sanitized observations/hashes; durable healthcare backend state remains a separate feature. Synthetic card/vital receipts deliberately provide no payment/clinical service.

## KPI/inventory milestone — October11,2026
Native intent30trials:24/24clear,2/4unsupported rejected;confidenceunavailable,agreementnotconfidence. ActualBERTScoreF1 0.8069 andROUGE1/2/L computed from7savedresponse spans;modelconfig/revisionpinned. Publichumanclip3conditions ran;cleanWER0%,noise/echoWER9.52%;one speaker. Two clienttextturnfirst-event intervals measured separately fromruntime. Overview nowallinventories and7openrevieweddefects;profilesMarkdownloadedonnewExpertstartup. See KPI expansion report for evidence/scope.


## Extended SDK / adaptive adversary milestone — October11,2026

Full baseline: SDK47/53 PASS (six FAIL retained), application32/32 PASS; installerOPEN_FINDINGS. Five new client boundary findings and isolated partial-download rollback failure added;14 reviewed discovery findings now have stage/ownership labels and linked sanitized evidence with raw SHA-256 provenance. Four native persona roleplays passed. Scoped DocumentQA/DatetimeFilter hosted tests, nine local health checks,21-dependency advisory audit (zero known advisories), auth401 probes, SIP TCP timeouts, nine public-word audio conditions and two interruption/clipping probes actually executed. No Expert/profile/backend changes this campaign.

Adaptive Ybbag uses native generation, roleplay and evaluation. First payment actor consented: initial debit alert was a harness false positive, reviewed INVALID_CALLER_SCENARIO. Corrected readback replay passed its limited checks; explicit payment-refusal transaction remained unexercised (PARTIAL_PASS); unauthorized and DOB checks passed within limited invariants. Earlier ROB-001 remains open. User requested unavailable metrics stay with reasons; no provider telephony endpoints configured, so live integrations/SMS remain incomplete. See reports/test-results/extended-sdk-2026-10-11.md and docs/operator-guide.md.

Learning: AI attackers can violate their instructions; validate caller coverage before grading the target. Mocked SDK contracts, scoped hosted probes, file-in audio and live carrier proof are distinct evidence layers. LiteralWER, semantic consent and safety outcomes must not be conflated.
