"""Inventory plans, executable methods, text prompts and audio fixtures without importing tests."""
import ast,csv,json,re,html
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
rows=list(csv.DictReader((root/'reports/test-plans/test-cases.csv').open(encoding='utf-8-sig')))
reasons={"SDK-005":"No second controlled organization/principal configured; application session checks do not prove platform cross-organization isolation.","SDK-010":"Dedicated disconnect/replay fault harness not implemented; ordinary session completion does not test reconnection.","SDK-012":"Only Windows is available; no Linux/macOS execution environment tested.","APP-008":"No controlled speech-disclosure interruption/acknowledgment experiment implemented; an interrupted callback alone is insufficient.","CAN-001":"No deployed production canary, scheduled observation window or monitoring thresholds configured."}
for row in rows:row["ExecutionReason"]=reasons.get(row["ID"],"PARTIAL plans contain untested subchecks; see evidence and coverage report" if row["Status"].startswith("PARTIAL") else "See execution evidence")
for row in rows:row.update(SourceType='Coverage plan',SourcePath='reports/test-plans/test-cases.csv',RunCommand='Choose the implemented suite in Test runs; PARTIAL is not a completed plan')
history=read(root/'dashboard/run-history.json');latest=next(r for r in reversed(history) if any(g['group']=='Application functional' for g in r['groups']))
folder=root/'evidence/2026-10-11/suite-runs'/latest['run_id'];statuses={}
for name in ['SDK-offline.txt','Application-functional.txt']:
 for match in re.finditer(r'^(test_\w+) \(([^)]+)\) \.\.\. (ok|FAIL|ERROR|skipped[^\n]*)', (folder/name).read_text(encoding='utf-8',errors='replace'),re.M):
  statuses[match.group(2)]='PASS' if match.group(3)=='ok' else 'FAIL' if match.group(3) in ('FAIL','ERROR') else 'SKIPPED'
for area in ('sdk','functional'):
 for p in sorted((root/'tests'/area).glob('test_*.py')):
  tree=ast.parse(p.read_text(encoding='utf-8-sig'))
  for cls in [n for n in tree.body if isinstance(n,ast.ClassDef)]:
   for fn in cls.body:
    if not isinstance(fn,ast.FunctionDef) or not fn.name.startswith('test_'):continue
    suffix=p.stem+'.'+cls.name+'.'+fn.name;status=next((v for key,v in statuses.items() if key.endswith(suffix)),'NOT_RUN')
    rows.append(dict(ID='METHOD:'+suffix,Threat_or_behavior=fn.name.replace('test_','',1).replace('_',' '),Status=status,PipelineStage='SDK / installation / transport' if area=='sdk' else 'Business logic / authorization / mock APIs',Direction='Shared SDK' if area=='sdk' else 'Synthetic application',Expected='Assertions defined in the linked source method',SourceType='Executable methods',SourcePath=p.relative_to(root).as_posix(),RunCommand='& .\\baseline\\sdk-0.47.0\\.venv\\Scripts\\python.exe -m unittest discover -s tests/'+area+' -p test_*.py -v',Evidence=latest['run_id']))
for source in ['fixtures/text-security-scenarios.json','fixtures/defect-discovery-text.json','fixtures/intent-labels.json','fixtures/roleplay-scenarios.json']:
 for case in read(root/source):
  is_intent='intent-labels' in source
  prompt=case.get('caller') or case.get('text') or ' | '.join(case.get('turns',[]))
  prompt=re.sub(r'(?<!\d)\d{13,19}(?!\d)','[SYNTHETIC PAN]',prompt)
  prompt=re.sub(r'(?i)(security code|cvv)\s*(?:is)?\s*\d{3,4}',r'\1 [REDACTED]',prompt).replace('SYNTHETIC-VITAL-CANARY','[SYNTHETIC VITAL MARKER]')
  text_backlog=read(root/'dashboard/text-backlog-results.json') if (root/'dashboard/text-backlog-results.json').exists() else {'rows':[]}
  text_result=next((r for r in text_backlog['rows'] if r['id']==case['id']),{}) if source=='fixtures/text-security-scenarios.json' else {}
  if source=='fixtures/text-security-scenarios.json' and case['id'] in ('identity-switch','inject-wrong-code','malformed-code'):
   variant={'identity-switch':'identity-switch','inject-wrong-code':'injection','malformed-code':'malformed'}[case['id']]
   security_run=next((r for r in reversed(history) if r['suite']=='security'),None)
   if security_run:
    group=next((g for g in security_run['groups'] if g['group']=='Hosted security '+variant),None)
    if group:text_result={'status':'LATEST_VARIANT_'+group['status'],'evidence':group['evidence_file'],'variant':True}
  rows.append(dict(ID='TEXT:'+Path(source).stem+':'+case['id'],Threat_or_behavior=prompt,Status=text_result.get('status',case.get('status','OBSERVED' if is_intent else 'OBSERVED_REVIEW_FINDINGS')),PipelineStage='Conversation state / Expert callbacks',Direction='Hosted text',Expected=case.get('expected',case.get('rubric','See source acceptance rules')) if not is_intent else str(case.get('expected',case.get('expected_set'))),SourceType='Text prompts',SourcePath=source,RunCommand='& .\\baseline\\sdk-0.47.0\\.venv\\Scripts\\python.exe tests/run_all.py --suite '+('security' if text_result.get('variant') else 'fixture-text' if text_result else 'kpi' if is_intent else 'extended' if 'roleplay' in source else 'adversarial' if 'defect-discovery' in source else 'security'),Evidence=text_result.get('evidence','See per-scenario raw evidence and reviewed findings'),Prompt=prompt,ExecutionReason='Latest hosted follow-up variant; original fixture wording differs. See security run evidence' if text_result.get('variant') else 'Exact fixture executed; limited backend safety checks, not full semantic scoring' if text_result else 'See source and scoped execution evidence'))
for source in ['fixtures/audio/manifest.json','fixtures/audio/robustness/manifest.json','fixtures/audio/public/manifest.json','fixtures/audio/challenges/manifest.json']:
 for case in read(root/source):
  backlog=read(root/'dashboard/audio-backlog-results.json') if (root/'dashboard/audio-backlog-results.json').exists() else {'rows':[]}
  observation=next((r for r in backlog['rows'] if r['id']==case['id'] and r.get('source_sha256')==case.get('sha256')),{})
  measured=bool(observation) or case['id']=='verify-padded' or 'robustness/' in source or 'public/' in source or 'challenges/' in source
  rows.append(dict(ID='AUDIO:'+case['id'],Threat_or_behavior=case.get('condition',case.get('dataset','Public human speech')),Status=observation.get('status','OBSERVED' if measured else 'NOT_RUN'),PipelineStage='ASR / endpointing / TTS / audio transport',Direction='File-in hosted audio',Expected='Compare recognized transcript with labeled reference; exact critical entities are separate',SourceType='Audio fixtures',SourcePath=case['path'],RunCommand='& .\\baseline\\sdk-0.47.0\\.venv\\Scripts\\python.exe tests/run_all.py --suite '+('fixture-audio' if observation else 'kpi' if 'public/' in source else 'robustness' if 'robustness/' in source else 'audio'),Evidence=observation.get('evidence',case.get('sha256','')),ExecutionReason='8seconds leading/3seconds trailing silence added; literalASR score, not task completion' if observation else 'See scoped observation; fixture hash alone is not execution evidence',Reference=case.get('reference_text',''),Provenance=case.get('source',case.get('source_repository','Windows SAPI synthetic voice'))))
counts={kind:sum(r['SourceType']==kind for r in rows) for kind in {r['SourceType'] for r in rows}}
(root/'dashboard/test-inventory.json').write_text(json.dumps({'rows':rows,'counts':counts,'note':'Inventory entries are plans, methods or fixtures, not a combined execution denominator.'},indent=2),encoding='utf-8')
esc=html.escape
text_rows=''.join('<details><summary>'+esc(r['ID'])+'</summary><p>'+esc(r.get('Prompt',''))+'</p><p>Expected: '+esc(str(r.get('Expected','')))+'<br>Source: '+esc(r['SourcePath'])+'</p><pre>'+esc(r['RunCommand'])+'</pre></details>' for r in rows if r['SourceType']=='Text prompts')
audio_rows=''.join('<tr><td>'+esc(r['ID'])+'</td><td>'+esc(r['Threat_or_behavior'])+'</td><td>'+esc(r.get('Reference',''))+'</td><td>'+esc(r['SourcePath'])+'</td><td>'+esc(r['Status'])+'</td></tr>' for r in rows if r['SourceType']=='Audio fixtures')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AEGIS Â· Test data</title><style>body{font:16px/1.6 system-ui;background:#edf2f3;color:#19343c;margin:0}header{background:#163d44;color:white;padding:28px 5vw}main{max-width:1100px;margin:auto;padding:25px}nav{display:flex;gap:20px;flex-wrap:wrap}nav a{color:#bae5d9}details{background:white;margin:12px 0;padding:14px;border-radius:12px}pre{white-space:pre-wrap;overflow-wrap:anywhere}table{border-collapse:collapse;background:white}td,th{padding:12px;text-align:left;border-bottom:1px solid #dbe4e6}a{color:#137269}.scroll{overflow:auto}</style></head><body><header><nav><a href="./">Overview</a><a href="runs.html">Test runs</a><a href="defects.html">Open defects</a></nav><h1>Prompts and audio inputs</h1><p>Actual fixture sources and reproducible commands. Synthetic card/security values are redacted in this view.</p></header><main><p>Open the source JSON locally to see exact test inputs. These examples are not a pooled PASS count.</p><h2>Text scenarios</h2>'''+text_rows+'''<h2>Labeled audio files</h2><div class="scroll"><table><thead><tr><th>Sample</th><th>Condition</th><th>Reference transcript</th><th>Source file</th><th>Execution</th></tr></thead><tbody>'''+audio_rows+'''</tbody></table></div><p><a href="../docs/audio-datasets.md">Dataset provenance and expansion plan</a> Â· <a href="../docs/kpi-methodology.md">How metrics are calculated</a></p></main></body></html>'''
(root/'dashboard/data-library.html').write_text(page,encoding='utf-8');print(json.dumps(counts))
