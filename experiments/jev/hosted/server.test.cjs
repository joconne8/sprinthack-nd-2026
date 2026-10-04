'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {createLab}=require('../lab.cjs'),{createHosted}=require('./server.cjs'),{JevProvider}=require('../provider.cjs');
const factory=emit=>new JevProvider({key:'injected-only',emit,fetchFn:async(_,options)=>{
 const q=JSON.parse(options.body),g=q.state.goal;
 const c=q.state.controls.find(c=>q.state.requested_field_label?c.label===q.state.requested_field_label:g.includes('Generate the')?c.role==='button':g.includes('verified current')?true:g.includes('Paid orders')?c.label==='Paid orders':c.href==='/upright/reports');assert(c);
 return {ok:true,json:async()=>({model:'jev-1.13.0',answers:{target:{type:'choice',choice:c.id,confidence:1,probabilities:Object.fromEntries(['STOP',...q.state.controls.map(c=>c.id)].map(id=>[id,id===c.id?1:0]))}},usage:{input_tokens:1,output_tokens:1}})};
}});
(async()=>{
 await assert.rejects(()=>createHosted({password:'short'}),/DEMO_PASSWORD/);
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'jev-hosted-tests-'));
 const lab=await createLab({baseUrl:process.env.BASE_URL||'http://127.0.0.1:4187',headed:false,stateRoot:root,providerFactory:factory});await new Promise(r=>lab.server.listen(0,'127.0.0.1',r));
 const hosted=await createHosted({lab,password:'test-password-at-least-16',maxRuns:3});await new Promise(r=>hosted.server.listen(0,'127.0.0.1',r));
 const base=`http://127.0.0.1:${hosted.server.address().port}`,auth='Basic '+Buffer.from('demo:test-password-at-least-16').toString('base64');
 const get=async route=>fetch(base+route,{headers:{Authorization:auth}});let token;
 const state=async()=>{const s=await(await get('/state')).json();token=s.token;return s;};
 const post=async(route,body={},headers={})=>fetch(base+route,{method:'POST',headers:{Authorization:auth,Origin:base,'X-Lab-Token':token,'Content-Type':'application/json',...headers},body:JSON.stringify(body)});
 const wait=async pred=>{const end=Date.now()+65000;while(Date.now()<end){const s=await state();if(pred(s))return s;await new Promise(r=>setTimeout(r,100));}throw Error('Wait timed out');};
 const dates={startDate:'2026-09-30',endDate:'2026-09-30',mode:'normal',provider:'replay'};
 try{
 assert.equal((await fetch(base+'/health')).status,200);
 for(const route of ['/','/state','/screenshot','/download/csv'])assert.equal((await fetch(base+route)).status,401);
 const html=await(await get('/')).text();assert(html.includes('Run paid-orders'));assert(!html.includes('<video'));
 await state();assert.equal((await post('/run',dates,{Origin:'https://attacker.example'})).status,403);assert.equal((await post('/run',dates,{'X-Lab-Token':'wrong'})).status,403);
 assert.equal((await post('/record/start')).status,404);assert.equal((await get('/download/csv')).status,409);
 console.log('PASS: fail-closed password, protected state/artifacts, CSRF, restricted routes, no premature downloads');
 assert.equal((await post('/run',dates)).status,200);assert.equal((await post('/run',dates)).status,409);
 let s=await wait(s=>['verified','stopped'].includes(s.phase));assert(s.result.ok,JSON.stringify(s));assert.equal(s.result.verification.rows_checked,128);assert(!('file' in s.result));assert(!JSON.stringify(s).includes(root));
 const csv=await get('/download/csv');assert.equal(csv.status,200);const bytes=Buffer.from(await csv.arrayBuffer());assert.equal(require('node:crypto').createHash('sha256').update(bytes).digest('hex'),s.result.sha256);
 const manifest=await(await get('/download/manifest')).json();assert.equal(manifest.row_count,128);assert.equal(manifest.file_checksum,s.result.sha256);assert((await(await get('/download/trace')).text()).includes('verified'));
 fs.appendFileSync(lab.state.result.file,'corrupt');assert.equal((await get('/download/csv')).status,400);
 console.log('PASS: isolated replay, active-run rejection, 128-row verified CSV/manifest/trace; corrupted artifact rejected');
 assert.equal((await post('/run',{...dates,provider:'jev',mode:'changed-label',startDate:'2026-10-01',endDate:'2026-10-02'})).status,200);
 s=await wait(s=>s.phase==='approval'||s.phase==='stopped');assert.equal(s.phase,'approval',JSON.stringify(s));assert.equal(s.pending.proposed.label,'Build export');assert.equal((await post('/approve',{id:s.pending.id,accept:true})).status,200);
 s=await wait(s=>['verified','stopped'].includes(s.phase));assert(s.result.ok);assert.equal(s.result.verification.rows_checked,256);assert.equal(s.provider,'injected-test-only');
 console.log('PASS: hosted injected Jev control selection, repair approval and 256-row verification');
 assert.equal((await post('/run',{...dates,mode:'session-expired'})).status,200);s=await wait(s=>['verified','stopped'].includes(s.phase));assert.equal(s.result.type,'expired_session');assert.equal((await get('/download/csv')).status,409);
 assert.equal((await post('/run',dates)).status,429);assert.equal(s.hosted.runsUsed,3);
 console.log('PASS: failed runs cannot download; process run budget enforced');
 fs.writeFileSync(path.join(root,'hosted-test-result.json'),JSON.stringify({status:'pass',provider:'injected-test-only',root},null,2));console.log('Evidence:',root);
 }finally{await hosted.close();await lab.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
