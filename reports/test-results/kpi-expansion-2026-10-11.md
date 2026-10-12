# KPI and dashboard expansion — October11,2026

Current step:measured KPI baselines, complete test inventory and editable Expert profile.

Actual results:
- Native six-choice intent helper:24/24 clear-intent trials correct;2/4 unsupported trials rejected. Diagnosis/prescription request mapped to appointments in both repetitions. This is a taxonomy/unsupported-input observation, not proof of medical advice or actual Expert routing failure. Repeat agreement93.33%, ambiguity16.67%; no numeric calibrated confidence is returned by the pinned public API.
- Seven recorded response spans:BERTScore meanF1 0.8069;ROUGE1/2/L meanF1 0.2509/0.1682/0.2439. DistilBERT revision/layer5 and local CPU configuration preserved. Safety/exact business assertions remain independent.
- Text submit to first native BotTTS event:0.281/0.531seconds for two turns. Not audio onset, ASRRTF, LLM compute time or a reliable percentile distribution.
- One public LibriSpeechtest-other recording:cleanWER/CER0/0;0dBnoiseWER9.52%,CER4.12%;delayedcopyWER9.52%,CER3.09%. The same21-word reference and speaker under three conditions; no representative accent/dialect inference.

Expected versus actual:Overview previously showed only39 high-level catalog rows, excluding48 executable method entries and separate prompt/audio inventories. Updated inventory adds all sources, statuses and commands (39plans,48methods,28textpromptrows,19audioassets). Inventory rows are not independent executed-test totals. Seven reviewed defect-discovery findings now appear in Open findings as well as their dedicated page. Failed/evaluator-disagreement records stay open.

Run histories now distinguish process runtime from response intervals, add commands/evidence pointers and record SDK/runtime/source/profile provenance for future runs; historical provenance is marked absent rather than fabricated. Additional Markdown files control purpose, scope, task guidance and on_question fallback through native SDK APIs on new Expert starts. Active phone listener still has its old loaded profile; no known vulnerability marked resolved by these defaults.

Test plans and commands:docs/runbook.md. Metric definitions:docs/kpi-methodology.md. Public corpus/noise/echo provenance:docs/audio-datasets.md. Profile controls:docs/agent-profile/README.md. Raw evidence:evidence/2026-10-11/kpi-expansion with unique folders; initial reference-typography run retained. Model assets local/ignored; reports and dashboard do not expose raw PAN/CVV.

Remaining:actual Expert routing on broader paraphrases, confidence/calibration if platform exposes suitable scores, isolated audio component timestamps, representative accents, live interruption/AEC, packet loss and transport scoring. Metrics and public sample were actually executed independently; the new one-command combinedKPI wrapper was added for repeatability and has not itself been used to claim another run.

Actual HarborCare routing/completion:4/6 initially completed against six labeled paraphrases, including identity-confirmation and billing questions with no finished result. Original records retained; targeted transcript reproduction is recorded separately. This is broader than the six-choice native helper score and does not establish the exact failure layer.

Final profile regression:run20261012T043036Z-34535e,32/32 applicationPASS;SDK15/16PASS and installerOPEN_FINDINGS. Full inventory134entries, not134executions. Existing listener profile is not refreshed by editing Markdown; restart explicitly to load it.

Targeted reproduction:billing completed on repeat;identity still had no finished workflow and the transcript switched to a different-account verification request despite a same-identity request. Its parent process ultimately reached55-secondTIMEOUT, with transcript/result text retained. ROB-008 documents the symptom; native request/classifier tracing is needed for root-cause attribution. Initial4/6benchmark and targeted1/2process outcomes remain separate. Inventory now135entries:40plans,48methods,28promptentries,19audioassets;Openfindings includes8reviewed discovery records.
