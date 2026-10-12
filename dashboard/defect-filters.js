const cards=[...document.querySelectorAll('article[data-stage]')];
for(const [id,key] of [['defect-stage','stage'],['defect-owner','owner']]){
 const select=document.getElementById(id);for(const value of [...new Set(cards.map(c=>c.dataset[key]))].sort()){const option=document.createElement('option');option.value=value;option.textContent=value;select.append(option);}
 select.addEventListener('change',()=>cards.forEach(c=>{c.hidden=!!((document.getElementById('defect-stage').value&&c.dataset.stage!==document.getElementById('defect-stage').value)||(document.getElementById('defect-owner').value&&c.dataset.owner!==document.getElementById('defect-owner').value));}));
}
