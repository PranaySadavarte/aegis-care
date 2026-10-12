"""Render metrics with explicit measured values, source and unavailable states."""
import json,html
from pathlib import Path
root=Path(__file__).resolve().parents[1];d=json.loads((root/"dashboard/metrics-snapshot.json").read_text())
a=d["asr"];h=d["latest_hosted"];g=d["scoped_call_checks"]
fmt=lambda v:"Not measured" if v is None else str(v)
security="; ".join(r["scenario"]+": "+r["status"] for r in d["security"])
pages={
"asr":("Speech recognition",[
("WER",format(a["WER"]*100,".2f")+"%","One synthetic clip. Text normalization only; spoken digit words versus 1001/4242 inflate lexical differences."),
("CER",format(a["CER"]*100,".2f")+"%","Same single-clip reference/hypothesis; not a population accuracy estimate."),
("Target digit strings",str(d["digit_presence"]["found"])+" / 2 present","Presence of 1001 and 4242 in recognized text; not a full entity-extraction benchmark."),
("Audio corpus",str(d["audio_files"])+" labeled WAVs","SAPI synthetic speech, noise/silence variants; no human accent/dialect coverage yet."),
("ASR latency / RTF","Unavailable component timing","End-to-end probe runtime cannot substitute for isolated ASR processing time."),
("Captured TTS output","7.83 seconds, nonzero signal","Native test_audio file capture succeeded; physical speaker audibility remains unverified.")]),
"llm":("Conversation and LLM",[
("Latest recorded hosted suite",str(h["pass"])+" / "+str(h["total"])+" groups passed","Run "+str(h["run_id"])+". Historical failed attempts retained; consult Test runs."),
("Process runtime p50 / p95",fmt(h["p50_process_seconds"])+" / "+fmt(h["p95_process_seconds"])+" s","Total scripted process time. Not speech or LLM component latency."),
("Scoped per-call authorization",str(g["pass"])+" PASS / "+str(g["fail"])+" FAIL / "+str(g["inconclusive"])+" inconclusive","Expert metadata checks only; not full semantic scoring."),
("Native rubric evaluation","Billing rubric passed","Reuse TestSession.evaluate. Broader security rubric outcomes appear under Robustness."),
("Intent accuracy / confidence","Not measured / not exposed","Need labeled intent dataset; native helper does not supply calibrated confidence."),
("BERTScore / ROUGE","Not measured","Require reference-answer dataset and established scoring libraries; safety checks stay separate.")]),
"robustness":("Robustness and recovery",[
("Application regression",str(d["functional"]["passed"])+" / "+str(d["functional"]["total"])+" passed","Deterministic backend, handler, lifecycle and credential checks."),
("Hosted text attacks",security,"Actual latest injection, identity-switch and malformed-input outcomes; NOT_RUN is explicit."),
("Speech fixtures",str(d["audio_files"])+" labeled samples","Original12-file corpus plus6 robustness fixtures;7 additional audio probes executed. See Defect discovery for measured conditions."),
("Human accents / dialects","Not tested","Consented representative recordings still needed."),
("Echo / overlap probes","Repeated credential corruption under delayed echo","Six file-input conditions plus one echo repeat executed. See Defect discovery. Live barge-in and physical AEC remain untested."),
("Playback diagnostic","Captured greeting available","Use the synthetic greeting player below; this avoids WebRTC and microphone capture.")])}
for slug,(title,rows) in pages.items():
    cards="".join("<article><h2>"+html.escape(n)+"</h2><strong>"+html.escape(v)+"</strong><p>"+html.escape(t)+"</p></article>" for n,v,t in rows)
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AEGIS Â· '+title+'</title><style>body{margin:0;background:#edf2f3;color:#19343c;font:16px/1.6 system-ui}header{background:#163d44;color:white;padding:32px 6vw}main{max-width:1050px;margin:auto;padding:24px}nav{display:flex;gap:18px;flex-wrap:wrap}a{color:#137269}header a{color:#bae5d9}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}article{background:white;border:1px solid #dbe4e6;border-radius:14px;padding:22px}h2{font-size:20px}strong{color:#88621e;font-size:21px}p{color:#566d74}audio{max-width:100%}</style></head><body><header><nav><a href="../">Overview</a><a href="../calls.html">Calls</a><a href="../runs.html">Test runs</a><a href="../defects.html">Defect discovery</a><a href="asr.html">ASR</a><a href="llm.html">LLM</a><a href="robustness.html">Robustness</a></nav><h1>'+title+'</h1><span>Actual measurements and explicit coverage limits</span></header><main><section>'+cards+'</section><h2>Local playback check</h2><p>Play the captured synthetic greeting. Hearing this confirms browser output, not microphone input or native helper device selection.</p><audio controls src="../assets/captured-demo-greeting.wav"></audio><p><a href="../../docs/native-metrics-review.md">Native APIs and definitions â†—</a></p></main></body></html>'
    (root/"dashboard/metrics"/(slug+".html")).write_text(page,encoding="utf-8")
