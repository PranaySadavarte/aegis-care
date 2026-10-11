# AEGIS Care scaffold audit — 2026-10-11
Current step: scaffold audit and architecture study. Feature implementation has not begun.
Scope: local harborcare-agent scaffold; no calls, deployment, purchase, or payment actions performed.

## Evidence and observations
- README, main.py, pyproject.toml, uv.lock, guava.toml and bundled documentation exist.
- main.py is the Guava introduction/RAG demo, not a healthcare agent. Expected: HarborCare patient workflows. Actual: introduction and Guava questions. Classification: unfinished application scope, not SDK defect.
- No Git repository or .gitignore existed at inspection. Expected: versioned, secret-safe baseline. Actual: no version control. Owner: AEGIS project. Recommendation: local Git baseline and ignored environments/evidence.
- uv.lock resolves guava-sdk 0.47.1; installed distribution directory also says 0.47.1. Runtime import was not verified.
- Local virtual environment records CPython 3.13.14; guava.toml selects python-sandbox:3.14; pyproject allows >=3.11. Expected: demonstrated local/hosted compatibility. Actual: different runtimes, untested. Owner: AEGIS project. Recommendation: choose a documented supported baseline after compatibility verification.
- Virtual environment Python invocation failed with "The file cannot be accessed by the system." Syntax/import tests remain BLOCKED, not passed. Classification: environment issue; cause unknown. Workaround: inspect base Python availability and recreate the environment after preserving dependency evidence.
- guava was not resolved on this session's PATH. CLI 0.47.0 installation/authentication are user-reported, not reverified. Owner: local environment. Recommendation: locate installed executable and inspect PATH before reinstalling.
- main.py embeds a phone number; guava.toml includes number and project/org identifiers. They are configuration data, not proof of provisioning, ownership, billing, authentication, or deployment. Redacted from this report.
- Demo logs caller questions and names. No healthcare data was processed. Before healthcare work, replace unrestricted content logging with redacted structured events. Classification: application privacy risk if demo is reused with patient data; no demonstrated leak.
- DocumentQA is constructed during module import. Audit/test tooling should avoid importing main.py until initialization side effects are reviewed.
- Current official starter documentation fetched from https://goguava.ai/docs/coding-agent-starter.md. SHA256 7656AF3A01E3475EFC662BBD0DFD4E10DC0308FD0B7400F9773660819D36AAF2 matches bundled documentation. Snapshot and original scaffold hash manifest retained locally.

## Prior security findings awaiting evidence
Unsigned CLI executable and lack of explicit installer binary integrity verification were reported in the prior conversation. Original installer, executable hash, signature output and review transcript were not supplied here. Status: historical/user-reported, not independently confirmed. Do not present these as newly reproduced vulnerabilities or infer exploitability.

## Architecture learning checkpoint
Guava hosts the Dialog System (speech recognition, conversational model, speech synthesis). Python Expert code connects over WebSocket and registers synchronous handlers. Call commands steer task/checklist collection. Tasks express workflow goals; Fields capture values, but collected identity values are not proof of patient identity. Authoritative synthetic backend checks must authorize access before sensitive task transitions.
Handlers run outside the real-time dialog thread according to official documentation; backend latency still needs caller-visible and failure-path testing.
Installed SDK source contains Agent handler registration and listen_phone. Source inspection is not runtime validation.

## Test plan and ownership
All following tests are PLANNED, not executed:
1. Environment/scaffold: locate CLI, verify version and signature; inspect installer integrity behavior; repair Python launcher; validate locked dependencies and syntax/imports without hosted side effects. Owner: AEGIS/local environment; vendor owns confirmed installer defects.
2. SDK: map Agent, Call, events, commands, transport, auth, threading, helpers and testing package; document errors, callbacks, retry semantics and cleanup from current docs/source.
3. Functional: synthetic identity verification, appointments, eligibility, claims, billing and simulated payments; assert access gates, state transitions, idempotency and backend errors. Owner: AEGIS application.
4. Conversation/security: failed verification, prompt injection, unauthorized disclosure, ambiguous identity, interrupted workflows and redacted logs; distinguish scripted app behavior from platform behavior.
5. Audio/reliability: consented test sessions, accents, noise, interruption, latency, disconnect/reconnect, timeouts and concurrent calls; retain timestamps and anonymized transcripts.
6. Cross-platform: Windows then isolated Linux/macOS environments when available; do not claim results from unavailable platforms.
7. Attribution: reproduce platform suspects in a minimal SDK example with version, timestamps, correlation IDs and expected/actual behavior before escalating to Guava.

## Completion criteria and next step
Scaffold audit documented; runtime readiness is NOT established. Next: locate CLI and repair/verify Python environment, then study SDK architecture before changing application code. No founder-ready verdict yet: assessment requires reproducible evidence and measured tests.
