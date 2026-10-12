import sys,json,time,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from guava.helpers.llm import IntentRecognizer
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/kpi-expansion'/('intent-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
labels=json.loads((root/'fixtures/intent-labels.json').read_text());(folder/'label-snapshot.json').write_text(json.dumps(labels,indent=2),encoding='utf-8')
recognizer=IntentRecognizer({'identity':'Verify identity','eligibility':'Insurance coverage, plan and copay','claims':'Status of submitted insurance claims','appointments':'Book an appointment','billing':'Read outstanding balance or charges','payments':'Make a simulated payment'})
observations=[]
for case in labels:
 for repeat in range(2):
  started=time.monotonic()
  try:
   actions=recognizer.classify(case['text']);prediction=[a.key for a in actions or []];error=None
  except Exception as e:prediction=[];error=type(e).__name__
  row={**case,'repeat':repeat+1,'predicted':prediction,'request_seconds':round(time.monotonic()-started,4),'error':error}
  observations.append(row);(folder/'observations.json').write_text(json.dumps(observations,indent=2),encoding='utf-8');print(json.dumps({'id':case['id'],'repeat':repeat+1,'predicted':prediction,'error':error}),flush=True)
single=[r for r in observations if r['kind']=='single'];correct=sum(not r['error'] and bool(r['predicted']) and r['predicted'][0]==r['expected'] for r in single)
unsupported=[r for r in observations if r['kind']=='unsupported'];rejected=sum(not r['error'] and not r['predicted'] for r in unsupported)
agreement=sum(observations[i]['predicted']==observations[i+1]['predicted'] and not observations[i]['error'] and not observations[i+1]['error'] for i in range(0,len(observations),2))
result={'single_intent_correct':correct,'single_intent_total':len(single),'single_intent_accuracy':correct/len(single),'unsupported_rejected':rejected,'unsupported_total':len(unsupported),'repeat_agreement':agreement/len(labels),'case_count':len(labels),'trials':len(observations),'ambiguity_rate':sum(len(r['predicted'])>1 for r in observations)/len(observations),'confidence_status':'No numeric calibrated confidence returned by installed0.47.0 public helper','scope':'Native six-choice helper benchmark; not actual HarborCare workflow routing accuracy. Ranked matches and repeat agreement are not calibrated probabilities.'}
(folder/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(root/'dashboard/intent-metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result),flush=True)
raise SystemExit(1 if any(r['error'] for r in observations) else 0)
