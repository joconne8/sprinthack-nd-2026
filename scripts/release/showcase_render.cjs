// Render every Aimsigh slide and verify offline navigation, media fit and notes.
const {chromium}=require('playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const output=path.resolve('presentation/aimsigh');
(async()=>{
  const build=JSON.parse(fs.readFileSync(path.join(output,'build.json')));
  if(build.draft&&!process.argv.includes('--allow-draft'))throw Error('Refusing to certify draft captures');
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  const errors=[],slides=[];
  try{
    const page=await browser.newPage({viewport:{width:1630,height:1005}});page.on('pageerror',e=>errors.push(e.message));
    await page.goto('file://'+path.join(output,'index.html'));assert.equal(await page.locator('.slide').count(),15);
    fs.mkdirSync(path.join(output,'slides'),{recursive:true});
    for(let i=0;i<15;i++){
      if(i)await page.getByRole('button',{name:'Next →',exact:true}).click();
      const active=page.locator('.slide.active');assert.equal(await active.getAttribute('id'),'slide-'+(i+1));
      const geometry=await active.evaluate(node=>{
        const footer=node.querySelector('footer').getBoundingClientRect();const checks=[...node.querySelectorAll(':scope > h1,:scope > .lead,:scope > .cards,:scope > .source-grid,:scope > .erd,:scope > .erd-note,:scope > .signature,:scope > .product-frame')].map(child=>({element:child.className||child.tagName,bottom:child.getBoundingClientRect().bottom,footer:footer.top}));
        return {overflow:checks.filter(c=>c.bottom>c.footer-7),images:[...node.querySelectorAll('img')].map(image=>({loaded:image.complete&&image.naturalWidth>0,fit:getComputedStyle(image).objectFit})),visible:[...document.querySelectorAll('.slide')].filter(s=>getComputedStyle(s).display!=='none').length};
      });
      assert.deepEqual(geometry.overflow,[],'Slide '+(i+1)+' footer overlap');assert.equal(geometry.visible,1);assert(geometry.images.every(image=>image.loaded&&image.fit==='contain'));
      await active.screenshot({path:path.join(output,'slides',String(i+1).padStart(2,'0')+'.png')});slides.push({slide:i+1,...geometry});
    }
    await page.keyboard.press('Home');assert.equal(await page.locator('.slide.active').getAttribute('id'),'slide-1');await page.keyboard.press('ArrowRight');assert.equal(await page.locator('.slide.active').getAttribute('id'),'slide-2');
    await page.getByRole('button',{name:'Speaker notes (N)',exact:true}).click();assert(await page.locator('.notes').isVisible());assert((await page.locator('#note-text').textContent()).includes('interview estimate'));
    await page.keyboard.press('Escape');assert(!(await page.locator('.notes').isVisible()));
    await page.getByRole('button',{name:'Recorded backup',exact:true}).click();assert(await page.locator('.video-modal').isVisible());await page.getByRole('button',{name:'Close recording',exact:true}).click();
    await page.emulateMedia({media:'print'});await page.pdf({path:path.join(output,'aimsigh-showcase.pdf'),preferCSSPageSize:true,printBackground:true});assert.deepEqual(errors,[]);
    fs.writeFileSync(path.join(output,'slides-verification.json'),JSON.stringify({passed:!build.draft,draft:build.draft,slide_count:15,duration_seconds:900,offline_navigation:true,speaker_notes:true,pdf:'aimsigh-showcase.pdf',screenshots_contained:true,slides},null,2)+'\n');
    console.log('PASS: all 15 '+(build.draft?'draft ':'')+'slides rendered; navigation, notes, media fit and PDF verified');
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
