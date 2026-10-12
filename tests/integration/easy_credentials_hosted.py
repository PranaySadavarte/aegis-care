import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
outcomes=[];agent,backend=create_agent(outcomes=outcomes)
with agent.test() as session:
    session.wait_for_turn();session.say("My synthetic patient ID is 1001. My synthetic verification code is 4242.")
    session.wait_for_turn();session.say("I choose billing.")
    session.wait_for_end()
assert len(outcomes)==1 and outcomes[0]["balance_cents"]==5000,outcomes
print(json.dumps({"assertion":"PASS","termination":session.termination_reason,"transcript":session.get_transcript()}))
