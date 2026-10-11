# Learning journal
## 2026-10-11 — Scaffold audit
Learned: CLI, Python SDK and hosted runtime have separate versions. A scaffold can exist without being runnable. A Field collects data; verification requires a trusted backend decision. Static source inspection and dependency metadata do not establish runtime compatibility.
Verified: scaffold files exist; official documentation snapshot matches bundled copy; dependency metadata identifies SDK 0.47.1.
Blocked: Python launcher cannot start; CLI is absent from current PATH.
Next study: Agent lifecycle, Call commands, event dispatch, transport/auth, errors and testing helpers. Use synthetic records only; simulate payments until explicitly authorized otherwise.
