import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from backend.synthetic import SyntheticBackend, AccessDenied, Conflict
class HealthcareContracts(unittest.TestCase):
    def setUp(self): self.b=SyntheticBackend()
    def test_all_reads_deny_unverified(self):
        for flow in ["eligibility","claims","billing","appointments"]:
            with self.subTest(flow=flow),self.assertRaises(AccessDenied): self.b.read("session",flow)
    def test_verification_and_read_workflows(self):
        self.assertTrue(self.b.verify("s","HC-1001","DEMO-42"))
        self.assertTrue(self.b.read("s","eligibility")["active"])
        self.assertEqual(self.b.read("s","claims")[0]["status"],"pending")
        self.assertEqual(self.b.read("s","billing")["balance_cents"],5000)
    def test_identity_switch_invalidates(self):
        self.b.verify("s","HC-1001","DEMO-42")
        self.assertFalse(self.b.verify("s","HC-1002","wrong"))
        with self.assertRaises(AccessDenied): self.b.read("s","billing")
    def test_booking_and_conflict(self):
        self.b.verify("a","HC-1001","DEMO-42");self.b.verify("b","HC-1002","DEMO-99")
        slot=self.b.slots[0]
        self.assertEqual(self.b.book("a",slot)["status"],"booked")
        self.assertEqual(self.b.book("a",slot)["status"],"already_booked")
        with self.assertRaises(Conflict): self.b.book("b",slot)
    def test_simulated_payment_idempotency(self):
        self.b.verify("s","HC-1001","DEMO-42")
        a=self.b.pay("s",1000,"SIMULATED-TOKEN",True,"k")
        self.assertEqual(a,self.b.pay("s",1000,"SIMULATED-TOKEN",True,"k"))
        self.assertEqual(self.b.read("s","billing")["balance_cents"],4000)
        with self.assertRaises(Conflict):self.b.pay("s",2000,"SIMULATED-TOKEN",True,"k")
    def test_payment_requires_auth_and_consent(self):
        with self.assertRaises(AccessDenied):self.b.pay("s",1000,"SIMULATED-TOKEN",True,"k")
        self.b.verify("s","HC-1001","DEMO-42")
        for amount,consent in [(-1,True),(6000,True),(1000,False),(True,True)]:
            with self.subTest(amount=amount,consent=consent),self.assertRaises(ValueError):
                self.b.pay("s",amount,"SIMULATED-TOKEN",consent,"k")
        self.assertEqual(self.b.read("s","billing")["balance_cents"],5000)
    def test_session_cleanup(self):
        self.b.verify("s","HC-1001","DEMO-42");self.b.close("s")
        with self.assertRaises(AccessDenied):self.b.subject("s")
if __name__=="__main__":unittest.main(verbosity=2)
