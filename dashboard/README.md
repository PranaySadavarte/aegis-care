# Local evaluation dashboard
Open dashboard/index.html directly, or serve the repository on localhost and visit /dashboard/.
The current preview is http://127.0.0.1:8765/dashboard/.
This is a recorded snapshot, not a live monitoring service. Search/filter cases, inspect findings and export sanitized JSON. Relative evidence links point to tracked reports.
Refresh data using the baseline Python interpreter with dashboard/build_data.py after recording new results. This reads preserved corrected offline output, catalog and hosted smoke metadata; it does not run tests.
The current visual summaries are scoped to the October 11 milestone; update run/finding summaries when adding future milestones. The dashboard is not an automatic run-history ingestion engine.
No raw secrets, phone numbers, binaries or call transcripts embedded. Local server is bound to 127.0.0.1; no external publication or paid hosting.
Verified: data generator validates 16 unique checks; 32 cases; JS syntax; HTTP 200; browser search SDK-002 yields one case; PARTIAL_FAIL filter yields one case; JSON export downloaded successfully.
SDK-016 and SDK-017 catalog statuses corrected to PARTIAL based on directional contracts and hosted smoke; no new SDK tests executed for dashboard QA.

Call history: run dashboard/serve.py with baseline interpreter, then use Refresh call records. It performs read-only native CLI import on demand, keeps timestamped raw evidence, and serves only dashboard/reports/docs. Four historical records recovered; expected scenarios unrecorded. Future listener events add masked workflow/result outcomes without credentials.
