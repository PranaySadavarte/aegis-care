import subprocess,json,time,sys,shutil,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[2];folder=root/"evidence/2026-10-11/harborcare"
for flow in (sys.argv[1:] or ["identity","eligibility","claims","billing","appointments","payments"]):
    target=folder/("hosted-"+flow+".json")
    if target.exists():
        archive=folder/"history";archive.mkdir(exist_ok=True)
        shutil.copy2(target,archive/(flow+"-"+uuid.uuid4().hex+".json"))
    started=time.monotonic()
    try:
        proc=subprocess.run([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/integration/harborcare_hosted.py"),flow],
                            cwd=root,capture_output=True,text=True,timeout=50)
        record={"workflow":flow,"exit_code":proc.returncode,"stdout":proc.stdout,"stderr":proc.stderr,"process_seconds":time.monotonic()-started}
    except subprocess.TimeoutExpired:
        record={"workflow":flow,"status":"TIMEOUT","limit_seconds":50}
    (folder/("hosted-"+flow+".json")).write_text(json.dumps(record,indent=2))
    print(json.dumps({k:v for k,v in record.items() if k not in ("stdout","stderr")}),flush=True)


