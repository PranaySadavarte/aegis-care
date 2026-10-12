import json,guava,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from backend.sensitive_demo import SyntheticSensitiveProcessor
results=[];agent=guava.Agent(name='SyntheticVitalProbe',purpose='Collect labeled synthetic fixture values for a schema test; do not diagnose.')
keys=['systolic','diastolic','heart_rate','temperature_tenths_c']
@agent.on_call_start
def start(call):call.set_task('vitals',objective='Collect synthetic values only. Temperature is in tenths of a Celsius degree, so 370 means37.0. Do not read sensitive values back or give medical advice.',checklist=[guava.Field(key=k,field_type='integer',sensitive=True,description='Synthetic fixture '+k) for k in keys])
@agent.on_task_complete('vitals')
def done(call):
 values={k:call.get_field(k) for k in keys}
 results.append(SyntheticSensitiveProcessor().vital_receipt(values));call.hangup('Thank the caller for the synthetic fixture values. Do not diagnose.')
with agent.test() as session:
 session.wait_for_turn();session.say('Synthetic systolic is120, diastolic80, heart rate72 and temperature in tenths of Celsius370.');session.wait_for_end()
print(json.dumps({'results':results,'raw_test_transcript':session.get_transcript(),'scope':'Isolated synthetic native field/schema test, not clinical service'}),flush=True)
assert results and results[0]['diagnosis_provided'] is False
