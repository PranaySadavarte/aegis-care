import json,re,math,wave,hashlib
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[1]
asr=json.loads((root/"evidence/2026-10-11/usability-repair/asr-baseline.json").read_text())
manifest=json.loads((root/"fixtures/audio/manifest.json").read_text())
padded=root/"fixtures/audio/variants/verify-padded.wav"
if not any(r["id"]=="verify-padded" for r in manifest):
    with wave.open(str(padded),"rb") as f:duration=f.getnframes()/f.getframerate()
    manifest.append({"id":"verify-padded","path":"variants/verify-padded.wav","reference_text":manifest[0]["reference_text"],
        "source":"Derived SAPI fixture","condition":"8 seconds leading silence and 3 trailing","duration_seconds":duration,
        "sample_rate":16000,"sha256":hashlib.sha256(padded.read_bytes()).hexdigest(),"status":"SINGLE_BASELINE_SCORED"})
    (root/"fixtures/audio/manifest.json").write_text(json.dumps(manifest,indent=2))
history=json.loads((root/"dashboard/run-history.json").read_text()) if (root/"dashboard/run-history.json").exists() else []
hosted=[r for r in history if r["suite"] in ("hosted","all")]
last=hosted[-1] if hosted else {}
groups=[g for g in last.get("groups",[]) if g["group"].startswith("Hosted") and not g["group"].startswith("Hosted security") and g["group"]!="Hosted defect discovery"]
durations=sorted(g["duration_seconds"] for g in groups if "duration_seconds" in g)
percentile=lambda p:round(durations[max(0,math.ceil(p*len(durations))-1)],3) if durations else None
calls=json.loads((root/"dashboard/calls.json").read_text())
gates=[c["evaluation"]["authorization_gate"] for c in calls["calls"] if c.get("evaluation")]
security_dirs=list((root/"evidence/2026-10-11/usability-repair").glob("security-*"))
security=[]
for name in ("injection","identity-switch","malformed"):
    paths=[folder/(name+".json") for folder in security_dirs if (folder/(name+".json")).exists()]
    path=max(paths,key=lambda p:p.stat().st_mtime) if paths else None
    security.append({"scenario":name,"status":json.loads(path.read_text())["status"] if path else "NOT_RUN"})
# Select the newest executed security group or standalone artifact by observation time.
for item in security:
    artifacts=[folder/(item["scenario"]+".json") for folder in security_dirs if (folder/(item["scenario"]+".json")).exists()]
    observed=max((p.stat().st_mtime for p in artifacts),default=0)
    for run in history:
        if not run.get("completed_at_utc"):continue
        stamp=datetime.fromisoformat(run["completed_at_utc"]).timestamp()
        for group in run.get("groups",[]):
            if group["group"]=="Hosted security "+item["scenario"] and stamp>observed:
                item["status"]=group["status"];observed=stamp
functional={"passed":26,"total":26,"source":"final-functional.txt"}
for run in reversed(history):
    group=next((g for g in run.get("groups",[]) if g["group"]=="Application functional"),None)
    if group:
        functional={"passed":group["total"]-group["failed"] if group.get("total") is not None and group.get("failed") is not None else None,
                    "total":group.get("total"),"source":run["run_id"],"status":group["status"]};break
sdk={"total":16,"passed":15,"failed":1,"scope":"Initial baseline"}
for run in reversed(history):
    group=next((g for g in run.get("groups",[]) if g["group"]=="SDK offline"),None)
    if group and group.get("total") is not None:
        sdk={"total":group["total"],"passed":group["total"]-group["failed"],"failed":group["failed"],"source":run["run_id"]};break
data={"generated_at_utc":datetime.now(timezone.utc).isoformat(),"asr":asr,"audio_files":(len(json.loads((root/"fixtures/audio/challenges/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/challenges/manifest.json").exists() else 0)+(len(json.loads((root/"fixtures/audio/public/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/public/manifest.json").exists() else 0)+len(manifest)+len(json.loads((root/"fixtures/audio/robustness/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/robustness/manifest.json").exists() else len(manifest),
      "sdk":sdk,
      "challenge_audio_files":len(json.loads((root/"fixtures/audio/challenges/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/challenges/manifest.json").exists() else 0,
      "public_audio_files":len(json.loads((root/"fixtures/audio/public/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/public/manifest.json").exists() else 0,
      "functional":functional,
      "latest_hosted":{"pass":sum(g["status"]=="PASS" for g in groups),"total":len(groups),"run_id":last.get("run_id"),
                       "p50_process_seconds":percentile(.5),"p95_process_seconds":percentile(.95)},
      "scoped_call_checks":{"pass":gates.count("PASS"),"fail":gates.count("FAIL"),"inconclusive":gates.count("INCONCLUSIVE"),"total":len(gates)},
      "security":security,"digit_presence":{"found":sum(x in asr.get("hypothesis","") for x in ("1001","4242")),"total":2},
      "notes":["One synthetic ASR clip; no human accent/dialect generalization.",
               "WER/CER compare text without numeral equivalence; spoken digit words versus numeric transcription affect scores.",
               "Process p50/p95 are total scripted test runtimes, not speech response latency."]}
(root/"dashboard/metrics-snapshot.json").write_text(json.dumps(data,indent=2))
print(json.dumps({"WER":asr.get("WER"),"CER":asr.get("CER"),"audio_files":(len(json.loads((root/"fixtures/audio/challenges/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/challenges/manifest.json").exists() else 0)+(len(json.loads((root/"fixtures/audio/public/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/public/manifest.json").exists() else 0)+len(manifest)+len(json.loads((root/"fixtures/audio/robustness/manifest.json").read_text(encoding="utf-8"))) if (root/"fixtures/audio/robustness/manifest.json").exists() else len(manifest),"security":security}))

