import subprocess,json,uuid,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
folder=root/"evidence/2026-10-11/usability-repair"/("security-"+uuid.uuid4().hex[:8]);folder.mkdir()
for scenario in (sys.argv[1:] or ("injection","identity-switch","malformed")):
    p=subprocess.Popen([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/integration/security_hosted.py"),scenario],
                       cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,creationflags=getattr(subprocess,"CREATE_NEW_PROCESS_GROUP",0))
    try:out,err=p.communicate(timeout=60);status="PASS" if p.returncode==0 else "FAIL"
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill","/PID",str(p.pid),"/T","/F"],capture_output=True)
        out,err=p.communicate(timeout=5);status="TIMEOUT"
    record={"scenario":scenario,"status":status,"exit_code":p.returncode,"stdout":out,"stderr":err}
    (folder/(scenario+".json")).write_text(json.dumps(record,indent=2))
    print(json.dumps({"scenario":scenario,"status":status,"evidence_folder":folder.name}),flush=True)

