// Actual application interactions shared by capture and narrated recording.
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),crypto=require('node:crypto');
const base=process.env.BASE_URL, output=path.resolve(process.env.SHOWCASE_OUTPUT||'presentation/aimsigh');
if(!base||!/^http:\/\/(127\.0\.0\.1|localhost):\d+$/.test(base))throw Error('BASE_URL must be a local HTTP origin');
const phases=process.env.DEMO_PHASES?JSON.parse(fs.readFileSync(process.env.DEMO_PHASES)):null;

async function walkthrough(page,context){
  fs.mkdirSync(path.join(output,'captures'),{recursive:true});fs.mkdirSync(path.join(output,'exports'),{recursive:true});
  const errors=[],timeline=[],results={},started=Date.now();page.setDefaultTimeout(20000);page.on('pageerror',e=>errors.push(e.message));
  async function get(relative){const response=await page.request.get(base+relative);assert.equal(response.status(),200,relative);return response.json()}
  async function scene(index,action){
    const start=(Date.now()-started)/1000;
    if(phases)await page.evaluate(({title,caption})=>{
      let node=document.querySelector('#walkthrough-caption');if(!node){node=document.createElement('div');node.id='walkthrough-caption';document.body.append(node)}
      Object.assign(node.style,{position:'fixed',left:'282px',right:'22px',bottom:'10px',zIndex:'10000',padding:'12px 20px',background:'#1c2521',color:'#fffef9',borderRadius:'8px',font:'16px Arial',pointerEvents:'none'});
      node.replaceChildren();const strong=document.createElement('strong');strong.textContent='RECORDED SCRIPTED LOCAL SHOWCASE · '+title;node.append(strong,document.createElement('br'),document.createTextNode(caption))
    },phases[index]);
    await action();
    if(phases)await page.waitForTimeout(Math.max(0,phases[index].duration*1000-(Date.now()-started-start*1000)));
    timeline.push({index,title:phases?.[index].title||String(index),start,end:(Date.now()-started)/1000});
  }
  async function capture(name,selector){
    if(selector){await page.locator(selector).scrollIntoViewIfNeeded();await page.waitForTimeout(250)}
    // Capture the actual viewport fully; the deck uses contain, never crops financial UI.
    await page.screenshot({path:path.join(output,'captures',name+'.png')});
  }
  async function metricsReady(){await page.locator('#metric-cards[aria-busy="false"]').waitFor();assert(await page.locator('[data-metric-id="net_sales"]').count())}
  async function run(recipe){
    if(recipe)await page.locator('#run-recipe').selectOption(recipe);
    const pending=page.waitForResponse(r=>r.url()===base+'/api/showcase/v1/runs'&&r.request().method()==='POST');
    await page.locator('#run-button').click();const request=await pending;assert([200,201,202].includes(request.status()));const created=await request.json();
    let result;const deadline=Date.now()+65000;
    do{result=await get('/api/showcase/v1/runs/'+created.run_id);if(['succeeded','needs_human'].includes(result.status))break;await page.waitForTimeout(500)}while(Date.now()<deadline);
    assert.equal(result.status,'succeeded',JSON.stringify(result));await page.locator('#run-button:not([disabled])').waitFor();results[result.source]=result;return result;
  }
  await page.goto(base+'/showcase');await metricsReady();const initial=await get('/api/showcase/v1/snapshot');
  assert(initial.sources.some(s=>s.coverage.missing_days.includes('2026-09-30')),'Use demo prepare/reset rehearsal state, not complete checkpoint');
  await scene(0,async()=>{results.initial_snapshot=initial;await capture('initial-dashboard');await page.locator('nav a[href="#collect"]').click()});
  await scene(1,async()=>{
    await page.locator('#record-source').selectOption('upright_replica');await page.locator('#record-start').click();
    const portal=page.frameLocator('#portal-frame');await portal.getByRole('link',{name:/Reports/,exact:false}).first().click();await portal.getByRole('link',{name:'Paid orders',exact:true}).click();
    await portal.locator('#start-date').fill('2026-09-29');await portal.locator('#end-date').fill('2026-09-29');await portal.locator('#timezone').selectOption('America/Indiana/Indianapolis');await portal.locator('#payment-status').selectOption('All');
    await portal.locator('#generate-report').click();await portal.getByRole('link',{name:'Download',exact:true}).first().waitFor();
    const download=page.waitForEvent('download');await portal.getByRole('link',{name:'Download',exact:true}).first().click();await(await download).saveAs(path.join(output,'exports','training-september29.csv'));
    await page.locator('#record-review:not([disabled])').click();await page.locator('#record-approve:not([disabled])').waitFor();await capture('recording','#recording-status');
    const reviewed=JSON.parse(await page.locator('#recipe-preview').textContent());fs.writeFileSync(path.join(output,'exports','reviewed-recipe.json'),JSON.stringify(reviewed,null,2)+'\n');
    const approvedRequest=page.waitForResponse(r=>r.url().endsWith('/approve')&&r.request().method()==='POST');await page.locator('#record-approve').click();const approved=await(await approvedRequest).json();
    await page.waitForFunction(id=>!document.querySelector('#run-button').disabled&&document.querySelector('#run-recipe').value===id,approved.recipe_id);
  });
  await scene(2,async()=>{
    await page.locator('#run-start').fill('2026-09-30');await page.locator('#run-end').fill('2026-09-30');assert.equal(await page.locator('#run-mode').inputValue(),'normal');
    const upright=await run();assert.equal(upright.source,'upright_replica');await capture('collection','#run-status');
    const cash=await page.locator('#run-recipe option').evaluateAll(options=>options.find(option=>option.textContent.startsWith('Cash Monkey')).value);await run(cash);
    results.snapshot=await get('/api/showcase/v1/snapshot');assert(results.snapshot.sources.every(s=>s.coverage.state==='complete'));await capture('collection','#run-status');
  });
  await scene(3,async()=>{
    await page.locator('nav a[href="#deliver"]').click();const download=page.waitForEvent('download');await page.locator('#workbook-download').click();const workbook=path.join(output,'exports','september2026.xlsx');await(await download).saveAs(workbook);
    cp.execFileSync(process.env.PYTHON||'python3',[path.resolve('scripts/release/showcase_workbook_preview.py'),'--workbook',workbook,'--output',path.join(output,'exports','workbook-preview.html')],{stdio:'inherit'});
    await page.goto('file://'+path.join(output,'exports','workbook-preview.html'));await page.screenshot({path:path.join(output,'captures','workbook.png')});
    if(phases)await page.waitForTimeout(Math.max(0,phases[3].duration*1000-3000));await page.goto(base+'/showcase#deliver');await page.locator('#workbook-download[href]').waitFor();await capture('delivery');
  });
  await scene(4,async()=>{
    await page.locator('nav a[href="#understand"]').click();await metricsReady();await capture('dashboard','#understand-heading');
    const snapshot_id=results.snapshot.snapshot_id;results.metrics=await get('/api/showcase/v1/metrics?snapshot_id='+snapshot_id);assert.equal(await page.locator('[data-metric-id="net_sales"]').getAttribute('data-value'),results.metrics.metrics.find(m=>m.metric_id==='net_sales').value);
  });
  await scene(5,async()=>{
    const snapshot_id=results.snapshot.snapshot_id;results.comparison=await get('/api/showcase/v1/comparison?snapshot_id='+snapshot_id);
    const metric=(r,id)=>r.metrics.find(m=>m.metric_id===id).value;
    assert.equal(metric(results.comparison.previous,'net_sales'),'60727.56');assert.equal(metric(results.comparison.current,'net_sales'),'61706.64');assert.equal(metric(results.comparison.previous,'labor_hours'),'420.00');assert.equal(metric(results.comparison.current,'labor_hours'),'588.00');assert.equal(results.comparison.verified_cause,false);
    await capture('comparison','#comparison-content');
  });
  await scene(6,async()=>{
    await page.locator('#question').fill('Why is revenue per labor hour down?');const pending=page.waitForResponse(r=>r.url()===base+'/api/showcase/v1/questions'&&r.request().method()==='POST');await page.locator('#ask-button').click();const response=await pending;assert.equal(response.status(),200);results.answer=await response.json();assert.equal(results.answer.intent,'productivity');assert.equal(results.answer.snapshot_id,results.snapshot.snapshot_id);assert(results.answer.citations.length>=2);
    await page.waitForFunction(()=>document.querySelector('#messages').textContent.includes('144.59')&&document.querySelector('#messages').textContent.includes('104.94'));
    await capture('conversation','#messages');await page.getByRole('link',{name:'Current period labor/cost inputs',exact:true}).click();await page.locator('#evidence-dialog[open]').waitFor();await page.waitForFunction(()=>document.querySelector('#evidence-loading').textContent==='');await capture('labor-evidence');await page.locator('#evidence-close').click();
    await page.locator('#comparison-evidence').click();await page.locator('#evidence-dialog[open]').waitFor();await page.waitForFunction(()=>document.querySelector('#evidence-loading').textContent==='');await capture('evidence');await page.locator('#evidence-close').click();
  });
  await scene(7,async()=>{
    await page.locator('#question').fill('Approve the accounting journal and predict next year');const pending=page.waitForResponse(r=>r.url()===base+'/api/showcase/v1/questions'&&r.request().method()==='POST');await page.locator('#ask-button').click();results.unsupported=await(await pending).json();assert.equal(results.unsupported.intent,'unsupported');await capture('unsupported','#messages');
    await page.locator('nav a[href="#deliver"]').click();await capture('final-delivery');
  });
  assert.deepEqual(errors,[]);const capture_sha256=Object.fromEntries(fs.readdirSync(path.join(output,'captures')).filter(file=>file.endsWith('.png')).map(file=>['captures/'+file,crypto.createHash('sha256').update(fs.readFileSync(path.join(output,'captures',file))).digest('hex')]));
  fs.writeFileSync(path.join(output,'capture-verification.json'),JSON.stringify({passed:true,recording:'Scripted Playwright walkthrough of actual local browser interactions; fictional sales; invented labor/cost inputs; no external model',initial_snapshot_id:initial.snapshot_id,snapshot_id:results.snapshot.snapshot_id,capture_sha256,results,timeline},null,2)+'\n');
  console.log('PASS: actual DOM recording, reviewed replay, two-source publication, XLSX, dashboard, comparison, conversation and evidence');return timeline;
}

async function main(){
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const context=await browser.newContext({viewport:{width:1440,height:960},acceptDownloads:true,...(phases?{recordVideo:{dir:path.join(output,'recording'),size:{width:1440,height:960}}}:{})});const page=await context.newPage();
  try{await walkthrough(page,context)}finally{const video=page.video();await context.close();if(video)await video.saveAs(path.join(output,'recording','walkthrough-original.webm'));await browser.close()}
}
if(require.main===module)main().catch(error=>{console.error(error);process.exitCode=1});
module.exports={walkthrough};
