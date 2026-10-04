// Deterministic DOM replay. This does not call Jev or any other model.
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

async function acquire(page, {baseUrl, source = 'upright', startDate = '2026-09-30', endDate = startDate, outputDir = 'artifacts', timeout = 12000}) {
  const cash = source === 'cash_monkey';
  assert(['upright', 'cash_monkey'].includes(source), 'Unsupported demo source.');
  const root = new URL(baseUrl);
  assert(['127.0.0.1', 'localhost', '[::1]'].includes(root.hostname), 'Replay is limited to a local synthetic replica.');
  page.setDefaultTimeout(timeout);
  await page.goto(`${baseUrl}/${cash ? 'cash-monkey' : 'upright'}`);
  await page.getByRole('navigation', {name: 'Demo portals'}).getByRole('link', {name: cash ? 'Cash Monkey' : 'Upright', exact: true}).waitFor();
  if (cash) {
    await page.getByRole('link', {name: 'Reports', exact: false}).filter({hasText: '▥ Reports'}).click();
    await page.getByRole('link', {name: 'Orders', exact: true}).click();
    await page.getByLabel('Order Date From:', {exact: true}).fill(startDate);
    await page.getByLabel('Order Date To:', {exact: true}).fill(endDate);
  } else {
    await page.getByRole('navigation', {name: 'Upright navigation'}).getByRole('link', {name: 'Reports', exact: false}).click();
    await page.getByRole('link', {name: 'Paid orders', exact: true}).click();
    await page.getByLabel('Start date', {exact: true}).fill(startDate);
    await page.getByLabel('End date', {exact: true}).fill(endDate);
  }
  const button = page.getByRole('button', {name: cash ? 'Submit' : 'Generate report', exact: true});
  const [response] = await Promise.all([
    page.waitForResponse(r => r.url().endsWith('/api/reports') && r.request().method() === 'POST', {timeout}),
    button.click(),
  ]);
  const job = await response.json();
  assert.equal(response.status(), 202, job.error || 'Report request failed.');
  const readyPromise = page.waitForFunction(() => {
    const message = document.getElementById('messages');
    if (message?.classList.contains('error')) return 'failed';
    return message?.classList.contains('success') ? 'ready' : false;
  }, null, {timeout});
  const state = await (await readyPromise).jsonValue();
  assert.equal(state, 'ready', await page.locator('#messages').innerText());
  const downloadLink = page.locator(cash ? '[data-testid="cash-download-link"]' : `[data-testid="download-${job.id}"]`);
  const downloadPromise = page.waitForEvent('download', {timeout});
  await downloadLink.click();
  const download = await downloadPromise;
  await fs.mkdir(outputDir, {recursive: true});
  const filePath = path.join(outputDir, download.suggestedFilename());
  await download.saveAs(filePath);
  const failure = await download.failure();
  assert.equal(failure, null, failure || 'Download failed.');
  const bytes = await fs.readFile(filePath);
  const manifestResponse = await page.request.get(`${baseUrl}/api/reports/${job.id}/manifest`);
  assert(manifestResponse.ok(), 'Manifest unavailable.');
  const manifest = await manifestResponse.json();
  const checksum = crypto.createHash('sha256').update(bytes).digest('hex');
  assert.equal(checksum, manifest.file_checksum, 'Downloaded bytes differ from manifest.');
  assert.equal(manifest.synthetic, true);
  assert.equal(manifest.requested_start_date, startDate);
  assert.equal(manifest.requested_end_date, endDate);
  assert.equal(manifest.source_name, `${source}_replica`);
  const lines = bytes.toString('utf8').trimEnd().split(/\r?\n/);
  assert.equal(lines.length - 1, manifest.row_count, 'Unexpected row count.');
  assert(lines[0].includes('synthetic') && lines[0].includes('reporting_date'), 'Missing required headers.');
  // Validate dates in every downloaded row, not only the manifest assertion.
  const header = lines[0].split(',');
  const dateColumn = header.indexOf('reporting_date');
  const syntheticColumn = header.indexOf('synthetic');
  const csvCells = line => [...line.matchAll(/(?:^|,)("(?:[^"]|"")*"|[^,]*)/g)].map(m => m[1].replace(/^"|"$/g, '').replace(/""/g, '"'));
  for (const line of lines.slice(1)) {
    const cells = csvCells(line);
    assert(cells[dateColumn] >= startDate && cells[dateColumn] <= endDate, 'Row lies outside requested dates.');
    assert.equal(cells[syntheticColumn], 'true');
  }
  const evidence = {...manifest, replay_version: 'dom-replay-v1', verification: {checksum_matches: true, rows_checked: manifest.row_count, dates_checked: true}};
  await fs.writeFile(filePath.replace(/\.csv$/, '.manifest.json'), JSON.stringify(evidence, null, 2) + '\n');
  return {filePath, bytes, manifest: evidence, jobId: job.id};
}

async function launchBrowser() {
  return chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
}

if (require.main === module) {
  const [source = 'upright', startDate = '2026-09-30', endDate = startDate] = process.argv.slice(2);
  (async () => {
    const browser = await launchBrowser();
    try {
      const page = await browser.newPage({acceptDownloads: true});
      const result = await acquire(page, {baseUrl: process.env.BASE_URL || 'http://127.0.0.1:4173', source, startDate, endDate, outputDir: process.env.OUTPUT_DIR || 'artifacts'});
      console.log(JSON.stringify({file: result.filePath, rows: result.manifest.row_count, checksum: result.manifest.file_checksum, synthetic: true}, null, 2));
    } finally { await browser.close(); }
  })().catch(error => { console.error(error.message); process.exitCode = 1; });
}
module.exports = {acquire, launchBrowser};
