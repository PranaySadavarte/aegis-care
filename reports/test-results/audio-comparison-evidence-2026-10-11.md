# Audio comparison: preserved evidence

Four sources and three paired conditions;24reference words per condition. MicroWER aggregates edits/words; macro WER averages sample WER. The latter amplifies one-word samples. These scores do not assert exact generated agent sentences or clinical safety.

| Source | Condition | Reference | Recognized | Edits / words | WER |
|---|---|---|---|---|---|
| librispeech-test-other-1688-142285-0007 | clean | i really was very much afraid of showing him how much shocked i was at some parts of what he said | I really was very much afraid of showing him how much shocked I was at some parts of what he said. | 0 / 21 | 0.00% |
| librispeech-test-other-1688-142285-0007 | noise0db | i really was very much afraid of showing him how much shocked i was at some parts of what he said | I really was very much afraid of showing him how much shopper I was at some part of what he said. | 2 / 21 | 9.52% |
| librispeech-test-other-1688-142285-0007 | echo180ms | i really was very much afraid of showing him how much shocked i was at some parts of what he said | I really was very much afraid of showing him how much shock I was at some part of what he said. | 2 / 21 | 9.52% |
| speech-commands-yes | clean | yes | Yes. | 0 / 1 | 0.00% |
| speech-commands-yes | noise0db | yes | Yeah. | 1 / 1 | 100.00% |
| speech-commands-yes | echo180ms | yes | Yes. | 0 / 1 | 0.00% |
| speech-commands-no | clean | no | No. | 0 / 1 | 0.00% |
| speech-commands-no | noise0db | no | No. | 0 / 1 | 0.00% |
| speech-commands-no | echo180ms | no | No. | 0 / 1 | 0.00% |
| speech-commands-stop | clean | stop | Stop. | 0 / 1 | 0.00% |
| speech-commands-stop | noise0db | stop | That. | 1 / 1 | 100.00% |
| speech-commands-stop | echo180ms | stop | Stop up. | 1 / 1 | 100.00% |

## Artifact provenance

- `evidence/2026-10-11/kpi-expansion/public-audio-f0496998/summary.json`; SHA-256 `4b1486fcb989414109eade8671695f0f77179b5261d19e72a2a6af7f8dff9248`; source audio SHA-256 `67dfc27041e572bea27936e75eedc542ccf6f3af5cc251a0ab4e1e947d787fc8`.
- `evidence/2026-10-11/kpi-expansion/public-audio-f9471e84/summary.json`; SHA-256 `121dbcb22d54ce518dc34c6723fea9797ce837cc4b7cba2773e34d1ab597fb47`; source audio SHA-256 `2e38228747f53aab91ed5fdd0d9be74f834cf43f136e59c4de33c428bcb98fba`.
- `evidence/2026-10-11/kpi-expansion/public-audio-7f1f82a7/summary.json`; SHA-256 `2fc1714c5bb282af9f71ce7bd7f17cc51378ba2fac219ab539273a0db8f314c0`; source audio SHA-256 `5d7193eb0fe19dccc8ae0cdf4a15280c8b94c5465ee3e3e55b0aec72f76b15c3`.
- `evidence/2026-10-11/kpi-expansion/public-audio-1a7ec6a6/summary.json`; SHA-256 `8911b0d1ab8b3ccad74abe8c53898c12a15ab2b4cf5e098d44a60e19762d5fa3`; source audio SHA-256 `3b0804b7e5ecf23816f81ee4cc4c243e608df36cc572ca49fb9bd10f926bacd7`.

## Interpretation

Noise changed yes to Yeah (lexically different, possibly semantically similar), and stop to That (control-word loss). Echo produced Stop up (insertion while retaining stop). Downstream safety effects are untested. A separate synthetic credential-echo benchmark repeatedly produced extra digits; see ROB-003. No ASR compute latency, physical AEC or representative accent score is inferred.