import pathlib,html
root=pathlib.Path(__file__).resolve().parents[1]
pages={
"asr":("Speech recognition",[
("WER / CER","Not measured","Reference and recognized transcripts; fixed normalization; use established scoring library."),
("ASR latency","Not measured","Audio endpoint to final transcript; validate available event timestamps."),
("ASR RTF","Unavailable in reviewed public API","Isolated ASR processing time / audio duration. Whole call duration is not ASR RTF."),
("Critical entity accuracy","Not measured","Patient ID, code, dates and amounts compared with synthetic references.")]),
"llm":("Conversation and LLM",[
("Intent accuracy","Not measured","Correct routed intents / labeled trials; six successful workflow checks alone do not establish general intent accuracy."),
("Confidence score","Not exposed in reviewed API","Do not fabricate model confidence or use rubric pass as a calibrated score."),
("Failure / fallback rate","Not measured","Define terminal failure/fallback events, denominator and attribution before running trials."),
("Latency distribution","Not measured","Use defined event boundaries and p50/p95/p99; retain sample size and conditions."),
("BERTScore / ROUGE","Planned; names provisional","Use established libraries with references; does not replace safety/groundedness checks."),
("Native semantic evaluation","Available; not used for HarborCare yet","Reuse TestSession.evaluate and roleplay; retain criteria, result and human review.")]),
"robustness":("Robustness and recovery",[
("Malformed inputs","Partial offline coverage","Variable serialization, event decoder and backend validation; more fuzz/fault cases needed."),
("Accents / dialects / noise","Not tested","Consented prerecorded synthetic speech; label subgroup and conditions without generalizing from small samples."),
("Interruptions / overlap / echoes","Not tested","Native test_audio and live transport tests; measure barge-in delay and workflow integrity."),
("Disconnect / timeout recovery","Not tested","Bounded process timeout is not demonstrated reconnect recovery."),
("Identity switch / payment duplicates","Partial backend coverage","Synthetic backend tests passed; live adversarial conversation pending.")])}
for slug,(title,rows) in pages.items():
    cards=''.join('<article><h2>'+html.escape(name)+'</h2><strong>'+html.escape(status)+'</strong><p>'+html.escape(detail)+'</p></article>' for name,status,detail in rows)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AEGIS · '''+title+'''</title><style>body{margin:0;background:#edf2f3;color:#19343c;font:16px/1.6 system-ui}header{background:#163d44;color:white;padding:32px 6vw}main{max-width:1050px;margin:auto;padding:24px}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:#137269}header a{color:#bae5d9}section{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:18px}article{background:white;border:1px solid #dbe4e6;border-radius:14px;padding:22px}h2{font-size:20px}strong{color:#88621e}p{color:#566d74}h1{letter-spacing:-.03em}</style><header><nav><a href="../">Overview</a><a href="asr.html">ASR</a><a href="llm.html">LLM</a><a href="robustness.html">Robustness</a></nav><h1>'''+title+'''</h1><span>Measurement readiness · no invented scores</span></header><main><p>Stage-specific evaluation. Native SDK functions are reused for sessions, rubric checks and audio capture; external numeric metrics remain planned.</p><section>'''+cards+'''</section><p><a href="../../docs/native-metrics-review.md">Native API review and metric definitions ↗</a></p></main></html>'''
    (root/'dashboard/metrics'/f'{slug}.html').write_text(page,encoding='utf-8')
