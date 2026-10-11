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
