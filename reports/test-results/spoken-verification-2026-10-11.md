# Spoken synthetic verification / local audio — 2026-10-11
Current step: real inbound testing exposed a verification usability limitation; application fix and regression testing.
Raw listener log contains four accepted inbound sessions with verification task completion and bot-hangup. User reports repeated synthetic verification failure. Field values were not logged; exact ASR/extraction mismatch is unknown.
Old backend compared exact HC-1001/DEMO-42 strings; case/spacing/hyphen variations were reproducibly rejected by that implementation. Classification: application input handling weakness / probable contributor, not proven ASR or SDK defect.

## Changes and actual tests
Easy synthetic credentials: 1001 / 4242 (second fixture 1002 / 9999). Old HC-1001/DEMO-42 and HC-1002/DEMO-99 remain valid.
Canonicalization accepts defined casing, whitespace/hyphen and all-digit-word sequences; no fuzzy similarity or substring acceptance. Wrong numbers, mismatched patient/code pairs, empty values and extra content remain denied.
Field descriptions ask for digit strings and prohibit guessing/disclosing codes. Denial logs exclude entered credentials.
Corrected on_session_end callback to current two-argument signature after application deprecation warning.
Initial normalization edit lost regex escaping; new tests caught three subcase failures. Fixed before restarting listener; both outputs preserved. This was an implementation error, not SDK behavior.
Corrected functional suite: 12 methods PASS; includes old workflow regressions and credential positive/negative subcases.
Updated authorized phone listener registered with zero other listeners. Phone effectiveness of easier credentials awaits another user call; registration alone is not validation.
In-memory synthetic backend reset on listener restart.

## Local audio and billing
Added --mode local using native Agent.call_local. Source shows temporary hosted WebRTC creation plus a native microphone/speaker helper. This is local audio I/O, not an offline dialog system.
No microphone session launched in this milestone. User can start from repository using baseline/sdk-0.47.0/.venv/Scripts/python.exe agent/harborcare.py --mode local.
No guaranteed usage-minute saving: public pricing describes active-agent minutes, but does not clearly establish free local/WebRTC usage. Exact account metering remains unverified.
Text chat avoids audio/PSTN for workflow debugging but hosted chat also should not be claimed free. Offline functional tests avoid hosted calls.
Sources: SDK 0.47.0 agent.py call_local and webrtc_helper.py; https://goguava.ai/docs/agent-testing ; https://goguava.ai/pricing.

## Integrity scope correction
webrtc_helper.py uses manifest sha256 via download_and_check for a newly downloaded helper. Static review only; helper download/tamper enforcement not executed here. Cached helper revalidation also not established.
This helper behavior does not fix the separate Windows CLI installer verification gap.
Raw evidence: evidence/2026-10-11/spoken-verification/ and prior phone listener logs, kept local; caller numbers/session IDs omitted from this report.
