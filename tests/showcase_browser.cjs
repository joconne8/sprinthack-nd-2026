// Real showcase acceptance: actual iframe clicks, approved replay, downloaded files.
// Expected amounts are independently specified; no screenshots or API stubs feed metrics.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8001';
const output = process.env.QA_OUTPUT || path.resolve('reports/SHOWCASE/browser');
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
  fs.mkdirSync(output, {recursive: true});
  const browser = await chromium.launch({headless: true,
    ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
  const context = await browser.newContext({acceptDownloads: true, viewport: {width: 1440, height: 1000}});
  const page = await context.newPage();
  page.setDefaultTimeout(15000);
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const observed = {completed: false, recordings: [], runs: [], checks: [], console_errors: errors};
  async function screenshot(name) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({path: path.join(output, name), fullPage: true});
  }
  async function json(route) {
    const response = await page.request.get(base + '/api/showcase/v1' + route);
    assert(response.ok(), await response.text());
    return response.json();
  }
  async function record(source, changedLabel = false) {
    await page.locator('[data-view="collect"]').click();
    await page.locator('#record-source').selectOption(source);
    const startResponse = page.waitForResponse(r => r.url().endsWith('/recordings') && r.request().method() === 'POST');
    await page.locator('#record-start').click();
    const recording = await (await startResponse).json();
    const portal = page.frameLocator('#portal-frame');
    if (source === 'upright_replica') {
      await portal.getByRole('link', {name: '▥ Reports', exact: true}).click();
      await portal.getByRole('link', {name: 'Paid orders', exact: true}).click();
      if (changedLabel) {
        await portal.getByRole('button', {name: 'Test controls', exact: true}).click();
        await portal.getByLabel('Scenario', {exact: true}).selectOption('changed-label');
      }
      await portal.getByLabel('Start date', {exact: true}).fill('2026-09-29');
      await portal.getByLabel('End date', {exact: true}).fill('2026-09-29');
      await portal.getByLabel('Timezone', {exact: true}).selectOption('America/Indiana/Indianapolis');
      await portal.getByLabel('Payment status', {exact: true}).selectOption('All');
      const generatedResponse = page.waitForResponse(r => r.url().endsWith('/showcase/portal/api/reports') && r.request().method() === 'POST');
      await portal.getByRole('button', {name: changedLabel ? 'Build export' : 'Generate report', exact: true}).click();
      const generated = await (await generatedResponse).json();
      await portal.locator('[data-report-id="' + generated.id + '"] [data-testid="report-status"]').filter({hasText: 'Complete'}).waitFor();
      const downloading = page.waitForEvent('download');
      await portal.locator('[data-testid="download-' + generated.id + '"]').click();
      const download = await downloading;
      await download.saveAs(path.join(output, 'recorded-upright-training.csv'));
    } else {
      await portal.getByRole('link', {name: '▥ Reports', exact: true}).click();
      await portal.getByRole('link', {name: 'Orders', exact: true}).click();
      await portal.getByLabel('Order Date From:', {exact: true}).fill('2026-09-29');
      await portal.getByLabel('Order Date To:', {exact: true}).fill('2026-09-29');
      await portal.getByRole('button', {name: 'Submit', exact: true}).click();
      const downloading = page.waitForEvent('download');
      await portal.locator('[data-testid="cash-download-link"]').click();
      const download = await downloading;
      await download.saveAs(path.join(output, 'recorded-cash-monkey-training.csv'));
    }
    await page.waitForFunction(() => !document.querySelector('#record-review').disabled);
    // Events are posted serially; review after the genuine download event arrives.
    await page.waitForFunction(() => /download/i.test(document.querySelector('#recording-events').textContent));
    await screenshot('recording-' + source + (changedLabel ? '-changed-label' : '') + '.png');
    await page.locator('#record-review').click();
    await page.waitForFunction(() => !document.querySelector('#record-approve').disabled);
    const preview = await page.locator('#recipe-preview').textContent();
    assert(preview.includes('{start_date}'), 'Recording must bind changing start dates');
    assert(preview.includes('{end_date}'), 'Recording must bind changing end dates');
    const approvedResponse = page.waitForResponse(r => r.url().endsWith('/approve') && r.request().method() === 'POST');
    await page.locator('#record-approve').click();
    const approved = await (await approvedResponse).json();
    assert.equal(approved.approved, true);
    assert.equal(approved.source, source);
    observed.recordings.push({recording_id: recording.recording_id, recipe_id: approved.recipe_id, source, changed_label: changedLabel, preview: JSON.parse(preview)});
    return approved.recipe_id;
  }
  async function run(recipe, source, mode = 'normal') {
    await page.locator('[data-view="collect"]').click();
    await page.locator('#run-recipe').selectOption(recipe);
    await page.locator('#run-start').fill('2026-09-30');
    await page.locator('#run-end').fill('2026-09-30');
    await page.locator('#run-mode').evaluate(node => node.closest('details').open = true);
    await page.locator('#run-mode').selectOption(mode);
    const acceptedResponse = page.waitForResponse(r => r.url().endsWith('/runs') && r.request().method() === 'POST');
    await page.locator('#run-button').click();
    const accepted = await (await acceptedResponse).json();
    assert(accepted.run_id, JSON.stringify(accepted));
    let result;
    const deadline = Date.now() + 90000;
    do {
      result = await json('/runs/' + accepted.run_id);
      if (['succeeded', 'needs_human'].includes(result.status)) break;
      await sleep(300);
    } while (Date.now() < deadline);
    assert(['succeeded', 'needs_human'].includes(result.status), JSON.stringify(result));
    await page.waitForFunction(() => !document.querySelector('#run-button').disabled);
    assert.equal(result.source, source);
    const eventResponse = await json('/runs/' + result.run_id + '/events');
    if (mode === 'normal' || recipe === observed.repaired_recipe) {
      assert.equal(result.status, 'succeeded', JSON.stringify(result));
      assert.equal(result.row_count, source === 'upright_replica' ? 128 : 32);
      const frame = eventResponse.events.find(event => event.frame_url);
      assert(frame, 'Replay must produce a real browser frame');
      const response = await page.request.get(base + frame.frame_url);
      assert(response.ok(), 'Browser frame should be downloadable');
      const bytes = await response.body();
      assert.equal(bytes.subarray(0, 8).toString('hex'), '89504e470d0a1a0a');
      fs.writeFileSync(path.join(output, 'frame-' + result.run_id + '.png'), bytes);
      const batchResponse = await page.request.get(base + '/api/v1/imports/' + result.batch_id);
      assert(batchResponse.ok());
      const batch = await batchResponse.json();
      const raw = await (await page.request.get(base + '/api/v1/files/' + batch.file.file_id)).body();
      assert.equal(crypto.createHash('sha256').update(raw).digest('hex'), result.checksum);
      fs.writeFileSync(path.join(output, 'acquired-' + result.run_id + '.csv'), raw);
      result.observed_import_state = batch.status;
    } else {
      assert.equal(result.status, 'needs_human', JSON.stringify(result));
      assert.equal(result.batch_id, null, 'A failed browser run must not submit a file');
      assert(result.cause, 'Failure should explain what needs review');
    }
    observed.runs.push({...result, observed_events: eventResponse.events});
    return result;
  }
  async function filter(start, end = start, source = 'all', platform = '', store = '') {
    await page.locator('[data-view="understand"]').click();
    await page.locator('#filter-start').fill(start);
    await page.locator('#filter-end').fill(end);
    await page.locator('#filter-source').selectOption(source);
    await page.locator('#filter-platform').selectOption(platform);
    await page.locator('#filter-store').selectOption(store);
    await page.locator('#filters button').click();
    await page.locator('#metric-cards[aria-busy="false"]').waitFor();
  }
  async function metric(name, value) {
    await page.waitForFunction(({name, value}) => document.querySelector('[data-metric-id="' + name + '"]')?.dataset.value === value, {name, value});
  }
  try {
    await page.goto(base + '/showcase');
    await page.locator('#metric-cards[aria-busy="false"]').waitFor();
    const initial = await json('/snapshot');
    assert(initial.sources.some(source => source.coverage.missing_days.includes('2026-09-30')), 'Use the rehearsal checkpoint state, not a pre-completed month');
    const uprightRecipe = await record('upright_replica');
    await run(uprightRecipe, 'upright_replica');
    const cashRecipe = await record('cash_monkey_replica');
    await run(cashRecipe, 'cash_monkey_replica');
    const complete = await json('/snapshot');
    assert(complete.sources.every(source => source.coverage.state === 'complete'), JSON.stringify(complete));
    const replay = await run(cashRecipe, 'cash_monkey_replica');
    assert.equal(replay.observed_import_state, 'duplicate_noop');
    await run(uprightRecipe, 'upright_replica', 'changed-label');
    const repairedRecipe = await record('upright_replica', true);
    observed.repaired_recipe = repairedRecipe;
    await run(repairedRecipe, 'upright_replica', 'changed-label');
    await run(uprightRecipe, 'upright_replica', 'session-expired');
    await run(cashRecipe, 'cash_monkey_replica', 'missing-report');
    // Show failures safely, then explicitly restore both sources before presenting comparisons.
    await run(uprightRecipe, 'upright_replica');
    await run(cashRecipe, 'cash_monkey_replica');
    await filter('2026-09-30', '2026-09-30', 'upright_replica');
    await metric('net_sales', '7127.78');
    await filter('2026-09-24', '2026-09-30');
    await metric('net_sales', '61706.64');
    await metric('labor_hours', '588.00');
    await metric('revenue_per_labor_hour', '104.94');
    await page.locator('#question').fill('Why is revenue per labor hour down?');
    await page.locator('#ask-button').click();
    await page.waitForFunction(() => document.querySelector('#messages').textContent.includes('104.94'));
    assert((await page.locator('#messages').textContent()).includes('144.59'));
    await page.locator('#daily-evidence').click();
    await page.locator('#evidence-dialog').waitFor({state: 'visible'});
    await page.waitForFunction(() => document.querySelector('#evidence-content').textContent.includes('61,706.64'));
    assert((await page.locator('#evidence-content').textContent()).includes('61706.64') || (await page.locator('#evidence-content').textContent()).includes('61,706.64'));
    await page.locator('#evidence-close').click();
    await screenshot('understand.png');
    await filter('2026-09-24', '2026-09-30', 'all', 'eBay');
    assert.equal(await page.locator('[data-metric-id="revenue_per_labor_hour"]').getAttribute('data-value'), '');
    assert.match(await page.locator('[data-metric-id="revenue_per_labor_hour"]').textContent(), /unavailable/i);
    await filter('2026-09-01', '2026-09-30');
    await metric('net_sales', '254059.40');
    await page.locator('[data-view="deliver"]').click();
    const workbookResponse = await page.request.get(new URL(await page.locator('#workbook-download').getAttribute('href'), base).href);
    assert(workbookResponse.ok());
    const workbook = await workbookResponse.body();
    assert.equal(workbook.subarray(0, 2).toString(), 'PK');
    fs.writeFileSync(path.join(output, 'september.xlsx'), workbook);
    await screenshot('deliver.png');
    const pinned = await json('/metrics?' + new URLSearchParams({snapshot_id: complete.snapshot_id, start_date: '2026-09-24', end_date: '2026-09-30', source: 'all'}));
    assert.equal(pinned.metrics.find(m => m.metric_id === 'net_sales').value, '61706.64');
    await page.setViewportSize({width: 390, height: 844});
    for (const view of ['understand', 'collect', 'deliver']) {
      await page.locator('[data-view="' + view + '"]').click();
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), 'Mobile overflow in ' + view);
      await screenshot('mobile-' + view + '.png');
    }
    await page.setViewportSize({width: 1440, height: 1000});
    await page.route('**/api/showcase/v1/metrics?*', route => route.fulfill({status: 503, contentType: 'application/json', body: JSON.stringify({error: {detail: 'QA metrics unavailable'}})}));
    await page.locator('[data-view="understand"]').click();
    await page.locator('#filters button').click();
    await page.locator('#global-error').waitFor({state: 'visible'});
    assert.equal(await page.locator('#metric-cards [data-metric-id]').count(), 0, 'Failed requests must clear old metric cards');
    assert.deepEqual(errors, [], 'Browser JavaScript errors');
    observed.checks = ['real record/review/approve for both portals', 'date-bound parameterized replay', 'actual CSV SHA-256 and importer', 'real PNG browser frames', 'same-file replay no-op', 'label drift/expired session/missing report fail closed', 'scoped metrics match independent week/month ledger', 'supported question and source evidence', 'platform labor unavailable', 'real downloadable workbook', 'pinned snapshot remains readable', 'desktop/mobile layouts', 'failed request clears stale cards'];
    observed.completed = true;
    fs.writeFileSync(path.join(output, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
    console.log(JSON.stringify({passed: true, checks: observed.checks, recordings: observed.recordings.length, runs: observed.runs.length, output}, null, 2));
  } catch (error) {
    observed.failure = error.message;
    throw error;
  } finally {
    fs.writeFileSync(path.join(output, 'observed.json'), JSON.stringify(observed, null, 2) + '\n');
    await screenshot('final-screen.png').catch(() => {});
    await browser.close();
  }
})().catch(error => {console.error(error); process.exitCode = 1;});
