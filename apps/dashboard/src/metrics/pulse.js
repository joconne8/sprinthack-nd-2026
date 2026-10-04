import {$, el, badge, money, timestamp} from '../common.js';
const names={'M-DEMO-NET-SALES':'Demo net sales','M-PLATFORM-CUSTOMERS':'Platform-local customers','R-LABOR-PRODUCTIVITY':'Labor productivity','R-MARGIN':'Net margin','R-SELL-THROUGH':'Sell-through','R-REVENUE-GROWTH':'Revenue growth','M-LISTINGS-CREATED':'Listings created','M-UNLISTED-BACKLOG':'Unlisted backlog'};
export function renderMetrics(response, inventory, onEvidence) {
  $('primary-metrics').replaceChildren();$('strategic-metrics').replaceChildren();
  response.metrics.forEach((metric,index)=>{
    const card=el('article',undefined,index<2 ? 'metric-card'+(index===0?' featured':'') : 'scorecard');
    const top=el('div',undefined,'metric-top');top.append(el(index<2?'div':'h3',names[metric.metric_id] || metric.metric_id,'metric-label'),badge(metric.availability));card.append(top);
    const value=metric.value===null?'Unavailable':metric.unit==='USD'?money(metric.value):metric.value;
    const number=el('div',value,index<2?'metric-value'+(metric.value===null?' unavailable':''):'score-value');number.dataset.metricId=metric.metric_id;number.dataset.value=metric.value??'';card.append(number);
    card.append(el('p',metric.availability_reason || (metric.metric_id==='M-DEMO-NET-SALES'?'Item sales − refunds · excludes shipping, tax and fees':'Distinct buyers within one marketplace. Choose a marketplace to view.')));
    if(index<2){const details=el('details');details.append(el('summary','Definition & version'),el('p',metric.definition+' · '+metric.metric_version));card.append(details);}
    if(index===0){const button=el('button','View source rows →','button small');button.dataset.testid='evidence-open';button.disabled=!response.metric_run_id || metric.value===null;button.onclick=()=>onEvidence(response);card.append(button);}
    $(index<2?'primary-metrics':'strategic-metrics').append(card);
  });
  for(const id of ['M-LISTINGS-CREATED','M-UNLISTED-BACKLOG']) {
    const metric=inventory?.metrics.find(metric=>metric.metric_id===id);
    const card=el('article',undefined,'scorecard');const top=el('div',undefined,'metric-top');top.append(el('h3',names[id]),badge(metric?.availability || 'unavailable'));card.append(top,el('div',metric?.value??'Unavailable','score-value'),el('p',metric?.availability_reason || 'Matching verified listing events / complete snapshot are not available for this scope.'));
    if(metric?.value!==null && metric?.value!==undefined)card.append(el('p','Separate synthetic inventory sidecars; not inferred from the acquired sales report.'));
    $('strategic-metrics').append(card);
  }
  $('coverage-badge').replaceWith(Object.assign(badge(response.coverage.state),{id:'coverage-badge'}));
  const details=[['Complete reporting days',response.coverage.complete_days.length+' / '+response.coverage.expected_days.length],['Last import',timestamp(response.freshness.latest_import_at)],['Publication',response.freshness.publication_state.replaceAll('_',' ')],['Source reconciliation',response.reconciliation_state]];
  $('coverage-details').replaceChildren(...details.map(([label,value])=>{const node=el('div');node.append(el('span',label,'label'),el('strong',value));return node;}));
  const missing=response.coverage.missing_or_partial_days;
  $('coverage-note').textContent=missing.length?'Missing or partial days: '+missing.slice(0,10).join(', ')+(missing.length>10?' …':'')+'. A successful download does not imply full-source coverage.':'All requested reporting days are covered by verified, unfiltered source windows.';
  $('freshness-warning').hidden=!response.freshness.warning;$('freshness-warning').textContent=response.freshness.warning || '';
  const scope=response.filters_applied;
  $('metric-scope').textContent=scope.start_date+' → '+scope.end_date+' · '+scope.source+' · '+(scope.platform || 'all marketplaces')+' · '+(scope.store || 'all stores, including unknown')+' · Eastern Time · USD';
}
