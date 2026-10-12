# Manual call history — 2026-10-11
Current step: inbound call observation and dashboard integration.
Used native Guava CLI conversations list/get/transcript against configured number, not a custom conversation API.
Four records returned, durations 0:43, 0:42, 0:36 and 0:40. Their locally preserved transcripts contain verification-denial markers. Expected scenarios were not recorded: these are unscored observed outcomes, not four failed automated tests.
CLI timestamps are presented with timezone explicitly unspecified; do not assume displayed date is the user's local date.
Raw originals retained under evidence/2026-10-11/call-history/, including timestamped imports. No phone numbers, raw session identifiers or transcripts exposed in dashboard data.
User-reported additional calls are not independently matched if absent from returned records; missing records do not prove no attempt.
New "Your inbound calls" dashboard shows stable hashed identifiers, platform timestamp, duration, observed outcome and grading limitation.
Refresh button invokes read-only native CLI retrieval using localhost server; no automatic background platform polling. Retrieval bounded to latest 30 inbound records since 2026-10-11; pagination not implemented.
Added append-only sanitized Expert start/finish/end events for future calls, recording workflow and result status only. Original transcripts/logs not overwritten.
Restarted approved phone listener with zero other listeners. Future records merge local Expert events with platform records using the same hashed call ID. Outcome recording itself is not a semantic correctness/safety grade.
Functional regression suite 12/12 PASS. New event recorder was not exercised by a live call yet; no new phone success claim.
Initial importer regex escaping error produced zero parsed rows despite four native records; corrected and re-imported; raw first attempt retained.
Preview only serves dashboard/, reports/ and docs/; raw evidence paths denied.

Verification: native refresh endpoint returned four records; browser displayed four individual rows and refresh updated the import timestamp. Raw evidence URL returned HTTP 403. JS syntax check passed.
