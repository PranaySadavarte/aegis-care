const d=window.AEGIS_DATA;
const el=id=>document.getElementById(id);
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
el("passed").textContent=d.checks.filter(c=>c.status==="ok").length+" / "+d.checks.length;
el("duration").textContent=d.hosted_seconds.toFixed(3)+" s";
el("checks").innerHTML=d.checks.map(c=>'<tr><td>'+esc(c.name)+'</td><td><span class="badge '+(c.status==="ok"?"pass":"fail")+'">'+(c.status==="ok"?"PASS":"FAIL")+'</span></td></tr>').join("");
el("pending").innerHTML=["Inbound establishment","Outbound connection","Aggregate field accuracy","Speech latency p50 / p95","Barge-in delay","Recovery / duplicate actions","Unauthorized action rate","RAG groundedness","Billed usage"].map(k=>'<div class="metric"><span>'+k+'</span><span class="muted">Not measured</span></div>').join("");
el("stage").innerHTML += [...new Set(d.cases.map(c=>c.PipelineStage))].map(s=>'<option value="'+esc(s)+'">'+esc(s)+'</option>').join("");
el("harborcare").innerHTML = (d.harborcare_runs||[]).map(r=>'<div class="metric"><span>'+esc(r.workflow)+'</span><span class="badge '+(r.status==="PASS"?"pass":"fail")+'">'+esc(r.status)+'</span></div>').join("") || "Hosted application runs pending";
function render(){const q=el("search").value.toLowerCase(),s=el("status").value;const rows=d.cases.filter(c=>(!s||c.Status===s)&&(!el("stage").value||c.PipelineStage===el("stage").value)&&JSON.stringify(c).toLowerCase().includes(q));el("count").textContent=rows.length+" / "+d.cases.length+" cases";el("cases").innerHTML=rows.map(c=>'<tr><td>'+esc(c.ID)+'</td><td>'+esc(c.PipelineStage)+'<br><small class="muted">'+esc(c.Direction)+'</small></td><td>'+esc(c.Threat_or_behavior)+'</td><td><span class="badge '+(c.Status==="PARTIAL_FAIL"?"fail":c.Status==="PARTIAL"?"warn":"")+'">'+esc(c.Status)+'</span></td><td>'+esc(c.Expected)+'</td></tr>').join("");}
el("stage").addEventListener("change",render);el("search").addEventListener("input",render);el("status").addEventListener("change",render);render();
el("export").addEventListener("click",()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(d,null,2)],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download="aegis-results-"+d.updated+".json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});

function showCalls(snapshot){
 d.manual_calls=snapshot;
 el("call-refresh").textContent="Last native import: "+snapshot.refreshed_at_utc+" · "+snapshot.calls.length+" returned records. Platform timestamp timezone is unspecified; no grading inferred.";
 el("call-history").innerHTML=snapshot.calls.map(c=>'<tr><td>'+esc(c.call)+'</td><td>'+esc(c.platform_time)+'<br><small class="muted">Timezone unspecified by CLI</small></td><td>'+esc(c.duration)+'</td><td>'+esc(c.outcome)+'</td><td>'+esc(c.grade)+'</td></tr>').join("")||'<tr><td colspan="5">No records returned. This does not prove no call attempt.</td></tr>';
}
if(window.AEGIS_CALLS)showCalls(window.AEGIS_CALLS);
el("refresh-calls").addEventListener("click",async()=>{
 const button=el("refresh-calls");button.disabled=true;el("call-refresh").textContent="Reading native Guava conversation records…";
 try{const response=await fetch("/api/calls/refresh");if(!response.ok)throw new Error();const snapshot=await response.json();if(!Array.isArray(snapshot.calls))throw new Error();showCalls(snapshot);}
 catch{el("call-refresh").textContent="Refresh unavailable. Previous snapshot retained. Open the local dashboard at port 8765 or use the native CLI conversation commands.";}
 finally{button.disabled=false;}
});


