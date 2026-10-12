# HarborCare synthetic prototype
Entrypoint: agent/harborcare.py. Use isolated SDK 0.47.0 interpreter from baseline.
Default --mode chat starts a hosted interactive text session; this is text-only and does not play audio. Windows requires windows-curses, now installed in the baseline environment. --mode text uses a plain terminal on the same native Agent.test session. --mode webrtc starts a live browser-audio channel. --mode phone uses the existing configured number with the user-approved synthetic test routing attachment.
Synthetic credentials: HC-1001 / DEMO-42; HC-1002 / DEMO-99.
Six workflows: identity, eligibility, claims, appointments (booking only), billing, payments (simulation only). Amounts are integer cents.
State resets on restart; no real API/payment/medical functionality; one workflow per call. Never supply real patient or card details.
Results: reports/test-results/harborcare-2026-10-11.md.
Run tests/functional with unittest for backend and native handler checks; integration hosted scripts consume live services and are bounded by the parent runner.

Voice-friendly demo: patient 1001, code 4242. Old codes remain accepted. --mode local uses native microphone/speaker helper and hosted WebRTC; may consume account usage. It is not offline mode.

Browser playback of the captured synthetic greeting was confirmed by the user. Native --mode local microphone capture and speaker routing remain unverified; permission Allow alone does not prove device routing. --mode webrtc offers a browser channel; use the temporary URL printed by the listener and choose microphone/speaker devices there. All hosted modes may consume account usage.
