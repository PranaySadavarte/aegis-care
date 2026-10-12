import subprocess,json,shutil,uuid
from pathlib import Path
root=Path(__file__).resolve().parents[2]
archive_root=root/"evidence/2026-10-11/usability-repair"
previous_files=['native-asr-process.json', 'asr-baseline.json', 'verify-agent.wav']
existing=[archive_root/name for name in previous_files if (archive_root/name).exists()]
if existing:
    archive=archive_root/("previous-audio-"+uuid.uuid4().hex[:8]);archive.mkdir()
    for previous in existing:shutil.copy2(previous,archive/previous.name)
p=subprocess.Popen([str(root/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"),str(root/"tests/audio/native_asr.py")],
                   cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                   creationflags=getattr(subprocess,"CREATE_NEW_PROCESS_GROUP",0))
try:out,err=p.communicate(timeout=40);status="EXITED"
except subprocess.TimeoutExpired:
    subprocess.run(["taskkill","/PID",str(p.pid),"/T","/F"],capture_output=True)
    out,err=p.communicate(timeout=5);status="TIMEOUT"
data={"status":status,"exit_code":p.returncode,"stdout":out,"stderr":err}
(root/"evidence/2026-10-11/usability-repair/native-asr-process.json").write_text(json.dumps(data,indent=2))
print(json.dumps(data))

raise SystemExit(0 if data["status"]=="EXITED" and data["exit_code"]==0 else 1)

