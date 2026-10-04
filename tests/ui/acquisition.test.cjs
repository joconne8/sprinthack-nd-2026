// Synthetic browser negatives; no live portal/session/model access.
const assert=require('node:assert/strict');const path=require('node:path');const http=require('node:http');
const {chromium}=require('playwright');const {runSkill}=require('../../acquisition/run_skill.cjs');
const skill=path.resolve(__dirname,'../../acquisition/skills/upright-paid-orders.skill.json');
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{})});
  let content='<h1>Unrelated page</h1>';
  const fake=http.createServer((request,response)=>{response.writeHead(200,{'Content-Type':'text/html'});response.end(content);});
  await new Promise(resolve=>fake.listen(0,'127.0.0.1',resolve));
  const options={baseUrl:process.env.REPLICA_URL,startDate:'2026-09-30',endDate:'2026-09-30',browser,outputDir:process.env.QA_TEMP};
  try{
    const logs=[];const log=console.error;console.error=value=>{logs.push(value);log(value);};
    let result;
    try{result=await runSkill(skill,{...options,mode:'missing-report',runId:'missing-case'});}finally{console.error=log;}
    assert.equal(result.type,'report_unavailable');assert.equal(result.ok,false);
    assert(logs.every(value=>{const line=JSON.parse(value);return line.run_id==='missing-case'&&line.skill==='upright-paid-orders-replica@0.2.0';}));
    result=await runSkill(skill,{...options,mode:'changed-label'});assert.equal(result.type,'label_changed');
    result=await runSkill(skill,{...options,mode:'timeout',deadlineMs:1000});assert.equal(result.type,'timeout');
    result=await runSkill(skill,{...options,baseUrl:`http://127.0.0.1:${fake.address().port}`});assert.equal(result.type,'wrong_page');
    for(const [body,type] of [['<input type="password">','expired_session'],['<h1>CAPTCHA required</h1>','captcha'],['<h1>MFA required</h1>','mfa'],['<h1>Access denied</h1>','access_denied']]){
      content=body;result=await runSkill(skill,{...options,baseUrl:`http://127.0.0.1:${fake.address().port}`});assert.equal(result.type,type);
    }
    result=await runSkill(skill,{...options,startDate:'2026-02-30'});assert.equal(result.type,'bad_params');
    result=await runSkill(skill,{...options,baseUrl:'https://vendor.example'});assert.equal(result.type,'host_not_allowed');
    console.log('PASS: wrong page, deadline timeout, unavailable report, control drift, session/MFA/CAPTCHA/permission stops, dates, host restriction and versioned logs.');
  }finally{await browser.close();await new Promise(resolve=>fake.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
