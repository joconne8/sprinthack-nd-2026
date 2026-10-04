const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {chromium}=require('playwright');const {createLab}=require('./lab.cjs');const {JevProvider}=require('./provider.cjs');
const pause=ms=>new Promise(r=>setTimeout(r,ms));
const factory=emit=>new JevProvider({key:'injected-only',emit,fetchFn:async(_,options)=>{
  const q=JSON.parse(options.body),g=q.state.goal;
  const c=q.state.controls.find(c=>q.state.requested_field_label?c.label===q.state.requested_field_label:
    g.includes('Generate the')?c.role==='button':g.includes('verified current')?true:g.includes('Paid orders')?c.label==='Paid orders':c.href==='/upright/reports');
  assert(c,'Injected fixture has no matching target');
  return {ok:true,json:async()=>({model:'jev-1.13.0',answers:{target:{type:'choice',choice:c.id,confidence:1,
    probabilities:Object.fromEntries(['STOP',...q.state.controls.map(c=>c.id)].map(id=>[id,id===c.id?1:0]))}},usage:{input_tokens:1,output_tokens:1}})};
}});
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jev-lab-tests-'));
  const lab=await createLab({browser,stateRoot:root,headed:false,baseUrl:process.env.BASE_URL||'http://127.0.0.1:4187',providerFactory:factory});
  await new Promise(r=>lab.server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${lab.server.address().port}`;
  const get=async()=>await(await fetch(base+'/state')).json();let token=(await get()).token;
  const post=async(route,body={})=>{
    const r=await fetch(base+route,{method:'POST',headers:{'Content-Type':'application/json','X-Lab-Token':token},body:JSON.stringify(body)});
    const b=await r.json();assert(r.ok,JSON.stringify(b));return b;
  };
  const wait=async predicate=>{const end=Date.now()+70000;while(Date.now()<end){const s=await get();if(predicate(s))return s;await pause(100);}throw new Error('Lab test wait timed out');};
  try{
    const forbidden=await fetch(base+'/record/start',{method:'POST'});assert.equal(forbidden.status,403);
    await post('/run',{workflow:'predefined',provider:'jev',mode:'normal',startDate:'2026-09-30',endDate:'2026-09-30'});
    const first=await wait(s=>['verified','stopped'].includes(s.phase));assert(first.result.ok,JSON.stringify(first));assert.equal(first.result.verification.rows_checked,128);assert.equal(first.recipe,null);assert.equal(first.provider,'injected-test-only');
    console.log('PASS: predefined first-run Jev path verifies 128 rows without fabricating a recording');
    await post('/record/start');const p=lab.page;
    await p.getByRole('navigation',{name:'Upright navigation'}).getByRole('link',{name:'▥ Reports',exact:true}).click();
    await p.getByRole('link',{name:'Paid orders',exact:true}).click();
    await p.getByLabel('Start date',{exact:true}).fill('2026-10-01');
    await p.getByLabel('End date',{exact:true}).fill('2026-10-02');
    await p.getByLabel('Timezone',{exact:true}).selectOption('America/Indiana/Indianapolis');
    await p.getByLabel('Payment status',{exact:true}).selectOption('All');
    const generated=p.waitForResponse(r=>r.request().method()==='POST'&&r.url().endsWith('/api/reports'));
    await p.getByRole('button',{name:'Generate report',exact:true}).click();const job=await(await generated).json();
    await p.locator('#messages.success').waitFor();
    const download=p.waitForEvent('download');download.catch(()=>{});await p.getByTestId(`download-${job.id}`).click();await download;await pause(250);
    await post('/record/finish');
    const reject=await fetch(base+'/recipe/save',{method:'POST',headers:{'X-Lab-Token':token},body:'{}'});assert.equal(reject.status,400);
    await post('/recipe/save',{parameterizeDates:true});const saved=await get();assert.equal(saved.recipe.recording.length,8);
    console.log('PASS: captures actual browser actions, rejects unreviewed dates, saves parameterized recipe');
    await post('/run',{provider:'replay',mode:'normal',startDate:'2026-09-30',endDate:'2026-09-30'});
    let s=await wait(s=>['verified','stopped'].includes(s.phase));assert(s.result.ok,JSON.stringify(s));assert.equal(s.result.verification.rows_checked,128);
    await post('/import');s=await get();assert.equal(s.publication.metrics.metrics[0].value,'7127.78');
    await post('/import');s=await get();assert.equal(s.publication.batch.status,'duplicate_noop');assert.equal(s.publication.metrics.metrics[0].value,'7127.78');
    console.log('PASS: captured recipe replays new dates; exact CSV imports; independent net-sales ledger and duplicate no-op agree');
    await post('/run',{provider:'replay',mode:'changed-label',startDate:'2026-10-01',endDate:'2026-10-02'});
    s=await wait(s=>['verified','stopped'].includes(s.phase));assert.equal(s.result.type,'label_changed');
    console.log('PASS: recorded deterministic recipe stops on DOM drift');
    await post('/run',{provider:'jev',mode:'changed-label',startDate:'2026-10-01',endDate:'2026-10-02'});
    s=await wait(s=>s.phase==='approval'||s.phase==='stopped');assert.equal(s.phase,'approval',JSON.stringify(s));assert.equal(s.pending.proposed.label,'Build export');
    await post('/approve',{id:s.pending.id,accept:true});s=await wait(s=>['verified','stopped'].includes(s.phase));assert(s.result.ok,JSON.stringify(s));assert.equal(s.result.verification.rows_checked,256);
    assert.equal(s.provider,'injected-test-only');assert.equal(s.recipe.steps.find(x=>x.name==='Generate report').name,'Generate report');
    await post('/import');s=await get();assert.equal(s.publication.metrics.metrics[0].value,'14255.20');
    console.log('PASS: injected Jev proposes renamed control, human approval gates execution, verified 256-row file publishes 14255.20');
    const ui=await browser.newPage();await ui.goto(base);await ui.waitForFunction(()=>document.getElementById('sales').textContent==='$14255.20');
    await ui.waitForFunction(()=>{const img=document.getElementById('viewport');return img.complete&&img.naturalWidth>0;});
    await ui.screenshot({path:path.join(root,'lab.png'),fullPage:true});await ui.close();
    await post('/run',{provider:'jev',mode:'changed-label',startDate:'2026-09-30',endDate:'2026-09-30'});
    s=await wait(s=>s.phase==='approval'||s.phase==='stopped');assert.equal(s.phase,'approval');await post('/approve',{id:s.pending.id,accept:false});
    s=await wait(s=>['verified','stopped'].includes(s.phase));assert.equal(s.result.ok,false);
    const failedImport=await fetch(base+'/import',{method:'POST',headers:{'X-Lab-Token':token},body:'{}'});assert.equal(failedImport.status,400);
    assert.equal(s.publication.metrics.metrics[0].value,'14255.20');
    console.log('PASS: rejected repair stops; failed run cannot import; last-good publication retained');
    await post('/run',{provider:'replay',mode:'session-expired',startDate:'2026-09-30',endDate:'2026-09-30'});
    s=await wait(s=>['verified','stopped'].includes(s.phase));assert.equal(s.result.type,'expired_session');assert.equal(s.publication.metrics.metrics[0].value,'14255.20');
    console.log('PASS: expired-session lab run stops and preserves published evidence');
    fs.writeFileSync(path.join(root,'verification.json'),JSON.stringify({provider:'injected-test-only',status:'pass',root},null,2));console.log('Evidence:',root);
  }finally{await lab.close();await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
