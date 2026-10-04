// ING-02 draft: config-driven deterministic Playwright acquisition. No model call.
// UNTESTED: Node/Playwright were not available in the authoring environment (see reports/ING-02).
// Returns a typed result; never throws for expected failures.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { chromium } = require('playwright');

const RESULT = { OK: 'ok', EXPIRED_SESSION: 'expired_session', WRONG_PAGE: 'wrong_page', TIMEOUT: 'timeout',
  LABEL_CHANGED: 'label_changed', HOST_NOT_ALLOWED: 'host_not_allowed', BAD_PARAMS: 'bad_params', DOWNLOAD_FAILED: 'download_failed' };

const DATE = /^\d{4}-\d{2}-\d{2}$/;
const fail = (type, detail, ctx) => ({ ok: false, type, detail, run_id: ctx.runId, skill_id: ctx.skill.skill_id, skill_version: ctx.skill.skill_version });
const log = (ctx, msg) => console.error(JSON.stringify({ run_id: ctx.runId, skill: `${ctx.skill.skill_id}@${ctx.skill.skill_version}`, msg }));

async function runSkill(skillPath, { baseUrl, startDate, endDate, outputDir = 'artifacts', runId = crypto.randomUUID(), browser, pageSetup }) {
  const skill = JSON.parse(fs.readFileSync(skillPath, 'utf8'));
  const ctx = { skill, runId };
  const host = new URL(baseUrl).hostname;
  if (!skill.allowed_hosts.includes(host)) return fail(RESULT.HOST_NOT_ALLOWED, host, ctx);
  if (!DATE.test(startDate) || !DATE.test(endDate) || startDate > endDate) return fail(RESULT.BAD_PARAMS, `${startDate}..${endDate}`, ctx);
  const own = !browser;
  browser = browser || await chromium.launch({ headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  try {
    const page = await browser.newPage({ acceptDownloads: true });
    page.setDefaultTimeout(skill.timeouts_ms.step);
    if (pageSetup) await pageSetup(page); // test hook only (e.g. select a replica failure mode)
    // Block navigation away from allowed hosts.
    await page.route('**/*', r => skill.allowed_hosts.includes(new URL(r.request().url()).hostname) ? r.continue() : r.abort());
    let jobId = null;
    page.on('response', async r => { if (r.url().endsWith('/api/reports') && r.request().method() === 'POST') { try { jobId = (await r.json()).id; } catch {} } });
    const scope = (s, p) => s.within ? p.getByRole(s.within.role, { name: s.within.name }) : p;
    for (const step of skill.steps) {
      const sub = v => v.replaceAll('{start_date}', startDate).replaceAll('{end_date}', endDate).replaceAll('{job_id}', jobId);
      log(ctx, `step ${step.op}`);
      try {
        if (step.op === 'goto') await page.goto(baseUrl + step.path);
        else if (step.op === 'click') await scope(step, page).getByRole(step.role, { name: step.name, exact: step.role === 'button' }).click();
        else if (step.op === 'fill') await page.getByLabel(step.label, { exact: true }).fill(sub(step.value));
        else if (step.op === 'wait_state') {
          const state = await (await page.waitForFunction(([sel, ok, bad]) => { const m = document.querySelector(sel); if (!m) return false; if (m.classList.contains(bad)) return 'failed'; return m.classList.contains(ok) ? 'ready' : false; }, [step.selector, step.ready_class, step.failed_class], { timeout: skill.timeouts_ms.total })).jsonValue();
          if (state === 'failed') {
            const text = (await page.locator(step.selector).innerText()).slice(0, 200);
            return fail(/session|expired/i.test(text) ? RESULT.EXPIRED_SESSION : RESULT.WRONG_PAGE, text, ctx);
          }
        } else if (step.op === 'download') {
          const dl = page.waitForEvent('download');
          await page.locator(sub(step.selector)).click();
          const d = await dl; fs.mkdirSync(outputDir, { recursive: true });
          const file = path.join(outputDir, d.suggestedFilename()); await d.saveAs(file);
          if (await d.failure()) return fail(RESULT.DOWNLOAD_FAILED, await d.failure(), ctx);
          const bytes = fs.readFileSync(file);
          const mres = await page.request.get(`${baseUrl}/api/reports/${jobId}/manifest`);
          if (!mres.ok()) return fail(RESULT.DOWNLOAD_FAILED, 'manifest unavailable', ctx);
          const manifest = await mres.json();
          return { ok: true, type: RESULT.OK, run_id: runId, skill_id: skill.skill_id, skill_version: skill.skill_version, file, manifest,
            sha256: crypto.createHash('sha256').update(bytes).digest('hex'), byte_size: bytes.length };
        }
      } catch (e) {
        const timedOut = e.name === 'TimeoutError';
        // A missing locator for a named control is treated as label/DOM drift, not guessed around.
        return fail(timedOut ? (step.op === 'wait_state' ? RESULT.TIMEOUT : RESULT.LABEL_CHANGED) : RESULT.WRONG_PAGE, `${step.op}: ${e.message.split('\n')[0]}`, ctx);
      }
    }
    return fail(RESULT.WRONG_PAGE, 'skill ended without a download', ctx);
  } finally { if (own) await browser.close(); }
}

if (require.main === module) {
  const [start, end = start] = process.argv.slice(2);
  runSkill(path.join(__dirname, 'skills', 'upright-paid-orders.skill.json'), { baseUrl: process.env.BASE_URL || 'http://127.0.0.1:4173', startDate: start, endDate: end, outputDir: process.env.OUTPUT_DIR || 'artifacts' })
    .then(r => { console.log(JSON.stringify(r, null, 2)); process.exitCode = r.ok ? 0 : 1; });
}
module.exports = { runSkill, RESULT };
