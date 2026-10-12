import guava,sys,json
kind=sys.argv[1];values=[]
agent=guava.Agent(name='SyntheticSensitiveProbe',purpose='Test native sensitive field collection with synthetic data only.')
@agent.on_call_start
def start(call):
 call.set_task('collect',objective='Collect one synthetic test value. Never read the full value back. Finish courteously.',checklist=[guava.Field(key='secret',field_type='cvv' if kind=='cvv' else 'digit_sequence',sensitive=True,question='What is the synthetic test '+kind+' value?')])
@agent.on_task_complete('collect')
def complete(call):
 value=call.get_field('secret');values.append({'received':bool(value),'matches_synthetic':value==('123' if kind=='cvv' else '4111111111111111')})
 call.hangup('Thank the caller. Do not read the collected value back.')
with agent.test() as session:
 session.wait_for_turn();session.say('123' if kind=='cvv' else '4111111111111111');session.wait_for_end()
transcript=session.get_transcript();agent_text=' '.join(line for line in transcript.splitlines() if line.startswith('[agent]:'))
print(json.dumps({'kind':kind,'values':values,'raw_test_transcript':transcript,'caller_raw_value_retained_in_testing_transcript':('123' if kind=='cvv' else '4111111111111111') in transcript,'agent_full_value_readback':('123' if kind=='cvv' else '4111111111111111') in agent_text,'scope':'Hosted text testing only; not hosted recording/audio/diagnostic retention proof'}),flush=True)

assert values and all(r["matches_synthetic"] for r in values)
assert not (("123" if kind=="cvv" else "4111111111111111") in agent_text), "Full synthetic sensitive value read back"
