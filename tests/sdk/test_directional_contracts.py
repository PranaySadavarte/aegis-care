"""Use actual SDK methods; no live service or outbound calls."""
from test_offline_contracts import unittest, guava, MockCall
from guava.events import decode_event_dict, OutboundCallFailed
from guava.call import Call
from guava.types.call_info import PSTNCallInfo
from pydantic import ValidationError
import warnings

class DirectionalContracts(unittest.TestCase):
    def test_inbound_event_decode(self):
        event = decode_event_dict({"event_type": "inbound-call",
                                   "caller_number": "+15555555555"})
        self.assertEqual(event.caller_number, "+15555555555")

    def test_outbound_connected_event_decode(self):
        self.assertEqual(decode_event_dict({"event_type": "outbound-call-connected"}).event_type,
                         "outbound-call-connected")

    def test_outbound_failure_event_decode(self):
        event = decode_event_dict({"event_type": "outbound-call-failed",
                                   "error_code": 503, "error_reason": "synthetic-unavailable"})
        self.assertIsInstance(event, OutboundCallFailed)
        self.assertEqual(event.error_code, 503)

    def test_outbound_failure_missing_reason_rejected(self):
        with self.assertRaises(ValidationError):
            decode_event_dict({"event_type": "outbound-call-failed", "error_code": 503})

    def test_unknown_event_warns_and_is_ignored(self):
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            self.assertIsNone(decode_event_dict({"event_type": "synthetic-future-event"}))
        self.assertEqual(len(captured), 1)

    def test_task_serializes_field_sensitive_flag(self):
        call = MockCall()
        call.set_task("synthetic-intake", objective="Collect synthetic identity",
                      checklist=[guava.Field(key="identity", field_type="text", sensitive=True)])
        command = call._command_queue[-1]
        self.assertEqual(command.task_id, "synthetic-intake")
        self.assertTrue(command.action_items[0].sensitive)
        # Serialization flag is not proof of actual hosted redaction.

    def test_outbound_reach_person_uses_sdk_task(self):
        call = MockCall()
        call.reach_person("Synthetic Person", voicemail_hangup=True)
        self.assertGreater(len(call._command_queue), 0)
        self.assertIn("contact_availability", call._field_keys_by_task_id[
            call._command_queue[-1].task_id])

    def test_production_call_state_and_command_isolation(self):
        info = PSTNCallInfo(from_number="+15555555555", to_number="+15555555556")
        a, b = Call("synthetic-a", info), Call("synthetic-b", info)
        a.set_variable("subject", "synthetic-a")
        self.assertIsNone(b.get_variable("subject"))
        self.assertEqual(a._command_queue.qsize(), 1)
        self.assertEqual(b._command_queue.qsize(), 0)

