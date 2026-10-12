"""Publish selected sanitized observations with raw path/hash provenance."""
import json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/findings/evidence';OUT.mkdir(parents=True,exist_ok=True)
FILE=ROOT/'reports/findings/robustness-findings-2026-10-11.json'
findings=json.loads(FILE.read_text())
def mask(text):
 text=re.sub(r'(?<![\w.])(?:\d[ -]?){12,18}\d(?![\w.])','[REDACTED_SYNTHETIC_PAN]',text)
 text=re.sub(r'(?i)((?:security code|cvv)(?: is)?\s*[:=]?\s*)123\b',r'\1[REDACTED_SYNTHETIC_CVV]',text)
 text=re.sub(r'\b123\b','[REDACTED_SYNTHETIC_CVV]',text)
 return text.replace('SYNTHETIC-NAMESPACE-B-ONLY','[REDACTED_SYNTHETIC_CANARY]')
def excerpts(path,fid):
 text=path.read_text(encoding='utf-8-sig',errors='replace')
 if path.suffix=='.txt':
  name={'SDK-X001':'test_transfer_invalid_destination_should_reject','SDK-X002':'test_voicemail_invalid_does_not_mutate_state','SDK-X003':'test_datetime_invented_slot_should_be_rejected','SDK-X004':'test_rag_empty_namespace_does_not_query_all_documents','SDK-X005':'test_tenacity_explicit_empty_contact_preserved'}.get(fid)
  match=re.search(r'FAIL: '+str(name)+r'.*?(?=\n={10}|\n-{10}\nRan)',text,re.S)
  return (match.group() if match else text[:1600])
 obj=json.loads(text);items=[]
 if 'stdout' in obj:
  for line in obj['stdout'].splitlines():
   try:row=json.loads(line)
   except (ValueError,TypeError):continue
   if 'transcript' in row:items=[row] # Last full transcript, no repeated progress copies.
   elif 'native_rubric' in row or 'secret_readback_invariant' in row:items.append(row)
  if not items:return text[:3000]
  result=[]
  for row in items:
   if 'transcript' in row:
    lines=row['transcript'].splitlines()
    keys={'ROB-001':['card','security code','consent'],'ROB-002':['emergency','urgent','patient','verification','911'],'ROB-004':['card','security code','canary','medical','diagnos','cannot'],'ROB-008':['different','patient','verification','confirm']}.get(fid,[])
    chosen=[s for s in lines if not keys or any(k in s.lower() for k in keys)]
    result+=chosen[-16:]
   else:result.append(json.dumps(row))
  return '\n'.join(result)
 return json.dumps(obj,indent=2)[:5000]
for f in findings:
 if f['id'] in ('SDK-F001','CLI-F001','CLI-F002'):continue
 paths=[]
 for ref in f['evidence'].split(';'):
  ref=ref.strip();relative=ref if ref.startswith('evidence/') else 'evidence/2026-10-11/robustness-audit/'+ref
  paths.extend(ROOT.glob(relative))
 lines=[f'# {f["id"]}: {f["classification"]}', '', '**Current step:** SDK and unchanged Expert adversarial evaluation.', '', f'**Status and scope:** {f["classification"]}. {f["attribution_confidence"]}.', '', f'**Stage:** {f["pipeline_stage"]}. **Owner category:** {f["ownership_category"]}.', '', f'**Problem:** {f["problem"]}', '', f'**Expected:** {f["expected"]}', '', f'**Actual:** {f["actual"]}', '', '**Preserved evidence:** Raw files are local and deliberately not served by the dashboard. SHA-256 identifies the exact artifact. Excerpts below redact synthetic payment canaries.', '']
 for path in paths:
  lines += [f'- Local path: `{path.relative_to(ROOT).as_posix()}`; SHA-256: `{hashlib.sha256(path.read_bytes()).hexdigest()}`.', '', '```text',mask(excerpts(path,f['id'])),'```','']
 if not paths:raise FileNotFoundError(f['id']+' evidence missing')
 lines += [f'**Proposed owner action / workaround (not applied):** {f["recommendation"]}', '', '**Retest:** Repeat the original case and independent invariant after an owner change. Preserve native judge output separately; broaden transport testing only with configured endpoints.', '', '**Limitation:** A mocked boundary or synthetic file input is not a live carrier, physical echo-cancellation, production privacy or compliance result.']
 f['evidence_report']='reports/findings/evidence/'+f['id']+'.md'
 (OUT/(f['id']+'.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8')
FILE.write_text(json.dumps(findings,indent=2)+'\n',encoding='utf-8')
# Original SDK error reproduced using an in-memory HTTP response; no request is sent.
import sys
sys.path.insert(0,str(ROOT))
import httpx
from guava.utils import check_response
response=httpx.Response(401,text='synthetic-sensitive-marker',request=httpx.Request('GET','https://offline.invalid/'))
try:check_response(response)
except httpx.HTTPStatusError as exc:actual=str(exc)
(OUT/'SDK-F001.md').write_text('# SDK-F001: Response body included in exception\n\nActual exception, reproduced with a synthetic in-memory response (no HTTP request):\n\n```text\n'+actual+'\n```\n\nProposed default message, not applied:\n\n```text\nHTTP 401 Unauthorized for url https://offline.invalid/; response body omitted\n```\n\nThe body marker must not appear in the default exception. Real response bodies may contain credentials, patient details, payment values or internal diagnostics; none should be copied wholesale into shared exceptions/logs. Request identifiers may be included only when present and allowlisted. URL query strings also need redaction when sensitive.\n\nReproduce: `python -m unittest discover -s tests/sdk -p test_offline_contracts.py -v`. Original source: `guava/utils.py:check_response`, SDK0.47.0; this is independent of uv installation. Raw suite output is preserved under `evidence/2026-10-11/suite-runs/`. No production secret leak is claimed.\n',encoding='utf-8')
for fid,title,actual in [('CLI-F001','Installed Windows CLI unsigned','The installed executable was observed as NotSigned in the prior Authenticode inspection.'),('CLI-F002','Installer verification controls absent','Current official installer source has no explicit downloaded-binary checksum comparison or Authenticode check. Neither control has been fixed.')]:
 (OUT/(fid+'.md')).write_text(f'# {fid}: {title}\n\n{actual}\n\n[Installer audit and evidence provenance](../../sdk-evaluation/installer-audit-2026-10-11.md)\n\nExpected owner behavior: publish a trusted digest/signing identity and enforce artifact verification before atomic replacement. This is a proposed solution, not an applied SDK or installer fix. Unsigned status is not evidence of malware. The originally used installer route/provenance remains unknown. Partial-download rollback evidence is documented in [CLI-X003](CLI-X003.md).\n',encoding='utf-8')
print(json.dumps({'reviewed_evidence_pages':len(findings),'original_findings_pages':3}))
