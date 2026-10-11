"""Version-specific offline SDK contracts. No real credentials or hosted calls."""
import os
import socket
import unittest
from unittest.mock import patch
from importlib.metadata import version

os.environ["GUAVA_API_KEY"] = "synthetic-aegis-key"
os.environ["GUAVA_BASE_URL"] = "https://offline.invalid/"
def no_network(*args, **kwargs):
    raise RuntimeError("Offline harness blocked network access")
socket.socket.connect = no_network
socket.create_connection = no_network

import httpx
import guava
from guava.testing import MockCall
from guava.auth import APIKeyAuth
from guava.utils import check_response
from guava.telemetry import telemetry_client

# Background telemetry remains disabled for these contract tests.
telemetry_client.send_event = lambda *args, **kwargs: None

class SDKContracts(unittest.TestCase):
    def test_exact_version(self):
        self.assertEqual(version("guava-sdk"), "0.47.0")

    def test_field_and_variable_isolation(self):
        a, b = MockCall("synthetic-a"), MockCall("synthetic-b")
        a.set_field("patient", "synthetic-patient-a")
        a.set_variable("verified", True)
        self.assertIsNone(b.get_field("patient"))
        self.assertIsNone(b.get_variable("verified"))
        self.assertEqual(a.get_field("patient"), "synthetic-patient-a")

    def test_non_json_variable_rejected_without_mutation(self):
        call = MockCall()
        with self.assertRaises(ValueError):
            call.set_variable("unsafe", object())
        self.assertIsNone(call.get_variable("unsafe"))
        self.assertEqual(len(call._command_queue), 0)

    def test_command_queues_isolated(self):
        a, b = MockCall(), MockCall()
        a.hangup()
        self.assertEqual(len(a._command_queue), 1)
        self.assertEqual(len(b._command_queue), 0)

    def test_patch_does_not_replace_original_handler(self):
        with patch("guava.agent.Client"):
            agent = guava.Agent(purpose="Offline SDK evaluation")
        @agent.on_action("synthetic")
        def original(call):
            call.set_variable("result", "original")
        cloned = agent.patch()
        @cloned.on_action("synthetic")
        def replacement(call):
            call.set_variable("result", "replacement")
        a, b = MockCall(), MockCall()
        agent._on_action_handlers["synthetic"](a)
        cloned._on_action_handlers["synthetic"](b)
        self.assertEqual(a.get_variable("result"), "original")
        self.assertEqual(b.get_variable("result"), "replacement")

    def test_api_key_repr_does_not_expose_dummy_secret(self):
        auth = APIKeyAuth("synthetic-secret-marker")
        self.assertNotIn("synthetic-secret-marker", repr(auth))
        self.assertEqual(auth.get_headers()["Authorization"], "Bearer synthetic-secret-marker")

    def test_success_response_preserved(self):
        response = httpx.Response(200, request=httpx.Request("GET", "https://offline.invalid/"))
        self.assertIs(check_response(response), response)

    def test_http_error_does_not_expose_sensitive_body(self):
        response = httpx.Response(401, text="synthetic-sensitive-marker",
                                  request=httpx.Request("GET", "https://offline.invalid/"))
        with self.assertRaises(httpx.HTTPStatusError) as raised:
            check_response(response)
        self.assertNotIn("synthetic-sensitive-marker", str(raised.exception))

if __name__ == "__main__":
    unittest.main(verbosity=2)
