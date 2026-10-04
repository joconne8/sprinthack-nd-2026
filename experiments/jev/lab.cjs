#!/usr/bin/env node
'use strict';
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {spawnSync}=require('node:child_process');
const {chromium}=require('playwright');
const {runSkill}=require('../../acquisition/run_skill.cjs');
const {runJev}=require('./run.cjs'),{JevProvider}=require('./provider.cjs');
const {verifyFile}=require('./verify.cjs'),{recorderScript}=require('./recorder.cjs');
const {buildRecipe,validateRecipe}=require('./recipe.cjs');

async function createLab({baseUrl=process.env.BASE_URL||'http://127.0.0.1:4173',
  stateRoot=path.resolve('.runtime/jev-lab'),headed=true,providerFactory, browser: suppliedBrowser}={}) {
  const url=new URL(baseUrl);
  if(url.protocol!=='http:' || !['127.0.0.1','localhost','[::1]'].includes(url.hostname) || url.username || url.password)
    throw new Error('Lab only supports the local synthetic portal');
  fs.mkdirSync(stateRoot,{recursive:true});
  const token=crypto.randomBytes(24).toString('hex');
  const state={phase:'idle',events:[],recording:[],recipe:null,result:null,publication:null,pending:null,error:null,
    synthetic:true,provider:null,usage:null};
  const savedRecipe=path.join(stateRoot,'recipe.json');
  if(fs.existsSync(savedRecipe)){state.recipe=validateRecipe(JSON.parse(fs.readFileSync(savedRecipe,'utf8')));state.recording=state.recipe.recording;state.phase='ready';}
  let browser=suppliedBrowser,page,recordingContext,recordingDownload=null,recordingJob=null,approval=null,cancelled=false,busy=false,lastScreenshot=null;
  async function capture(p){try{lastScreenshot=await p.screenshot({type:'jpeg',quality:65});}catch{}}
  const emit=(phase,detail)=>{state.events.push({phase,elapsed_ms:Date.now()-(state.began||Date.now()),...detail});};
  async function getBrowser(){
    if(!browser) browser=await chromium.launch({headless:!headed,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
    return browser;
  }
  async function closeRecording(){
    if(page&&!page.isClosed())await capture(page);
    if(recordingContext) await recordingContext.close(); recordingContext=null; page=null;
  }
  async function startRecording(){
    if(busy || state.phase==='recording') throw new Error('Finish the current session first');
    await closeRecording(); state.recording=[];state.events=[];state.recipe=null;state.result=null;state.publication=null;
    state.error=null;recordingDownload=null;recordingJob=null;state.phase='recording';state.began=Date.now();
    recordingContext=await (await getBrowser()).newContext({acceptDownloads:true});
    await recordingContext.route('**/*',route=>new URL(route.request().url()).origin===url.origin?route.continue():route.abort());
    await recordingContext.exposeBinding('recordStep',async(source,event)=>{
      if(state.phase!=='recording' || new URL(source.frame.url()).origin!==url.origin) return;
      state.recording.push(event);emit('record', {step:event.label,action:event.op});
      const entry=event;
      setTimeout(async()=>{
        try{entry.after=await source.page.locator('body').innerText();entry.after=entry.after.slice(0,1500);}catch{entry.after='Page transitioned; next recorded action identifies the destination';}
      },150);
    });
    await recordingContext.addInitScript(recorderScript);
    await recordingContext.addInitScript(()=>sessionStorage.setItem('replica-mode','normal'));
    page=await recordingContext.newPage();
    page.on('response',async response=>{
      if(response.request().method()==='POST' && response.url()===url.origin+'/api/reports'){
        try{const job=await response.json();if(job.id)recordingJob=job.id;}catch{}
      }
    });
    page.on('download',download=>{
      recordingDownload=(async()=>{
        const downloadUrl=new URL(download.url());
        const match=downloadUrl.pathname.match(/^\/api\/reports\/([a-f0-9]+)\/download$/);
        if(!match || downloadUrl.origin!==url.origin) throw new Error('Recording downloaded an unsupported file');
        if(match[1]!==recordingJob)throw new Error('Download the report generated during this recording, not an older report');
        const response=await page.request.get(`${url.origin}/api/reports/${match[1]}/manifest`);
        if(!response.ok()) throw new Error('Recording manifest unavailable');
        const manifest=await response.json();
        const file=path.join(stateRoot,'recording.csv'); await download.saveAs(file);
        const result={ok:true,file,manifest};
        verifyFile(result,manifest.requested_start_date,manifest.requested_end_date);
        if(manifest.source_name!=='upright_replica' || manifest.report_type!=='paid_orders' || !manifest.synthetic)
          throw new Error('Recording did not download the scoped synthetic report');
        return result;
      })();
      recordingDownload.catch(error=>{state.error=error.message;});
    });
    await page.goto(url.origin+'/upright');
  }
  async function finishRecording(){
    if(state.phase!=='recording') throw new Error('No recording active');
    if(!recordingDownload) throw new Error('Generate and download the CSV before finishing recording');
    await recordingDownload;state.phase='review';await closeRecording();
  }
  async function saveRecipe(body){
    if(state.phase!=='review') throw new Error('Finish recording before reviewing');
    state.recipe=buildRecipe(state.recording,{parameterizeDates:body.parameterizeDates===true,recordingVerified:!!recordingDownload});
    fs.writeFileSync(path.join(stateRoot,'recipe.json'),JSON.stringify(state.recipe,null,2));state.phase='ready';
  }
  async function execute(body){
    if(busy || state.phase==='recording') throw new Error('A browser session is already active');
    if(!state.recipe && body.workflow!=='predefined') throw new Error('Record and review a recipe first');
    if(!['replay','jev'].includes(body.provider)) throw new Error('Choose replay or Jev');
    if(!['normal','changed-label','session-expired','missing-report','delayed'].includes(body.mode)) throw new Error('Unsupported scenario');
    const validDate=v=>/^2026-\d{2}-\d{2}$/.test(v||'') && !Number.isNaN(Date.parse(v)) && new Date(v).toISOString().slice(0,10)===v;
    if(!validDate(body.startDate)||!validDate(body.endDate)||body.startDate>body.endDate) throw new Error('Choose valid ordered 2026 dates');
    const recipe=body.workflow==='predefined' ? JSON.parse(fs.readFileSync(path.join(__dirname,'../../acquisition/skills/upright-paid-orders.skill.json'),'utf8')) : validateRecipe(state.recipe);
    if(body.workflow==='predefined')recipe.timeouts_ms.total=60000;
    const provider=body.provider==='jev' ? (providerFactory ? providerFactory(emit) : new JevProvider({emit,deadline:Date.now()+60000})) : null;
    busy=true;cancelled=false;state.phase='running';state.provider=providerFactory&&provider?'injected-test-only':body.provider;
    state.events=[];state.error=null;state.result=null;state.pending=null;state.usage=null;state.began=Date.now();
    const directory=path.join(stateRoot,'runs',crypto.randomUUID());fs.mkdirSync(directory,{recursive:true});
    const skillPath=path.join(directory,'recipe.json');fs.writeFileSync(skillPath,JSON.stringify(recipe,null,2));
    (async()=>{
      try{
        const request={baseUrl:url.origin,startDate:body.startDate,endDate:body.endDate,mode:body.mode,
          outputDir:directory,browser:await getBrowser(),skillPath,headed,
          approve: proposal=>new Promise((resolve,reject)=>{
            state.phase='approval';state.pending={id:crypto.randomUUID(),...proposal};emit('repair_proposed',state.pending);
            const timer=setTimeout(()=>{approval=null;state.pending=null;state.phase='running';reject(new Error('Repair approval timed out'));},15000);
            approval={resolve:()=>{clearTimeout(timer);state.phase='running';state.pending=null;resolve();},
              reject:()=>{clearTimeout(timer);state.phase='running';state.pending=null;reject(new Error('Operator rejected repair'));}};
          }),
          pageSetup:async p=>{page=p;const close=p.close.bind(p);p.close=async(...args)=>{await capture(p);return close(...args);};emit('browser',{message:body.workflow==='predefined'?'Executing predefined synthetic workflow; no video learning':'Executing operator-reviewed recipe'});}};
        let result=provider?await runJev(request,provider,emit):await runSkill(skillPath,request);
        if(cancelled) result={ok:false,type:'cancelled',detail:'Operator cancelled'};
        if(result.ok) result.verification=verifyFile(result,body.startDate,body.endDate);
        state.result=result;state.usage=provider?provider.usage():{model_calls:0};state.phase=result.ok?'verified':'stopped';
        emit(result.ok?'verified':'stop',{result});
        if(result.ok) fs.writeFileSync(path.join(directory,'source.manifest.json'),JSON.stringify(result.manifest,null,2));
        fs.writeFileSync(path.join(directory,'result.json'),JSON.stringify({provider:state.provider,usage:state.usage,result},null,2));
        // A reviewed replacement is a proposal, never silently promoted to the saved recipe.
        const repairs=state.events.filter(e=>e.phase==='repair_approved');
        if(result.ok&&repairs.length) fs.writeFileSync(path.join(directory,'repair-proposal.json'),JSON.stringify({base_version:recipe.skill_version,
          repairs,status:'verified run; separate recipe review required'},null,2));
      }catch(error){state.phase='stopped';state.error=error.code?error.message:'Browser run stopped; inspect evidence';state.result={ok:false,type:error.code||'run_failed'};emit('stop',{error:state.error});}
      finally{fs.writeFileSync(path.join(directory,'trace.jsonl'),state.events.map(e=>JSON.stringify(e)).join('\n')+'\n');busy=false;page=null;approval=null;state.pending=null;}
    })();
  }
  async function importVerified(){
    if(busy||!state.result?.ok) throw new Error('A verified completed acquisition is required');
    const response=spawnSync('python3',[path.join(__dirname,'handoff.py')],{input:JSON.stringify({result:state.result,state_root:path.join(stateRoot,'pipeline')}),encoding:'utf8',timeout:20000});
    if(response.status!==0) throw new Error('Import failed; verified file retained and last-good metrics retained');
    state.publication=JSON.parse(response.stdout);emit('import',{batch:state.publication.batch.status});
    fs.writeFileSync(path.join(path.dirname(state.result.file),'publication.json'),JSON.stringify(state.publication,null,2));
  }
  async function cancel(){cancelled=true;if(approval)approval.reject();if(page)await page.close().catch(()=>{});if(state.phase==='recording'){await closeRecording();state.phase='stopped';}}
  const server=http.createServer(async(req,res)=>{
    const send=(status,body,type='application/json')=>{res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(type==='application/json'?JSON.stringify(body):body);};
    try{
      const host=req.headers.host?.split(':')[0];if(!['127.0.0.1','localhost'].includes(host))return send(403,{error:'Loopback only'});
      if(req.method==='GET'&&req.url==='/')return send(200,fs.readFileSync(path.join(__dirname,'lab.html')),'text/html');
      if(req.method==='GET'&&req.url==='/walkthrough.webm'){
        const file=path.join(stateRoot,'walkthrough.webm');
        if(!fs.existsSync(file))return send(404,{error:'Generate the walkthrough video first'});
        return send(200,fs.readFileSync(file),'video/webm');
      }
      if(req.method==='GET'&&req.url==='/lab.js')return send(200,fs.readFileSync(path.join(__dirname,'lab-ui.js')),'text/javascript');
      if(req.method==='GET'&&req.url==='/state')return send(200,{...state,token,keyConfigured:!!process.env.TYPESAFE_API_KEY,screenshotAvailable:!!lastScreenshot,browserLive:!!page&&!page.isClosed()});
      if(req.method==='GET'&&req.url.split('?')[0]==='/screenshot'){
        if(page&&!page.isClosed())await capture(page);
        if(!lastScreenshot)return send(204,'','image/jpeg');
        return send(200,lastScreenshot,'image/jpeg');
      }
      if(req.method!=='POST'||req.headers['x-lab-token']!==token)return send(403,{error:'Local session token required'});
      if(req.headers.origin && !['http://'+req.headers.host].includes(req.headers.origin))return send(403,{error:'Origin mismatch'});
      let raw='';for await(const chunk of req){raw+=chunk;if(raw.length>65536)throw new Error('Request too large');}
      const body=JSON.parse(raw||'{}');
      if(req.url==='/record/start')await startRecording();
      else if(req.url==='/record/finish')await finishRecording();
      else if(req.url==='/recipe/save')await saveRecipe(body);
      else if(req.url==='/run')await execute(body);
      else if(req.url==='/approve'){
        if(!approval||body.id!==state.pending?.id)throw new Error('No matching repair pending');
        const pending=state.pending;emit(body.accept?'repair_approved':'repair_rejected',{proposal:pending});
        body.accept?approval.resolve():approval.reject();approval=null;
      }else if(req.url==='/import')await importVerified();
      else if(req.url==='/cancel')await cancel();
      else return send(404,{error:'Unknown operation'});
      return send(200,{ok:true});
    }catch(error){send(400,{error:error.code?error.message:error.message});}
  });
  return {server,state,get page(){return page;},async close(){await cancel();await closeRecording();if(browser&&!suppliedBrowser)await browser.close();await new Promise(resolve=>server.close(resolve));}};
}
if(require.main===module)(async()=>{
  const lab=await createLab({headed:!process.argv.includes('--headless')});
  lab.server.listen(Number(process.env.LAB_PORT||4190),'127.0.0.1',()=>console.log('Synthetic Jev workflow lab: http://127.0.0.1:'+(process.env.LAB_PORT||4190)));
  process.on('SIGINT',async()=>{await lab.close();process.exit(0);});
})().catch(e=>{console.error(e.message);process.exitCode=1;});
module.exports={createLab};
