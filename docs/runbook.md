# Test-plan runbook — PowerShell

Run from C:\Users\prana\aegis-care. The baseline SDK remains0.47.0. Commands execute tests, not the entire planned catalog. Hosted suites consume account usage; bounds are local process limits, not carrier billing caps.

```powershell
Set-Location -LiteralPath 'C:\Users\prana\aegis-care'
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite offline
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite hosted
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite security
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite adversarial
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite robustness
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite kpi
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/run_all.py --suite all
```

Select one command; do not paste the whole block unless you intend to run every suite separately and again in all. Offline includes32 application/16SDK methods and installer source audit; known failure/open findings are expected. Hosted includes workflow conversations and native rubric. Security includes three earlier adversarial scripts. Adversarial adds independent product gaps and sensitive-field/hostile text probes. Robustness covers six paired synthetic audio conditions. KPI measures native intent helper, recorded-responseBERTScore/ROUGE, text-turn event interval and public human audio. Metric observations are not acceptancePASS assertions.

Focused commands:
```powershell
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/security/product_audit.py
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/integration/run_defect_discovery.py card-volunteered
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/metrics/intent_accuracy.py
& .\baseline\metrics\.venv\Scripts\python.exe tests/metrics/answer_similarity.py
& .\baseline\sdk-0.47.0\.venv\Scripts\python.exe tests/audio/public_probe.py
```

The full KPI wrapper supplies process-tree bounds. Direct public probe is interactive/operator managed. Raw evidence uses unique localfolders under evidence/2026-10-11. Dashboard Test runs shows commands/source commit/profile hash for new runs; older runs explicitly lack that metadata. Test data lists sources. Overview inventory counts plans/methods/prompts/assets separately; do not add them into a passing-test denominator.

Agent edits:docs/agent-profile/README.md explains the Markdown profile. New create_agent calls load it; restart your listener to apply changes. Use the isolated interpreter with agent/harborcare.py --mode text or --mode webrtc for manual checks. Browser/native audio uses hosted services and is not assumed free. Active phone process retains its previously loaded profile until restarted.

KPI environment is isolated under baseline/metrics, with its own requirements.lock.txt and fixed model revision in fixtures/kpi-config.json. Reuse these rather than silently upgrading the SDK environment.


Current startup, fixed-suite commands and manual synthetic challenges: [Operator guide](operator-guide.md). Expanded SDK/adaptive results: reports/test-results/extended-sdk-2026-10-11.md. Known failing discovery assertions are intentionally retained.
