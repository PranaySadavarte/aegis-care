import json,subprocess,uuid,concurrent.futures,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/kpi-expansion'/('expert-routing-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
def run(label):
 p=subprocess.Popen([str(root/'baseline/sdk-0.47.0/.venv/Scripts/python.exe'),'tests/metrics/expert_routing.py',label],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
 try:out,err=p.communicate(timeout=55);status='PASS' if p.returncode==0 else 'FAIL'
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
 (folder/(label+'.json')).write_text(json.dumps({'status':status,'stdout':out,'stderr':err,'exit_code':p.returncode},indent=2),encoding='utf-8')
 return {'workflow':label,'status':status}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,(sys.argv[1:] or ['identity','eligibility','claims','appointments','billing','payments'])))
summary={'correct':sum(r['status']=='PASS' for r in rows),'total':len(rows),'rows':rows,'scope':'One labeled paraphrase per workflow, native Agent.test and actual Expert completion; no unsupported or multi-intent cases','profile_loaded':'docs/agent-profile at process start'}
(folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');
if len(sys.argv)==1:(root/'dashboard/expert-routing-metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary),flush=True)
raise SystemExit(1 if any(r['status']!='PASS' for r in rows) else 0)
