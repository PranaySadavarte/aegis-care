# Assertion policy and layered tests
Do not require an entire generated response to match an exact sentence. Equivalent wording is valid: "Your balance is fifty dollars" and "You owe $50" can have the same correct value.
Assert exact patient bindings, extracted fixture values, transaction amounts, task/action outcomes and safety boundaries. Required fixed disclosures/scripts can have exact checks; natural conversational phrasing gets semantic criteria.
Native TestSession.evaluate evaluates rubric semantics; it is not calibrated confidence. WER/CER intentionally compare recognized text with an audio reference, using explicit normalization. They are not sentence-matching assertions for LLM replies.
Use native MockCall/test/roleplay/test_audio/callback helpers for orchestration. Use standard jiwer for ASR scoring rather than duplicating edit-distance code.
Text scenarios: fixtures/text-security-scenarios.json; executable scripted security turns: tests/integration/security_hosted.py. Offline handler guards: tests/functional/test_security_handlers.py and test_identity_routing.py.
Current layered progression: deterministic guards -> hosted text safety -> synthetic labeled audio baseline -> later representative human audio and scored transport tests. Existing manual phone calls remain exploratory.
