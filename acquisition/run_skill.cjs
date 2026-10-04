// Versioned deterministic synthetic replay. DOM/report text is data, never instructions.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { chromium } = require('playwright');
const RESULT = { OK: 'ok', EXPIRED_SESSION: 'expired_session', WRONG_PAGE: 'wrong_page', TIMEOUT: 'timeout', LABEL_CHANGED: 'label_changed', HOST_NOT_ALLOWED: 'host_not_allowed', BAD_PARAMS: 'bad_params', DOWNLOAD_FAILED: 'download_failed', REPORT_UNAVAILABLE: 'report_unavailable' };
const fail = (type, detail, ctx) => ({ok: false, type, detail, run_id: ctx.runId, skill_id: ctx.skill.skill_id, skill_version: ctx.skill.skill_version});
const validDate = value => /^2026-\d{2}-\d{2}$/.test(value) && !Number.isNaN(Date.parse(value)) && new Date(value).toISOString().slice(0, 10) === value;

async function runSkill(skillPath, {baseUrl, startDate, endDate, outputDir = 'artifacts', runId = crypto.randomUUID(), browser, pageSetup, mode = 'normal', deadlineMs}) {
  const skill = JSON.parse(fs.readFileSync(skillPath, 'utf8'));
  const ctx = {skill, runId};
  let url;
  try { url = new URL(baseUrl); } catch { return fail('bad_params', 'Invalid replica address', ctx); }
  if (url.protocol !== 'http:' || !skill.allowed_hosts.includes(url.hostname) || url.username || url.password) return fail('host_not_allowed', url.hostname, ctx);
  if (!validDate(startDate) || !validDate(endDate) || startDate > endDate) return fail('bad_params', `${startDate}..${endDate}`, ctx);
  if (!['normal', 'session-expired', 'missing-report', 'changed-label', 'delayed', 'timeout'].includes(mode)) return fail('bad_params', 'Unknown synthetic mode', ctx);
  const own = !browser;
  const total = Math.min(deadlineMs || skill.timeouts_ms.total, skill.timeouts_ms.total);
  const deadline = Date.now() + total;
  const remaining = () => { const ms = deadline-Date.now(); if (ms <= 0) {const e = new Error('Overall acquisition deadline exceeded'); e.name = 'DeadlineError'; throw e;} return Math.min(skill.timeouts_ms.step, ms); };
  let page, failureType = 'wrong_page', lastCategory = '';
  try {
    browser = browser || await chromium.launch({headless: true, timeout: remaining(), ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
    page = await browser.newPage({acceptDownloads: true});
    await page.addInitScript(value => sessionStorage.setItem('replica-mode', value), mode === 'timeout' ? 'delayed' : mode);
    if (pageSetup) await pageSetup(page);
    await page.route('**/*', route => {
      const target = new URL(route.request().url());
      return target.origin === url.origin ? route.continue() : route.abort();
    });
    let jobId = null;
    page.on('response', async response => {
      if (response.url().startsWith(url.origin + '/api/reports')) {
        try { const body = await response.json(); if (body.id && response.request().method() === 'POST') jobId = body.id; if (body.error_category) lastCategory = body.error_category; } catch {}
      }
    });
    for (const step of skill.steps) {
      const timeout = remaining();
      page.setDefaultTimeout(timeout);
      failureType = ['fill', 'select', 'click'].includes(step.op) ? 'label_changed' : 'wrong_page';
      console.error(JSON.stringify({run_id: runId, skill: `${skill.skill_id}@${skill.skill_version}`, msg: `step ${step.op}`}));
      const sub = value => value.replaceAll('{start_date}', startDate).replaceAll('{end_date}', endDate).replaceAll('{job_id}', jobId);
      const scope = step.within ? page.getByRole(step.within.role, {name: step.within.name, exact: true}) : page;
      if (step.op === 'goto') {
        const response = await page.goto(url.origin + step.path, {timeout});
        if (!response?.ok() || new URL(page.url()).origin !== url.origin) return fail('wrong_page', 'Replica page did not match the requested destination', ctx);
        const body = await page.locator('body').innerText();
        if (await page.locator('input[type=password]').count()) return fail('expired_session', 'Sign-in required; stop and use the human fallback', ctx);
        if (/captcha/i.test(body)) return fail('captcha', 'Human CAPTCHA verification required', ctx);
        if (/multi.factor authentication|MFA required/i.test(body)) return fail('mfa', 'Human authentication required', ctx);
        if (/access denied/i.test(body)) return fail('access_denied', 'Provider or operator permission required', ctx);
      } else if (step.op === 'assert') {
        await page.getByRole(step.role, {name: step.name, exact: true}).waitFor({state: 'visible', timeout});
      } else if (step.op === 'click') {
        await scope.getByRole(step.role, {name: step.name, exact: true}).click({timeout});
      } else if (step.op === 'fill') {
        await page.getByLabel(step.label, {exact: true}).fill(sub(step.value), {timeout});
      } else if (step.op === 'select') {
        await page.getByLabel(step.label, {exact: true}).selectOption(step.value, {timeout});
      } else if (step.op === 'wait_state') {
        failureType = 'timeout';
        const state = await (await page.waitForFunction(([selector, ok, bad]) => {
          const element = document.querySelector(selector);
          return element?.classList.contains(bad) ? 'failed' : element?.classList.contains(ok) ? 'ready' : false;
        }, [step.selector, step.ready_class, step.failed_class], {timeout: Math.max(1, deadline-Date.now())})).jsonValue();
        if (state === 'failed') {
          const text = (await page.locator(step.selector).innerText()).slice(0, 200);
          const type = /session|expired/i.test(text) || lastCategory === 'session_expired' ? 'expired_session' : /not available|unavailable|missing report/i.test(text) || lastCategory === 'missing_report' ? 'report_unavailable' : /captcha/i.test(text) ? 'captcha' : /mfa/i.test(text) ? 'mfa' : /denied/i.test(text) ? 'access_denied' : 'wrong_page';
          return fail(type, text, ctx);
        }
      } else if (step.op === 'download') {
        failureType = 'download_failed';
        if (!jobId) return fail('wrong_page', 'Missing report job identity', ctx);
        const downloadPromise = page.waitForEvent('download', {timeout: remaining()});
        await page.locator(sub(step.selector)).click({timeout: remaining()});
        const download = await downloadPromise;
        fs.mkdirSync(outputDir, {recursive: true});
        const file = path.join(outputDir, path.basename(download.suggestedFilename()));
        await download.saveAs(file);
        if (await download.failure()) return fail('download_failed', await download.failure(), ctx);
        const bytes = fs.readFileSync(file);
        const response = await page.request.get(`${url.origin}/api/reports/${jobId}/manifest`, {timeout: remaining()});
        if (!response.ok()) return fail('download_failed', 'Manifest unavailable', ctx);
        const manifest = await response.json();
        const sha256 = crypto.createHash('sha256').update(bytes).digest('hex');
        if (manifest.file_checksum !== sha256 || manifest.requested_start_date !== startDate || manifest.requested_end_date !== endDate || manifest.source_name !== skill.source_name || manifest.report_type !== skill.report_type || manifest.synthetic !== true) return fail('download_failed', 'Downloaded artifact differs from requested manifest', ctx);
        return {ok: true, type: 'ok', run_id: runId, skill_id: skill.skill_id, skill_version: skill.skill_version, file, manifest, sha256, byte_size: bytes.length};
      } else return fail('wrong_page', 'Unknown skill operation', ctx);
    }
    return fail('wrong_page', 'Skill ended without a download', ctx);
  } catch (error) {
    const type = error.name === 'DeadlineError' || Date.now() >= deadline ? 'timeout' : error.name === 'TimeoutError' ? failureType : /executable|browser.*launch/i.test(error.message) ? 'runtime_unavailable' : 'wrong_page';
    return fail(type, error.message.split('\n')[0], ctx);
  } finally {
    if (page) await page.close().catch(() => {});
    if (own && browser) await browser.close().catch(() => {});
  }
}

if (require.main === module) {
  const request = process.argv[2] === '--request' ? JSON.parse(fs.readFileSync(process.argv[3], 'utf8')) : {startDate: process.argv[2], endDate: process.argv[3] || process.argv[2], baseUrl: process.env.BASE_URL || 'http://127.0.0.1:4173', outputDir: process.env.OUTPUT_DIR || 'artifacts'};
  runSkill(path.join(__dirname, 'skills/upright-paid-orders.skill.json'), request)
    .then(result => {console.log(JSON.stringify(result)); process.exitCode = result.ok ? 0 : 1;});
}
module.exports = {runSkill, RESULT};
