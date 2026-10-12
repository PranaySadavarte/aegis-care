# AEGIS Care
QA umbrella for the HarborCare synthetic healthcare administrative agent.
Caller-facing prototype: agent/harborcare.py; synthetic backend: backend/synthetic.py.
Local dashboard: http://127.0.0.1:8765/dashboard/ — Overview, Calls, Test runs, ASR, LLM and robustness pages.
Run supported suites with baseline/sdk-0.47.0/.venv/Scripts/python.exe tests/run_all.py --suite offline, hosted, or all. Hosted uses live services; offline includes the static installer audit.
After each instrumented call: limited local authorization/outcome checks. Full suites run on demand. Broad planned catalog, audio/outbound scenarios and production features remain incomplete.
Read PROJECT_CONTEXT.md, QA_FINDINGS.md and reports/test-results/service-runner-2026-10-11.md for exact results.
Original harborcare-agent scaffold and prior evidence retained. No real patient records/payments. Do not provide real personal/card details.
