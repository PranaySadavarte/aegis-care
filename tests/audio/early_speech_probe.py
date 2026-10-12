import sys,json,time,uuid,jiwer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/extended-sdk'/('barge-in-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True);events=[];agent,_=create_agent()
@agent.on_agent_speech
def agent_speech(call,event):events.append({'kind':'agent','utterance':event.utterance,'interrupted':event.interrupted,'at_monotonic':time.monotonic()})
@agent.on_caller_speech
def caller_speech(call,event):events.append({'kind':'caller','utterance':event.utterance,'utterance_id':event.utterance_id,'at_monotonic':time.monotonic()})
case=next(r for r in json.loads((root/'fixtures/audio/challenges/manifest.json').read_text()) if r['id']==(sys.argv[1] if len(sys.argv)>1 else 'early-verification'))
agent.test_audio(root/case['path'],folder/'output.wav')
result={'events':events,'interrupted_flags':sum(e.get('interrupted',False) for e in events),'scope':'Native file-in early-speech probe; callback timestamps are receipt times, not acoustic start/end. Audible onset/barge-in delay not measured.'}
result['sample_id']=case['id']
heard={}
for e in events:
 if e['kind']=='caller':heard[e.get('utterance_id') or str(len(heard))]=e['utterance']
hyp=' '.join(heard.values());transform=jiwer.Compose([jiwer.ToLowerCase(),jiwer.RemovePunctuation(),jiwer.RemoveMultipleSpaces(),jiwer.Strip()])
result['WER']=jiwer.wer(transform(case['reference_text']),transform(hyp)) if hyp else None
result['CER']=jiwer.cer(transform(case['reference_text']),transform(hyp)) if hyp else None
(folder/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');
if len(sys.argv)==1:(root/'dashboard/interruption-results.json').write_text(json.dumps({'interrupted_flags':result['interrupted_flags'],'event_count':len(events),'scope':result['scope']},indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
