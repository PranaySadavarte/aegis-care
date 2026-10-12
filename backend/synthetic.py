"""Synthetic-only in-memory healthcare backend. Not production authentication."""
from threading import RLock
from copy import deepcopy
import re
def canonical(value):
    if not isinstance(value,str) or not re.fullmatch(r"[A-Za-z0-9\s-]+",value): return ""
    words={"zero":"0","one":"1","two":"2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9"}
    parts=value.lower().split()
    if parts and all(part in words or part.isdigit() for part in parts):
        return "".join(words.get(part,part) for part in parts)
    return re.sub(r"[\s-]","",value).upper()

class AccessDenied(Exception): pass
class Conflict(Exception): pass
class SyntheticBackend:
    def __init__(self):
        self.lock=RLock()
        self.patients={
            "HC-1001":{"spoken_code":"4242","code":"DEMO-42","eligibility":{"plan":"Synthetic Bronze","active":True,"copay":25},
                       "claims":[{"id":"CL-DEMO-1","status":"pending","amount_cents":4000}],
                       "balance_cents":5000},
            "HC-1002":{"spoken_code":"9999","code":"DEMO-99","eligibility":{"plan":"Synthetic Silver","active":False,"copay":None},
                       "claims":[],"balance_cents":2500}}
        self.authorized={}
        self.slots=["2026-10-15 09:00","2026-10-15 14:00"]
        self.bookings={}
        self.transactions={}
    def verify(self, session, patient_id, code):
        with self.lock:
            self.authorized.pop(session,None)
            normalized_id=canonical(patient_id)
            patient_id=next((key for key in self.patients
                             if normalized_id in (canonical(key),key.split("-")[1])),None)
            record=self.patients.get(patient_id)
            if record and canonical(code) in (canonical(record["code"]),record["spoken_code"]):
                self.authorized[session]=patient_id
                return True
            return False
    def subject(self, session):
        patient=self.authorized.get(session)
        if not patient: raise AccessDenied("Synthetic verification required")
        return patient
    def read(self, session, workflow):
        with self.lock:
            patient=self.subject(session)
            row=self.patients[patient]
            if workflow=="eligibility": return deepcopy(row["eligibility"])
            if workflow=="claims": return deepcopy(row["claims"])
            if workflow=="billing": return {"balance_cents":row["balance_cents"],"currency":"USD"}
            if workflow=="appointments":
                return {"available":list(self.slots),"booked":[slot for slot,owner in self.bookings.items() if owner==patient]}
            raise ValueError("Unsupported workflow")
    def book(self, session, slot):
        with self.lock:
            patient=self.subject(session)
            if slot in self.bookings:
                if self.bookings[slot]==patient: return {"slot":slot,"status":"already_booked"}
                raise Conflict("Synthetic slot unavailable")
            if slot not in self.slots: raise ValueError("Unsupported slot")
            self.bookings[slot]=patient
            self.slots.remove(slot)
            return {"slot":slot,"status":"booked"}
    def pay(self, session, amount_cents, token, consent, key):
        with self.lock:
            patient=self.subject(session)
            if type(amount_cents) is not int or amount_cents<=0: raise ValueError("Invalid amount")
            if token!="SIMULATED-TOKEN" or consent is not True: raise ValueError("Simulation consent/token required")
            request=(patient,amount_cents,token)
            if key in self.transactions:
                previous,saved=self.transactions[key]
                if previous!=request: raise Conflict("Idempotency key reused with different request")
                return deepcopy(saved)
            if amount_cents>self.patients[patient]["balance_cents"]: raise ValueError("Amount exceeds synthetic balance")
            self.patients[patient]["balance_cents"]-=amount_cents
            result={"status":"simulated_only","amount_cents":amount_cents,"remaining_cents":self.patients[patient]["balance_cents"]}
            self.transactions[key]=(request,result)
            return deepcopy(result)
    def close(self, session):
        with self.lock: self.authorized.pop(session,None)


