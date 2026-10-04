import {$,api,query,errorNotice,clearError} from './common.js';
import {renderMetrics} from './metrics/pulse.js';
import {openEvidence} from './provenance/evidence.js';
import {initializeOperations,refreshOperations} from './operations/intake.js';

for(let number=1;number<=24;number++)$('metric-store').append(new Option('Synthetic store GW-'+String(number).padStart(3,'0'),'GW-'+String(number).padStart(3,'0')));
const names={overview:'Leadership pulse',operations:'Report intake',evidence:'Source evidence'};
function navigate(){
  const view=location.hash.slice(1) in names ? location.hash.slice(1) : 'overview';
  for(const id of Object.keys(names))$(id+'-view').hidden=id!==view;
  for(const link of document.querySelectorAll('[data-view]')){if(link.dataset.view===view)link.setAttribute('aria-current','page');else link.removeAttribute('aria-current');}
  $('view-name').textContent=names[view];
  if(view==='operations')refreshOperations();
}
let generation=0,controller=null;
async function loadMetrics(){
  const current=++generation;controller?.abort();controller=new AbortController();
  const filters={start_date:$('metric-start').value,end_date:$('metric-end').value,source:$('metric-source').value,platform:$('metric-platform').value||null,store:$('metric-store').value||null};
  $('metrics-content').setAttribute('aria-busy','true');$('metrics-content').classList.add('busy');$('metric-loading').textContent='Updating verified metrics…';
  document.querySelector('[data-testid="evidence-open"]')?.setAttribute('disabled','');
  try{
    const response=await api('/api/v1/metrics?'+query(filters),undefined,controller.signal);
    let inventory=null;
    if(!filters.platform){try{inventory=await api('/api/v1/inventory?'+query({start_date:filters.start_date,end_date:filters.end_date,store:filters.store}),undefined,controller.signal);}catch(error){if(error.name==='AbortError')throw error;errorNotice(new Error('Inventory status could not be loaded. Sales metrics remain available.'));}}
    if(current!==generation)return;
    renderMetrics(response,inventory,openEvidence);
  }catch(error){if(error.name!=='AbortError'&&current===generation){errorNotice(error);$('primary-metrics').replaceChildren();$('strategic-metrics').replaceChildren();$('coverage-details').replaceChildren();$('coverage-badge').textContent='Unavailable';$('coverage-badge').className='badge unavailable';$('freshness-warning').hidden=true;$('coverage-note').textContent='Metrics could not be loaded. Apply valid filters or retry; no mock values are shown.';}}
  finally{if(current===generation){$('metrics-content').setAttribute('aria-busy','false');$('metrics-content').classList.remove('busy');$('metric-loading').textContent='';}}
}
$('filters').onsubmit=event=>{event.preventDefault();clearError();loadMetrics();};
async function imported(manifest,changeScope=true){
  if(changeScope){
    if(![...$('metric-source').options].some(option=>option.value===manifest.source_name))$('metric-source').append(new Option(manifest.source_name+' · synthetic',manifest.source_name));
    $('metric-start').value=manifest.requested_start_date;$('metric-end').value=manifest.requested_end_date;$('metric-source').value=manifest.source_name;$('metric-platform').value='';$('metric-store').value='';
  }
  await loadMetrics();
}
window.addEventListener('hashchange',navigate);navigate();
initializeOperations(imported);loadMetrics();
