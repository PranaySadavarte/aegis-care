import sys,json,wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from agent.harborcare import create_agent
root=Path(__file__).resolve().parents[2];agent,_=create_agent()
agent.test_audio(root/"fixtures/audio/variants/silence.wav",root/"evidence/2026-10-11/usability-repair/captured-agent.wav")
path=root/"evidence/2026-10-11/usability-repair/captured-agent.wav"
with wave.open(str(path),"rb") as f:
    result={"sample_rate":f.getframerate(),"frames":f.getnframes(),"duration_seconds":f.getnframes()/f.getframerate(),"channels":f.getnchannels(),"sample_width":f.getsampwidth()}
print(json.dumps(result))
