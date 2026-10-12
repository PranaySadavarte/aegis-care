"""Score original audio fixtures with a documented padded-input protocol."""
import sys,json,uuid,subprocess,time,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def child(folder,case_id):
 sys.path.insert(0,str(ROOT))
 import numpy as np,soundfile as sf,jiwer
 from agent.harborcare import create_agent
 case=next(r for r in json.loads((ROOT/'fixtures/audio/manifest.json').read_text()) if r['id']==case_id)
 source=ROOT/'fixtures/audio'/case['path'];data,rate=sf.read(source,dtype='float32')
 if data.ndim>1:data=data.mean(axis=1)
 submitted=folder/(case_id+'-submitted.wav');sf.write(submitted,np.concatenate([np.zeros(rate*8,dtype='float32'),data,np.zeros(rate*3,dtype='float32')]),rate,subtype='PCM_16')
 utterances={};outcomes=[];agent,_=create_agent(outcomes=outcomes)
 @agent.on_caller_speech
 def speech(call,event):utterances[event.utterance_id or str(len(utterances))]=event.utterance
 started=time.monotonic();agent.test_audio(submitted,folder/(case_id+'-agent.wav'))
 hypothesis=' '.join(utterances.values());t=jiwer.Compose([jiwer.ToLowerCase(),jiwer.RemovePunctuation(),jiwer.RemoveMultipleSpaces(),jiwer.Strip()]);reference=t(case['reference_text']);h=t(hypothesis)
 result={'id':case_id,'status':'OBSERVED','source_path':source.relative_to(ROOT).as_posix(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'submitted_sha256':hashlib.sha256(submitted.read_bytes()).hexdigest(),'reference':case['reference_text'],'hypothesis':hypothesis,'speech_events':len(utterances),'WER':jiwer.wer(reference,h) if reference else None,'CER':jiwer.cer(reference,h) if reference else None,'silent_reference':not bool(reference),'speech_on_silence':bool(hypothesis) if not reference else None,'process_seconds':round(time.monotonic()-started,3),'scope':'Native ASR fixture observation with8seconds leading and3seconds trailing silence; not a scored healthcare task or acoustic latency.'}
 (folder/(case_id+'-result.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({'id':case_id,'speech_events':len(utterances),'WER':result['WER']}),flush=True)
def run():
 folder=ROOT/'evidence/2026-10-11/audio-backlog'/uuid.uuid4().hex[:8];folder.mkdir(parents=True)
 cases=json.loads((ROOT/'fixtures/audio/manifest.json').read_text());(folder/'manifest-snapshot.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
 rows=[]
 for case in cases:
  if case['id']=='verify-padded':continue
  p=subprocess.Popen([sys.executable,__file__,'--child',str(folder),case['id']],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
  try:out,err=p.communicate(timeout=45);status='OBSERVED' if p.returncode==0 else 'ERROR'
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
  (folder/(case['id']+'-process.json')).write_text(json.dumps({'status':status,'stdout':out,'stderr':err,'exit_code':p.returncode},indent=2),encoding='utf-8')
  result_path=folder/(case['id']+'-result.json');r=json.loads(result_path.read_text(encoding='utf-8')) if result_path.exists() else {}
  rows.append({'id':case['id'],'status':status,'WER':r.get('WER'),'CER':r.get('CER'),'speech_events':r.get('speech_events'),'speech_on_silence':r.get('speech_on_silence'),'evidence':(result_path if result_path.exists() else folder/(case['id']+'-process.json')).relative_to(ROOT).as_posix(),'source_sha256':r.get('source_sha256')});print(json.dumps(rows[-1]),flush=True)
  (folder/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 (ROOT/'dashboard/audio-backlog-results.json').write_text(json.dumps({'rows':rows,'scope':'Original11unscored fixture sources exercised through8s/3s padded native audio; literalWER/CER not semantic workflow pass/fail'},indent=2),encoding='utf-8')
 return 1 if any(r['status']!='OBSERVED' for r in rows) else 0
if __name__=='__main__':
 if len(sys.argv)>1:child(Path(sys.argv[2]),sys.argv[3])
 else:raise SystemExit(run())
