const d=window.AEGIS_DATA;
const el=id=>document.getElementById(id);
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
el("passed").textContent=d.checks.filter(c=>c.status==="ok").length+" / "+d.checks.length;
el("duration").textContent=d.hosted_seconds.toFixed(3)+" s";
el("checks").innerHTML=d.checks.map(c=>'<tr><td>'+esc(c.name)+'</td><td><span class="badge '+(c.status==="ok"?"pass":"fail")+'">'+(c.status==="ok"?"PASS":"FAIL")+'</span></td></tr>').join("");
el("pending").innerHTML=["Inbound establishment","Outbound connection","Aggregate field accuracy","Speech latency p50 / p95","Barge-in delay","Recovery / duplicate actions","Unauthorized action rate","RAG groundedness","Billed usage"].map(k=>'<div class="metric"><span>'+k+'</span><span class="muted">Not measured</span></div>').join("");
function render(){const q=el("search").value.toLowerCase(),s=el("status").value;const rows=d.cases.filter(c=>(!s||c.Status===s)&&JSON.stringify(c).toLowerCase().includes(q));el("count").textContent=rows.length+" / "+d.cases.length+" cases";el("cases").innerHTML=rows.map(c=>'<tr><td>'+esc(c.ID)+'</td><td>'+esc(c.Component)+'<br><small class="muted">'+esc(c.InstallationMethodScope)+'</small></td><td>'+esc(c.Threat_or_behavior)+'</td><td><span class="badge '+(c.Status==="PARTIAL_FAIL"?"fail":c.Status==="PARTIAL"?"warn":"")+'">'+esc(c.Status)+'</span></td><td>'+esc(c.Expected)+'</td></tr>').join("");}
el("search").addEventListener("input",render);el("status").addEventListener("change",render);render();
el("export").addEventListener("click",()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(d,null,2)],{type:"application/json"}));const a=document.createElement("a");a.href=url;a.download="aegis-results-"+d.updated+".json";a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
