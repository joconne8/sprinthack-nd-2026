#!/usr/bin/env node
'use strict';
const http=require('node:http'),crypto=require('node:crypto'),fs=require('node:fs'),path=require('node:path');
const {spawn}=require('node:child_process');
const {createLab}=require('../lab.cjs');const {verifyFile}=require('../verify.cjs');
const digest=s=>crypto.createHash('sha256').update(s).digest();
async function createHosted({lab,password=process.env.DEMO_PASSWORD,maxRuns=Number(process.env.HOSTED_MAX_RUNS||5)}={}){
 if(typeof password!=='string'||password.length<16)throw Error('Set DEMO_PASSWORD to at least 16 characters');
 if(!Number.isInteger(maxRuns)||maxRuns<1||maxRuns>50)throw Error('HOSTED_MAX_RUNS must be 1–50');
 if(!lab?.server.listening)throw Error('Internal lab must be listening');
 const internal=`http://127.0.0.1:${lab.server.address().port}`;let runs=0;
 const server=http.createServer(async(req,res)=>{
  const send=(status,body,type='application/json')=>{res.writeHead(status,{'Content-Type':type,'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY','Content-Security-Policy':"default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'"});res.end(type==='application/json'&&!Buffer.isBuffer(body)?JSON.stringify(body):body);};
  try{
   const url=new URL(req.url,'http://localhost');
   if(req.method==='GET'&&url.pathname==='/health')return send(200,{ok:true,synthetic:true});
   const auth=req.headers.authorization||'';let supplied='';
   if(auth.startsWith('Basic '))supplied=Buffer.from(auth.slice(6),'base64').toString('utf8');
   if(!crypto.timingSafeEqual(digest(supplied),digest('demo:'+password))){res.setHeader('WWW-Authenticate','Basic realm="Synthetic Jev demo", charset="UTF-8"');return send(401,{error:'Sign in as demo with your demo password'});}
   if(req.method==='GET'&&url.pathname==='/')return send(200,fs.readFileSync(path.join(__dirname,'index.html')),'text/html');
   if(req.method==='GET'&&url.pathname==='/app.js')return send(200,fs.readFileSync(path.join(__dirname,'app.js')),'text/javascript');
   if(req.method==='GET'&&['/download/csv','/download/manifest','/download/trace'].includes(url.pathname)){
    const result=lab.state.result;
    if(!result?.ok||['running','approval','recording'].includes(lab.state.phase))return send(409,{error:'A completed verified download is required'});
    verifyFile(result,result.manifest.requested_start_date,result.manifest.requested_end_date);
    const kind=url.pathname.split('/').at(-1);
    const file=kind==='csv'?result.file:path.join(path.dirname(result.file),kind==='manifest'?'source.manifest.json':'trace.jsonl');
    res.setHeader('Content-Disposition',`attachment; filename="${kind==='csv'?'paid-orders.csv':kind==='manifest'?'source.manifest.json':'trace.jsonl'}"`);
    return send(200,fs.readFileSync(file),kind==='csv'?'text/csv':kind==='manifest'?'application/json':'application/x-ndjson');
   }
   const allowed=req.method==='GET'?['/state','/screenshot']:req.method==='POST'?['/run','/approve','/cancel']:[];
   if(!allowed.includes(url.pathname))return send(404,{error:'Unknown operation'});
   let body;
   if(req.method==='POST'){
    // Browser POSTs must carry the session token and originate on this public host.
    if(!req.headers.origin)return send(403,{error:'Same-origin request required'});
    const origin=new URL(req.headers.origin);
    if(!['https:','http:'].includes(origin.protocol)||origin.host!==req.headers.host)return send(403,{error:'Origin rejected'});
    const state=await(await fetch(internal+'/state')).json();
    if(req.headers['x-lab-token']!==state.token)return send(403,{error:'Session token required'});
    let raw='';for await(const chunk of req){raw+=chunk;if(raw.length>8192)return send(413,{error:'Request too large'});}
    body=JSON.parse(raw||'{}');
    if(url.pathname==='/run'){
     if(['running','approval','recording'].includes(state.phase))return send(409,{error:'A run is already active'});
     if(runs>=maxRuns)return send(429,{error:'Demo run budget exhausted; operator restart required'});
     runs++; // Count admitted attempts, including invalid parameters; concurrent requests cannot exceed the cap.
     body={provider:body.provider,mode:body.mode,startDate:body.startDate,endDate:body.endDate,workflow:'predefined'};
    }
   }
   const response=await fetch(internal+url.pathname+url.search,{method:req.method,headers:req.method==='POST'?{'Content-Type':'application/json','X-Lab-Token':req.headers['x-lab-token']}:{},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(15000)});
   if(url.pathname==='/state'){
    const state=await response.json();state.hosted={runsUsed:runs,maxRuns};
    // Hide server filesystem paths; downloads are served only through verified routes.
    if(state.result)state.result={ok:state.result.ok,type:state.result.type,manifest:state.result.manifest,sha256:state.result.sha256,verification:state.result.verification};
    state.events=state.events.map(e=>e.result?{...e,result:{ok:e.result.ok,type:e.result.type,manifest:e.result.manifest,sha256:e.result.sha256}}:e);
    return send(response.status,state);
   }
   return send(response.status,Buffer.from(await response.arrayBuffer()),response.headers.get('content-type')||'application/json');
  }catch{send(400,{error:'Request failed; inspect the operator evidence'});}
 });
 server.requestTimeout=20000;server.headersTimeout=10000;
 return {server,async close(){await new Promise(r=>server.close(r));}};
}
async function start(){
 // Fail closed before opening any ports or starting the portal.
 if(!process.env.DEMO_PASSWORD||process.env.DEMO_PASSWORD.length<16)throw Error('Configure DEMO_PASSWORD (16+ characters) in Replit Secrets');
 const root=path.resolve(__dirname,'../../..');
 const probe=http.createServer();
 await new Promise(r=>probe.listen(0,'127.0.0.1',r));
 const freePort=probe.address().port;await new Promise(r=>probe.close(r));
 const portalPort=Number(process.env.INTERNAL_PORT||freePort);
 if(!Number.isInteger(portalPort)||portalPort<1024||portalPort>65535)throw Error('Invalid INTERNAL_PORT');
 const child=spawn('python3',[path.join(root,'data ingestion/server.py'),'--host','127.0.0.1','--port',String(portalPort)],{cwd:root,stdio:['ignore','ignore','inherit'],env:{PATH:process.env.PATH,LANG:process.env.LANG,PYTHONUNBUFFERED:'1'}});
 let exited=false;child.on('exit',()=>{exited=true;});child.on('error',()=>{exited=true;});
 let lab,hosted;
 try{
  const deadline=Date.now()+10000;let ready=false;
  while(Date.now()<deadline&&!exited){try{const r=await fetch(`http://127.0.0.1:${portalPort}/upright`,{signal:AbortSignal.timeout(500)});if(r.ok){ready=true;break;}}catch{}await new Promise(r=>setTimeout(r,100));}
  if(!ready||exited)throw Error('Internal synthetic portal failed to start');
  lab=await createLab({baseUrl:`http://127.0.0.1:${portalPort}`,stateRoot:path.join(root,'.runtime/jev-hosted'),headed:false});
  await new Promise(r=>lab.server.listen(0,'127.0.0.1',r));
  hosted=await createHosted({lab});
  await new Promise((resolve,reject)=>{hosted.server.once('error',reject);hosted.server.listen(Number(process.env.PORT||3000),'0.0.0.0',resolve);});
  console.log('Hosted synthetic Jev demo listening; key configured: '+Boolean(process.env.TYPESAFE_API_KEY));
  const close=async()=>{await hosted.close();await lab.close();child.kill();process.exit(0);};
  process.once('SIGINT',close);process.once('SIGTERM',close);
  child.once('exit',()=>{console.error('Internal portal stopped');close();});
 }catch(e){if(hosted)await hosted.close();if(lab)await lab.close();child.kill();throw e;}
}
if(require.main===module)start().catch(e=>{console.error(e.message);process.exitCode=1;});
module.exports={createHosted};
