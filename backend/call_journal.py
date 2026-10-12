"""Append-only sanitized manual call outcomes; no credentials, numbers or transcript."""
import json,hashlib
from datetime import datetime,timezone
from threading import Lock
class CallJournal:
    def __init__(self,path):self.path=path;self.lock=Lock()
    def __call__(self,call,event,detail=None):
        row={"call":"call-"+hashlib.sha256(call.id.encode()).hexdigest()[:10],
             "at_utc":datetime.now(timezone.utc).isoformat(),"event":event,"detail":detail}
        with self.lock:
            self.path.parent.mkdir(parents=True,exist_ok=True)
            with self.path.open("a",encoding="utf-8") as out:out.write(json.dumps(row)+"\n")

