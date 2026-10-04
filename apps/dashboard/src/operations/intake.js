import {$,el,api,table,badge,action,timestamp,query,errorNotice,clearError} from '../common.js';
let afterImport=()=>{},polling=false;
const stages={pending:'Request queued',collecting:'Collecting the synthetic report…',verifying:'Checking dates, headers and exact file bytes…',importing:'Reconciling the verified file…',complete:'Verified report imported. Metrics are ready.',failed:'Collection or import needs attention.'};

export function initializeOperations(onImported){
  afterImport=onImported;
  $('collect-form').onsubmit=collect;
  $('upload-form').onsubmit=upload;
  $('refresh-history').onclick=refreshOperations;
  document.addEventListener('inspect-batch',event=>inspectBatch(event.detail));
  const sources=[['Cash Monkey orders','Portal export hypothesis','Synthetic upload only','Sales + payout; overlaps need review'],['Upright paid orders','Portal export','Synthetic collection','Authoritative source selected per metric'],['Jewelry report','Manual upload hypothesis','Not connected','Item enrichment; not revenue'],['OSM / PB / EasyPost shipping','Export / lookup hypothesis','Not connected','Expense; not revenue'],['FedEx charges / refunds','Export / lookup hypothesis','Not connected','Expense and refund netting'],['ShopGoodwill reports','Portal export hypothesis','Not connected','Potential Upright transaction overlap'],['Goodwill Books statement','Scheduled file hypothesis','Not connected','Settlement; not transaction revenue'],['eBay listing sales','Authorized API / export hypothesis','Not connected','Listing events and sales'],['Amazon payments summary','Generated report hypothesis','Not connected','Settlement; not transaction revenue']];
  $('source-map').replaceChildren(table(['Report source','Acquisition class','Demo connection','Financial role'],sources));
  return refreshOperations();
}

export async function refreshOperations(){
  try{
    const [history,imports]=await Promise.all([api('/api/v1/acquisition-runs'),api('/api/v1/imports')]);
    $('collect-button').disabled=polling || !history.runtime_available;
    if(!history.runtime_available)$('collection-status').textContent='Collection is not configured here. Upload the original CSV and manifest, or ask the demo maintainer.';
    else if(!polling)$('collection-status').textContent='Ready for an on-demand synthetic report. No production email is sent.';
    $('last-success').textContent=history.last_success_at?'Last successful collection: '+timestamp(history.last_success_at):'No successful collection yet.';
    $('run-history').replaceChildren(history.runs.length?table(['Requested report period','Collection','Import','Publication','Attempts','Next action'],history.runs.map(run=>{
      const next=el('div');next.append(el('div',run.cause || (run.status==='succeeded'?'Verified file retained.':'Collecting requested report…')));
      if(run.owner_role)next.append(el('small',run.owner_role));
      if(run.batch_id)next.append(action('Review import',()=>inspectBatch(run.batch_id)));
      return [run.start_date+' → '+run.end_date,badge(run.status),badge(run.import_state),badge(run.publication_state),run.attempts.length+' / '+run.max_attempts,next];
    })):el('p','No collection requests yet. Choose a report period above.','empty'));
    $('import-history').replaceChildren(imports.imports.length?table(['Report / source','Source period','Import','Accepted','Duplicates','Rejected','Evidence'],imports.imports.map(batch=>[
      batch.source+' · '+batch.report_type,batch.period.start_date+' → '+batch.period.end_date,badge(batch.status),batch.counts.accepted_rows,batch.counts.duplicate_rows,batch.counts.rejected_rows,action('Review batch',()=>inspectBatch(batch.batch_id))
    ])):el('p','No imported files. Collect a report or use the manual upload.','empty'));
    for(const batch of imports.imports){if(![...$('metric-source').options].some(option=>option.value===batch.source)){$('metric-source').append(new Option(batch.source+' · synthetic',batch.source));}}
    const active=history.runs.find(run=>['pending','running'].includes(run.status));
    if(active&&!polling)pollRun(active.run_id);
  }catch(error){errorNotice(error);}
}

async function collect(event){
  event.preventDefault();clearError();
  $('collect-button').disabled=true;
  try{
    const run=await api('/api/v1/acquisition-runs',{start_date:$('request-start').value,end_date:$('request-end').value,mode:$('request-mode').value});
    await pollRun(run.run_id);
  }catch(error){errorNotice(error);$('collection-status').textContent=error.message;$('collect-button').disabled=false;}
}

async function pollRun(runId){
  if(polling)return;
  polling=true;$('collect-button').disabled=true;$('collect-button').textContent='Collecting…';
  const deadline=Date.now()+95000;
  try{
    while(Date.now()<deadline){
      const run=await api('/api/v1/acquisition-runs/'+runId);
      $('collection-status').textContent=(stages[run.stage]||run.stage)+(run.cause?' '+run.cause:'')+(run.owner_role?' Next owner: '+run.owner_role+'.':'');
      if(!['pending','running'].includes(run.status)){
        if(run.status==='succeeded')await afterImport({requested_start_date:run.start_date,requested_end_date:run.end_date,source_name:run.source});
        break;
      }
      await new Promise(resolve=>setTimeout(resolve,700));
    }
    if(Date.now()>=deadline)$('collection-status').textContent='Collection is taking longer than expected. Refresh history to inspect its persisted result; use manual upload if needed.';
  }catch(error){errorNotice(error);$('collection-status').textContent='Unable to read collection status. Refresh history to check the saved result.';}
  finally{
    const message=$('collection-status').textContent;
    polling=false;$('collect-button').textContent='Collect & verify report';
    await refreshOperations();$('collection-status').textContent=message;
  }
}

async function upload(event){
  event.preventDefault();clearError();$('upload-button').disabled=true;$('upload-status').textContent='Verifying the original files…';
  let manifest;
  try{
    const file=$('csv-file').files[0], metadata=$('manifest-file').files[0];
    if(file.size>8*1024*1024 || metadata.size>1024*1024)throw new Error('Choose a CSV smaller than 8 MiB and a manifest smaller than 1 MiB.');
    manifest=JSON.parse(await metadata.text());
    const batch=await api('/api/v1/imports',{csv_text:await file.text(),manifest,allow_corrections:$('allow-corrections').checked});
    $('upload-status').textContent=batch.status==='duplicate_noop'?'This report was already imported. Published totals are unchanged.':'Verified import complete. Published metrics are ready.';
    await refreshOperations();await afterImport(manifest);await inspectBatch(batch.batch_id);
  }catch(error){
    $('upload-status').textContent='Import was not published. '+error.message;errorNotice(error);
    await refreshOperations();
    if(error.body?.batch_id)await inspectBatch(error.body.batch_id);
    if(manifest)await afterImport(manifest,false);
  }finally{$('upload-button').disabled=false;}
}

export async function inspectBatch(id){
  try{
    const batch=await api('/api/v1/imports/'+encodeURIComponent(id));
    const target=$('batch-detail');target.hidden=false;target.replaceChildren(el('h2','Import evidence & exceptions'));
    target.append(el('p',batch.source+' · '+batch.period.start_date+' → '+batch.period.end_date+' · '+batch.period.source_timezone,'muted'),el('p','Batch '+batch.batch_id,'mono'),badge(batch.status));
    const download=el('a','Download the exact archived CSV');download.href='/api/v1/files/'+batch.file.file_id;download.download='synthetic-report.csv';
    const metadata=el('a','Download matching manifest');metadata.href='/api/v1/imports/'+batch.batch_id+'/manifest';metadata.download='synthetic-report.manifest.json';
    const links=el('div',undefined,'detail-links');links.append(download,metadata);target.append(el('p','SHA-256: '+batch.file.checksum,'mono'),links);
    const controls=batch.reconciliation;
    if(controls)target.append(el('p',`Source rows: ${controls.source_rows} · accepted: ${controls.accepted_rows} · duplicate: ${controls.duplicate_rows} · rejected: ${controls.rejected_rows} · counts balanced: ${controls.counts_balanced?'yes':'no'}`),el('pre',JSON.stringify(controls,null,2)));
    if(batch.error)target.append(el('p',batch.error.detail,'notice error'));
    target.append(el('h3','Exception history'));
    if(!batch.exceptions.length)target.append(el('p','No exceptions recorded for this batch.','muted'));
    for(const item of batch.exceptions){
      target.append(el('p',item.code+' · '+(item.row_number===null?'Batch control':'Source row '+item.row_number)+' · '+item.owner_role),el('p',item.detail,'muted'),badge(item.status));
      if(item.status==='resolved'){target.append(el('p','Resolution note: '+item.resolution,'muted'));continue;}
      const form=el('form',undefined,'resolution-form');const input=el('input');input.required=true;input.placeholder='Document your review; missing values stay unknown';input.setAttribute('aria-label','Resolution note for '+item.code+' source row '+item.row_number);
      const button=el('button','Record review note','button small');button.type='submit';form.append(input,button);
      form.onsubmit=async event=>{event.preventDefault();try{await api('/api/v1/exceptions/'+item.id+'/resolve',{resolution:input.value});await inspectBatch(id);}catch(error){errorNotice(error);}};target.append(form);
    }
    const rejected=action('Inspect rejected source rows',async()=>{
      const response=await api('/api/v1/imports/'+batch.batch_id+'/rows?'+query({status:'rejected',limit:50}));
      const block=el('pre',JSON.stringify(response.rows,null,2));target.append(el('p',response.total_rows+' rejected rows · first 50 shown'),block);
    });target.append(rejected);
  }catch(error){errorNotice(error);}
}
