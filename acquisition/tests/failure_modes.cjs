// Runs the skill against the local replica for two date ranges and each failure mode. Requires the replica on :4173.
const assert = require('node:assert/strict');
const path = require('node:path');
const { chromium } = require('playwright');
const { runSkill } = require('../run_skill.cjs');
const skill = path.join(__dirname, '..', 'skills', 'upright-paid-orders.skill.json');
const base = process.env.BASE_URL || 'http://127.0.0.1:4173';
const out = process.env.OUTPUT_DIR || '/tmp/ing02-tests';
const mode = m => page => page.addInitScript(v => sessionStorage.setItem('replica-mode', v), m);
(async () => {
  const browser = await chromium.launch({ headless: true, ...(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {}) });
  const run = (o) => runSkill(skill, { baseUrl: base, outputDir: out, browser, startDate: '2026-09-30', endDate: '2026-09-30', ...o });
  const results = {};
  try {
    const a = await run({}); const b = await run({ startDate: '2026-10-01', endDate: '2026-10-02' });
    assert(a.ok && b.ok); assert.notEqual(a.sha256, b.sha256); assert.equal(a.manifest.row_count, 128); assert.equal(b.manifest.row_count, 256);
    assert.equal(a.sha256, a.manifest.file_checksum); results.two_ranges = 'pass';
    const exp = await run({ pageSetup: mode('session-expired') }); assert.equal(exp.type, 'expired_session', JSON.stringify(exp)); results.expired_session = 'pass';
    const miss = await run({ pageSetup: mode('missing-report') }); assert(!miss.ok && miss.type !== 'ok', JSON.stringify(miss)); results.missing_report = `pass (${miss.type})`;
    const lab = await run({ pageSetup: mode('changed-label') }); assert.equal(lab.type, 'label_changed', JSON.stringify(lab)); results.changed_label = 'pass';
    const wrong = await run({ baseUrl: 'http://example.com' }); assert.equal(wrong.type, 'host_not_allowed'); results.host_not_allowed = 'pass';
    const bad = await run({ startDate: '2026-10-02', endDate: '2026-10-01' }); assert.equal(bad.type, 'bad_params'); results.reversed_dates = 'pass';
    const slow = await run({ pageSetup: mode('delayed') }); assert(slow.ok, JSON.stringify(slow)); results.delayed_still_succeeds = 'pass';
  } finally { await browser.close(); console.log(JSON.stringify(results, null, 2)); }
})().catch(e => { console.error('FAIL', e.message); process.exitCode = 1; });
