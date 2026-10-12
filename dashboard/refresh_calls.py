"""Read-only native conversation import. Secrets/transcripts stay in local evidence."""
import subprocess,re,json,hashlib,datetime,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def enrich_lifecycle(calls,events):
    grouped={}
    for event in events:grouped.setdefault(event["call"],[]).append(event)
    for row in calls:
        history=grouped.get(row["call"],[])
        starts=[e for e in history if e["event"]=="started"]
        ends=[e for e in history if e["event"]=="ended"]
        channels=[e.get("channel") for e in history if e.get("channel") not in (None,"unknown")]
        if channels:row["channel"]=channels[-1]
        elif row["evidence"]=="Local sanitized Expert event":row["channel"]="Unclassified local session"
        else:row["channel"]="phone"
        row["duration_source"]="Guava platform"
        if row["duration"]=="Not returned":
            row["duration"]="Duration unavailable";row["duration_source"]="No closing event / platform duration"
            if starts and ends:
                start=datetime.datetime.fromisoformat(starts[0]["at_utc"]);end=datetime.datetime.fromisoformat(ends[-1]["at_utc"])
                seconds=(end-start).total_seconds()
                if seconds>=0:
                    row["duration"]=str(int(seconds)//60)+":"+str(int(seconds)%60).zfill(2)
                    row["duration_seconds"]=round(seconds,3);row["duration_source"]="Expert lifecycle timestamps, not carrier billing"
            if starts:
                row["platform_time"]=starts[0]["at_utc"];row["timezone"]="UTC Expert timestamp"
        if ends and row["outcome"]=="In progress":row["outcome"]="Ended without an Expert result"
        elif not ends and row["outcome"]=="In progress":row["outcome"]="No closing event recorded; status unconfirmed"
    return calls

def refresh_calls():
    config=tomllib.loads((ROOT/"harborcare-agent/guava.toml").read_text())
    cli=Path.home()/"AppData/Local/guava/bin/guava.exe"
    stamp=datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    folder=ROOT/"evidence/2026-10-11/call-history"/stamp
    folder.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run([str(cli),"conversations","list","--direction","inbound","--to",config["phone_number"],"--date-from","2026-10-11","-n","30"],
                        capture_output=True,text=True,timeout=20)
    (folder/"list-raw.txt").write_text(proc.stdout,encoding="utf-8")
    (folder/"stderr-raw.txt").write_text(proc.stderr,encoding="utf-8")
    if proc.returncode: raise RuntimeError("Native conversation retrieval failed; raw evidence saved")
    calls=[]
    for line in proc.stdout.splitlines():
        match=re.search(r"([0-9]+:[0-9]{2}) +([a-f0-9]{16}) *$",line)
        if not match: continue
        duration,identifier=match.groups()
        local=ROOT/"evidence/2026-10-11/call-history"/(identifier+"-transcript.txt")
        transcript=local.read_text(encoding="utf-8-sig") if local.exists() else ""
        denial=bool(re.search(r"verification.*fail|unable to verify|could not verify",transcript,re.I))
        calls.append({"call":"call-"+hashlib.sha256(identifier.encode()).hexdigest()[:10],
                      "platform_time":line.strip()[:16],"timezone":"Not specified by CLI output",
                      "duration":duration,"direction":"inbound","workflow":"Not established",
                      "outcome":"Transcript reports verification denial" if denial else "Outcome not retrieved",
                      "grade":"Unscored — expected scenario not recorded",
                      "evidence":"Native Guava conversation list"+("; locally preserved transcript" if transcript else "")})
    events_path=ROOT/"evidence/2026-10-11/call-history/manual-events.jsonl"
    events=[]
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            try: events.append(json.loads(line))
            except json.JSONDecodeError: continue
    by_call={row["call"]:row for row in calls}
    for event in events:
        row=by_call.get(event["call"])
        if row is None:
            row={"call":event["call"],"platform_time":"Pending platform record","timezone":"UTC event times available","duration":"Not returned","direction":"inbound","workflow":"Not established","outcome":"In progress","grade":"Unscored","evidence":"Local sanitized Expert event"}
            calls.append(row);by_call[event["call"]]=row
        if event["event"]=="finished":
            row["workflow"]=event["detail"]["workflow"]
            row["outcome"]="Expert outcome: "+event["detail"]["result_status"]
            if event.get("evaluation"): row["evaluation"]=event["evaluation"];row["grade"]="Scoped authorization check: "+event["evaluation"]["authorization_gate"]
        if event["event"]=="ended":
            row["termination"]=event["detail"]["termination"]
            if event.get("evaluation"):
                row["evaluation"]=event["evaluation"]
                row["grade"]="Scoped authorization check: "+event["evaluation"]["authorization_gate"]
    calls=enrich_lifecycle(calls,events)
    data={"refreshed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"calls":calls,
          "note":"At most 30 inbound records for the configured number since 2026-10-11. Empty/missing records do not prove no call attempt. No transcripts or phone numbers embedded."}
    (ROOT/"dashboard/calls.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
    (ROOT/"dashboard/calls.js").write_text("window.AEGIS_CALLS = "+json.dumps(data)+";",encoding="utf-8")
    return data
if __name__=="__main__":
    result=refresh_calls()
    print(json.dumps({"retrieved":len(result["calls"]),"refreshed_at_utc":result["refreshed_at_utc"]}))
