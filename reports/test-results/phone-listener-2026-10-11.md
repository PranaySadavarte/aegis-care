# Inbound listener registration — 2026-10-11
Current step: approved synthetic HarborCare inbound phone test.
User explicitly approved attachment to existing configured number and confirmed BERTScore/ROUGE metric names.
Launched native Agent.listen_phone using isolated SDK 0.47.0; no deployment or number purchase.
Observed SDK log: "Started listing on phone number [REDACTED]. 0 other listeners registered."
Registration is confirmed; PSTN establishment, speech quality, end-to-end workflow outcome and no-answer resolution are not yet established.
Raw registration output: evidence/2026-10-11/phone-listener/listener-log.txt.
Listener execution session at launch: 17324. Local Expert must remain running to handle calls. In-memory backend resets if process restarts.
Startup warning: websockets connect() should use a context manager or legacy=True; emitted from guava/socket/client.py:156 with websockets 17.2. Registration succeeded. Classification: observed compatibility/deprecation warning; future impact unassessed, no confirmed failure or security vulnerability.
Earlier automatic approval rejection remains part of historical record. Explicit user approval subsequently supplied and approved attachment executed successfully.
No user call result recorded at this milestone.
Synthetic test inputs: HC-1001 / DEMO-42. One workflow per call. Use synthetic records and simulated payments only.
