// Exercise Hugh's unchanged skill. This is shared runtime/integration evidence.
const assert = require('node:assert/strict');
const path = require('node:path');
const { runSkill } = require('../acquisition/run_skill.cjs');
const skill = path.resolve(__dirname, '../acquisition/skills/upright-paid-orders.skill.json');
(async () => {
  const results = [];
  for (const [startDate, endDate] of [['2026-09-30', '2026-09-30'], ['2026-10-01', '2026-10-02']]) {
    const result = await runSkill(skill, {baseUrl: process.env.BASE_URL, startDate, endDate, outputDir: process.env.OUTPUT_DIR});
    assert(result.ok, JSON.stringify(result));
    assert.equal(result.sha256, result.manifest.file_checksum);
    results.push(result);
  }
  assert.notEqual(results[0].sha256, results[1].sha256);
  const failed = await runSkill(skill, {
    baseUrl: process.env.BASE_URL, startDate: '2026-09-30', endDate: '2026-09-30', outputDir: process.env.OUTPUT_DIR,
    pageSetup: page => page.addInitScript(() => sessionStorage.setItem('replica-mode', 'session-expired')),
  });
  assert.equal(failed.type, 'expired_session');
  assert.equal(failed.ok, false);
  console.log(JSON.stringify({results, expired_session: failed}));
})().catch(error => {console.error(error); process.exitCode = 1;});
