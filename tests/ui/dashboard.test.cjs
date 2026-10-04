// Developer UI regressions; Jack mc owns independent acceptance separately.
const assert=require('node:assert/strict');
const fs=require('node:fs');const path=require('node:path');
const crypto=require('node:crypto');
const {chromium}=require('playwright');
const base=process.env.BASE_URL;const out=process.env.OUTPUT_DIR;
const failures=[];const comparisons=[];
(async()=>{
  fs.mkdirSync(out,{recursive:true});
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  page.on('pageerror',error=>failures.push(error.message));
  const json=async route=>{const response=await page.request.get(base+route);assert(response.ok(),await response.text());return response.json();};
  const value=()=>page.locator('[data-metric-id="M-DEMO-NET-SALES"]');
  const loaded=()=>page.locator('#metrics-content[aria-busy="false"]').waitFor();
  const compare=async filters=>{
    const expected=await json('/api/v1/metrics?'+new URLSearchParams(filters));
    await loaded();assert.equal(await value().getAttribute('data-value'),expected.metrics[0].value??'');
    comparisons.push({filters,api:expected.metrics[0].value,ui:await value().textContent()});return expected;
  };
  async function collect(start,end,mode='normal'){
    await page.goto(base+'/#operations');await page.locator('#request-start').fill(start);await page.locator('#request-end').fill(end);
    if(mode!=='normal'){await page.getByText('Demo failure scenario',{exact:true}).click();await page.locator('#request-mode').selectOption(mode);}
    await page.locator('#collect-button').click();
    await page.waitForFunction(()=>!document.querySelector('#collect-button').disabled,{},{timeout:20000});
    const history=await json('/api/v1/acquisition-runs');return history.runs[0];
  }
  try{
    await page.goto(base);await loaded();assert.equal(await value().textContent(),'Unavailable');
    assert(await page.locator('.disclosure').innerText().then(text=>text.includes('Synthetic demo')));
    const first=await collect('2026-09-30','2026-09-30');assert.equal(first.status,'succeeded');assert.equal(first.import_state,'imported');assert.equal(first.coverage_state,'complete');
    await page.getByRole('link',{name:'Leadership pulse',exact:true}).click();
    const scope={start_date:'2026-09-30',end_date:'2026-09-30',source:'upright_replica'};
    const displayed=await compare(scope);assert.equal(displayed.metrics[0].value,'7127.78');
    await page.screenshot({path:path.join(out,'leadership.png'),fullPage:true});
    assert.equal(await page.locator('[data-metric-id="R-MARGIN"]').textContent(),'Unavailable');
    await page.locator('[data-testid="evidence-open"]').click();await page.locator('#evidence-content').waitFor();
    assert.equal(await page.locator('#evidence-scope-total').getAttribute('data-value'),'7127.78');
    assert((await page.locator('#evidence-run').textContent()).includes(displayed.metric_run_id));
    await page.locator('#evidence-next').click();await page.getByText('Rows 51–100 of 128',{exact:true}).waitFor();
    await page.getByRole('button',{name:'Inspect row',exact:true}).first().click();await page.locator('#row-detail pre').waitFor();
    assert((await page.locator('#row-detail pre').textContent()).includes('paid_order_id'));
    await page.screenshot({path:path.join(out,'source-evidence.png'),fullPage:true});
    await page.getByRole('link',{name:'Back to pulse',exact:true}).click();
    await page.locator('#metric-platform').selectOption('eBay');await page.locator('#metric-store').selectOption('GW-001');await page.getByRole('button',{name:'Apply filters',exact:true}).click();
    await compare({...scope,platform:'eBay',store:'GW-001'});
    const alternative=await collect('2026-10-01','2026-10-02');assert.equal(alternative.row_count,256);assert.equal(alternative.status,'succeeded');
    const repeated=await collect('2026-10-01','2026-10-02');assert.equal(repeated.import_state,'duplicate_noop');
    const denied=await collect('2026-10-01','2026-10-02','session-expired');assert.equal(denied.status,'needs_human');assert.equal(denied.attempts.length,1);assert.equal(denied.import_state,'not_submitted');
    assert((await page.locator('#collection-status').textContent()).includes('Next owner'));
    await page.screenshot({path:path.join(out,'operations.png'),fullPage:true});
    const batch=await json('/api/v1/imports/'+first.batch_id);const manifest=await json('/api/v1/imports/'+first.batch_id+'/manifest');
    const raw=await (await page.request.get(base+'/api/v1/files/'+batch.file.file_id)).body();
    assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),first.checksum);
    assert.equal(first.checksum,batch.file.checksum);assert.equal(manifest.file_checksum,first.checksum);
    assert.equal(manifest.acquisition_run_id,first.run_id);assert.equal(manifest.payment_status,'All');
    fs.writeFileSync(path.join(out,'checksum-chain.json'),JSON.stringify({run:first,manifest,batch_id:batch.batch_id,archived_sha256:crypto.createHash('sha256').update(raw).digest('hex'),same_bytes_verified:true},null,2)+'\n');
    fs.writeFileSync(path.join(out,'download-manifests.json'),JSON.stringify([manifest,await json('/api/v1/imports/'+alternative.batch_id+'/manifest')],null,2)+'\n');
    const file=path.join(process.env.QA_TEMP,'upload.csv');const metadata=path.join(process.env.QA_TEMP,'upload.json');fs.writeFileSync(file,raw);fs.writeFileSync(metadata,JSON.stringify(manifest));
    await page.locator('#csv-file').setInputFiles(file);await page.locator('#manifest-file').setInputFiles(metadata);await page.locator('#upload-button').click();
    await page.getByText('This report was already imported. Published totals are unchanged.',{exact:true}).waitFor();
    manifest.file_checksum='0'.repeat(64);fs.writeFileSync(metadata,JSON.stringify(manifest));await page.locator('#manifest-file').setInputFiles(metadata);await page.locator('#upload-button').click();
    await page.locator('#upload-status').filter({hasText:'Import was not published.'}).waitFor();
    await page.getByRole('link',{name:'Leadership pulse',exact:true}).click();await loaded();
    await page.locator('#freshness-warning').waitFor();assert.equal(await value().getAttribute('data-value'),'7127.78');
    await page.route('**/api/v1/metrics?*',route=>route.fulfill({status:500,contentType:'application/json',body:JSON.stringify({error:{detail:'Injected API outage'}})}));
    await page.getByRole('button',{name:'Apply filters',exact:true}).click();await page.locator('#global-error').filter({hasText:'Injected API outage'}).waitFor();assert.equal(await value().count(),0);
    await page.unroute('**/api/v1/metrics?*');await page.getByRole('button',{name:'Apply filters',exact:true}).click();await loaded();
    await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
    await page.locator('#metric-platform').selectOption('GoodwillBooks');
    await page.getByRole('button',{name:'Apply filters',exact:true}).click();await loaded();
    // A verified complete source with no rows in a marketplace has a real zero.
    await compare({...scope,platform:'GoodwillBooks'});assert.equal(await value().textContent(),'$0.00');
    await page.locator('#metric-source').selectOption('cash_monkey_replica');await page.locator('#metric-platform').selectOption('');
    await page.getByRole('button',{name:'Apply filters',exact:true}).click();await loaded();
    assert.equal(await value().textContent(),'Unavailable');
    assert.deepEqual(failures,[]);
    fs.writeFileSync(path.join(out,'comparisons.json'),JSON.stringify({passed:true,comparisons,checks:['empty state','real collection and publication','alternate dates','repeat no-op','expired session owner/no retry','manual replay','failed import/last-good','store/platform filters','pinned evidence/pagination','source row','API outage/no mock','mobile layout','verified empty scope is zero / missing source unavailable','no browser script errors']},null,2)+'\n');
    console.log('PASS: complete operator → acquisition → verified import → leadership → pinned source-evidence flow; negatives and mobile layout.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
