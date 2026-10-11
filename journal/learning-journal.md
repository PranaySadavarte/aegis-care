# Learning journal
## 2026-10-11 — Scaffold audit
Learned: CLI, Python SDK and hosted runtime have separate versions. A scaffold can exist without being runnable. A Field collects data; verification requires a trusted backend decision. Static source inspection and dependency metadata do not establish runtime compatibility.
Verified: scaffold files exist; official documentation snapshot matches bundled copy; dependency metadata identifies SDK 0.47.1.
Blocked: Python launcher cannot start; CLI is absent from current PATH.
Next study: Agent lifecycle, Call commands, event dispatch, transport/auth, errors and testing helpers. Use synthetic records only; simulate payments until explicitly authorized otherwise.

## 2026-10-11 — Persistent project context milestone
Created PROJECT_CONTEXT.md and QA_FINDINGS.md after reviewing repository status and existing evidence. Recorded the 0.47.0 evaluation target versus the actual 0.47.1 scaffold SDK. No additional runtime/behavior tests ran.
Concept: a lockfile identifies resolved package versions; installed metadata identifies an installation, while a successful import is a separate runtime check. Version-specific evidence is necessary for valid vendor attribution.
