"""Publish reviewed metrics only; keep raw evidence and metadata SQLite local."""
import json,re,sqlite3,hashlib,html
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1];raw=root/'evidence/2026-10-11/robustness-audit'
findings=json.loads((root/'reports/findings/robustness-findings-2026-10-11.json').read_text())
rows=[]
for path in sorted(raw.glob('audio-*/*-result.json'))+sorted(raw.glob('echo-repeat-*/*-result.json')):
 r=json.loads(path.read_text());hyp=r.get('hypothesis','');words=dict(zip('zero one two three four five six seven eight nine'.split(),'0123456789'))
 h=' '.join(words.get(t,t) for t in re.sub(r'[^a-z0-9 ]',' ',hyp.lower()).split());h=re.sub(r'(?<!\w)(?:[0-9] +)+[0-9](?!\w)',lambda m:m.group().replace(' ',''),h)
 exact=sum(bool(re.search(r'(?<![0-9])'+x+r'(?![0-9])',h)) for x in ('1001','4242'))
 rows.append({'id':r['id'],'condition':r['condition'],'WER':r.get('WER'),'CER':r.get('CER'),'numeral_equivalent_WER':r.get('numeral_equivalent_WER'),'exact_credentials':exact,'evidence':path.relative_to(raw).as_posix()})
text=[]
for path in sorted(raw.glob('text-*/*.json')):
 if path.stem in ('summary','scenario-snapshot'):continue
 r=json.loads(path.read_text());text.append({'id':r['id'],'native_process_status':r['status'],'evidence':path.relative_to(raw).as_posix()})
data={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'findings':findings,'audio':rows,'text':text,'limits':'Synthetic-only. Native verdicts are distinct from reviewed findings; file overlap does not validate physical AEC or live interruption.'}
(root/'dashboard/defect-results.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
with sqlite3.connect(raw/'qa-observations.sqlite3') as db:
 db.execute('CREATE TABLE IF NOT EXISTS observations (evidence_path TEXT, sha256 TEXT, case_id TEXT, kind TEXT, sanitized_json TEXT, PRIMARY KEY(evidence_path,sha256))')
 for row in rows+text:
  digest=hashlib.sha256((raw/row['evidence']).read_bytes()).hexdigest()
  db.execute('INSERT OR IGNORE INTO observations VALUES (?,?,?,?,?)',(row['evidence'],digest,row['id'],'audio' if 'WER' in row else 'text',json.dumps(row)))
 db.execute('CREATE TABLE IF NOT EXISTS finding_reviews (finding_id TEXT, review_sha256 TEXT, sanitized_json TEXT, PRIMARY KEY(finding_id,review_sha256))')
 for finding in findings:
  encoded=json.dumps(finding,sort_keys=True);db.execute('INSERT OR IGNORE INTO finding_reviews VALUES (?,?,?)',(finding['id'],hashlib.sha256(encoded.encode()).hexdigest(),encoded))
esc=html.escape
cards=''.join('<article><small>'+esc(f['id']+' · '+f['severity'])+'</small><h2>'+esc(f['classification'])+'</h2><p>'+esc(f['problem'])+'</p><p><b>Owner:</b> '+esc(f['owner'])+'</p><p><b>Next action:</b> '+esc(f['recommendation'])+'</p></article>' for f in findings)
fmt=lambda v:'Unavailable' if v is None else format(v*100,'.2f')+'%'
table=''.join('<tr><td>'+esc(r['id'])+'</td><td>'+fmt(r['WER'])+'</td><td>'+fmt(r['CER'])+'</td><td>'+fmt(r['numeral_equivalent_WER'])+'</td><td>'+str(r['exact_credentials'])+'/2</td></tr>' for r in rows)
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AEGIS · Defect discovery</title><style>body{font:16px/1.6 system-ui;background:#edf2f3;color:#19343c;margin:0}header{background:#163d44;color:white;padding:28px 5vw}nav{display:flex;gap:20px;flex-wrap:wrap}nav a{color:#bae5d9}main{max-width:1100px;margin:auto;padding:25px}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:16px}article{background:white;border:1px solid #dbe4e6;border-radius:14px;padding:20px}small{color:#a04c25}h2{font-size:20px}table{width:100%;background:white;border-collapse:collapse}th,td{text-align:left;padding:12px;border-bottom:1px solid #dbe4e6}a{color:#137269}</style></head><body><header><nav><a href="./">Overview</a><a href="calls.html">Calls</a><a href="runs.html">Test runs</a><a href="metrics/robustness.html">Robustness</a></nav><h1>Defect discovery</h1><p>Failures, evaluator disagreements and unverified risks remain visible.</p></header><main><p>Seven hostile text scenarios plus targeted follow-ups; six audio conditions plus an echo repeat. Native judgments are not treated as ground truth. Synthetic data only.</p><section>'''+cards+'''</section><h2>Measured audio conditions</h2><p>Literal WER/CER and numeral-equivalent WER are separate. Exact credentials require full digit matches: extra trailing digits are failures.</p><table><thead><tr><th>Condition</th><th>Literal WER</th><th>CER</th><th>Numeral WER</th><th>Exact credentials</th></tr></thead><tbody>'''+table+'''</tbody></table><p>These file-input observations do not measure isolated ASR latency, acoustic echo cancellation, live barge-in or real accent coverage.</p><p><a href="../reports/sdk-evaluation/product-robustness-assessment-2026-10-11.md">Product assessment and evidence map</a></p><p>Run Defect discovery or Noise / echo from Test runs. Hosted suites may consume usage. Raw evidence and the QA database remain local and are not served.</p></main></body></html>'''
(root/'dashboard/defects.html').write_text(page,encoding='utf-8')
print(json.dumps({'findings':len(findings),'audio_observations':len(rows),'text_observations':len(text),'database':'local metadata-only SQLite'}))
