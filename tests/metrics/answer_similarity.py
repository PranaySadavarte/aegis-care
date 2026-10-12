import os,json,sys,uuid,statistics,re,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2];os.environ['HF_HOME']=str(root/'evidence/models');os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
from rouge_score import rouge_scorer
from bert_score import BERTScorer
from huggingface_hub import snapshot_download,HfApi
folder=root/'evidence/2026-10-11/kpi-expansion'/('similarity-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
history=json.loads((root/'dashboard/run-history.json').read_text());last=next(r for r in reversed(history) if r['suite']=='hosted')
refs=json.loads((root/'fixtures/answer-references.json').read_text());pairs=[]
for ref in refs:
 p=root/'evidence/2026-10-11/suite-runs'/last['run_id']/('Hosted-'+ref['workflow']+'.txt')
 records=[]
 for line in p.read_text(encoding='utf-8').splitlines():
  try:record=json.loads(line)
  except ValueError:continue
  if record.get('transcript'):records.append(record)
 if not records:continue
 transcript=records[-1]['transcript'];tail=transcript.rsplit('[caller]:',1)[-1]
 candidate=' '.join(line.partition('[agent]:')[2].strip() for line in tail.splitlines() if line.startswith('[agent]:'))
 pairs.append({**ref,'candidate':candidate,'source_run':last['run_id'],'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(folder/'answer-pairs.json').write_text(json.dumps(pairs,indent=2),encoding='utf-8')
rouge=rouge_scorer.RougeScorer(['rouge1','rouge2','rougeL'],use_stemmer=True)
for pair in pairs:pair['rouge']={k:dict(precision=v.precision,recall=v.recall,f1=v.fmeasure) for k,v in rouge.score(pair['reference'],pair['candidate']).items()}
(folder/'rouge-results.json').write_text(json.dumps(pairs,indent=2),encoding='utf-8')
config=json.loads((root/'fixtures/kpi-config.json').read_text());model=config['model'];revision=config['model_revision']
local=snapshot_download(model,revision=revision,allow_patterns=['config.json','tokenizer.json','tokenizer_config.json','vocab.txt','special_tokens_map.json','model.safetensors'])
scorer=BERTScorer(model_type=local,num_layers=5,lang='en',device='cpu',idf=False,rescale_with_baseline=False)
P,R,F=scorer.score([p['candidate'] for p in pairs],[p['reference'] for p in pairs],batch_size=4)
for i,pair in enumerate(pairs):pair['bert_score']={'precision':float(P[i]),'recall':float(R[i]),'f1':float(F[i])}
result={'sample_count':len(pairs),'source_run':last['run_id'],'model':model,'model_revision':revision,'num_layers':5,'idf':False,'baseline_rescaling':False,'bert_score_f1_mean':statistics.mean(float(x) for x in F),'rouge_f1_means':{key:statistics.mean(p['rouge'][key]['f1'] for p in pairs) for key in ['rouge1','rouge2','rougeL']},'pairs':pairs,'scope':'Seven recorded synthetic outcome response spans, not entire calls; similarity does not establish factual accuracy or safety.'}
(folder/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8');(root/'dashboard/answer-metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='pairs'}),flush=True)
