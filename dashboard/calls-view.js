const el=id=>document.getElementById(id);
const esc=v=>String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function showCalls(s){el("call-refresh").textContent="Native import "+s.refreshed_at_utc+" · "+s.calls.length+" calls. CLI timestamp timezone unspecified.";el("call-history").innerHTML=s.calls.map(c=>'<tr><td>'+esc(c.call)+'</td><td>'+esc(c.platform_time)+'</td><td>'+esc(c.duration)+'</td><td>'+esc(c.workflow)+'<br>'+esc(c.outcome)+'</td><td>'+esc(c.grade)+'</td></tr>').join("");}
if(window.AEGIS_CALLS)showCalls(window.AEGIS_CALLS);
el("refresh-calls").addEventListener("click",async()=>{el("refresh-calls").disabled=true;try{const r=await fetch("/api/calls/refresh");if(!r.ok)throw new Error();showCalls(await r.json());}catch{el("call-refresh").textContent="Refresh unavailable; previous snapshot retained.";}finally{el("refresh-calls").disabled=false;}});
