'use strict';
const $=id=>document.getElementById(id);let token,state,loading=false,lastImage=0;
async function action(route,body={}){
  try{const r=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json','X-Lab-Token':token},body:JSON.stringify(body)});
    const result=await r.json();if(!r.ok)throw new Error(result.error);$('error').textContent='';await refresh();
  }catch(e){$('error').textContent=e.message;}
}
$('present').onclick=()=>{$('provider').value='jev';action('/run',{workflow:'predefined',provider:'jev',startDate:$('start').value,endDate:$('end').value,mode:$('scenario').value});};
$('record').onclick=()=>action('/record/start');$('finish').onclick=()=>action('/record/finish');
$('save').onclick=()=>action('/recipe/save',{parameterizeDates:$('parameterize').checked});
$('run').onclick=()=>action('/run',{startDate:$('start').value,endDate:$('end').value,provider:$('provider').value,mode:$('scenario').value});
$('cancel').onclick=()=>action('/cancel');$('import').onclick=()=>action('/import');
$('approve').onclick=()=>action('/approve',{id:state.pending.id,accept:true});
$('reject').onclick=()=>action('/approve',{id:state.pending.id,accept:false});
async function refresh(){
  if(loading)return;loading=true;
  try{
    state=await(await fetch('/state')).json();token=state.token;
    $('phase').textContent=state.phase;$('key').textContent=state.keyConfigured?'Jev key configured on server':'Jev key absent on server; replay remains available';
    if(state.error)$('error').textContent=state.error;
    const running=['running','approval'].includes(state.phase);
    $('present').disabled=running||state.phase==='recording'||!state.keyConfigured;
    $('record').disabled=running||state.phase==='recording';$('finish').disabled=state.phase!=='recording';
    $('save').disabled=state.phase!=='review';$('run').disabled=running||!state.recipe||state.phase==='recording';
    $('import').disabled=running||!state.result?.ok;
    $('recorded').replaceChildren(...state.recording.map(s=>{const li=document.createElement('li');li.textContent=`${s.op} · ${s.label}${s.value?' · '+s.value:''}`;return li;}));
    $('recipe').textContent=state.recipe?JSON.stringify(state.recipe.steps,null,2):'No recipe saved';
    if(state.recipe)$('parameterize').checked=true;
    $('approval').hidden=!state.pending;
    if(state.pending)$('proposal').textContent=`${state.pending.original} → ${state.pending.proposed.label}. Confidence ${state.pending.decision.confidence}; probability ${state.pending.decision.probability}.`;
    $('usage').textContent=state.usage?`${state.provider}: ${state.usage.model_calls} calls; input tokens ${state.usage.input_tokens??'unknown'}`:state.provider?`Mode: ${state.provider}`:'No model calls';
    $('trace').textContent=state.events.slice(-45).map(e=>JSON.stringify(e)).join('\n');
    $('verification').textContent=state.result?.ok?`Verified ${state.result.manifest.row_count} synthetic rows · ${state.result.manifest.requested_start_date} through ${state.result.manifest.requested_end_date}\nSHA-256 ${state.result.sha256}`:state.result?`Run stopped: ${state.result.type}. No new verified file.`:'No verified download yet.';
    if(state.publication){const m=state.publication.metrics;const sales=m.metrics.find(x=>x.metric_id==='M-DEMO-NET-SALES');
      $('sales').textContent=sales.value===null?'Unavailable':`$${sales.value}`;
      $('publication').textContent=`${state.publication.batch.status} · ${m.filters_applied.start_date}–${m.filters_applied.end_date} · ${m.evidence.row_count} rows · coverage ${m.coverage.state} · ${m.reconciliation_state}. Other sources unconnected.`;
      $('evidence').textContent=JSON.stringify(state.publication,null,2);
    }else{$('sales').textContent='Unavailable';$('publication').textContent='No published data yet. Other sources are unconnected.';$('evidence').textContent='No evidence yet';}
    $('view-note').textContent=state.browserLive?'Current screenshot of the live local browser. Use the separate portal window while recording.':state.screenshotAvailable?'Last captured portal screenshot; the browser run has finished.':'Open a recording to see the local portal.';
    if((state.browserLive||state.screenshotAvailable)&&Date.now()-lastImage>1000){lastImage=Date.now();$('viewport').hidden=false;$('viewport').src='/screenshot?t='+lastImage;}
  }catch(e){$('error').textContent='Lab connection unavailable';}finally{loading=false;}
}
refresh();setInterval(refresh,500);
