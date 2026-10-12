import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tests/sdk"))
from test_offline_contracts import patch,MockCall,guava
from agent.harborcare import create_agent
from backend.synthetic import AccessDenied
class NativeIdentityRouting(unittest.TestCase):
    def test_switch_intent_clears_prior_authorization(self):
        with patch("guava.agent.Client"):agent,b=create_agent()
        call=MockCall();b.verify(call.id,"1001","4242")
        with patch("guava.helpers.llm.IntentRecognizer.classify",return_value=[guava.SuggestedAction(key="switch_patient")]):
            actions=agent._on_action_requested(call,"I am another patient")
        self.assertEqual(actions[0].key,"switch_patient")
        with self.assertRaises(AccessDenied):b.subject(call.id)
    def test_switch_uses_fresh_field_keys(self):
        with patch("guava.agent.Client"):agent,b=create_agent()
        call=MockCall();b.verify(call.id,"1001","4242")
        agent._on_action_handlers["switch_patient"](call)
        self.assertEqual(call._field_keys_by_task_id["switch_verify"],["new_patient_id","new_verification_code"])
        call.set_field("new_patient_id","1002");call.set_field("new_verification_code","4242")
        agent._on_task_complete_handlers["switch_verify"](call)
        with self.assertRaises(AccessDenied):b.subject(call.id)
