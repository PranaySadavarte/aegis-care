import json,urllib.request,urllib.error
from pathlib import Path
from guava.health import HealthContext,HealthServer
root=Path(__file__).resolve().parents[2];ctx=HealthContext();rows=[]
with HealthServer(ctx,host='127.0.0.1',port=0) as server:
 port=server._server.server_address[1]
 for state in ['starting','running','draining','stopped']:
  ctx.set_state(state)
  for route in ['live','ready']:
   try:
    with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/'+route,timeout=2) as r:status=r.status
   except urllib.error.HTTPError as e:status=e.code
   expected=200 if (route=='live' and state!='stopped') or (route=='ready' and state=='running') else 503
   rows.append({'state':state,'route':route,'actual':status,'expected':expected,'status':'PASS' if status==expected else 'FAIL'})
rows.append({'check':'server_thread_stopped','status':'PASS' if not server._thread.is_alive() else 'FAIL'})
(root/'evidence/2026-10-11/extended-sdk/health-results.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows))
raise SystemExit(1 if any(r['status']!='PASS' for r in rows) else 0)
