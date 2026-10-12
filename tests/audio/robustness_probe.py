import json,sys,time,re
from pathlib import Path
import jiwer
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
root=Path(__file__).resolve().parents[2];case=next(r for r in json.loads((root/'fixtures/audio/robustness/manifest.json').read_text()) if r['id']==sys.argv[1])
folder=Path(sys.argv[2]);utterances={};outcomes=[];agent,b=create_agent(outcomes=outcomes)
@agent.on_caller_speech
def speech(call,event):utterances[event.utterance_id or str(len(utterances))]=event.utterance
started=time.monotonic();agent.test_audio(root/case['path'],folder/(case['id']+'-response.wav'))
hyp=' '.join(utterances.values());transform=jiwer.Compose([jiwer.ToLowerCase(),jiwer.RemovePunctuation(),jiwer.RemoveMultipleSpaces(),jiwer.Strip()]);ref=transform(case['reference_text']);h=transform(hyp)
words=dict(zip('zero one two three four five six seven eight nine'.split(),'0123456789'))
def numeric(text):
 tokens=[words.get(t,t) for t in text.split()];s=' '.join(tokens)
 return re.sub(r'(?<!\w)(?:[0-9] +)+[0-9](?!\w)',lambda m:m.group().replace(' ',''),s)
record={'id':case['id'],'condition':case['condition'],'hypothesis':hyp,'reference':case['reference_text'],'elapsed_process_seconds':round(time.monotonic()-started,3),'speech_events':len(utterances),'outcomes':outcomes,'scope':'File-in hosted ASR observation; no isolated timing/AEC/live barge-in claim'}
if hyp:
 record.update(WER=jiwer.wer(ref,h),CER=jiwer.cer(ref,h),numeral_equivalent_WER=jiwer.wer(numeric(ref),numeric(h)),target_digit_strings_found=sum(bool(re.search(r'(?<![0-9])'+x+r'(?![0-9])',numeric(h))) for x in ('1001','4242')),echo_greeting_present=('welcome' in h and 'harborcare' in h.replace(' ','')))
else:record['scoring_status']='NO_SPEECH_EVENT'
(folder/(case['id']+'-result.json')).write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record),flush=True)
