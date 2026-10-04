// Acceptance expectations come from the handwritten ledger, not API calculations.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('playwright');
const base = process.env.BASE_URL;
const input = process.env.QA_INPUT;
const output = process.env.QA_OUTPUT;
const ledger = JSON.parse(fs.readFileSync(path.join(input, 'expected.json')));

(async () => {
  const browser = await chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
  const context = await browser.newContext({viewport: {width: 1440, height: 900}});
  const page = await context.newPage();
  page.setDefaultTimeout(10000);
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const observations = {ledger_checks: [], acquired: [], checks: []};
  const net = () => page.locator('[data-metric-id="M-DEMO-NET-SALES"]');
  const json = async route => {
    const response = await page.request.get(base + route);
    assert(response.ok(), await response.text());
    return response.json();
  };
  async function scope(start, end = start, platform = '', store = '', source = 'upright_replica') {
    await page.goto(base + '/#overview');
    await page.locator('#metric-start').fill(start);
    await page.locator('#metric-end').fill(end);
    await page.locator('#metric-source').selectOption(source);
    await page.locator('#metric-platform').selectOption(platform);
    await page.locator('#metric-store').selectOption(store);
    await page.getByRole('button', {name: 'Apply filters', exact: true}).click();
    await page.locator('#metrics-content[aria-busy="false"]').waitFor();
  }
  async function expectNet(expected, label) {
    await page.waitForFunction(value => document.querySelector('[data-metric-id="M-DEMO-NET-SALES"]')?.dataset.value === value, expected);
    assert.equal(await net().getAttribute('data-value'), expected);
    observations.ledger_checks.push({label, expected, displayed: await net().textContent()});
  }
  async function upload(name, corrections = false, failed = false) {
    await page.goto(base + '/#operations');
    await page.locator('#csv-file').setInputFiles(path.join(input, name + '.csv'));
    await page.locator('#manifest-file').setInputFiles(path.join(input, name + '.json'));
    await page.locator('#allow-corrections').setChecked(corrections);
    await page.locator('#upload-button').click();
    await page.waitForFunction(() => !document.querySelector('#upload-button').disabled);
    assert((await page.locator('#upload-status').textContent()).includes(failed ? 'Import was not published.' : name === 'initial' && observations.ledger_checks.length ? 'already imported' : 'Verified import complete.'));
  }
  async function collect(start, end, mode = 'normal') {
    await page.goto(base + '/#operations');
    await page.locator('#request-start').fill(start);
    await page.locator('#request-end').fill(end);
    await page.locator('.demo-options').evaluate(node => node.open = true);
    await page.locator('#request-mode').selectOption(mode);
    await page.locator('#collect-button').click();
    await page.waitForFunction(() => !document.querySelector('#collect-button').disabled, {}, {timeout: 20000});
    return (await json('/api/v1/acquisition-runs')).runs[0];
  }
  try {
    await scope('2026-09-30');
    assert.equal(await net().textContent(), 'Unavailable');
    await upload('initial'); await scope('2026-09-30');
    const initial = ledger.core_ledger.expected.after_initial.net;
    await expectNet(initial, 'handwritten initial ledger / decoy fields excluded');
    assert.equal(await page.locator('[data-metric-id="R-MARGIN"]').textContent(), 'Unavailable');
    await page.locator('[data-testid="evidence-open"]').click();
    await page.locator('#evidence-content').waitFor();
    assert.equal(await page.locator('#evidence-scope-total').getAttribute('data-value'), initial);
    const pinned = (await page.locator('#evidence-run').textContent()).split(': ')[1];
    await page.getByRole('button', {name: 'Inspect row', exact: true}).first().click();
    assert((await page.locator('#row-detail pre').textContent()).includes('<img src=x'));
    assert.equal(await page.locator('#row-detail img').count(), 0);
    assert.equal(await page.evaluate(() => window.__qaInjection), undefined);
    await upload('initial'); await scope('2026-09-30'); await expectNet(initial, 'duplicate upload no double counting');
    await upload('overlap'); await scope('2026-09-30');
    await expectNet(ledger.core_ledger.expected.after_overlap.net, 'overlap only adds new row');
    const evidence = await json('/api/v1/evidence?' + new URLSearchParams({start_date: '2026-09-30', end_date: '2026-09-30', source: 'upright_replica', run_id: pinned}));
    assert.equal(evidence.scope_total, initial); assert.equal(evidence.total_rows, 3);
    await upload('correction', false, true); await scope('2026-09-30');
    await expectNet(ledger.core_ledger.expected.after_unapproved_correction.net, 'unapproved correction preserves publication');
    assert(await page.locator('#freshness-warning').isVisible());
    await upload('correction', true); await scope('2026-09-30');
    await expectNet(ledger.core_ledger.expected.after_approved_correction.net, 'explicit approved correction');
    await upload('invalid', false, true);
    await page.getByRole('button', {name: 'Inspect rejected source rows', exact: true}).click();
    await page.getByText('1 rejected rows · first 50 shown', {exact: true}).waitFor();
    assert((await page.locator('#batch-detail').textContent()).includes('1 rejected rows'));
    assert((await page.locator('#batch-detail').textContent()).includes('1.005'));
    await scope('2026-09-30'); await expectNet(ledger.core_ledger.expected.after_approved_correction.net, 'malformed financial row preserves last-good');
    await upload('keys'); await scope('2026-10-03');
    const keys = ledger.buyer_store_keys.expected;
    await expectNet(keys.all_platforms_net, 'all source rows including unknown stores');
    assert.equal(await page.locator('[data-metric-id="M-PLATFORM-CUSTOMERS"]').textContent(), 'Unavailable');
    await scope('2026-10-03', '2026-10-03', 'eBay'); await expectNet(keys.ebay_net, 'marketplace revenue');
    assert.equal(await page.locator('[data-metric-id="M-PLATFORM-CUSTOMERS"]').textContent(), keys.ebay_customers);
    await scope('2026-10-03', '2026-10-03', '', 'GW-001'); await expectNet(keys.store_gw001_net, 'known store');
    await scope('2026-10-03', '2026-10-03', '', 'unknown'); await expectNet(keys.store_unknown_net, 'missing and unmapped store');
    await scope('2026-10-02', '2026-10-03');
    assert.equal(await page.locator('#coverage-badge').textContent(), 'partial');
    await scope('2026-10-02'); assert.equal(await net().textContent(), 'Unavailable');
    await scope('2026-10-03', '2026-10-03', '', '', 'cash_monkey_replica');
    assert.equal(await net().textContent(), 'Unavailable');
    for (const [start, end] of [['2026-09-29', '2026-09-29'], ['2026-09-27', '2026-09-28']]) {
      const run = await collect(start, end); assert.equal(run.status, 'succeeded');
      await scope(start, end);
      const displayed = await net().getAttribute('data-value');
      const batch = await json('/api/v1/imports/' + run.batch_id);
      const original = await (await page.request.get(base + '/api/v1/files/' + batch.file.file_id)).body();
      const rawFile = 'acquired-' + start + '.csv'; fs.writeFileSync(path.join(output, rawFile), original);
      assert.equal(crypto.createHash('sha256').update(original).digest('hex'), run.checksum);
      observations.acquired.push({start, end, displayed_value: displayed, checksum: run.checksum, raw_file: rawFile, batch_id: run.batch_id});
    }
    const replay = await collect('2026-09-27', '2026-09-28'); assert.equal(replay.import_state, 'duplicate_noop');
    for (const mode of ['session-expired', 'missing-report']) {
      const failure = await collect('2026-09-27', '2026-09-28', mode);
      assert.equal(failure.status, 'needs_human'); assert.equal(failure.import_state, 'not_submitted'); assert.equal(failure.attempts.length, 1);
      assert((await page.locator('#collection-status').textContent()).includes('Next owner'));
    }
    await scope('2026-09-29');
    await page.screenshot({path: path.join(output, 'dashboard.png'), fullPage: true});
    await page.setViewportSize({width: 390, height: 844});
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
    await page.screenshot({path: path.join(output, 'mobile.png'), fullPage: true});
    await page.route('**/api/v1/metrics?*', route => route.fulfill({status: 500, contentType: 'application/json', body: JSON.stringify({error: {detail: 'QA API outage'}})}));
    await page.getByRole('button', {name: 'Apply filters', exact: true}).click();
    await page.locator('#global-error').filter({hasText: 'QA API outage'}).waitFor(); assert.equal(await net().count(), 0);
    assert.deepEqual(errors, []);
    observations.checks = ['untrusted source text escaped', 'pinned prior run preserved', 'ledger/replay/overlap/corrections', 'rejected raw row visible', 'store/marketplace/customer scope', 'partial/missing source unavailable', 'two actual acquired periods', 'auth/report failure with owner', 'mobile layout', 'API failure no mock'];
    fs.writeFileSync(path.join(output, 'observed.json'), JSON.stringify(observations, null, 2) + '\n');
    console.log('PASS: browser acceptance against handwritten ledger and acquired source bytes');
  } finally { await context.close(); await browser.close(); }
})().catch(error => {console.error(error); process.exitCode = 1;});
