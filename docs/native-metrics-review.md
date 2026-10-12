# Native metric reuse review — SDK 0.47.0
Retrieved current full starter bundle and reviewed relevant architecture/testing/helper sections and installed testing/session.py, testing/protocol.py and Agent audio/testing entrypoints. This is a scoped public-API review, not proof that Guava has no internal metrics.
Native:
- MockCall and Agent.patch for deterministic callback tests.
- Agent.test / roleplay, TestSession.say/get_transcript and stable outcome assertions.
- TestSession.evaluate for hosted rubric checks; uses a generated pass/fail result, not calibrated confidence or a numeric BERT/ROUGE score.
- Agent.test_audio for audio-in/audio-out capture; reviewed, not executed.
- Caller/agent speech callbacks and event records for correlation; available timestamps/audio segmentation must be validated before latency claims.

Not found as public metric functions in reviewed 0.47.0 API: CER, WER, standalone ASR RTF, calibrated intent confidence, BERTScore and ROUGE. Do not implement substitutes for native session APIs.
Use established metric libraries (e.g. Hugging Face Evaluate/jiwer, bert-score, rouge-score) after exact-version/dependency review; not installed or invoked this milestone.
Sources: https://goguava.ai/docs/agent-testing ; https://goguava.ai/docs/coding-agent-starter.md ; https://huggingface.co/docs/evaluate/en/choosing_a_metric ; https://huggingface.co/learn/audio-course/chapter5/evaluation

Measurement plan:
CER/WER require reference and recognized transcripts, fixed normalization and edit counts. Report critical entity accuracy separately.
ASR RTF = isolated recognition processing time / audio duration. Hosted whole-agent roundtrip cannot be relabeled ASR RTF; mark unavailable without component timing.
Intent accuracy = correctly routed labeled intents / labeled intent trials. No calibrated confidence exposed in reviewed public API; do not turn rubric pass into confidence.
Failure/fallback rates require predefined terminal failure and fallback events and denominators, split by fault cause.
Latency distribution requires event boundary definition, clock alignment and p50/p95/p99 with sample size; process duration is separate.
BERTScore/ROUGE (confirmed by user) need reference answers and evaluator configuration; similarity does not prove authorization, medical correctness or groundedness.
Robustness: malformed events/inputs, accents, dialects, noise, echoes, interruption/overlap, silence, disconnects, identity switching and injection. Text trials cannot measure accent/dialect/audio behavior.



Update October11:Agent.test_audio and caller-speech callbacks actually executed;Jiwer4.0.0 and pinnedNumPy/SoundFile used. Native sensitivePAN/CVV and vital fields exercised in isolated hosted text probes. TestSession.evaluate observed falsePASS and apparentfalseFAIL; exact safety guards added. Historical statements above are milestone-scoped, not current NOT_RUN status. See robustness assessment for measured results and unverified production redaction/AEC/RTF.
