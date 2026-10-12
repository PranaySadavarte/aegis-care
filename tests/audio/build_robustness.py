import json,hashlib
from pathlib import Path
import numpy as np
import soundfile as sf
root=Path(__file__).resolve().parents[2];folder=root/'fixtures/audio/robustness';folder.mkdir(exist_ok=True)
voice,sr=sf.read(root/'fixtures/audio/clean/verify.wav',dtype='float64');assert sr==16000
reference='My patient ID is one zero zero one. My verification code is four two four two.'
rows=[]
def save(id,x,condition,**extra):
 peak=float(np.max(np.abs(x)));gain=min(1,0.98/max(peak,1e-12));x=x*gain
 padded=np.concatenate([np.zeros(sr*8),x,np.zeros(sr*3)])
 path=folder/(id+'.wav');sf.write(path,padded,sr,subtype='PCM_16')
 rows.append(dict(id=id,path=path.relative_to(root).as_posix(),reference_text=reference,condition=condition,seed=47,sample_rate=sr,duration_seconds=len(padded)/sr,global_gain=gain,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**extra))
save('clean-control',voice,'Clean paired control')
rng=np.random.default_rng(47);noise=rng.normal(size=len(voice));power=np.mean(voice**2)
for snr in (20,10,0):
 n=noise*np.sqrt(power/(np.mean(noise**2)*10**(snr/10)))
 save('noise-'+str(snr)+'db',voice+n,'Additive Gaussian noise',measured_prequantization_snr_db=float(10*np.log10(power/np.mean(n*n))))
delay=int(sr*.18);echo=np.pad(voice,(delay,0))[:len(voice)]*.65
save('delayed-echo',voice+echo,'Caller delayed copy, 180 ms, gain 0.65; reverberation proxy, not speaker AEC test')
greet,gsr=sf.read(root/'dashboard/assets/captured-demo-greeting.wav');greet=np.interp(np.arange(int(len(greet)*sr/gsr))/sr,np.arange(len(greet))/gsr,greet)
echo=np.zeros(len(voice));take=min(len(echo),len(greet));echo[:take]=greet[:take]
save('agent-speech-overlap',voice+.6*echo,'Recorded agent greeting mixed with caller at gain0.6; single-channel contamination, not live barge-in')
(folder/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps({'created':len(rows),'snr_db':[20,10,0],'limitations':'No human accents, real acoustic AEC or live interruptions measured'}))
