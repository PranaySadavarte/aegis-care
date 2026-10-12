"""Native local audio diagnostic; bounded, stops only owned process tree."""
import subprocess,json
from pathlib import Path
root=Path(__file__).resolve().parents[2]
p=subprocess.Popen([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),"-u",str(root/"agent/harborcare.py"),"--mode","local"],
                   cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                   creationflags=getattr(subprocess,"CREATE_NEW_PROCESS_GROUP",0))
try:
    out,err=p.communicate(timeout=18);status="EXITED"
except subprocess.TimeoutExpired:
    subprocess.run(["taskkill","/PID",str(p.pid),"/T","/F"],capture_output=True)
    out,err=p.communicate(timeout=5);status="BOUNDED_STOP"
record={"status":status,"exit_code":p.returncode,"stdout":out,"stderr":err,"note":"Runtime alone does not prove audible audio or microphone capture"}
(root/"evidence/2026-10-11/usability-repair/local-audio.json").write_text(json.dumps(record,indent=2))
print(json.dumps({"status":status,"exit_code":p.returncode,"diagnostic_tail":(out+err)[-1800:]}))
