"""Synthetic processing only; not payment tokenization service or clinical validation."""
import uuid
class SyntheticSensitiveProcessor:
 def card_receipt(self,pan,cvv):
  # Restrict to our designated test fixture; reject real or other card inputs.
  if pan!='4111111111111111' or cvv!='123':raise ValueError('Only designated synthetic fixture is supported')
  return {'synthetic_only':True,'opaque_demo_token':'demo-'+uuid.uuid4().hex,'last_four':'1111'}
 def vital_receipt(self,values):
  # Fixture schema bounds, not normal clinical ranges or triage advice.
  bounds={'systolic':(1,300),'diastolic':(1,200),'heart_rate':(1,300),'temperature_tenths_c':(100,500)}
  if set(values)!=set(bounds):raise ValueError('Invalid synthetic vital schema')
  if any(type(values[k]) is not int or not lo<=values[k]<=hi for k,(lo,hi) in bounds.items()):raise ValueError('Invalid synthetic vital value')
  return {'synthetic_only':True,'validated_fields':list(bounds),'diagnosis_provided':False}
