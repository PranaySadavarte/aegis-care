# HarborCare editable agent profile

persona.md sets the native Agent purpose. scope.md, safety.md, verification.md and payments.md are appended to each native task objective. question-fallback.md supplies the on_question fallback answer.

The files are read when create_agent starts. Restart the relevant Expert process to apply edits; existing listener processes keep the profile they loaded. Edit tone/scope here and rerun identical regression/adversarial cases. Markdown is conversational guidance, not an authorization/amount validator. Backend safety gates still execute in Python. Do not add patient records, credentials, real card details or clinical advice.

These defaults move existing intent into readable files; they do not establish that the card-readback or emergency findings are fixed. Add proposed stricter behavior as a separately reviewed profile change and preserve before/after evidence.
