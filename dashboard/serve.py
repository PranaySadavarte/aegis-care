from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Lock
from pathlib import Path
import json,subprocess
from refresh_calls import refresh_calls
root=Path(__file__).resolve().parents[1]
lock=Lock()
active_run=None
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
    def end_headers(self):
        self.send_header("Cache-Control","no-store")
        super().end_headers()
    def do_POST(self):
        global active_run
        allowed_hosts=("127.0.0.1:8765","localhost:8765")
        origin=self.headers.get("Origin")
        if self.path!="/api/tests/start" or self.headers.get("Host") not in allowed_hosts or origin not in (None,"http://127.0.0.1:8765","http://localhost:8765"):
            self.send_error(403);return
        try:
            length=int(self.headers.get("Content-Length","0"))
            if length<1 or length>1024: raise ValueError()
            request=json.loads(self.rfile.read(length))
            suite=request.get("suite")
            if suite not in ("offline","hosted","security","audio","adversarial","robustness","kpi","all"):raise ValueError()
            with lock:
                state_path=root/"dashboard/run-status.json"
                state=json.loads(state_path.read_text()) if state_path.exists() else {}
                if (active_run and active_run.poll() is None) or state.get("status")=="RUNNING":
                    body=json.dumps({"error":"A suite is already running"}).encode();code=409
                else:
                    active_run=subprocess.Popen([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/run_all.py"),"--suite",suite],
                                                cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                                                creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
                    body=json.dumps({"started":True,"suite":suite}).encode();code=202
            self.send_response(code);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(body)
        except (ValueError,json.JSONDecodeError):
            self.send_error(400,"Invalid fixed suite request")
    def do_GET(self):
        if self.path=="/api/calls/refresh":
            try:
                with lock:data=refresh_calls()
                body=json.dumps(data).encode()
                self.send_response(200)
            except Exception:
                body=json.dumps({"error":"Call refresh failed; retained previous snapshot. Check local evidence."}).encode()
                self.send_response(503)
            self.send_header("Content-Type","application/json");self.send_header("Cache-Control","no-store")
            self.end_headers();self.wfile.write(body)
        else:
            candidate=Path(self.translate_path(self.path)).resolve()
            if not any(candidate.is_relative_to(root/area) for area in ("dashboard","reports","docs")):
                self.send_error(403,"Only dashboard and sanitized reports are served")
                return
            super().do_GET()
if __name__=="__main__":
    print("Dashboard on http://127.0.0.1:8765/dashboard/",flush=True)
    ThreadingHTTPServer(("127.0.0.1",8765),Handler).serve_forever()
