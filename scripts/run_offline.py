"""Portable core regression runner; does not require private installer evidence."""
from pathlib import Path
import subprocess,sys,datetime,uuid,json,re
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'evidence'/'portable-offline'/(datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]);folder.mkdir(parents=True)
rows=[]
for area in ('sdk','functional'):
 p=subprocess.run([sys.executable,'-m','unittest','discover','-s','tests/'+area,'-p','test_*.py','-v'],cwd=ROOT,capture_output=True,text=True,timeout=45)
 text=p.stdout+'\n'+p.stderr;(folder/(area+'.txt')).write_text(text,encoding='utf-8')
 m=re.search(r'Ran (\d+) tests?',text);failure=re.search(r'FAILED \(([^)]+)\)',text)
 row={'area':area,'total':int(m.group(1)) if m else None,'exit_code':p.returncode,'status':'PASS' if p.returncode==0 else 'FAIL','failure_summary':failure.group(1) if failure else None,'raw_evidence':(folder/(area+'.txt')).relative_to(ROOT).as_posix()};rows.append(row);print(json.dumps(row))
(folder/'summary.json').write_text(json.dumps({'groups':rows,'scope':'Fresh core unit/contract run. No installer source audit, hosted calls or dashboard history replacement.'},indent=2),encoding='utf-8')
print('Known discovery assertions may fail. Read raw evidence; do not delete failures to make this suite green.')
sys.exit(1 if any(x['exit_code'] for x in rows) else 0)
