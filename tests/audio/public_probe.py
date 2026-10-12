import sys,json,time,uuid
from pathlib import Path
import soundfile as sf,numpy as np,jiwer,guava
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
root=Path(__file__).resolve().parents[2];manifest=json.loads((root/'fixtures/audio/public/manifest.json').read_text());row=manifest[0]
folder=root/'evidence/2026-10-11/kpi-expansion'/('public-audio-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
x,sr=sf.read(root/row['path']);assert sr==16000
if x.ndim>1:x=x.mean(axis=1)
rows=[]
for condition in ['clean','noise0db','echo180ms']:
 signal=x.copy()
 if condition=='noise0db':
  n=np.random.default_rng(47).normal(size=len(x));signal=x+n*np.sqrt(np.mean(x*x)/np.mean(n*n))
 if condition=='echo180ms':signal=x+.65*np.pad(x,(int(sr*.18),0))[:len(x)]
 gain=min(1,.98/max(float(np.max(np.abs(signal))),1e-12));signal*=gain
 source=folder/(condition+'-input.wav');sf.write(source,np.concatenate([np.zeros(sr*8),signal,np.zeros(sr*3)]),sr,subtype='PCM_16')
 heard={};agent=guava.Agent(name='PublicASRProbe',purpose='Listen to a public read-speech sample for transcription evaluation.')
 @agent.on_call_start
 def start(call):call.set_task('listen',objective='Listen to a caller reading a sample sentence.',checklist=[guava.Field(key='sample',description='The caller reads the sample sentence.')])
 @agent.on_caller_speech
 def speech(call,event):heard[event.utterance_id or str(len(heard))]=event.utterance
 begin=time.monotonic();agent.test_audio(source,folder/(condition+'-output.wav'));hyp=' '.join(heard.values())
 transform=jiwer.Compose([jiwer.ToLowerCase(),jiwer.RemovePunctuation(),jiwer.RemoveMultipleSpaces(),jiwer.Strip()]);ref=transform(row['reference_text']);h=transform(hyp)
 word=jiwer.process_words(ref,h);char=jiwer.process_characters(ref,h)
 result={'condition':condition,'reference':row['reference_text'],'hypothesis':hyp,'WER':word.wer,'CER':char.cer,'word_edits':word.substitutions+word.deletions+word.insertions,'reference_words':len(ref.split()),'char_edits':char.substitutions+char.deletions+char.insertions,'reference_chars':len(ref),'speech_events':len(heard),'signal_duration_seconds':len(x)/sr,'process_seconds':time.monotonic()-begin,'gain':gain,'scope':'One LibriSpeech test-other read-speech clip; conditions paired. No accent representativeness or audible turn timing claim.'}
 rows.append(result);(folder/(condition+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
summary={'dataset':row['dataset'],'sample_id':row['id'],'source_sha256':row['sha256'],'license':row['license'],'rows':rows,'scope':'Three conditions on one human recording, not3 independent speakers'}
(folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');(root/'dashboard/public-audio-metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
