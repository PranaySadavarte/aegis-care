# Suggestions for the next AEGIS Care review

The current objective remains scrutiny and evidence, not silently fixing the Expert. The founders' email will be drafted only when requested; nothing has been sent.

## Make the evaluation stronger

1. Define an explicit threat model: patient, family member, verified representative, staff, unknown caller, and attacker with a copied patient code. Separate credential authentication, caller identity, patient subject and disclosure authority.
2. Keep the original known failures as mandatory regressions, including the credentials-first brother case and card readback. Passing variants do not close those failures. Repeat selected cases to measure variability with denominators.
3. Make backend outcomes and required safety constraints the primary verdicts. Keep native judge results, caller-validity checks and human review separately visible. A spoken refusal is insufficient if a later tool result discloses the information.
4. Expand the small audio set with labeled clinical administration phrases, identifiers, amounts, dates and control words across licensed speakers/noise types. Keep clean/noise/echo pairs and exact critical-field scores. Record which altered words change intent versus only wording.
5. Add time-aligned duplex instrumentation before reporting audible latency, physical echo cancellation or interruption recovery. Process runtime and transcript timestamps cannot substitute for acoustic boundaries.
6. Add controlled representative authorization/revocation and cross-organization test resources before claiming privacy coverage. Review actual vendor contracts/BAA, retention/deletion and payment-provider boundaries before legal/production assurance.
7. Give every finding a stable detector case, reproducible input, observed result, owner category, confidence, raw hash and explicit limits. Prioritize reproducible disclosure/safety failures over cosmetic or speculative gaps.
8. TreatYbbag as a search tool, not an oracle. Measure attack coverage: did it actually refuse consent, claim third-party access, or ask for prohibited readback? Preserve invalid attacker runs. Add adaptive audio only through a bidirectional harness; fixed replay must stay labeled replay.

## Suggested later dashboard simplification

These are suggestions, not additional removals performed now.

- Retire the historical1/1smoke headline from the main Overview; keep it in run history. It is too small and old to represent current reliability.
- Move process-runtime percentiles to an execution diagnostics view; keep speech/ASR/LLM timing separate with unavailable reasons.
- Keep one findings registry and one visible evidence link per card; place implementation paths, hashes and commands in expandable detail.
- Separate coverage plans, executable methods, prompt fixtures and audio observations. Do not present their combined inventory count as a test pass-rate denominator.
- Keep one main audio interpretation page with paired changes, actual recognized text, critical fields and limitations. Preserve narrow microphone/playback diagnostics in a secondary page.
- Keep unavailable KPIs visible with concise reasons, as previously requested, but do not mix them with measured performance totals.
- Remove execution-order lists from the dashboard; project work ordering belongs in a separate planning document. That requested removal is completed.

## Founder-facing report structure

Lead with the reproduced sensitive readback and representative disclosure, followed by evaluator reliability, SDK boundary defects and installer integrity/rollback observations. For each, include a minimal reproducer, sanitized excerpt, detector case, version/profile hash and owner recommendation. Distinguish user reports from reproduced failures and synthetic project policies from legal compliance determinations. Include the small audio study as a scoped measurement, not broad ASR accuracy. State the five unrun plans and missing provider integrations plainly.
