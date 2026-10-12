import json,unittest,tempfile
from pathlib import Path
from types import SimpleNamespace
from backend.call_journal import CallJournal
class CallObservationJournal(unittest.TestCase):
    def test_result_is_evaluated_without_raw_identifier(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"events.jsonl";journal=CallJournal(path);call=SimpleNamespace(id="private-session-marker")
            journal(call,"finished",{"workflow":"billing","result_status":"returned","verified":True})
            row=json.loads(path.read_text())
            self.assertEqual(row["evaluation"]["authorization_gate"],"PASS")
            self.assertNotIn("private-session-marker",path.read_text())
    def test_ended_without_result_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"events.jsonl";journal=CallJournal(path);call=SimpleNamespace(id="private-session-marker")
            journal(call,"ended",{"termination":"caller-hangup"})
            self.assertEqual(json.loads(path.read_text())["evaluation"]["authorization_gate"],"INCONCLUSIVE")
