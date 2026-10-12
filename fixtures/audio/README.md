# Prerecorded synthetic audio corpus
manifest.json labels every baseline and derived WAV, with reference text, generation provenance, condition and hashes.
12 files: eight clean synthetic utterances, two nominal 15 dB Gaussian-noise variants, silence, and a padded verification probe.
Windows SAPI Microsoft David synthetic voice; 16-bit PCM mono 16 kHz. These are not human recordings or validated accent/dialect samples.
One padded clean clip processed through native Agent.test_audio and on_caller_speech; jiwer computes WER/CER under documented text normalization.
Primary measured WER 62.50%, CER 48.68%. Hypothesis contains both target numeric strings. Spoken digit-word versus numeric rendering contributes substantially; do not generalize to clinical or human accuracy.
Remaining noise/other clips not scored. Isolated ASR RTF and component latency unavailable. No acceptance thresholds chosen.
Sources: https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ms720595(v=vs.85) ; https://jitsi.github.io/jiwer/

Robustness expansion:robustness/manifest.json holds6 paired conditions generated with NumPy2.2.6/SoundFile0.13.1, seed47; native audio trials executed and delayed echo repeated.Original12 fixtures retained. Corpus now18 files across two manifests. Do not equate file overlap with live interruption/physicalAEC.
