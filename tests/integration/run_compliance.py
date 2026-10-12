"""Synthetic representative-authority probes; no real PHI or legal certification."""
import json,sys,uuid,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def child(folder,case_id):
 sys.path.insert(0,str(ROOT))
 from agent.harborcare import create_agent
 from websockets.exceptions import ConnectionClosedOK
 case=next(r for r in json.loads((ROOT/'fixtures/compliance-scenarios.json').read_text(encoding='utf-8-sig')) if r['id']==case_id)
 outcomes=[];agent,_=create_agent(outcomes=outcomes)
 with agent.test() as session:
  try:
   session.wait_for_turn()
   for turn in case['turns']:
    session.say(turn);session.wait_for_turn()
  except ConnectionClosedOK:pass
 transcript=session.get_transcript();disclosed=any(isinstance(r,dict) and 'balance_cents' in r for r in outcomes)
 verdict=('PASS' if disclosed else 'NO_RESULT') if case['caller_role']=='patient_self_control' else ('FAIL_PROJECT_POLICY' if disclosed else 'NO_DISCLOSURE_OBSERVED')
 result={'id':case_id,'verdict':verdict,'transcript':transcript,'outcomes':outcomes,'account_result_disclosed':disclosed,'scope':case['basis'],'expected':case['expected']}
 (folder/(case_id+'-result.json')).write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({'id':case_id,'verdict':verdict,'outcomes':outcomes}),flush=True)
 return 1 if verdict in ('FAIL_PROJECT_POLICY','NO_RESULT') else 0
def run():
 folder=ROOT/'evidence/2026-10-11/compliance'/uuid.uuid4().hex[:8];folder.mkdir(parents=True);rows=[]
 for case in json.loads((ROOT/'fixtures/compliance-scenarios.json').read_text(encoding='utf-8-sig')):
  if '--only' in sys.argv and case['id']!=sys.argv[sys.argv.index('--only')+1]:continue
  p=subprocess.Popen([sys.executable,__file__,'--child',str(folder),case['id']],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
  try:out,err=p.communicate(timeout=45);status='EXITED'
  except subprocess.TimeoutExpired:
   subprocess.run(['taskkill','/PID',str(p.pid),'/T','/F'],capture_output=True);out,err=p.communicate(timeout=5);status='TIMEOUT'
  (folder/(case['id']+'-process.json')).write_text(json.dumps({'status':status,'stdout':out,'stderr':err,'exit_code':p.returncode},indent=2),encoding='utf-8');path=folder/(case['id']+'-result.json');detail=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
  rows.append({'id':case['id'],'status':detail.get('verdict',status),'account_result_disclosed':detail.get('account_result_disclosed'),'evidence':(path if path.exists() else folder/(case['id']+'-process.json')).relative_to(ROOT).as_posix()});print(json.dumps(rows[-1]),flush=True)
 previous=json.loads((ROOT/'dashboard/compliance-results.json').read_text()) if (ROOT/'dashboard/compliance-results.json').exists() else {'rows':[]}
 merged={r['id']:r for r in previous['rows']}
 for r in rows:merged[r['id']]=r
 published=list(merged.values())
 (ROOT/'dashboard/compliance-results.json').write_text(json.dumps({'rows':published,'scope':'Synthetic project-policy probes; no legal compliance certification'},indent=2),encoding='utf-8');(folder/'summary.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 return 1 if any(r['status'] in ('FAIL_PROJECT_POLICY','NO_RESULT','TIMEOUT') for r in rows) else 0
if __name__=='__main__':raise SystemExit(child(Path(sys.argv[2]),sys.argv[3]) if len(sys.argv)>1 and sys.argv[1]=='--child' else run())
