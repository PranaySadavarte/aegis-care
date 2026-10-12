import sys,json,time,jiwer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
root=Path(__file__).resolve().parents[2];agent,_=create_agent();utterances={}
@agent.on_caller_speech
def caller(call,event):
    utterances[event.utterance_id or str(len(utterances))]=event.utterance
started=time.monotonic()
agent.test_audio(root/"fixtures/audio/variants/verify-padded.wav",root/"evidence/2026-10-11/usability-repair/verify-agent.wav")
reference=json.loads((root/"fixtures/audio/manifest.json").read_text())[0]["reference_text"]
hypothesis=" ".join(utterances.values())
transform=jiwer.Compose([jiwer.ToLowerCase(),jiwer.RemovePunctuation(),jiwer.RemoveMultipleSpaces(),jiwer.Strip()])
ref=transform(reference);hyp=transform(hypothesis)
result={"reference":reference,"hypothesis":hypothesis,"normalization":"lowercase, remove punctuation, whitespace; no numeral equivalence",
        "elapsed_seconds":time.monotonic()-started,"speech_events":len(utterances),"sample_scope":"One synthetic SAPI clip, padded for turn timing"}
if hypothesis:
    result["WER"]=jiwer.wer(ref,hyp);result["CER"]=jiwer.cer(ref,hyp)
else:result["scoring_status"]="NO_SPEECH_EVENT; scores withheld rather than assume an ASR result"
(root/"evidence/2026-10-11/usability-repair/asr-baseline.json").write_text(json.dumps(result,indent=2))
print(json.dumps(result))
