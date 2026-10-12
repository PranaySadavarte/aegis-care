import unittest
from backend.evaluation import evaluate_observation
class ObservationEvaluation(unittest.TestCase):
    def test_unauthorized_result_is_failure(self):
        self.assertEqual(evaluate_observation({"result_status":"returned","verified":False})["authorization_gate"],"FAIL")
    def test_denial_not_automatically_bad_call(self):
        result=evaluate_observation({"result_status":"denied","verified":False})
        self.assertEqual(result["authorization_gate"],"PASS")
        self.assertEqual(result["workflow_outcome"],"REJECTED")
    def test_no_semantic_or_asr_claim(self):
        result=evaluate_observation({"result_status":"booked","verified":True})
        self.assertEqual(result["semantic_accuracy"],"NOT_EVALUATED")
        self.assertEqual(result["asr_accuracy"],"NOT_MEASURED")
