import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
root=Path(__file__).resolve().parents[2];label=sys.argv[1]
case=next(r for r in json.loads((root/'fixtures/intent-labels.json').read_text()) if r.get('expected')==label)
observed=[]
def record(call,event,detail=None):
 if event=='finished':observed.append(detail)
agent,_=create_agent(recorder=record)
with agent.test() as s:
 s.wait_for_turn();s.say('My patient ID is1001 and verification code is4242.');s.wait_for_turn();s.say(case['text'])
 if label=='appointments':s.wait_for_turn();s.say('Book October15 2026 at9AM, the2026-10-15 09:00slot.')
 if label=='payments':s.wait_for_turn();s.say('I consent to a simulated payment of1000cents, yes.')
 s.wait_for_end()
print(json.dumps({'expected':label,'prompt':case['text'],'observed':observed,'transcript':s.get_transcript(),'termination':s.termination_reason,'correct':bool(observed) and observed[-1]['workflow']==label,'scope':'One labeled paraphrase per workflow, native Agent.test and actual Expert task completion'}),flush=True)
raise SystemExit(0 if observed and observed[-1]['workflow']==label else 1)
