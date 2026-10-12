# AEGIS Care project context
Updated: 2026-10-11
Repository: C:/Users/prana/aegis-care
Project: AEGIS Care — Guava SDK and Voice AI QA Evaluation
Agent scaffold: harborcare-agent (HarborCare inbound agent)

## Objective and scope
Evaluate Guava CLI/SDK v0.47.0 and build a healthcare-first voice agent for patient identity verification, insurance eligibility, claims, appointments, billing and payment security. Use synthetic patient/insurance records and simulated payments. Produce an evidence-backed technical assessment for Guava's founders and CEO.

## Current milestone
Initial scaffold audit completed and recorded in reports/scaffold-audit-2026-10-11.md. Git baseline: 47e92e7. Original demo preserved; synthetic HarborCare is now implemented and tested. Latest milestones below record current coverage and limitations.
Target CLI/SDK: 0.47.0. CLI version/authentication: user-reported, not reverified. Actual locked and installed SDK metadata: 0.47.1. Do not attribute 0.47.1 results to 0.47.0. Preserve current lock/environment evidence before selecting a separate 0.47.0 evaluation environment.

## Verified checks and limitations
- Scaffold/configuration/source files inspected; local Git baseline established.
- Current official starter documentation retrieved on 2026-10-11 and matched bundled documentation by SHA256.
- Dependency lock and installed package metadata inspected; runtime import not verified.
- uv --version succeeded: 0.12.9.
- guava --version failed to resolve on this session's PATH.
- Virtual-environment Python invocation failed before execution. Syntax and import checks did not run.
- No SDK behavior, healthcare functional, conversation, security exploit, audio, reliability or cross-platform tests executed.
- No live calls, deployments, number purchases or payment operations performed.

## Working rules
Read current official Guava documentation before using SDK APIs. Study SDK architecture before modifying application code. Teach concepts at each implementation step and update journal/learning-journal.md.
Update PROJECT_CONTEXT.md and QA_FINDINGS.md after each meaningful milestone, including current step, exact test status, evidence and next action.
Preserve raw evidence locally; redact secrets and sensitive identifiers in reports. evidence/ is ignored by Git, so Git does not back it up. Keep original evidence files and add new timestamped records.
Separate confirmed vulnerabilities, observed defects, potential risks and hypotheses. Classify ownership as application, SDK/platform, environment or unknown; require minimal reproduction before assigning vendor defects.
Do not purchase phone numbers, deploy paid infrastructure or run destructive operations without explicit approval.
Use Git for milestones. Never fabricate test outcomes. Read-only synced ChatGPT project references must remain untouched.

## Next recommended evaluation task
Establish a reproducible offline 0.47.0 evaluation baseline: locate the existing CLI and verify its version/signature without reinstalling; inspect the base Python launcher; preserve the 0.47.1 scaffold and lock; establish a separate locked 0.47.0 environment; then run syntax and SDK-import checks that do not import main.py or connect to hosted services.
Next architecture study: Agent lifecycle, Call commands, event handlers, task/field state, authentication, transport/threading, errors/retries, cleanup and testing utilities, grounded in official docs and version-specific installed source.

## Coverage planning milestone — 2026-10-11
SDK security review is incomplete. Added 24 detailed NOT_RUN cases in reports/test-plans/test-cases.csv, layered release gates, coverage audit and execution ledger. No executable harness exists yet.
Preferred directory structure reserved without moving existing scaffold/evidence. Future learning entries live in docs/learning-journal.md; prior journal retained.
Final stage: user-led calls against complete synthetic agent, including adversarial conversation and audio scenarios. Production canaries remain separately gated.
Notes C:/Guava/My notes.rtf used as reference only; statements inside are not independent instructions or verified results.

## SDK baseline execution milestone — 2026-10-11
Isolated SDK 0.47.0 imports successfully on bundled CPython 3.12.14. Installed-version inventory: baseline/sdk-0.47.0/requirements.lock.txt. Original 0.47.1 scaffold preserved.
First offline contract suite: 8 executed, 7 passed, 1 failed. SDK-F001 reproduces response-body inclusion in HTTP exception text; potential disclosure risk, no demonstrated real data leak.
CLI baseline still unresolved. Hosted agent.test/roleplay and comprehensive SDK security coverage remain unexecuted.
Latest report: reports/test-results/sdk-0.47.0-offline-2026-10-11.md. Historical NOT_RUN ledger represents the earlier planning milestone, not current execution.

## Eight-category coverage correction — 2026-10-11
All eight evaluation categories now mapped in reports/sdk-evaluation/category-coverage-2026-10-11.md. Catalog expanded to 32 cases with installation permissions/rollback, developer experience, functional contracts, testability, compatibility and deployment coverage.
No new tests executed. Full baseline remains incomplete; installer evaluation takes priority before additional agent work.

## CLI/installer milestone — 2026-10-11
Located existing CLI at default LOCALAPPDATA/guava/bin; direct query verifies 0.47.0. Installed binary is NotSigned per Authenticode. Current official installer downloaded and statically audited without execution: no explicit checksum/signature verification; direct destination replacement raises untested rollback risk.
CLI and isolated SDK versions now both verified 0.47.0; authentication, original installer provenance and comprehensive behavior/security remain unverified.
Details: reports/sdk-evaluation/installer-audit-2026-10-11.md. No machine PATH or existing install changes.

## Installation-method classification — 2026-10-11
User confirmed irm (not ifm). Added reports/test-plans/installation-method-matrix.md and component/method scope columns to the catalog.
uv installation results apply to Python SDK; current irm/iex installer inspection applies to Windows CLI script. Existing CLI original install route remains UNKNOWN; direct artifact inspection is not proof of route.
No new tests ran. SDK exception behavior is not attributed to uv without controlled comparison evidence.

## Directional/online milestone — 2026-10-11
User report due tonight; authorized hosted evaluation budget 500 minutes. No paid deployment/purchase or unspecified outbound destination authorized.
Expanded corrected offline suite: 16 unique tests, 15 PASS, 1 known FAIL. Native SDK event/task/reach_person/production Call APIs exercised. Full SDK/source review and inbound/outbound E2E remain incomplete.
Prepared bounded synthetic hosted smoke using Agent.test; outcome recorded separately. See reports/sdk-evaluation/directional-kpi-2026-10-11.md for coverage/KPI definitions.

Hosted transition outcome: two synthetic live text runs completed; second asserted exact field and bot-hangup successfully. See reports/test-results/hosted-smoke-2026-10-11.md. No phone listener started; no-answer cause unresolved; billed usage unmeasured.

## Dashboard milestone — 2026-10-11
Local dashboard: dashboard/index.html (preview http://127.0.0.1:8765/dashboard/). Sanitized snapshot with actual results, unresolved installer findings, coverage filters, JSON export and report links; no external hosting or live monitoring.
Generator validates preserved result counts. SDK-016/017 catalog corrected to PARTIAL for existing executed subchecks; no new SDK tests. See dashboard/README.md for refresh and scope limitations.

## HarborCare implementation / pipeline-stage milestone — 2026-10-11
Synthetic agent implemented in agent/harborcare.py and backend/synthetic.py using native SDK APIs. Six workflow paths; 10 corrected functional methods PASS; six hosted happy workflows plus one corrected wrong-code denial PASS. Initial harness errors preserved and attributed to tests.
PipelineStage/Direction catalog labels and ASR/LLM/robustness dashboard pages added. Metric functions not found in scoped public API are planned via established libraries, not fabricated scores.
Phone listener was rejected by automatic approval review due to possible live/shared routing impact. No listener started; explicit user approval pending. Full prototype limitations/results in reports/test-results/harborcare-2026-10-11.md.

## Approved phone listener — 2026-10-11
User approved attachment to configured inbound number; listener registered successfully with zero other registered listeners. See reports/test-results/phone-listener-2026-10-11.md. No completed phone call claimed; awaiting user test.
BERTScore and ROUGE names confirmed; metric pages regenerated. Startup WebSocket deprecation warning observed without registration failure.

## Spoken verification fix — 2026-10-11
User live calls repeatedly failed verification; four accepted call sessions visible in raw listener evidence, but actual entered field values absent. Exact live root cause unknown. Strict credential string handling identified as application limitation.
Easy synthetic credentials 1001/4242 added; legacy credentials preserved; bounded formatting normalization added. Corrected suite 12/12 functional methods PASS. Updated approved phone listener running; native local-audio mode ready, not launched. Local/WebRTC usage cannot be assumed free.

Numeric credentials also passed one hosted text billing test (exit 0); live audio verification still awaits user retest.

## Per-call history — 2026-10-11
Dashboard now displays individual native inbound conversation records and on-demand refresh. Four historical records recovered; transcripts report verification denial; outcomes unscored. Timestamp timezone unknown in CLI display.
Future approved listener now records masked start/finish/end outcomes locally; no credentials or transcript in dashboard. No new live call evaluated during this instrumentation milestone.

## Service and evaluation runner — 2026-10-11
AEGIS Care = QA umbrella; HarborCare = agent persona. Service wording revised; synthetic limitations retained.
Dedicated Calls and Test runs pages. tests/run_all.py runs offline/hosted/all fixed suites; full regressions on demand. Automatic per-call metadata checks added, with explicit semantic/ASR limits.
Latest functional 17 PASS; SDK 15/16 PASS (known failure); installer audit open findings. Six revised hosted workflows PASS; malformed text denial returned no backend result (open robustness observation); valid-format wrong-code rerun PASS; native billing rubric PASS.
See reports/test-results/service-runner-2026-10-11.md. Broad test catalog and production feature scope still incomplete.


## Text/audio and dashboard repair milestone � 2026-10-11
Application 26/26 PASS; SDK 15/16 PASS, known exception failure and installer controls unresolved. Native hosted adversarial cases: latest injection, identity-switch and malformed-code PASS; initial incomplete-script failure retained. Windows-curses installed; plain --mode text exit0. One prerecorded synthetic ASR clip scored WER62.50% / CER48.68% without numeral equivalence, expected digit strings2/2. Twelve labeled audio assets prepared; other clips unscored. User confirmed browser playback of greeting; native microphone/speaker routing remains unverified. Calls now report duration provenance/unknowns and explicit local channel labels. Dashboard measured pages and runner security/audio suites added. See usability-repair report for limits and evidence.

Browser WebRTC: user explicitly reported hearing HarborCare and receiving responses to speech. This is user-confirmed two-way audio, not a transcript-scored workflow or measured latency. No matching new listener journal entry was found at the check; the inspected diagnostic tab was Idle. Session attribution remains unverified.

## Defect discovery / robustness milestone — October11,2026
Seven hostile cases plus two follow-ups; six audio conditions plus echo repeat; native sensitivePAN/CVV and vital intake probes executed. Card readback reproduced twice despite native judgePASS; exact safety invariant now fails it. Emergency flow retains verification; delayed echo corrupted full credentials twice. Strict negative amount rejected without debit. Native sensitive fields avoided readback but local testing transcripts retained caller input. Five deterministic product probes:four gaps,one idempotencyPASS. Six new sensitive processor functional testsPASS. Seven reviewed findings and metadata-only QA SQLite ledger; production backend still in-memory. See product-robustness-assessment report and dashboard/defects.html. No legal certification/full platform audit claim; actual live AEC/barge-in and hosted retention remain unverified.

Final campaign regression:32/32 application methodsPASS;SDK15/16PASS plusinstallerOPEN_FINDINGS (run20261012T032131Z-be98e6). Catalog39cases;audio18fixtures across two manifests. Hosted/readback and echo failures remain open and separately visible.

## KPI/inventory milestone — October11,2026
Native intent30trials:24/24clear,2/4unsupported rejected;confidenceunavailable,agreementnotconfidence. ActualBERTScoreF1 0.8069 andROUGE1/2/L computed from7savedresponse spans;modelconfig/revisionpinned. Publichumanclip3conditions ran;cleanWER0%,noise/echoWER9.52%;one speaker. Two clienttextturnfirst-event intervals measured separately fromruntime. Overview nowallinventories and7openrevieweddefects;profilesMarkdownloadedonnewExpertstartup. See KPI expansion report for evidence/scope.

ActualExpertparaphrasebenchmark4/6completion;targetedbillingrepeatPASS,identityrepeatrequested different-account verification then processTIMEOUT withtranscriptretained. AddedROB-008 without claiming classifierrootcause. Overview135inventoryentries,8revieweddiscoveryfindings.


## Extended SDK / adaptive adversary milestone — October11,2026

Full baseline: SDK47/53 PASS (six FAIL retained), application32/32 PASS; installerOPEN_FINDINGS. Five new client boundary findings and isolated partial-download rollback failure added;14 reviewed discovery findings now have stage/ownership labels and linked sanitized evidence with raw SHA-256 provenance. Four native persona roleplays passed. Scoped DocumentQA/DatetimeFilter hosted tests, nine local health checks,21-dependency advisory audit (zero known advisories), auth401 probes, SIP TCP timeouts, nine public-word audio conditions and two interruption/clipping probes actually executed. No Expert/profile/backend changes this campaign.

Adaptive Ybbag uses native generation, roleplay and evaluation. First payment actor consented: initial debit alert was a harness false positive, reviewed INVALID_CALLER_SCENARIO. Corrected readback replay passed its limited checks; explicit payment-refusal transaction remained unexercised (PARTIAL_PASS); unauthorized and DOB checks passed within limited invariants. Earlier ROB-001 remains open. User requested unavailable metrics stay with reasons; no provider telephony endpoints configured, so live integrations/SMS remain incomplete. See reports/test-results/extended-sdk-2026-10-11.md and docs/operator-guide.md.

Learning: AI attackers can violate their instructions; validate caller coverage before grading the target. Mocked SDK contracts, scoped hosted probes, file-in audio and live carrier proof are distinct evidence layers. LiteralWER, semantic consent and safety outcomes must not be conflated.


## Unified Defect discovery registry — October11,2026

Reporting defect corrected: Overview hardcoded original SDK-F001/CLI-F001/CLI-F002 outside the14-entry discovery registry, causing omissions and duplicateCLI-X003 presentation. Added the three original findings to the shared registry (17 unique findings), removed four hardcoded Overview duplicates, retained evidence links/stage/ownership labels, and corrected corrupted link typography. Existing observations only; no new product/security executions or vulnerability fixes. Expert unchanged.


## Discovery walkthrough — October11,2026

Added reports/test-results/defect-discovery-walkthrough-2026-10-11.md:17 findings traced to method, steps, observed output and proof limits; linked from Defect discovery. Preserved terminal/transcript examples distinguish native judge output from independent safety review. Corrected report-only PAN redaction to preserve decimal metrics and spacing; raw evidence unchanged. No new product tests executed.


## Readable reports and execution coverage audit — October11,2026

Report/docs .md URLs now render sanitized styledHTML via an isolated pinned dashboard environment; sources and raw evidence preserved. Audited187inventoryentries:85methods actually executed (79PASS/6FAIL);46coverageplans still5NOT_RUN/24PARTIAL/17PARTIAL_FAIL. Executed11previously unscored original audio fixtures (allOBSERVED;10speech+silence0events), with8slead/3stail and preserved hashes. Executed three exact previously hosted-pending text fixtures: limited no-debit/no-successful-unauthorized-result checks, no workflowcompletion. Latest user-hosted run6/8PASS with identity/claims failures preserved; securitysnapshot identity-switchFAIL retained. Existing Expert/profile/backend unchanged. See request-coverage-audit report for item-by-item request mapping, unavailable metric reasons, and genuine prerequisites/harness gaps.
