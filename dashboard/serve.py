from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from threading import Lock
from pathlib import Path
import json
from refresh_calls import refresh_calls
root=Path(__file__).resolve().parents[1]
lock=Lock()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(root),**kwargs)
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


