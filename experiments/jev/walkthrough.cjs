#!/usr/bin/env node
'use strict';
// Staged manual-paced browser walkthrough, not a human recording or model training.
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');const {verifyFile}=require('./verify.cjs');
(async()=>{
 const base=new URL(process.env.BASE_URL||'http://127.0.0.1:4173');
 if(base.protocol!=='http:'||!['127.0.0.1','localhost','[::1]'].includes(base.hostname)||base.username||base.password)throw Error('Synthetic loopback portal only');
 const root=path.resolve('.runtime/jev-lab');fs.mkdirSync(root,{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
 try{
 const context=await browser.newContext({acceptDownloads:true,viewport:{width:1280,height:800},recordVideo:{dir:path.join(root,'video-takes'),size:{width:1280,height:800}}});
 await context.route('**/*',r=>new URL(r.request().url()).origin===base.origin?r.continue():r.abort());
 const p=await context.newPage(),video=p.video();const pause=()=>p.waitForTimeout(1600);
 await p.goto(base.origin+'/upright');await pause();
 await p.getByRole('navigation',{name:'Upright navigation'}).getByRole('link',{name:'▥ Reports',exact:true}).click();await pause();
 await p.getByRole('link',{name:'Paid orders',exact:true}).click();await pause();
 await p.getByLabel('Start date',{exact:true}).fill('2026-10-01');await pause();
 await p.getByLabel('End date',{exact:true}).fill('2026-10-02');await pause();
 await p.getByLabel('Timezone',{exact:true}).selectOption('America/Indiana/Indianapolis');await pause();
 await p.getByLabel('Payment status',{exact:true}).selectOption('All');await pause();
 const response=p.waitForResponse(r=>r.request().method()==='POST'&&r.url()===base.origin+'/api/reports');
 await p.getByRole('button',{name:'Generate report',exact:true}).click();const job=await(await response).json();
 await p.locator('#messages.success').waitFor();await pause();
 const pending=p.waitForEvent('download');pending.catch(()=>{});await p.getByTestId(`download-${job.id}`).click();const download=await pending;
 const file=path.join(root,'walkthrough.csv');await download.saveAs(file);
 const manifest=await(await p.request.get(base.origin+`/api/reports/${job.id}/manifest`)).json();
 const verification=verifyFile({ok:true,file,manifest},'2026-10-01','2026-10-02');
 await pause();await context.close();await video.saveAs(path.join(root,'walkthrough.webm'));
 fs.writeFileSync(path.join(root,'walkthrough-evidence.json'),JSON.stringify({synthetic:true,scripted:true,provider:null,manifest,verification},null,2));
 console.log(JSON.stringify({video:path.join(root,'walkthrough.webm'),verification}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e.message);process.exitCode=1;});
