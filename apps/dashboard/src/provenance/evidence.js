import {$,el,api,query,money,table,action,errorNotice} from '../common.js';
let pinned=null,offset=0,total=0,generation=0;
const limit=50;
export async function openEvidence(response) {pinned=structuredClone(response);offset=0;location.hash='evidence';await load();}
async function load(){
  if(!pinned)return;
  const current=++generation,selected=pinned;
  try{
    const body=await api('/api/v1/evidence?'+query({...selected.filters_applied,reporting_timezone:null,run_id:selected.metric_run_id,offset,limit}));
    if(current!==generation)return;
    if(body.scope_total !== selected.metrics[0].value)throw new Error('Source evidence does not match the displayed metric. Contact the data maintainer.');
    total=body.total_rows;$('evidence-empty').hidden=true;$('evidence-content').hidden=false;
    $('evidence-scope-total').textContent=money(body.scope_total);$('evidence-scope-total').dataset.value=body.scope_total;
    $('evidence-scope').textContent=body.filters_applied.start_date+' → '+body.filters_applied.end_date+' · '+body.filters_applied.source+' · '+(body.filters_applied.platform||'all marketplaces')+' · '+(body.filters_applied.store||'all stores')+' · '+total+' supporting rows';
    $('evidence-run').textContent='Pinned metric run: '+body.metric_run_id;
    $('evidence-table').replaceChildren(table(['Reporting day','Marketplace','Store','Item sales','Refunds','Demo net sales','Source row','Evidence'],body.rows.map(row=>[
      row.reporting_date,row.platform,row.store_id||'Unknown',money(row.gross_item_sales),money(row.refunds),money(row.demo_net_sales),row.source_row_number,action('Inspect row',()=>inspect(row))
    ])));
    $('evidence-page').textContent=total ? `Rows ${offset+1}–${Math.min(offset+limit,total)} of ${total}` : 'No supporting rows for this scope';
    $('evidence-prev').disabled=offset===0;$('evidence-next').disabled=offset+limit>=total;
  }catch(error){errorNotice(error);}
}
async function inspect(row){
  const target=$('row-detail');target.hidden=false;target.replaceChildren(el('h2','Original source row '+row.source_row_number));
  const links=el('div',undefined,'detail-links');const download=el('a','Download exact source CSV');download.href='/api/v1/files/'+row.file_id;
  const batch=action('Review import & exceptions',()=>{location.hash='operations';document.dispatchEvent(new CustomEvent('inspect-batch',{detail:row.batch_id}));});links.append(download,batch);target.append(links);
  target.append(el('p','File SHA-256: '+row.file_id,'mono'),el('p','Batch: '+row.batch_id+' · Parser: '+row.parser_version+' · Rules: '+row.rule_version,'mono'),el('p','Source day: '+row.source_date+' · Reporting day: '+row.reporting_date+' · Source timestamp: '+(row.source_timestamp||'Date-only source'),'muted'),el('pre',JSON.stringify(row.original_row,null,2)));
  target.scrollIntoView({behavior:'smooth',block:'nearest'});
}
$('evidence-prev').onclick=()=>{offset=Math.max(0,offset-limit);load();};$('evidence-next').onclick=()=>{if(offset+limit<total){offset+=limit;load();}};
