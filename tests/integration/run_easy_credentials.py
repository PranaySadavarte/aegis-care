import json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[2]
try:
 p=subprocess.run([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/integration/easy_credentials_hosted.py")],capture_output=True,text=True,cwd=root,timeout=50)
 r={"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
except subprocess.TimeoutExpired:r={"status":"TIMEOUT","limit_seconds":50}
(root/"evidence/2026-10-11/spoken-verification/hosted-easy.json").write_text(json.dumps(r,indent=2))
print(json.dumps({k:v for k,v in r.items() if k not in ("stdout","stderr")}))
