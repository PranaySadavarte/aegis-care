import subprocess,json,uuid,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[2]
folder=root/"evidence/2026-10-11/robustness-audit"/("text-"+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
cases=json.loads((root/"fixtures/defect-discovery-text.json").read_text())
summary=[]
(folder/"scenario-snapshot.json").write_text(json.dumps(cases,indent=2),encoding="utf-8")
for case in cases:
 if len(sys.argv)>1 and case['id'] not in sys.argv[1:]:continue
 p=subprocess.Popen([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/integration/defect_discovery.py"),case['id']],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
 try:out,err=p.communicate(timeout=55);status='PASS' if p.returncode==0 else 'FAIL'
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
 row={'id':case['id'],'at_utc':datetime.now(timezone.utc).isoformat(),'status':status,'exit_code':p.returncode,'stdout':out,'stderr':err}
 (folder/(case['id']+'.json')).write_text(json.dumps(row,indent=2),encoding='utf-8')
 summary.append({'id':case['id'],'status':status});print(json.dumps({'id':case['id'],'status':status,'folder':folder.name}),flush=True)

(folder/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
raise SystemExit(1 if any(r["status"]!="PASS" for r in summary) else 0)
