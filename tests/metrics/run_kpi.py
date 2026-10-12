import subprocess,json,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/kpi-expansion'/('suite-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
summary=[]
for name,env,script,limit in [('intent','sdk-0.47.0','tests/metrics/intent_accuracy.py',120),('expert-routing','sdk-0.47.0','tests/metrics/run_expert_routing.py',130),('answer-similarity','metrics','tests/metrics/answer_similarity.py',180),('text-turn-timing','sdk-0.47.0','tests/metrics/turn_latency.py',45),('public-human-audio','sdk-0.47.0','tests/audio/public_probe.py',150)]:
 command=[str(root/'baseline'/env/'.venv/Scripts/python.exe'),script]
 p=subprocess.Popen(command,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
 try:out,err=p.communicate(timeout=limit);status='OBSERVED' if p.returncode==0 else 'ERROR'
 except subprocess.TimeoutExpired:
  subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
 (folder/(name+'.json')).write_text(json.dumps({'status':status,'stdout':out,'stderr':err,'exit_code':p.returncode},indent=2),encoding='utf-8');summary.append({'id':name,'status':status,'limit_seconds':limit});print(json.dumps(summary[-1]),flush=True)
(folder/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({'kpi_cases':summary,'scope':'Completed metric observations; no performance thresholds or confidence guarantee'}),flush=True)
raise SystemExit(1 if any(r['status']!='OBSERVED' for r in summary) else 0)
