# AEGIS Care QA findings
Updated: 2026-10-11
Current step: scaffold audit complete; runtime/version baseline pending.
No independently confirmed security vulnerabilities or completed SDK behavioral tests at this milestone.

## Findings register
| ID | Status / owner | Expected versus actual | Evidence | Recommendation / workaround |
| --- | --- | --- | --- | --- |
| QA-001 | Confirmed version mismatch / project | Target SDK 0.47.0; lock and installed metadata identify 0.47.1 | harborcare-agent/uv.lock; .venv/Lib/site-packages/guava_sdk-0.47.1.dist-info | Preserve current environment; evaluate 0.47.0 separately; label all results by exact version |
| QA-002 | Observed environment blocker / local environment; cause unknown | CLI version query should execute; guava not resolved on session PATH | Prior audit and session command output | Locate existing executable; inspect PATH; do not infer missing installation or invalid authentication |
| QA-003 | Observed environment blocker / local environment; cause unknown | Python should run syntax/import checks; launcher failed with "The file cannot be accessed by the system." | Prior audit and session command output; .venv/pyvenv.cfg | Inspect base interpreter before repairing/recreating environment; runtime tests remain blocked |
| QA-004 | Confirmed unfinished scope / application | Healthcare workflows required; source is introduction/RAG demo | harborcare-agent/main.py | Study architecture, then implement gated synthetic workflows |
| QA-005 | Potential privacy risk / application | Patient-related logs should be redacted; demo logs questions and caller names | Static inspection of main.py | Redact structured events before healthcare tests; no observed data leak |
| QA-006 | Compatibility hypothesis / project | Demonstrated local/hosted compatibility; local metadata 3.13.14, configured hosted image 3.14 | .venv/pyvenv.cfg; guava.toml; pyproject.toml | Verify supported runtime matrix; differing versions alone are not a defect |
| QA-007 | Historical user report, unverified / installer owner if reproduced | Expected documented signature/integrity checks; prior report describes unsigned executable and absent installer integrity verification | Original executable, installer and signature transcript not available in reviewed evidence | Recover original evidence; independently inspect exact binaries/scripts; do not claim confirmed vulnerability or exploitability |
| QA-008 | Resolved process gap / project | Version control and ignore rules required; originally absent, now present | Commit 47e92e7; .gitignore | Continue milestone commits; preserve ignored evidence separately |

## Checks actually performed
| Check | Actual outcome |
| --- | --- |
| Scaffold/source/configuration inspection | Completed; demo scope and logging/import-time initialization identified |
| Documentation retrieval and SHA256 comparison | Match: 7656AF3A01E3475EFC662BBD0DFD4E10DC0308FD0B7400F9773660819D36AAF2 |
| Lock/installed package metadata inspection | SDK 0.47.1 identified; no runtime import |
| uv version query | Succeeded: 0.12.9 |
| CLI version query | Failed: command unresolved |
| Python syntax/import invocation | Blocked before Python execution; neither check ran |
| Git baseline and status | Commit 47e92e7 created; clean repository observed before this documentation milestone |

## Evidence handling
Preserved evidence/2026-10-11/official-coding-agent-starter.md and scaffold-sha256.csv without modification. Source snapshot and hashes are raw artifacts; prior command outputs remain in conversation history, summarized in the audit. Full original command transcripts were not saved as local files. Do not represent summaries as raw transcripts.
Reports omit configured phone/project/organization identifiers. Historical security evidence remains missing. No clinical records or payment credentials were used.

## Planned tests — not run
- Baseline: exact CLI/SDK versions, signature/installer checks, dependency reproducibility, syntax and safe SDK imports.
- SDK: event registration/dispatch, task/field transitions, commands, errors, retries, threading and session cleanup.
- Healthcare: synthetic verification and access denial, eligibility, claims, appointment conflicts, billing and simulated payment authorization/idempotency.
- Conversation/security: prompt injection, unauthorized disclosure, interruptions, ambiguity and log redaction.
- Audio/reliability: noise, accents, barge-in, latency, disconnects, timeouts and concurrency.
- Cross-platform: Windows, Linux and macOS only where actually available.

## Owner escalation standard
For every meaningful finding record exact versions, timestamp, current step, expected/actual behavior, reproduction, raw evidence location, impact, confidence, owner and workaround. SDK/platform attribution requires a minimal reproduction excluding application logic where feasible. Observations and hypotheses must never be promoted to confirmed vulnerabilities without supporting evidence.

## Coverage milestone — 2026-10-11
QA-009: Confirmed coverage gap / AEGIS project. Expected detailed executed SDK security cases before application troubleshooting; actual broad plans only at inspection. Added 24 detailed cases and stage gates; all NOT_RUN. No executable automation yet. Proposed solution: establish exact-version runtime baseline then implement and execute cases, retaining evidence.
Coverage report: reports/sdk-evaluation/coverage-audit-2026-10-11.md.
Catalog: reports/test-plans/test-cases.csv. Execution ledger: reports/test-results/execution-status-2026-10-11.md.
No new confirmed vulnerabilities. Identity contamination, API exposure, prompt injection, echo and interrupted-disclosure notes are test hypotheses. Previously reported favorable call observations are not AEGIS test results.

## SDK baseline execution — 2026-10-11
QA-010 / SDK-F001: confirmed exception-content behavior, potential privacy risk; Guava SDK owner. SDK 0.47.0 check_response copies synthetic sensitive response body into HTTPStatusError message. Offline security acceptance test fails. No real credential/PHI leak demonstrated; severity and hosted impact unassessed.
Proposed workaround: safe status/correlation-only boundary logging; not yet implemented/tested. Vendor recommendation: default-redacted bounded diagnostics.
8 offline tests ran: 7 PASS, 1 FAIL. Detailed scope, expected/actual, raw evidence reference, limitations and remaining coverage in reports/test-results/sdk-0.47.0-offline-2026-10-11.md.
QA-003 workaround validated for new isolated environment only: bundled Python runs; original scaffold launcher not repaired.
QA-001 target SDK baseline resolved separately; original scaffold still uses 0.47.1. QA-002 CLI verification remains blocked.

## Coverage correction — 2026-10-11
QA-011: evaluation coverage/sequencing gap, AEGIS owner. Installer case SDK-002 existed but was not implemented/executed; developer experience and deployment lacked dedicated cases. Added SDK-013 through SDK-020 and eight-category coverage matrix. These remain NOT_RUN. No new vulnerability claims.
Expected comprehensive category tracking before declaring a baseline; actual only isolated Python SDK subset verified. Next prioritize CLI and non-executing installer inspection. Prior results/evidence unchanged.

## Installer evidence milestone — 2026-10-11
QA-002 resolved for discovery/version: CLI exists at default install path and directly reports 0.47.0. PATH repair not performed.
QA-007 refined with new evidence: CLI-F001 confirms exact installed binary is NotSigned; CLI-F002 confirms current downloaded installer lacks explicit checksum/AuthentiCode verification. Original 0.47.0 installer provenance remains unverified. These are confirmed control gaps, not demonstrated exploitation.
CLI-H001 potential incomplete replacement/rollback risk remains hypothesis; failure injection not run.
SDK-002 now PARTIAL. Evidence hashes, owner recommendations and proposed untested workarounds recorded in reports/sdk-evaluation/installer-audit-2026-10-11.md.

## Installation-method attribution — 2026-10-11
SDK-F001 reproduced after uv SDK installation; not established as uv-specific.
CLI-F001 unsigned binary observed directly; original installation method unknown.
CLI-F002 verification gap belongs to current downloaded Windows installer; not retroactively assigned to original installed binary's setup.
Added method-specific test matrix; no new executions or findings. Optional pip comparison and package artifact/hash enforcement tests remain NOT_RUN.

## Directional evaluation — 2026-10-11
16 corrected unique offline tests: 15 PASS, 1 existing SDK-F001 failure; no new vulnerabilities.
Initial discovery duplication corrected; raw initial and corrected outputs retained. Production Call isolation is sequential only.
User-reported inbound no-answer remains an unverified symptom with unknown cause; hosted text smoke does not establish phone routing readiness.
Current docs' DocumentQA namespace warning added to test planning; not reproduced here.

Hosted results: native Agent.test completed twice; second exact field/termination assertions passed. This establishes live text test viability, not phone routing or authorization security. Detailed evidence and KPI limitations in reports/test-results/hosted-smoke-2026-10-11.md.

Dashboard milestone: installer control gaps remain unresolved and separate from unit-test failure count. Healthcare implementation and phone/audio KPIs remain pending. Browser search/filter/export validated; no vulnerability fix or SDK test executed during this milestone.

## Application milestone — 2026-10-11
10 corrected functional test methods PASS; seven corrected hosted scenarios PASS. Initial claims assertion type error and wrong-code extra-turn wait were harness defects, corrected with original evidence preserved.
Application scope limitations, AEGIS owner: public demo identity codes; process-memory records/ledger; single-workflow call; only booking, not reschedule/cancel; adversarial/audio and production protections incomplete.
SDK/installer findings remain unresolved; no new SDK vulnerability demonstrated.
Phone attachment blocked by automatic approval review; routing unchanged. Report contains precise rejection and pending approval.

Phone milestone: approved listener registration confirmed; zero other listeners reported. Previous no-answer symptom not yet confirmed resolved until a user call succeeds.
QA-012: observed WebSocket connect() deprecation warning during SDK 0.47.0 startup; registration succeeded. Compatibility observation, not proven defect/vulnerability. Preserve warning for dependency/runtime review.

QA-013: application verification usability. Exact-match-only credential handling rejects formatting variations; repeated live failures user-reported, actual ASR/field values unavailable. Defined normalization and simple numeric aliases implemented and functional-tested; phone outcome after fix unverified.
Initial normalization escaping bug caught and corrected before listener restart; raw initial failures retained.
Four accepted PSTN sessions observed; no successful healthcare phone workflow claimed. Local microphone/WebRTC mode uses hosted service; metering unknown.
WebRTC helper checksum path found by static review; distinct from unresolved CLI installer checksum/AuthentiCode gaps.

QA-014: observability gap, AEGIS application. Manual calls were absent from snapshot dashboard; added native conversation import and masked per-call outcome journal. Four historical denial records recovered, not automatically graded. Refresh latest 30 records is on demand; no historical pagination/full recording viewer yet.
12 functional regression methods PASS; live validation of newly added recorder awaits another call. Raw originals retained.

QA-015: hosted malformed-code path produced no expected backend result in revised service; assertion failed, exact cause unverified because initial transcript not saved. Valid-format wrong numeric code rerun passed; original failure retained. Owner undetermined between application flow/hosted dialog pending minimal reproduction; no unauthorized disclosure demonstrated.
QA-016: caller experience / evaluation orchestration gap addressed with service-style wording, dedicated pages, fixed runner and limited per-call authorization observation. This does not complete broad semantic/audio/production evaluation.
Native SDK TestSession.evaluate billing rubric actually executed and passed. Latest run results/limits in service-runner report.

## Usability and audio milestone � 2026-10-11
QA-017: confirmed Windows chat dependency gap (_curses missing), AEGIS packaging owner. windows-curses2.4.2 installed; import PASS and plain native text command exit0. Native manual TUI remains unverified.
QA-018: confirmed dashboard labeling gap, AEGIS owner: absent duration displayed �Not returned� and local sessions could appear inbound. Explicit source, lifecycle derivation and unknown status/channel implemented; two deterministic checks PASS. No missing-platform-duration root cause claimed.
QA-019: native microphone/speaker usability issue remains unverified in cause. Allow registry state and hosted call registration do not prove routing. Captured synthetic output is nonzero; user hears browser playback. Browser WebRTC diagnostic prepared, actual microphone exchange pending.
26 application methods PASS. Three latest hosted adversarial scenarios PASS with native rubric; initial injection script inactivity failure preserved, not evidence of disclosure. One-clip WER62.50%/CER48.68% includes spoken-digit versus numeral mismatch; not broad ASR failure rate. SDK response-body issue, unsigned executable and installer verification controls remain unresolved.

Browser WebRTC: user explicitly reported hearing HarborCare and receiving responses to speech. This is user-confirmed two-way audio, not a transcript-scored workflow or measured latency. No matching new listener journal entry was found at the check; the inspected diagnostic tab was Idle. Session attribution remains unverified.

## Robustness and sensitive-data discovery — October11,2026
ROB-001: full syntheticPAN/CVV readback reproduced twice; application policy failure, upstream dialog cause not isolated. ROB-002: emergency guidance followed by verification requests. ROB-003: delayed caller echo appended credential digits in two file-in probes, no authbypass/physicalAEC failure proved. ROB-004: native evaluator falsePASS on card readback twice and apparent falseFAIL on canary refusal; exact invariants override judges. ROB-005: native sensitive-field local text test transcripts retain caller values; hosted recording/diagnostic redaction not verified. ROB-006: no attempt limits/durable backendstate, known demo gaps. ROB-007: direct synthetic journal detail injection persists marker, live exploit pathunproved. Strict negative-payment follow-upPASS; originalcaller authorized conditional correction, not a demonstrated unauthorizedcharge. Raw failures preserved and reviewed status separate. See structured seven-finding JSON and product robustness assessment.
