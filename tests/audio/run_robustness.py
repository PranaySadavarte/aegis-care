import subprocess,json,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/robustness-audit'/('audio-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
summary=[]
(folder/'manifest-snapshot.json').write_bytes((root/'fixtures/audio/robustness/manifest.json').read_bytes())
for case in json.loads((root/'fixtures/audio/robustness/manifest.json').read_text()):
 p=subprocess.Popen([str(root/'baseline/sdk-0.47.0/.venv/Scripts/python.exe'),str(root/'tests/audio/robustness_probe.py'),case['id'],str(folder)],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
 try:out,err=p.communicate(timeout=45);status='OBSERVED' if p.returncode==0 else 'ERROR'
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
 (folder/(case['id']+'-process.json')).write_text(json.dumps(dict(id=case['id'],status=status,exit_code=p.returncode,stdout=out,stderr=err),indent=2),encoding='utf-8')
 summary.append({'id':case['id'],'status':status});print(json.dumps({'id':case['id'],'status':status,'folder':folder.name}),flush=True)

(folder/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
raise SystemExit(1 if any(r["status"]!="OBSERVED" for r in summary) else 0)
