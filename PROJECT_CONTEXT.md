# AEGIS Care project context
Updated: 2026-10-11
Repository: C:/Users/prana/aegis-care
Project: AEGIS Care — Guava SDK and Voice AI QA Evaluation
Agent scaffold: harborcare-agent (HarborCare inbound agent)

## Objective and scope
Evaluate Guava CLI/SDK v0.47.0 and build a healthcare-first voice agent for patient identity verification, insurance eligibility, claims, appointments, billing and payment security. Use synthetic patient/insurance records and simulated payments. Produce an evidence-backed technical assessment for Guava's founders and CEO.

## Current milestone
Initial scaffold audit completed and recorded in reports/scaffold-audit-2026-10-11.md. Git baseline: 47e92e7. Application remains Guava's introduction/RAG demo; healthcare features have not been implemented.
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
