// Injected responses test adapter plumbing, not real Jev accuracy.
const assert = require('node:assert/strict');
const path = require('node:path');
const {chromium} = require('playwright');
const {runJev} = require('./run.cjs');
const {runSkill} = require('../../acquisition/run_skill.cjs');
const {JevProvider} = require('./provider.cjs');
const {observe, recheck} = require('./dom.cjs');
const {verifyFile} = require('./verify.cjs');
const fs = require('node:fs');
const baseUrl = process.env.BASE_URL || 'http://127.0.0.1:4187';
const skill = path.resolve(__dirname, '../../acquisition/skills/upright-paid-orders.skill.json');
const cases = [];
const pass = name => { cases.push(name); console.log('PASS:', name); };
const injected = () => new JevProvider({key: 'offline-test-only', fetchFn: async (_, options) => {
  const req = JSON.parse(options.body), controls = req.state.controls, goal = req.state.goal;
  const c = controls.find(c => goal.includes('Generate the') ? c.role === 'button' :
    goal.includes('verified current') ? true : goal.includes('Paid orders') ? c.label === 'Paid orders' :
    goal.includes('Reports') ? c.href === '/upright/reports' : goal.endsWith(c.label));
  assert(c, `No injected fixture match for ${goal}`);
  return {ok: true, json: async () => ({model: 'jev-1.13.0', answers: {target: {type: 'choice', choice: c.id,
    confidence: 1, probabilities: Object.fromEntries(['STOP', ...controls.map(c => c.id)].map(id => [id, id === c.id ? 1 : 0]))}}, usage: {input_tokens: 1, output_tokens: 1}})};
}});
(async () => {
  const browser = await chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
  const request = {baseUrl, browser, startDate: '2026-09-30', endDate: '2026-09-30', outputDir: '/private/tmp/jev-browser-tests'};
  try {
    for (const [startDate, endDate, count, mode] of [['2026-09-30','2026-09-30',128,'normal'], ['2026-10-01','2026-10-02',256,'changed-label'], ['2026-09-30','2026-09-30',128,'delayed']]) {
      const r = await runJev({...request, startDate, endDate, mode}, injected());
      assert(r.ok, JSON.stringify(r)); assert.equal(verifyFile(r, startDate, endDate).rows_checked, count);
      pass(`injected Jev ${mode}: ${count} rows`);
      const bad = {...r, manifest: {...r.manifest, file_checksum: 'bad'}};
      assert.throws(() => verifyFile(bad, startDate, endDate));
      assert.throws(() => verifyFile(r, '2026-01-01', '2026-01-02'));
    }
    pass('checksum and row-date mismatches rejected');
    const baseline = await runSkill(skill, {...request, mode: 'changed-label'});
    assert.equal(baseline.type, 'label_changed'); pass('deterministic changed-label stops');
    for (const [mode, expected] of [['session-expired','expired_session'], ['missing-report','report_unavailable']]) {
      const r = await runJev({...request, mode}, injected()); assert.equal(r.type, expected, JSON.stringify(r)); pass(mode);
    }
    const reversed = await runJev({...request, startDate:'2026-10-02',endDate:'2026-10-01'}, injected());
    assert.equal(reversed.type, 'bad_params'); pass('reversed dates rejected');
    const low = {choose: async () => {const e = new Error('low'); e.code = 'low_confidence'; throw e;}};
    assert.equal((await runJev(request, low)).type, 'low_confidence'); pass('low confidence stops browser');
    const page = await browser.newPage();
    await page.setContent('<button>Generate report</button><button disabled>Disabled</button><button hidden>Hidden</button>');
    const observed = await observe(page, 'button'); assert.equal(observed.candidates.length, 1);
    await page.locator('button').first().evaluate(el => el.textContent = 'Changed');
    await assert.rejects(recheck(observed.targets.get('control_1')), {code:'stale_target'});
    await page.close(); pass('hidden/disabled excluded; stale target rejected');
    fs.writeFileSync('/private/tmp/jev-browser-tests/results.json', JSON.stringify({provider:'injected-test-only',cases},null,2));
  } finally {await browser.close();}
})().catch(e => {console.error(e); process.exitCode=1;});
