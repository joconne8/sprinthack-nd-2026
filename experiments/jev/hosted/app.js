'use strict';
const $=id=>document.getElementById(id);let state,token,loading=false,lastImage=0,actionError='';
async function action(route,body={}){try{const r=await fetch(route,{method:'POST',headers:{'Content-Type':'application/json','X-Lab-Token':token},body:JSON.stringify(body)});const data=await r.json();if(!r.ok)throw Error(data.error);actionError='';await refresh();}catch(e){actionError=e.message;$('error').textContent=actionError;}}
$('run').onclick=()=>action('/run',{provider:$('provider').value,mode:$('scenario').value,startDate:$('start').value,endDate:$('end').value});
$('cancel').onclick=()=>action('/cancel');$('approve').onclick=()=>action('/approve',{id:state.pending.id,accept:true});$('reject').onclick=()=>action('/approve',{id:state.pending.id,accept:false});
async function refresh(){if(loading)return;loading=true;try{const r=await fetch('/state');if(!r.ok)throw Error('Connection unavailable');state=await r.json();token=state.token;
const busy=['running','approval'].includes(state.phase);$('phase').textContent=state.phase;$('run').disabled=busy||state.hosted.runsUsed>=state.hosted.maxRuns||($('provider').value==='jev'&&!state.keyConfigured);$('cancel').disabled=!busy;
$('key').textContent=state.keyConfigured?'Jev key configured on server':'Jev key missing; configure TYPESAFE_API_KEY in Replit Secrets';$('budget').textContent=`Run attempts: ${state.hosted.runsUsed} / ${state.hosted.maxRuns}`;
$('error').textContent=actionError||state.error||'';$('approval').hidden=!state.pending;if(state.pending)$('proposal').textContent=`${state.pending.original} → ${state.pending.proposed.label}. Confidence ${state.pending.decision.confidence}; selected probability ${state.pending.decision.probability}.`;
$('downloads').hidden=busy||!state.result?.ok;
$('verification').textContent=state.result?.ok?`Verified ${state.result.manifest.row_count} synthetic rows · ${state.result.manifest.requested_start_date} through ${state.result.manifest.requested_end_date}. SHA-256 ${state.result.sha256}`:state.result?`Stopped: ${state.result.type}. No verified download.`:'No verified file yet.';
const last=state.events.at(-1);$('usage').textContent=state.usage?`${state.provider}: ${state.usage.model_calls} calls; input tokens ${state.usage.input_tokens??'unknown'}; elapsed ${last?.elapsed_ms??'unknown'} ms`:state.provider?`Mode: ${state.provider}`:'No model calls';$('trace').textContent=state.events.slice(-30).map(e=>JSON.stringify(e)).join('\n');
$('view-note').textContent=state.browserLive?'Current browser screenshots; Jev receives DOM controls, not screenshots.':state.screenshotAvailable?'Last captured browser screenshot.':'Start a run to see browser activity.';
if((state.browserLive||state.screenshotAvailable)&&Date.now()-lastImage>1000){lastImage=Date.now();$('viewport').hidden=false;$('viewport').src='/screenshot?t='+lastImage;}
}catch(e){$('error').textContent=e.message;}finally{loading=false;}}
refresh();setInterval(refresh,500);
