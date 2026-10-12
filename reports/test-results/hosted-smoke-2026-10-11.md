# Hosted text smoke results — 2026-10-11
SDK: 0.47.0, Windows/Python 3.12.14. Uses native Agent.test, set_task, Field, get_field, hangup and TestSession utterance/turn/end APIs.
Two live synthetic text smoke runs executed under authorized 500-minute ceiling. No phone call, number purchase or deployment.
First run: exit 0, no stderr, bot-hangup; session duration 9.609 seconds, total process 11.156 seconds. Transcript confirms synthetic code exchange; field value not directly asserted in first run.
Second run: exit 0, total process 8.062 seconds. Added assertions for captured test_code == AEGIS-TEST-42 and termination_reason == bot-hangup; both passed.
Raw originals: evidence/2026-10-11/hosted-smoke/first-run.json and result-raw.json. Only synthetic content used.
Hard outer process timeout: 60 seconds; no timeout occurred. This process bound is not a demonstrated server-side billing cap.
No usage-meter query performed; actual billed minutes unknown. Wall-clock duration is not billing evidence.
KPIs: asserted hosted smoke 1/1 successful; preliminary unasserted smoke separate. Sample too small for reliability claim. Neither duration is speech latency.
Phone no-answer remains unverified; Agent.test does not register a phone listener. Next inspect inbound listener/routing using existing project configuration, then user-led call; outbound requires approved destination.
