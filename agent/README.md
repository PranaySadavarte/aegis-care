# HarborCare synthetic prototype
Entrypoint: agent/harborcare.py. Use isolated SDK 0.47.0 interpreter from baseline.
Default --mode chat starts a hosted interactive text session. --mode webrtc starts a live browser-audio channel. --mode phone uses the existing configured number but requires the pending explicit routing-attachment approval before execution.
Synthetic credentials: HC-1001 / DEMO-42; HC-1002 / DEMO-99.
Six workflows: identity, eligibility, claims, appointments (booking only), billing, payments (simulation only). Amounts are integer cents.
State resets on restart; no real API/payment/medical functionality; one workflow per call. Never supply real patient or card details.
Results: reports/test-results/harborcare-2026-10-11.md.
Run tests/functional with unittest for backend and native handler checks; integration hosted scripts consume live services and are bounded by the parent runner.
