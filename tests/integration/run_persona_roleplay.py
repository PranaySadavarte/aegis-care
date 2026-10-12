import subprocess,json,uuid,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/extended-sdk'/('roleplay-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
rows=[];cases=json.loads((root/'fixtures/roleplay-scenarios.json').read_text());(folder/'scenario-snapshot.json').write_text(json.dumps(cases,indent=2),encoding='utf-8')
for case in cases:
 if len(sys.argv)>1 and case["id"] not in sys.argv[1:]:continue
 p=subprocess.Popen([str(root/'baseline/sdk-0.47.0/.venv/Scripts/python.exe'),'tests/integration/persona_roleplay.py',case['id']],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
 try:out,err=p.communicate(timeout=90);status='PASS' if p.returncode==0 else 'FAIL'
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
 (folder/(case['id']+'.json')).write_text(json.dumps({'status':status,'stdout':out,'stderr':err,'exit_code':p.returncode},indent=2),encoding='utf-8');rows.append({'id':case['id'],'status':status});print(json.dumps(rows[-1]),flush=True)
(folder/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');
previous=json.loads((root/'dashboard/roleplay-results.json').read_text()) if (root/'dashboard/roleplay-results.json').exists() else {'rows':[]}
merged={r['id']:r for r in previous['rows']}
for r in rows:merged[r['id']]=r
(root/'dashboard/roleplay-results.json').write_text(json.dumps({'rows':list(merged.values()),'scope':'Generated-caller roleplays with native persona override; latest per-scenario outcomes; not physical voice/persona transport proof'},indent=2),encoding='utf-8')

raise SystemExit(1 if any(r['status']!='PASS' for r in rows) else 0)
