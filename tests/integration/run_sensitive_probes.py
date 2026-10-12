import subprocess,json,uuid,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/robustness-audit'/('sensitive-probes-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
summary=[]
for name,args in [('pan',['sensitive_field_probe.py','pan']),('cvv',['sensitive_field_probe.py','cvv']),('vitals',['vitals_probe.py'])]:
 p=subprocess.Popen([str(root/'baseline/sdk-0.47.0/.venv/Scripts/python.exe'),str(root/'tests/integration'/args[0])]+args[1:],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
 try:out,err=p.communicate(timeout=45);status='OBSERVED' if p.returncode==0 else 'FAIL'
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
 (folder/(name+'.json')).write_text(json.dumps(dict(status=status,exit_code=p.returncode,stdout=out,stderr=err),indent=2),encoding='utf-8');summary.append({'id':name,'status':status});print(json.dumps(summary[-1]),flush=True)
(folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
raise SystemExit(1 if any(r['status']!='OBSERVED' for r in summary) else 0)
