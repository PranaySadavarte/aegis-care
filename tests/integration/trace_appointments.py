"""Trace existing appointment regression without modifying Expert behavior."""
import sys,json,runpy,subprocess,uuid,datetime,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
if '--child' in sys.argv:
 from guava.helpers.llm import IntentRecognizer
 original=IntentRecognizer.classify
 def trace(self,*args,**kwargs):
  result=original(self,*args,**kwargs)
  print(json.dumps({'routing_trace':{'request':args[0] if args else kwargs,'matches':[getattr(x,'key',str(x)) for x in result] if isinstance(result,list) else str(result)}}),flush=True)
  return result
 IntentRecognizer.classify=trace
 sys.argv=[str(root/'tests/integration/harborcare_hosted.py'),'appointments']
 runpy.run_path(sys.argv[0],run_name='__main__')
else:
 folder=root/'evidence/2026-10-12'/('appointments-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
 record={'started_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Existing native Agent.test appointment control with pass-through intent trace; no PSTN call; no Expert modifications'}
 for name,cmd in [('focused-offline',[sys.executable,'-m','unittest','discover','-s','tests/functional','-p','test_harborcare_handlers.py','-v']),('hosted-appointments',[sys.executable,__file__,'--child'])]:
  try:
   p=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=50)
   text=p.stdout+'\n'+p.stderr;status='PASS' if p.returncode==0 else 'FAIL'
  except subprocess.TimeoutExpired as e:
   text=(e.stdout.decode('utf-8',errors='replace') if isinstance(e.stdout,bytes) else e.stdout or '')+'\n'+(e.stderr.decode('utf-8',errors='replace') if isinstance(e.stderr,bytes) else e.stderr or '');status='TIMEOUT'
  (folder/(name+'.txt')).write_text(text,encoding='utf-8')
  record[name]={'status':status,'evidence':(folder/(name+'.txt')).relative_to(root).as_posix(),'sha256':hashlib.sha256(text.encode()).hexdigest()}
 record['completed_at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 (folder/'summary.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
 (root/'dashboard/appointment-diagnostic.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
 print(json.dumps(record))
