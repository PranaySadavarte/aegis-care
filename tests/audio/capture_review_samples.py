"""Capture real native TTS for911review and a separate Ybbag-seeded audio replay."""
import sys,json,uuid,subprocess,hashlib,shutil,time,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def child(folder,case_id):
 sys.path.insert(0,str(ROOT))
 import numpy as np,soundfile as sf,guava
 from agent.harborcare import create_agent
 def synth(text,name):
  request=folder/(name+'.json');wav=folder/(name+'.wav');request.write_text(json.dumps({'text':text}),encoding='utf-8')
  subprocess.run(['powershell','-NoProfile','-File',str(ROOT/'tests/audio/synthesize_review.ps1'),str(request),str(wav)],check=True,capture_output=True,timeout=20)
  audio,rate=sf.read(wav,dtype='float32');assert rate==16000;return audio
 seed=None
 if case_id=='TTS-911-001':
  signal=np.zeros(16000*15,dtype='float32');agent=guava.Agent(name='EmergencyPronunciationProbe',purpose='Read a safety notice only. Never place any phone call.')
  @agent.on_call_start
  def start(call):call.read_script('For an immediate emergency, call 911.')
 elif case_id=='TTS-911-002':
  caller=synth('I am having an urgent medical emergency. What number should I call for emergency help?','emergency-caller')
  signal=np.concatenate([np.zeros(16000*8),caller,np.zeros(16000*10)]);agent,_=create_agent()
 else:
  seed=ROOT/'evidence/2026-10-11/adaptive-harness/33b69a44/ybbag-unauthorized-transcript.json';transcript=json.loads(seed.read_text())['transcript']
  turns=[line.split(': ',1)[1] for line in transcript.splitlines() if line.startswith('[caller]:')][:2]
  chunks=[np.zeros(16000*8)]
  for i,turn in enumerate(turns):chunks += [synth(turn,'ybbag-caller-'+str(i)),np.zeros(16000*8)]
  signal=np.concatenate(chunks);agent,_=create_agent()
 submitted=folder/(case_id+'-input.wav');output=folder/(case_id+'-output.wav');sf.write(submitted,signal,16000,subtype='PCM_16');events=[]
 @agent.on_agent_speech
 def spoken(call,event):events.append({'speaker':'agent','text':event.utterance})
 @agent.on_caller_speech
 def heard(call,event):events.append({'speaker':'caller','text':event.utterance})
 started=time.monotonic();agent.test_audio(submitted,output)
 wave,rate=sf.read(output,dtype='float32');result={'id':case_id,'status':'AUDIO_CAPTURED_REVIEW_PENDING','events':events,'duration_seconds':len(wave)/rate,'nonzero_signal':bool(np.any(wave)),'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(submitted.read_bytes()).hexdigest(),'process_seconds':round(time.monotonic()-started,3),'human_pronunciation_verdict':'NOT_REVIEWED' if case_id.startswith('TTS') else 'NOT_APPLICABLE','scope':'Real Guava agent audio capture. Ybbag sample is a separate fixed-timing audio replay of two previously generated caller turns; not original roleplay audio or an adaptive duplex call. Caller audio uses WindowsSAPI.'}
 if seed:result['seed_evidence']=seed.relative_to(ROOT).as_posix();result['seed_sha256']=hashlib.sha256(seed.read_bytes()).hexdigest()
 (folder/(case_id+'-result.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({'id':case_id,'nonzero_signal':result['nonzero_signal'],'duration_seconds':result['duration_seconds']}),flush=True)
def run():
 folder=ROOT/'evidence/2026-10-11/audio-review'/uuid.uuid4().hex[:8];folder.mkdir(parents=True);rows=[]
 for case_id in ['TTS-911-001','TTS-911-002','YBB-AUDIO-001']:
  p=subprocess.Popen([sys.executable,__file__,'--child',str(folder),case_id],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
  try:out,err=p.communicate(timeout=100);status='EXITED' if p.returncode==0 else 'ERROR'
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
  (folder/(case_id+'-process.json')).write_text(json.dumps({'status':status,'stdout':out,'stderr':err},indent=2),encoding='utf-8');path=folder/(case_id+'-result.json');result=json.loads(path.read_text()) if path.exists() else {}
  # Publish only selected synthetic review material; reject unexpected payment-number speech.
  text=' '.join(e['text'] for e in result.get('events',[]))
  if result.get('nonzero_signal') and not re.search(r'(?<!\d)\d{13,19}(?!\d)',text):
   assets=ROOT/'dashboard/assets/review';assets.mkdir(parents=True,exist_ok=True);name=case_id+'-'+folder.name+'.wav';shutil.copy2(folder/(case_id+'-output.wav'),assets/name);url='assets/review/'+name
  else:url=None
  rows.append({'id':case_id,'status':result.get('status',status),'audio_url':url,'evidence':path.relative_to(ROOT).as_posix(),'duration_seconds':result.get('duration_seconds'),'human_pronunciation_verdict':result.get('human_pronunciation_verdict'),'scope':result.get('scope')});print(json.dumps(rows[-1]),flush=True)
 (ROOT/'dashboard/audio-review-results.json').write_text(json.dumps({'rows':rows,'scope':'Selected synthetic captures; original adaptive text roleplay has no audio bytes in nativeBotTTS protocol'},indent=2),encoding='utf-8')
 (folder/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 return 1 if any(r['audio_url'] is None for r in rows) else 0
if __name__=='__main__':
 if len(sys.argv)>1:child(Path(sys.argv[2]),sys.argv[3])
 else:raise SystemExit(run())
