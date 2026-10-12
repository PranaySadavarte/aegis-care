const d=window.AEGIS_DATA;
const el=id=>document.getElementById(id);
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
el("passed").textContent=d.checks.filter(c=>c.status==="ok").length+" / "+d.checks.length;
el("duration").textContent=d.hosted_seconds.toFixed(3)+" s";
el("checks").innerHTML=d.checks.map(c=>'<tr><td>'+esc(c.name)+'</td><td><span class="badge '+(c.status==="ok"?"pass":"fail")+'">'+(c.status==="ok"?"PASS":"FAIL")+'</span></td></tr>').join("");
el("pending").innerHTML=["Inbound establishment","Outbound connection","Aggregate field accuracy","Speech latency p50 / p95","Barge-in delay","Recovery / duplicate actions","Unauthorized action rate","RAG groundedness","Billed usage"].map(k=>'<div class="metric"><span>'+k+'</span><span class="muted">Not measured</span></div>').join("");
el("stage").innerHTML += [...new Set(d.cases.map(c=>c.PipelineStage))].map(s=>'<option value="'+esc(s)+'">'+esc(s)+'</option>').join("");
el("harborcare").innerHTML = (d.harborcare_runs||[]).map(r=>'<div class="metric"><span>'+esc(r.workflow)+'</span><span class="badge '+(r.status==="PASS"?"pass":"fail")+'">'+esc(r.status)+'</span></div>').join("") || "Hosted application runs pending";
function render(){const q=el("search").value.toLowerCase(),s=el("status").value;const rows=d.cases.filter(c=>(!s||c.Status===s)&&(!el("stage").value||c.PipelineStage===el("stage").value)&&(!el("inventory").value||c.SourceType===el("inventory").value)&&JSON.stringify(c).toLowerCase().includes(q));el("count").textContent=rows.length+" / "+d.cases.length+" cases";el("cases").innerHTML=rows.map(c=>'<tr><td>'+esc(c.ID)+'</td><td>'+esc(c.PipelineStage)+'<br><small class="muted">'+esc(c.Direction)+'</small></td><td>'+esc(c.Threat_or_behavior)+'</td><td><span class="badge '+(c.Status==="PARTIAL_FAIL"?"fail":c.Status==="PARTIAL"?"warn":"")+'">'+esc(c.Status)+'</span></td><td>'+esc(c.Expected)+'</td><td>'+esc(c.SourcePath||c.Evidence||'')+'<details><summary>Run command</summary><pre>'+esc(c.RunCommand||'See Test runs and runbook')+'</pre></details></td></tr>').join("");}
el("stage").addEventListener("change",render);el("search").addEventListener("input",render);el("status").addEventListener("change",render);render();
el("export").addEventListener("click",()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(d,null,2)],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download="aegis-results-"+d.updated+".json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});


fetch("calls.json",{cache:"no-store"}).then(r=>r.json()).then(s=>{d.manual_calls=s;if(el("call-count"))el("call-count").textContent=s.calls.length;}).catch(()=>{if(el("call-count"))el("call-count").textContent="See Calls";});

fetch("metrics-snapshot.json",{cache:"no-store"}).then(r=>r.json()).then(m=>{
if (el("functional-summary")) el("functional-summary").textContent = m.functional.passed + "/" + m.functional.total + " application regression methods passed. Separate defect-discovery failures are shown on their own page.";
const rows=[["Application tests",m.functional.passed+"/"+m.functional.total],
["ASR WER (one synthetic clip)",(m.asr.WER*100).toFixed(2)+"%"],
["ASR CER (same clip)",(m.asr.CER*100).toFixed(2)+"%"],
["Labeled audio corpus",m.audio_files+" files"],
["Latest hosted suite",m.latest_hosted.pass+"/"+m.latest_hosted.total],
["Speech latency / barge-in","Not measured"],
["ASR RTF / model confidence","Not exposed by reviewed API"],
["Billed usage / real accent coverage","Not measured"]];
el("pending").innerHTML=rows.map(([k,v])=>'<div class="metric"><span>'+esc(k)+'</span><strong>'+esc(v)+'</strong></div>').join("");
}).catch(()=>{el("pending").textContent="Metric snapshot unavailable; no values inferred.";});
window.addEventListener("error",e=>{const note=document.createElement("p");note.textContent="Display error: "+e.message+" — reload this page.";document.querySelector("main").prepend(note);});

fetch("test-inventory.json",{cache:"no-store"}).then(r=>r.json()).then(i=>{
 d.cases=i.rows;
 for(const [id,key,label] of [["inventory","SourceType","All inventories"],["stage","PipelineStage","All pipeline stages"],["status","Status","All statuses"]]){
  el(id).innerHTML='<option value="">'+label+'</option>'+[...new Set(i.rows.map(r=>r[key]))].sort().map(v=>'<option value="'+esc(v)+'">'+esc(v)+'</option>').join("");
 }
 el("inventory").addEventListener("change",render);render();
}).catch(()=>{el("count").textContent="Inventory unavailable; showing recorded catalog only.";});
fetch("defect-results.json",{cache:"no-store"}).then(r=>r.json()).then(i=>{
 el("discovered-findings").innerHTML=i.findings.map(f=>'<article class="finding"><span class="badge fail">Open '+esc(f.id)+'</span><h3>'+esc(f.classification)+'</h3><p>'+esc(f.problem)+'</p><p>Owner: '+esc(f.owner)+'</p><a href="defects.html">Expected, actual, evidence and next action</a></article>').join("");
}).catch(()=>{el("discovered-findings").textContent="Reviewed defects unavailable; open the Defect discovery page.";});
