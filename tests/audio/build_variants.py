"""Create reproducible noise/silence variants; no ASR scoring claims."""
import wave,json,array,random,math,hashlib
from pathlib import Path
folder=Path(__file__).resolve().parents[2]/"fixtures/audio"
rows=json.loads((folder/"manifest.json").read_text(encoding="utf-8-sig"))
rows=[r for r in rows if r["path"].startswith("clean/") or r["id"]=="verify-padded"]
new=[]
for row in rows:
    path=folder/row["path"]
    with wave.open(str(path),"rb") as f:
        assert f.getnchannels()==1 and f.getsampwidth()==2 and f.getframerate()==16000
        samples=array.array("h",f.readframes(f.getnframes()))
        row["duration_seconds"]=round(len(samples)/16000,3)
        row["sha256"]=hashlib.sha256(path.read_bytes()).hexdigest()
        row["sample_rate"]=16000
    if row["id"] in ("verify","billing"):
        random.seed(42)
        rms=math.sqrt(sum(x*x for x in samples)/max(1,len(samples)))
        noise_rms=rms/(10**(15/20))
        mixed=array.array("h",(max(-32768,min(32767,round(x+random.gauss(0,noise_rms)))) for x in samples))
        target=folder/"variants"/(row["id"]+"-noise15.wav")
        with wave.open(str(target),"wb") as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000);f.writeframes(mixed.tobytes())
        new.append({**row,"id":row["id"]+"-noise15","path":"variants/"+target.name,"condition":"Gaussian noise, nominal 15 dB SNR","sha256":hashlib.sha256(target.read_bytes()).hexdigest()})
silence=folder/"variants/silence.wav"
with wave.open(str(silence),"wb") as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000);f.writeframes(bytes(16000*2*8))
new.append({"id":"silence","path":"variants/silence.wav","reference_text":"","condition":"8 seconds silence","source":"Generated zero PCM","duration_seconds":8,"sample_rate":16000,"sha256":hashlib.sha256(silence.read_bytes()).hexdigest(),"status":"CREATED_NOT_SCORED"})
(folder/"manifest.json").write_text(json.dumps(rows+new,indent=2),encoding="utf-8")
print(json.dumps({"labeled_files":len(rows+new),"validation":"PCM 16-bit mono 16kHz","human_accents":"Not represented","asr_scores":"Not measured"}))
