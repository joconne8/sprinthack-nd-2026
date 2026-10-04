'use strict';
const fs = require('node:fs');
const path = require('node:path');
const canonical = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../../acquisition/skills/upright-paid-orders.skill.json')));
const expected = [
  {op:'click',role:'link',name:'▥ Reports',within:{role:'navigation',name:'Upright navigation'}},
  {op:'click',role:'link',name:'Paid orders'},
  {op:'fill',label:'Start date',value:'{start_date}'},
  {op:'fill',label:'End date',value:'{end_date}'},
  {op:'select',label:'Timezone',value:'America/Indiana/Indianapolis'},
  {op:'select',label:'Payment status',value:'All'},
  {op:'click',role:'button',name:'Generate report'},
  {op:'download',selector:'[data-testid="download-{job_id}"]'}
];
function classify(event) {
  if (event.op==='click' && event.label==='▥ Reports' && event.href==='/upright/reports') return 0;
  if (event.op==='click' && event.label==='Paid orders' && event.href==='/upright/reports/paid-orders') return 1;
  if (event.op==='fill' && event.label==='Start date') return 2;
  if (event.op==='fill' && event.label==='End date') return 3;
  if (event.op==='select' && event.label==='Timezone' && event.value==='America/Indiana/Indianapolis') return 4;
  if (event.op==='select' && event.label==='Payment status' && event.value==='All') return 5;
  if (event.op==='click' && event.label==='Generate report' && event.role==='button') return 6;
  if (event.op==='click' && event.label==='Download' && /^\/api\/reports\/[a-f0-9]+\/download$/.test(event.href)) return 7;
  return -1;
}
function buildRecipe(events, {parameterizeDates, recordingVerified} = {}) {
  if (!parameterizeDates) throw new Error('Review and explicitly parameterize both date fields');
  if (!recordingVerified) throw new Error('Recording must finish with a verified report download');
  const captured=[];
  for (const event of events) {
    const index=classify(event);
    if(index<0) throw new Error('Recording contains unsupported action; record the scoped paid-orders journey again');
    // A date input may emit change more than once before proceeding.
    if (captured.at(-1)?.index===index && [2,3].includes(index)) captured[captured.length-1]={index,event};
    else captured.push({index,event});
  }
  if (captured.length!==8 || captured.some((e,i)=>e.index!==i))
    throw new Error('Record Reports, Paid orders, both dates, Eastern timezone, All payments, Generate, then Download in order');
  return {...structuredClone(canonical), skill_id:'recorded-upright-paid-orders',skill_version:'1.0.0',
    status:'operator-reviewed synthetic recipe',timeouts_ms:{step:5000,total:60000},
    recording: captured.map(({event})=>event), parameters:['start_date','end_date'],
    steps:[{op:'goto',path:'/upright'},{op:'assert',role:'navigation',name:'Upright navigation'},
      expected[0],expected[1],{op:'assert',role:'heading',name:'Paid Order Report'},
      ...expected.slice(2,7),canonical.steps.find(s=>s.op==='wait_state'),expected[7]]};
}
function validateRecipe(recipe) {
  const rebuilt=buildRecipe(recipe.recording,{parameterizeDates:true,recordingVerified:true});
  for(const key of ['allowed_hosts','source_name','report_type','parameters','steps','timeouts_ms'])
    if(JSON.stringify(recipe[key])!==JSON.stringify(rebuilt[key])) throw new Error('Recipe differs from allowed reviewed workflow');
  return recipe;
}
module.exports={buildRecipe,validateRecipe,classify};
