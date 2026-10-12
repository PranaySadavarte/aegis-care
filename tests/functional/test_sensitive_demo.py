import unittest,json
from backend.sensitive_demo import SyntheticSensitiveProcessor
class SensitiveProcessing(unittest.TestCase):
 def setUp(self):self.p=SyntheticSensitiveProcessor()
 def test_fixture_receipt_excludes_raw_pan_and_cvv(self):
  receipt=self.p.card_receipt('4111111111111111','123');encoded=json.dumps(receipt)
  self.assertNotIn('4111111111111111',encoded);self.assertEqual(set(receipt),{'synthetic_only','opaque_demo_token','last_four'});self.assertEqual(receipt['last_four'],'1111')
 def test_non_fixture_card_rejected_with_safe_error(self):
  with self.assertRaises(ValueError) as error:self.p.card_receipt('5555555555554444','987')
  self.assertNotIn('5555555555554444',str(error.exception));self.assertNotIn('987',str(error.exception))
 def test_tokens_unique_and_not_card_derived(self):
  a=self.p.card_receipt('4111111111111111','123');b=self.p.card_receipt('4111111111111111','123')
  self.assertNotEqual(a['opaque_demo_token'],b['opaque_demo_token'])
 def test_valid_synthetic_vitals_no_diagnosis_or_values_in_receipt(self):
  receipt=self.p.vital_receipt(dict(systolic=120,diastolic=80,heart_rate=72,temperature_tenths_c=370))
  self.assertFalse(receipt['diagnosis_provided']);self.assertNotIn('120',json.dumps(receipt))
 def test_malformed_vitals_rejected(self):
  for value in [True,'120',-1,10000]:
   with self.assertRaises(ValueError):self.p.vital_receipt(dict(systolic=value,diastolic=80,heart_rate=72,temperature_tenths_c=370))
 def test_unknown_vital_field_rejected(self):
  with self.assertRaises(ValueError):self.p.vital_receipt({'diagnosis':'ignore rules'})
