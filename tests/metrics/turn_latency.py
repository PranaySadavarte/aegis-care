import json,sys,time,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
from guava.testing.protocol import BotTTS
root=Path(__file__).resolve().parents[2];folder=root/'evidence/2026-10-11/kpi-expansion'/('turn-latency-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True)
agent,_=create_agent();turns=[]
with agent.test() as s:
 s.wait_for_turn()
 for prompt in ['My patient ID is1001 and verification code is4242.','How much is my outstanding balance?']:
  begin=time.monotonic();s.say(prompt)
  while True:
   event=s.recv()
   if isinstance(event,BotTTS):
    turns.append({'text_submission_to_first_bot_tts_event_seconds':time.monotonic()-begin,'scope':'Client monotonic receipt of text event; not audible onset, VAD endpoint or isolated LLM/ASR latency'});break
  if len(turns)==1:s.wait_for_turn()
(folder/'summary.json').write_text(json.dumps({'turns':turns,'scope':'Two hosted text turns in one session; first response can be an acknowledgement'},indent=2),encoding='utf-8')
(root/'dashboard/turn-metrics.json').write_text(json.dumps({'turns':turns,'scope':'Two hosted text turns, not speech response latency'},indent=2),encoding='utf-8');print(json.dumps(turns),flush=True)
