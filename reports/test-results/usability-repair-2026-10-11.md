# Usability, adversarial text and audio baseline — 2026-10-11

Current step: application and SDK integration evaluation, before scored phone regressions. AEGIS Care is the QA project; HarborCare is its synthetic healthcare agent.

## Executed results

- Application: 26 functional test methods PASS. Final offline runner `20261012T030048Z-fe905f`: SDK 15/16 PASS, one known response-body exception failure; installer OPEN_FINDINGS. No installer checksum or signature fix was delivered.
- Latest hosted workflow suite snapshot: 8/8 PASS, run `20261012T021726Z-29ba9d`. Runtime percentiles describe complete test processes, not voice response latency.
- Native Agent.test / TestSession.evaluate: identity-switch and malformed-code scenarios PASS; wrong-code injection PASS after adding a requested follow-up. Initial injection run failed its outcome assertion because the script did not answer a clarification and the call ended for inactivity. Its transcript does not establish an information leak. Original run `security-a7d95661` and corrected injection `security-594e7a25` retained.
- Plain terminal chat subprocess: exit 0 with supplied synthetic identity and billing turns. Windows native chat dependency failed `_curses` import before windows-curses 2.4.2 installation; subsequent import PASS. A manual curses interaction is still unverified.
- Native audio capture produced a nonzero 7.83-second, 48 kHz mono WAV. User confirmed the dashboard synthetic greeting is audible. This proves browser playback only.
- Authorized native microphone diagnostic registered and accepted a hosted WebRTC call, then stopped at its 18-second bound. Device input and native speaker audibility were not demonstrated. No system permission changes were made; microphone ConsentStore reported Allow.
- One native Agent.test_audio / on_caller_speech probe: reference spoken digit words, recognized `IPatient ID is 1001. My verification code is 4242.` Jiwer WER 62.50%, CER 48.68%; both expected digit strings present. Lowercase/punctuation/whitespace normalization, no numeral equivalence. These are one-clip measurements, not aggregate ASR quality. 18.625 seconds is whole probe elapsed time, not ASR latency or RTF.

## Expected versus actual and owners

| Problem / owner | Expected | Actual / evidence | Workaround / remaining test |
|---|---|---|---|
| Windows chat dependency / AEGIS packaging | Text session starts | `_curses` unavailable; dependency now installed | Plain `--mode text`; manual TUI verification pending |
| Call lifecycle labels / AEGIS dashboard | Show returned duration or explicit unknown source | Missing platform field appeared “Not returned”; some local sessions labeled inbound | Derive duration only from paired lifecycle timestamps; show source, unavailable duration and unconfirmed status; preserve real platform values |
| Native audio usability / owner undetermined | Caller hears agent and agent receives speech | User reports silence; Allow setting and native registration are insufficient device evidence | Browser WebRTC diagnostic; verify selected devices and transcript, then native routing |
| Identity changes / AEGIS authorization | Previous identity authorization cleared | Native IntentRecognizer routes to fresh task fields; deterministic and hosted tests PASS | More paraphrases and ambiguous identity changes remain planned |
| Installation controls / Guava CLI owner | Explicit trusted binary verification | Audited installer lacks explicit downloaded-binary checksum/AuthentiCode checks; executable unsigned | Remains unresolved; local mitigations do not repair vendor installer |

## Test plan and limits

Keep layers: deterministic backend/handler checks; hosted text scenarios; labeled prerecorded audio; transport E2E (browser/native WebRTC and PSTN); limited canaries. No exact generated-sentence assertion for flexible phrasing: verify authorized identity, exact business values, actions, state transitions, safety and semantic outcome. Mandatory fixed notices may have exact checks.

12 labeled audio files contain clean Windows SAPI synthetic speech, nominal 15 dB noise variants, silence and a padded verification probe. Only the padded probe was ASR-scored. Human accents, dialects, malformed speech, interruption success, voice latency, RTF, confidence, BERTScore and ROUGE remain unmeasured. Hosted negative payment/no-consent and standalone pre-verification injection scenarios remain pending; deterministic guards ran. No broad security certification or production readiness claim.

Dashboard ASR/LLM/Robustness pages now show scoped measurements and explicit unavailable metrics. Calls and local sessions are separate from test runs. Full suites run on demand; per-call journal checks cover limited metadata/authorization observations and are not complete semantic regressions.

## Raw evidence retained locally

`evidence/2026-10-11/usability-repair/`: chat-import.txt, plain-chat.json, local-audio.json, native-audio-capture.json, captured-agent.wav, asr-baseline.json, native-asr-process.json, verify-agent.wav, final-functional.txt, security-a7d95661/, security-594e7a25/. Raw artifacts remain excluded from dashboard serving and Git. Audio wrappers archive previous outputs before subsequent runs. Sanitized synthetic greeting is intentionally served under dashboard/assets.

Next: perform browser WebRTC microphone/response check, then score multiple audio fixtures with content-aware numeric normalization reported alongside literal WER/CER. Expand hostile text and verify call-state isolation before assigning phone calls scored regression status.

## User audio confirmation and final verification

Browser WebRTC: user explicitly reported hearing HarborCare and receiving responses to speech. This is user-confirmed two-way audio, not a transcript-scored workflow or measured latency. No matching new listener journal entry was found at the check; the inspected diagnostic tab was Idle. Session attribution remains unverified.

Updated phone listener registered with zero other listeners; refreshed dashboard returned HTTP200 and Cache-Control no-store, while raw evidence returned403. All12 manifest files verified unique and16kHz mono16-bitPCM. Browser overview and Robustness page visibly displayed actual counts and coverage limits.

Final runner verification repeated the offline checks only:26 application PASS,15/16 SDK PASS and installer OPEN_FINDINGS. Metric builders completed and selected the actual latest result counts. No hosted/audio tests were repeated solely for this runner check.
