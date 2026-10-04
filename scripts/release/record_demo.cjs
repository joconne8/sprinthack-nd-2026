const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL, output = process.env.DEMO_OUTPUT;
const phases = JSON.parse(fs.readFileSync(process.env.DEMO_PHASES));
(async () => {
  const browser = await chromium.launch({headless:true, ...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
  const context = await browser.newContext({viewport:{width:1440,height:900}, recordVideo:{dir:output,size:{width:1440,height:900}}});
  const page = await context.newPage(); page.setDefaultTimeout(15000);
  const errors = []; page.on('pageerror', e => errors.push(e.message));
  const beginning = Date.now(), timeline = [];
  async function scene(number, action) {
    const phase = phases[number], start = (Date.now()-beginning)/1000;
    await page.evaluate(({label,text}) => {
      let node = document.querySelector('#recorded-demo-caption');
      if(!node) {node=document.createElement('div');node.id='recorded-demo-caption';document.body.append(node);}
      Object.assign(node.style,{position:'fixed',left:'240px',right:'24px',bottom:'14px',zIndex:'10000',padding:'16px 22px',background:'#142e45',color:'white',borderRadius:'10px',fontFamily:'Arial, sans-serif',pointerEvents:'none',boxShadow:'0 8px 30px #0003'});
      node.replaceChildren();const title=document.createElement('strong');title.textContent=label;node.append(title,document.createElement('br'),document.createTextNode(text));
    }, {label:`RECORDED SYNTHETIC DEMO · ${number+1}/${phases.length} · ${phase.title}`,text:phase.caption});
    await action();
    await page.waitForTimeout(Math.max(1200, (phase.duration+1)*1000-(Date.now()-beginning-start*1000)));
    timeline.push({...phase,start,end:(Date.now()-beginning)/1000});
  }
  const loaded = () => page.locator('#metrics-content[aria-busy="false"]').waitFor();
  async function collect(start,end,mode='normal') {
    await page.getByRole('link',{name:'Report intake',exact:true}).click();
    await page.locator('#request-start').fill(start);await page.locator('#request-end').fill(end);
    await page.locator('.demo-options').evaluate(node=>node.open=true);
    await page.locator('#request-mode').selectOption(mode);await page.locator('#collect-button').click();
    await page.waitForFunction(()=>!document.querySelector('#collect-button').disabled,{},{timeout:25000});
  }
  try {
    await page.goto(base);await loaded();
    await scene(0,async()=>{assert.equal(await page.locator('[data-metric-id="M-DEMO-NET-SALES"]').textContent(),'Unavailable');});
    await scene(1,async()=>{await collect('2026-09-30','2026-09-30');assert((await page.locator('#run-history').textContent()).includes('succeeded'));await page.screenshot({path:path.join(output,'operations.png'),fullPage:true});});
    await scene(2,async()=>{await page.getByRole('link',{name:'Leadership pulse',exact:true}).click();await loaded();assert.equal(await page.locator('[data-metric-id="M-DEMO-NET-SALES"]').textContent(),'$7,127.78');await page.screenshot({path:path.join(output,'leadership.png'),fullPage:true});});
    await scene(3,async()=>{await page.locator('[data-testid="evidence-open"]').click();await page.locator('#evidence-content').waitFor();await page.getByRole('button',{name:'Inspect row',exact:true}).first().click();await page.locator('#row-detail').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(output,'source.png'),fullPage:true});});
    await scene(4,async()=>{await collect('2026-10-01','2026-10-02');await page.getByRole('link',{name:'Leadership pulse',exact:true}).click();await loaded();assert.equal(await page.locator('[data-metric-id="M-DEMO-NET-SALES"]').textContent(),'$14,255.20');});
    await scene(5,async()=>{await collect('2026-10-01','2026-10-02');assert((await page.locator('#run-history').textContent()).includes('duplicate noop'));});
    await scene(6,async()=>{await collect('2026-10-01','2026-10-02','session-expired');assert((await page.locator('#collection-status').textContent()).includes('Next owner'));await page.screenshot({path:path.join(output,'safe-failure.png'),fullPage:true});});
    await scene(7,async()=>{await page.getByRole('link',{name:'Leadership pulse',exact:true}).click();await loaded();assert.equal(await page.locator('[data-metric-id="R-MARGIN"]').textContent(),'Unavailable');});
    assert.deepEqual(errors,[]);
  } finally {
    const video=page.video();await context.close();await video.saveAs(path.join(output,'demo-original.webm'));await browser.close();
  }
  fs.writeFileSync(path.join(output,'timeline.json'),JSON.stringify({passed:true,recording:'Actual browser interactions; fictional source data; offline synthetic voiceover',phases:timeline},null,2)+'\n');
  console.log('PASS: recorded actual collection, dashboard, source rows, alternate dates, replay and failure');
})().catch(error=>{console.error(error);process.exitCode=1;});
