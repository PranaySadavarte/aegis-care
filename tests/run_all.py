"""Run fixed suites; no phone calls or deployment. Hosted suites consume live usage."""
import argparse,subprocess,json,re,time,uuid,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
PY=ROOT/"baseline/sdk-0.47.0/.venv/Scripts/python.exe"
def atomic(path,obj):
    temp=path.with_suffix(".tmp");temp.write_text(json.dumps(obj,indent=2),encoding="utf-8");temp.replace(path)
def run(suite):
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:6]
    folder=ROOT/"evidence/2026-10-11/suite-runs"/run_id;folder.mkdir(parents=True)
    state={"run_id":run_id,"suite":suite,"started_at_utc":datetime.now(timezone.utc).isoformat(),"status":"RUNNING","groups":[]}
    atomic(ROOT/"dashboard/run-status.json",state)
    groups=[]
    if suite in ("offline","adversarial","all"):
        groups += [("SDK offline",["-m","unittest","discover","-s","tests/sdk","-p","test_*.py","-v"],30),
                   ("Application functional",["-m","unittest","discover","-s","tests/functional","-p","test_*.py","-v"],30),
                   ("Installer source audit",["@powershell","-NoProfile","-File","tests/sdk/audit_installer.ps1","-InstallerPath","evidence/2026-10-11/installer-audit/install-current.ps1"],30)]
    if suite in ("hosted","all"):
        for flow in ("identity","eligibility","claims","billing","appointments","payments","denied"):
            groups.append(("Hosted "+flow,["tests/integration/harborcare_hosted.py",flow],50))
        groups.append(("Hosted native rubric billing",["tests/integration/harborcare_hosted.py","billing","--rubric"],50))
    if suite in ("security","all"):
        for scenario in ("injection","identity-switch","malformed"):
            groups.append(("Hosted security "+scenario,["tests/integration/security_hosted.py",scenario],60))
    if suite in ("audio","all"):
        groups.append(("Audio file capture",["tests/audio/run_native_capture.py"],40))
        groups.append(("Audio ASR observation",["tests/audio/run_native_asr.py"],50))
    if suite in ("adversarial","all"):
        groups.append(("Sensitive field observations",["tests/integration/run_sensitive_probes.py"],150))
        groups.append(("Product security audit",["tests/security/product_audit.py"],30))
        groups.append(("Hosted defect discovery",["tests/integration/run_defect_discovery.py"],430))
    if suite in ("robustness","all"):
        groups.append(("Audio robustness observations",["tests/audio/run_robustness.py"],300))
    for label,args,limit in groups:
        started=time.monotonic()
        try:
            command=([shutil.which("pwsh") or shutil.which("powershell")]+args[1:]) if args[0]=="@powershell" else [str(PY)]+args
            p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=limit)
            output=p.stdout+p.stderr
            (folder/(label.replace(" ","-")+".txt")).write_text(output,encoding="utf-8")
            match=re.search(r"Ran ([0-9]+) tests?",output)
            failures=re.search(r"failures=([0-9]+)",output);errors=re.search(r"errors=([0-9]+)",output)
            total=int(match.group(1)) if match else (1 if label.startswith("Hosted") else None)
            fail=int(failures.group(1)) if failures else 0;err=int(errors.group(1)) if errors else 0
            result={"group":label,"status":"PASS" if p.returncode==0 else "FAIL","exit_code":p.returncode,
                    "total":total,"failed":fail+err if match else (1 if p.returncode else 0),
                    "duration_seconds":round(time.monotonic()-started,3)}
            if label=="Product security audit" and p.stdout:
                audit=json.loads(p.stdout)
                result["total"]=len(audit["checks"]);result["failed"]=sum(c["status"]=="FAIL" for c in audit["checks"])
            if label=="Installer source audit" and p.returncode==0:
                audit=json.loads(p.stdout)
                result["status"]="OPEN_FINDINGS" if not audit["explicit_hash_verification_command_present"] or not audit["explicit_authenticode_command_present"] else "OBSERVED"
                result["failed"]=None
                result["observations"]={"explicit_hash_check":audit["explicit_hash_verification_command_present"],"explicit_signature_check":audit["explicit_authenticode_command_present"]}
            if (label.startswith("Audio") or label=="Sensitive field observations") and p.returncode==0:
                result["status"]="OBSERVED";result["failed"]=None
        except subprocess.TimeoutExpired:
            result={"group":label,"status":"TIMEOUT","total":None,"failed":None,"limit_seconds":limit}
        state["groups"].append(result);atomic(ROOT/"dashboard/run-status.json",state)
    state["status"]="PASS" if all(g["status"] in ("PASS","OBSERVED") for g in state["groups"]) else "FAIL"
    state["completed_at_utc"]=datetime.now(timezone.utc).isoformat()
    atomic(folder/"summary.json",state);atomic(ROOT/"dashboard/run-status.json",state)
    history_path=ROOT/"dashboard/run-history.json"
    history=json.loads(history_path.read_text()) if history_path.exists() else []
    history.append(state);atomic(history_path,history)
    for builder in ("build_metrics_snapshot.py","build_metrics_pages.py","build_defect_dashboard.py"):
        updated=subprocess.run([str(PY),str(ROOT/"dashboard"/builder)],cwd=ROOT,capture_output=True,text=True,timeout=15)
        (folder/(builder+".txt")).write_text(updated.stdout+updated.stderr,encoding="utf-8")
        if updated.returncode:print("Metric refresh failed; previous snapshot retained. See local builder evidence.")
    print(json.dumps(state));return 0 if state["status"]=="PASS" else 1
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--suite",choices=["offline","hosted","security","audio","adversarial","robustness","all"],default="offline")
    raise SystemExit(run(parser.parse_args().suite))
