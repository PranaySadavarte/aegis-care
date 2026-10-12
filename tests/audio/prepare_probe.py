import wave,json,array
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with wave.open(str(root/"fixtures/audio/clean/verify.wav"),"rb") as f:data=f.readframes(f.getnframes())
target=root/"fixtures/audio/variants/verify-padded.wav"
with wave.open(str(target),"wb") as f:
    f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000)
    f.writeframes(bytes(16000*2*8)+data+bytes(16000*2*3))
with wave.open(str(root/"evidence/2026-10-11/usability-repair/captured-agent.wav"),"rb") as f:
    samples=array.array("h",f.readframes(f.getnframes()))
print(json.dumps({"captured_output_nonzero":any(samples),"peak_sample":max(map(abs,samples),default=0)}))
