import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"dashboard"))
from refresh_calls import enrich_lifecycle
class CallLabels(unittest.TestCase):
    def row(self):return {"call":"masked","duration":"Not returned","platform_time":"Pending","timezone":"unknown","outcome":"In progress","evidence":"Local sanitized Expert event"}
    def test_completed_duration_uses_events(self):
        events=[{"call":"masked","event":"started","at_utc":"2026-10-12T01:00:00+00:00","channel":"local"},{"call":"masked","event":"ended","at_utc":"2026-10-12T01:00:42+00:00","channel":"local"}]
        row=enrich_lifecycle([self.row()],events)[0]
        self.assertEqual(row["duration"],"0:42")
        self.assertEqual(row["channel"],"local")
        self.assertEqual(row["outcome"],"Ended without an Expert result")
    def test_no_completion_is_not_claimed_active(self):
        row=enrich_lifecycle([self.row()],[])[0]
        self.assertEqual(row["duration"],"Duration unavailable")
        self.assertIn("status unconfirmed",row["outcome"])
