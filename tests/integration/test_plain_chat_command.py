import subprocess,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
try:
    p=subprocess.run([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),"-u",str(root/"agent/harborcare.py"),"--mode","text"],
                     cwd=root,input=chr(10).join(["My patient ID is 1001 and my code is 4242.","billing",""]),
                     capture_output=True,text=True,timeout=50)
    data={"exit_code":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
except subprocess.TimeoutExpired:data={"status":"TIMEOUT","limit_seconds":50}
(root/"evidence/2026-10-11/usability-repair/plain-chat.json").write_text(json.dumps(data,indent=2))
print(json.dumps({k:v for k,v in data.items() if k not in ("stdout","stderr")}))
