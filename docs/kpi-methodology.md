# KPI definitions and evidence

## ASR
WER=(substitutions+deletions+insertions)/reference word count. CER uses character edit counts/reference characters. Jiwer4.0.0 supplies edit alignment. Lowercase, remove punctuation, collapse spaces and strip both reference and hypothesis consistently; character scores include remaining spaces. Reference text is labeled before execution. WER can exceed100% with insertions. Missing transcript/event evidence needs an explicit failed/unavailable observation, not an invented score.

Literal and numeral-equivalent scores are separately labeled. Spoken digit words and numeric transcription can have high literal WER despite correct values. Critical credentials require a complete digit sequence match: a target inside a longer sequence does not count. Inspect insertion/deletion/substitution patterns; do not combine human/noisy/echo trials into one unqualified accuracy percentage. Three conditions on one clip are not three independent speakers.

## Time
Process runtime includes registration, greeting, caller duration, silence padding, conversation, model/transport, teardown and scoring. Use it for execution cost only. Longer calls naturally increase it.

Text-turn event interval=client monotonic time from TestSession.say to first native BotTTS receipt. Current two observations are not audible first response, speech endpoint latency, ASR latency, LLM inference time or representativep95. First event may be an acknowledgement. Speech response latency needs caller acoustic endpoint to first audible agent sample in a synchronized stream. Guava0.47.0 reviewed speech-event types lack these acoustic timestamps. ASRRTF needs isolated recognition compute time/audio duration; file-playback runtime divided by duration is not ASRRTF.

## Intent
Native IntentRecognizer benchmark has15 labeled prompts, two trials each:12 clear intents, one ambiguous prompt and two unsupported prompts. Clear top1 accuracy and unsupported rejection have separate denominators. Repeat agreement and multi-match ambiguity rate are useful diagnostics, not calibrated probabilities. Installed0.47.0 exposes ordered SuggestedActions, not numeric confidence. No confidence score is fabricated. This six-choice helper benchmark is separate from HarborCare's actual dialog workflow selection and its one-choice identity-switch helper.

## BERTScore and ROUGE
Seven saved synthetic outcome-turn response spans are scored against independent backend/task references. Candidate includes acknowledgements/fillers after the final caller turn. BERTScore0.3.13 uses revision-pinned DistilBERT layer5, CPU, noIDF and no baseline rescaling. Record model revision, library versions and full pairs; these scores cannot be compared directly with a different encoder/configuration. The initial run with typographic reference errors is retained; final run uses corrected spacing.

ROUGE-score0.1.2 computes stemmed ROUGE1/2/L precision, recall andF1. Report means across the seven response spans, not a semantic pass rate. Similarity can miss wrong amounts, unsafe readback or unauthorized access. Exact business/security invariants and native rubric/human review remain separate. A high BERTScore does not establish medical correctness or compliance.

Official interfaces reused: [Guava testing](https://goguava.ai/docs/agent-testing), [intent helpers](https://goguava.ai/docs/intent-helpers), speech callbacks. Standard scorer sources: [BERTScore](https://github.com/Tiiiger/bert_score), [Google ROUGE](https://github.com/google-research/google-research/tree/master/rouge). Scoped API review did not find native numeric WER/CER/BERTScore/ROUGE functions.

Actual Expert routing/completion baseline:one paraphrase per administrative workflow, six native Agent.test sessions with finished-event workflow observations.4/6completed; missing completion is not sufficient evidence of an incorrect intent label. Preserve helper classification and Expert completion scores separately.
