const {test}=require('node:test'),assert=require('node:assert/strict');
const {buildRecipe,validateRecipe}=require('./recipe.cjs');
const events=[{op:'click',label:'▥ Reports',href:'/upright/reports'},
  {op:'click',label:'Paid orders',href:'/upright/reports/paid-orders'},
  {op:'fill',label:'Start date',value:'2026-09-30'}, {op:'fill',label:'End date',value:'2026-09-30'},
  {op:'select',label:'Timezone',value:'America/Indiana/Indianapolis'}, {op:'select',label:'Payment status',value:'All'},
  {op:'click',label:'Generate report',role:'button'}, {op:'click',label:'Download',href:'/api/reports/abc123/download'}];
const reviewed={parameterizeDates:true,recordingVerified:true};
test('recipe derives ordered steps and parameters from captured events',()=>{
  const recipe=buildRecipe(events,reviewed);assert.equal(recipe.steps.find(s=>s.label==='Start date').value,'{start_date}');
  assert.equal(validateRecipe(recipe),recipe);
});
test('missing review/download or unsupported/reordered events fail',()=>{
  assert.throws(()=>buildRecipe(events,{}));assert.throws(()=>buildRecipe(events,{parameterizeDates:true}));
  assert.throws(()=>buildRecipe([...events,{op:'click',label:'Delete'}],reviewed));
  const reordered=[...events];[reordered[0],reordered[1]]=[reordered[1],reordered[0]];
  assert.throws(()=>buildRecipe(reordered,reviewed));
});
test('recipe edits cannot expand hosts, report types or actions',()=>{
  for(const edit of [r=>r.allowed_hosts.push('example.com'),r=>r.report_type='paid_order_items',r=>r.steps.push({op:'click',name:'Delete'}),r=>r.timeouts_ms.total=999999]){
    const recipe=buildRecipe(events,reviewed);edit(recipe);assert.throws(()=>validateRecipe(recipe));
  }
});
