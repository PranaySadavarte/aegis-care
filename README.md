# AEGIS Care
QA umbrella for the HarborCare synthetic healthcare administrative agent.
Caller-facing prototype: agent/harborcare.py; synthetic backend: backend/synthetic.py.
Local dashboard: http://127.0.0.1:8765/dashboard/ — Overview, Calls, Test runs, ASR, LLM and robustness pages.
Run supported suites with baseline/sdk-0.47.0/.venv/Scripts/python.exe tests/run_all.py --suite offline, hosted, or all. Hosted uses live services; offline includes the static installer audit.
After each instrumented call: limited local authorization/outcome checks. Full suites run on demand. Broad planned catalog, audio/outbound scenarios and production features remain incomplete.
Read PROJECT_CONTEXT.md, QA_FINDINGS.md and reports/test-results/service-runner-2026-10-11.md for exact results.
Original harborcare-agent scaffold and prior evidence retained. No real patient records/payments. Do not provide real personal/card details.

### Text and audio evaluation update
Use the baseline interpreter with `agent/harborcare.py --mode text` for plain terminal chat. `--mode chat` is text-only; `--mode webrtc` prints a temporary browser audio URL; `--mode local` uses native audio helper and hosted services. Browser two-way audio is user-confirmed, native helper routing remains unverified. Synthetic patient1001 / code4242. On Test runs select offline, hosted, security, audio or all; full tests run on demand. Corpus references are in fixtures/audio/manifest.json and text scenarios in fixtures/text-security-scenarios.json; executed hostile scripts in tests/integration/security_hosted.py. See reports/test-results/usability-repair-2026-10-11.md for actual results and limitations.

### Defect discovery and robustness
Open dashboard/defects.html for reviewed failures and measured noise/echo conditions. Baseline Python runs tests/run_all.py --suite adversarial or --suite robustness; hostedusage applies. Prompt fixtures:fixtures/defect-discovery-text.json. Audio:fixtures/audio/robustness/manifest.json. Full assessment:reports/sdk-evaluation/product-robustness-assessment-2026-10-11.md. SyntheticSensitiveProcessor is isolated test processing, not wired into live payments/clinical service; QA SQLite tracks metadata, not patient records.

KPI measurements and commands:docs/kpi-methodology.md anddocs/runbook.md. Test inputs:dashboard/data-library.html. Agent behavior files:docs/agent-profile/README.md;loaded on newExpert startup. Overview includes all inventories andreviewed open defects. KPI suite uses a separate CPUmetrics environment andfixed model revision.


Current startup, fixed-suite commands and manual synthetic challenges: [Operator guide](docs/operator-guide.md). Expanded SDK/adaptive results: reports/test-results/extended-sdk-2026-10-11.md. Known failing discovery assertions are intentionally retained.
