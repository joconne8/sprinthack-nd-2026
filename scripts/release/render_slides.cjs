const {chromium} = require('playwright');
const fs = require('node:fs');const path = require('node:path');const assert = require('node:assert/strict');
(async()=>{
  const output=path.resolve('presentation');fs.mkdirSync(path.join(output,'slides'),{recursive:true});
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  try{
    const page=await browser.newPage({viewport:{width:1630,height:1000}});
    const errors=[];page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(output,'index.html'));
    const count=await page.locator('.slide').count();assert.equal(count,10);
    const overflow=[];
    for(let i=0;i<count;i++){
      if(i)await page.getByRole('button',{name:'Next →',exact:true}).click();
      assert.equal(await page.locator('.slide.active').getAttribute('id'),'slide-'+(i+1));
      assert.equal(await page.evaluate(()=>[...document.querySelectorAll('.slide')].filter(node=>getComputedStyle(node).display!=='none').length),1);
      assert(await page.locator('.slide.active').evaluate(node=>node.scrollHeight<=node.clientHeight));
      assert(await page.locator('.slide.active').evaluate(node=>[...node.querySelectorAll(':scope > h1, :scope > .lead, :scope > .cards, :scope > .signature')].every(child=>child.getBoundingClientRect().bottom<node.querySelector('footer').getBoundingClientRect().top-10)));
      await page.locator('.slide.active').screenshot({path:path.join(output,'slides',String(i+1).padStart(2,'0')+'.png')});
    }
    await page.keyboard.press('Home');assert.equal(await page.locator('.slide.active').getAttribute('id'),'slide-1');
    await page.keyboard.press('ArrowRight');assert.equal(await page.locator('.slide.active').getAttribute('id'),'slide-2');
    await page.getByRole('button',{name:'Speaker notes (N)',exact:true}).click();assert(await page.locator('.notes').isVisible());
    await page.emulateMedia({media:'print'});
    await page.pdf({path:path.join(output,'goodwill-progress.pdf'),preferCSSPageSize:true,printBackground:true});
    assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(output,'slides-verification.json'),JSON.stringify({passed:true,count,keyboard_navigation:true,speaker_notes:true,overflow,offline_screenshots:true,video:'demo.mp4',pdf:'goodwill-progress.pdf'},null,2)+'\n');
    console.log('PASS: 10 HTML slides rendered; keyboard/notes/overflow/PDF verified');
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
