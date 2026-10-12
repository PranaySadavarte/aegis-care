# Appointment diagnostic — October 12, 2026

## Current step

Expert workflow / native intent-helper investigation. Original phone symptom: appointment request asked for a different account. No new PSTN call was placed, and no Expert behavior was changed.

## Actual versus expected

Expected: verified patient selects appointments, receives available slots, chooses one, and receives a booked result. Actual focused hosted trace:

```json
{"routing_trace": {"request": "I choose appointments", "matches": ["switch_patient"]}}
{"routing_trace": {"request": "Book October fifteenth 2026 at nine AM, the 2026-10-15 09:00 slot.", "matches": "None"}}
```

The native classifier false positive is confirmed for this execution. The Expert's action-request handler calls backend.close before returning the SuggestedAction; that clears verification even before Guava decides whether to execute/confirm the switch. The hosted appointment process timed out after 50 seconds without a booked result. Timeout is a harness bound, not measured speech latency. This does not isolate the original phone call without its transcript/action trace.

## Tests actually run

- Focused deterministic handler file: 3 methods PASS, including a six-workflow subcase method and two denial methods. It bypasses natural-language classification, so it cannot prove correct routing.
- Existing hosted appointment scenario with pass-through classification trace: TIMEOUT. No response or classifier result was mocked/modified.
- Previous full hosted suite appointment case: PASS. Keep both observations; do not rewrite that historical pass.

## Implementation and limitations

Booking handlers and backend.book exist. Synthetic slots are October 15, 2026 at 09:00 and 14:00; booked slots are removed from available choices for that running backend. No real calendar, timezone policy or persistent clinic storage is implemented. One workflow per call; separate listener processes have separate in-memory backends. Appointment failure is therefore not explained by an absent booking branch.

## Owner recommendation / workaround

Primary Expert owner: invalidate verified state only when an actual patient switch is executed/confirmed. Native helper owner: review false-positive matching and descriptions; one enabled switch intent can still return an inappropriate match. These are proposed changes, not applied fixes. For manual comparison, explicitly request an appointment for the same verified patient, then compare with a natural scheduling paraphrase. If either asks for another account, preserve the failure rather than supplying unrelated credentials.

[Manual appointment script and usage guide](../../dashboard/agent-guide.html) / [ROB-011 evidence](../findings/evidence/ROB-011.md).

Official docs describe action request as a proposal followed by a separate execute/confirmation step: [Guava action callbacks](https://goguava.ai/docs/on-action-request-execute). Task completion is driven by checklist fields: [set_task](https://goguava.ai/docs/set-task).

## Preserved evidence

- focused-offline: PASS; raw local `evidence/2026-10-12/appointments-2de6f26c/focused-offline.txt`; SHA-256 `4626cd5109d0a13a4b4025af78b03b366b4b927f2aa59e1c55b531f3d5c616a3`.
- hosted-appointments: TIMEOUT; raw local `evidence/2026-10-12/appointments-2de6f26c/hosted-appointments.txt`; SHA-256 `457453238183f6d1885025785228811fa9c46f3d8a4a55f935aa8670c9e38211`.
