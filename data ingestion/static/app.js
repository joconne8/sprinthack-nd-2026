'use strict';
const app = document.getElementById('app');
const modeSelect = document.getElementById('test-mode');
modeSelect.value = sessionStorage.getItem('replica-mode') || 'normal';
const money = value => new Intl.NumberFormat('en-US', {style: 'currency', currency: 'USD'}).format(Number(value));
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[char]));
const link = (href, text, selected = false) => `<a href="${href}" ${selected ? 'aria-current="page"' : ''}>${text}</a>`;
const path = location.pathname.replace(/\/$/, '') || '/';
const source = path.startsWith('/cash-monkey') ? 'cash_monkey' : 'upright';
const isCash = source === 'cash_monkey';
const reportType = path.endsWith('paid-order-items') ? 'paid_order_items' : isCash ? 'orders' : 'paid_orders';
const isForm = path.includes('paid-order') || path === '/cash-monkey/reports/orders';
let pollTimer;
let currentJob;
let requestBusy = false;

document.getElementById('test-toggle').addEventListener('click', event => {
  const controls = document.getElementById('test-controls');
  controls.hidden = !controls.hidden;
  event.currentTarget.setAttribute('aria-expanded', String(!controls.hidden));
});
modeSelect.addEventListener('change', () => {
  sessionStorage.setItem('replica-mode', modeSelect.value);
  const button = document.querySelector('#generate-report');
  if (button) button.textContent = modeSelect.value === 'changed-label' ? 'Build export' : isCash ? 'Submit' : 'Generate report';
  if (modeSelect.value === 'session-expired') showMessage('Expired demo session selected. Report requests will stop until you choose Normal.', 'warning');
});

function sparkline(seed = 0) {
  const shapes = ['0,30 16,20 30,25 43,9 55,19 69,8 82,22 96,14 110,25', '0,9 16,24 30,21 43,30 55,20 69,24 82,14 96,17 110,23'];
  return `<svg class="sparkline" aria-hidden="true" viewBox="0 0 110 40"><polyline points="${shapes[seed % 2]}" /></svg>`;
}
function uprightHeader() {
  return `<header class="portal-header"><a href="/upright" class="upright-brand">upright<span>®</span></a><span class="organization">Goodwill Industries of Michiana</span><nav aria-label="Upright navigation">${link('/upright', '⌂ Home', path === '/upright')}${link('/upright/reports', '▥ Reports', path.includes('reports'))}<span class="operator">Demo operator <span class="avatar">D</span></span></nav></header>`;
}
function uprightSide() {
  return `<aside class="upright-sidebar"><h3>In-app reports</h3>${link('/upright/reports', 'User productivity', path === '/upright/reports')}<span>Operational productivity</span><span>Poster overview</span><span>Poster targets</span><span>Manifests</span><span>Suppliers</span><span>Top sales</span><span>Event logs</span><span>Sales by category</span><h3>Downloads</h3><span>Goodwillfinds listings</span><span>Shopgoodwill listings</span><span>eBay listings</span>${link('/upright/reports/paid-orders', 'Paid orders', reportType === 'paid_orders' && isForm)}${link('/upright/reports/paid-order-items', 'Paid order items', reportType === 'paid_order_items' && isForm)}<span>Orders</span><span>Refunds</span><span>Manifest items</span><span>Shipments</span><span>Products</span><span>Embedded listings</span><p class="side-note">Only the highlighted report journeys are implemented.</p></aside>`;
}
function cashHeader() {
  return `<header class="cash-header"><a href="/cash-monkey" class="cash-brand"><span class="monkey-mark">CM</span><span>CashMonkey<small>S O L U T I O N S</small></span></a><span>Workspace: Goodwill Michiana <b>DEMO</b></span></header>`;
}
function cashSide() {
  return `<aside class="cash-sidebar"><div class="cash-user"><span class="avatar">D</span>Welcome <b>demo_operator</b></div>${link('/cash-monkey', '▦ Manager Dashboard', path === '/cash-monkey')}<span>◆ List Merchant</span><span>▣ Fulfill Merchant</span><span>▤ FacRec Helper</span><span>⚙ Workstation Settings</span><span>▢ Condition Notes</span><span>◇ Channel Settings</span><span>♙ Manage Users</span>${link('/cash-monkey/reports', '▥ Reports', path.includes('/reports'))}<div class="account-caption">Account:</div><div class="account-static">276 - Goodwill Michiana</div><p class="side-note">Synthetic training workspace</p></aside>`;
}
function dateFields(legacy = false) {
  return legacy ? `<div class="legacy-field"><label for="start-date">Order Date From:</label><input id="start-date" name="start_date" type="date" value="2026-09-30" min="2026-01-01" max="2026-12-31" required><small>(required · inclusive · UTC)</small></div><div class="legacy-field"><label for="end-date">Order Date To:</label><input id="end-date" name="end_date" type="date" value="2026-09-30" min="2026-01-01" max="2026-12-31" required><small>(required · inclusive · UTC)</small></div>` : `<fieldset class="date-fields"><legend>Between</legend><div><label for="start-date">Start date</label><input id="start-date" name="start_date" type="date" value="2026-09-30" min="2026-01-01" max="2026-12-31" required></div><div><label for="end-date">End date</label><input id="end-date" name="end_date" type="date" value="2026-09-30" min="2026-01-01" max="2026-12-31" required></div></fieldset>`;
}
function messages() { return `<div id="messages" role="status" aria-live="polite" hidden></div>`; }
function previewMarkup() {
  return `<section id="report-preview" hidden><h3>Report preview <span class="subtle">· synthetic records</span></h3><div class="preview-controls" id="preview-totals"></div><p id="preview-note" class="muted"></p><div class="table-scroll"><table id="preview-table"><thead></thead><tbody></tbody></table></div></section>`;
}
function uprightForm() {
  return `<h1>${reportType === 'paid_order_items' ? 'Paid Order Items Report' : 'Paid Order Report'}</h1><div class="about"><b>ⓘ About this report</b><p>This report includes all orders paid within a given date range. Optionally filter by channel or refund status.</p></div><h3>Generate report for dates</h3><form id="report-form">${dateFields()}<label for="timezone">Timezone</label><select id="timezone"><option value="America/Los_Angeles">Pacific Time — America/Los_Angeles</option><option value="America/Indiana/Indianapolis">Eastern Time — Indianapolis</option><option value="UTC">UTC</option></select><small class="form-hint">Use America/Los_Angeles for SGW. Selected timezone is applied to payment timestamps.</small><label for="channel">Channel</label><select id="channel"><option value="">All</option><option>Shopgoodwill</option><option>eBay</option><option>Goodwillfinds</option></select><label for="payment-status">Payment status</label><select id="payment-status"><option>Paid</option><option>Refunded</option><option>All</option></select><button class="primary" id="generate-report" type="submit">${modeSelect.value === 'changed-label' ? 'Build export' : 'Generate report'}</button><small class="form-hint">The real screen mentions email delivery. This replica makes the report available below; no email is sent.</small></form>${messages()}<section class="past-reports"><h3>Past reports</h3><div class="table-scroll"><table><thead><tr><th>Created by</th><th>Created</th><th>Requested period</th><th>Status</th><th>Link</th></tr></thead><tbody id="report-history"><tr><td colspan="5" class="empty-row">No reports yet. Generate a report to create a download.</td></tr></tbody></table></div></section>${previewMarkup()}`;
}
function productivity() {
  const rows = Array.from({length: 13}, (_, i) => `<tr><td>demo_operator_${String(i + 1).padStart(2, '0')}</td>${[i === 0 ? 35 : '—', '—', i % 3 === 0 ? 11 : '—', i % 4 === 0 ? 10 : '—', '—', '—', '—'].map(v => `<td>${v}</td>`).join('')}</tr>`).join('');
  return `<h1>User productivity</h1><p class="muted">Synthetic operational overview · Select Paid orders under Downloads to follow the presentation.</p><div class="inline-filters"><label>From <input type="date" value="2026-09-30" disabled></label><label>To <input type="date" value="2026-09-30" disabled></label><span class="muted">Illustrative overview</span></div><div class="table-scroll"><table class="productivity-table"><thead><tr>${['User', 'Accepted', 'Rejected', 'Photographed', 'Posted', 'Shelved', 'Purged', 'Picked'].map(t => `<th>${t}</th>`).join('')}</tr></thead><tbody><tr class="totals"><td>Totals</td><td>35</td><td>—</td><td>73</td><td>50</td><td>3</td><td>10</td><td>—</td></tr>${rows}</tbody></table></div>`;
}
function uprightHome() {
  const cards = [['PAID ORDERS', '128', 'Selected demo day', '/upright/reports/paid-orders', 'View orders'], ['UNFULFILLED ORDERS', '243', 'Illustrative', '/upright/reports', 'View overview'], ['UNPROCESSED MANIFEST ITEMS', '10,059', 'Illustrative', '/upright/reports', 'View overview'], ['PURGABLE PRODUCTS', '454', 'Illustrative', '/upright/reports', 'View overview']];
  return `${uprightHeader()}<main class="upright-home"><h1>Welcome back!</h1><p class="muted">Here’s what’s going on with your operation today.</p><div class="stat-grid">${cards.map((c, i) => `<article class="stat-card"><h3>${c[0]}</h3><div class="stat-value">${c[1]}${sparkline(i)}</div><div class="stat-bottom"><span>${c[2]}</span><a href="${c[3]}">${c[4]}</a></div></article>`).join('')}</div><div class="home-alert"><b>Action required</b><span>6 synthetic Shopgoodwill listings failed</span><a href="/upright/reports">Review reports</a></div><div class="home-panels"><article><h3>LISTINGS</h3><p class="large-value">48 <small>↓ 37.5%</small></p><p class="muted">Illustrative listings today</p><hr><h3>WEEKLY CHANNEL SALES</h3>${['Shopgoodwill', 'eBay', 'Goodwillfinds'].map((c, i) => `<div class="sales-line"><span>${c}</span><b>${money(15013 - i * 2800)}</b>${sparkline(i)}</div>`).join('')}</article><article><h3>WEEKLY SUPPLIER SALES <span class="subtle">Last 7 days · illustrative</span></h3>${Array.from({length: 6}, (_, i) => `<div class="sales-line"><span>Store${String(i + 9).padStart(2, '0')}</span><b>${money(1364 + i * 273)}</b>${sparkline(i)}</div>`).join('')}<a href="/upright/reports">Show all reports</a></article></div><p class="muted">Overview numbers reproduce the layout only. Downloaded reports use their own generated synthetic records.</p></main>`;
}
function consoleCharts() {
  return `<div class="cash-console"><div class="console-nav"><b>CashMonkey</b><span>Executive</span><span>Overview</span><span>Sales</span><span>Inventory</span><span class="active">Orders</span><span>Production</span></div><h4>CashMonkey Software Orders <span>Illustrative</span></h4><div class="bar-chart gray">${Array.from({length: 12}, (_, i) => `<div style="height:${20 + ((i * 17) % 65)}%"><span>${80 + i * 15}</span></div>`).join('')}</div><h4>Orders: Monthly revenue by channel</h4><div class="channel-band"><span>Amazon-MF</span><span>Goodwillbooks</span><span>eBay</span></div><div class="bar-chart stacked">${Array.from({length: 12}, (_, i) => `<div style="height:${20 + i * 6}%"><i></i><i></i><i></i></div>`).join('')}</div><div class="month-labels">${['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'].map(m => `<span>${m}</span>`).join('')}</div></div>`;
}
function cashReports() {
  return `<h1>▥ Reports</h1><h2 class="purple">The CashMonkey Console</h2>${consoleCharts()}<p class="muted">Console charts are illustrative. Use Orders below to generate a real synthetic report.</p><hr><h2>Reports</h2><h3>Orders Reports</h3><p><a href="/cash-monkey/reports/orders">Orders</a> — Report showing items ordered, source, quantity, revenue and payout information.</p><p class="muted">One line per unit. Bookkeeping definitions in this demo are documented with the download.</p><h3>Inventory Reports</h3><p class="muted">Inventory reports are outside the two implemented journeys.</p>`;
}
function cashForm() {
  return `<h1>Orders Report</h1><p>Showing orders across all marketplaces, with payout information where available. <b>One line per unit!</b></p><form id="report-form" class="legacy-form">${dateFields(true)}<div class="legacy-field"><label for="accounts">Accounts:</label><select id="accounts" multiple size="4"><option>276 - Goodwill Michiana</option><option>277 - Goodwill Michiana (Stores)</option></select><small>Optional · ⌘/Ctrl-click to select multiple. No selection includes both accounts.</small></div><div class="legacy-field"><label for="channels">Channel:</label><select id="channels" multiple size="3"><option>Amazon-MF</option><option>eBay</option><option>Goodwillbooks</option></select><small>Optional · ⌘/Ctrl-click to select multiple</small></div><div class="legacy-field"><label for="order-ids">Order IDs:</label><textarea id="order-ids" rows="2" placeholder="One ID per line"></textarea><small>Optional · exact IDs, separated by commas or new lines</small></div><div class="legacy-field"><label for="skus">SKUs:</label><textarea id="skus" rows="2" placeholder="One SKU per line"></textarea><small>Optional · exact SKUs</small></div><div class="legacy-field"><label for="format">Format:</label><select id="format"><option>CSV</option></select><small>CSV is the implemented format.</small></div><button id="generate-report" type="submit" class="legacy-submit">${modeSelect.value === 'changed-label' ? 'Build export' : 'Submit'}</button><p class="muted">Each unit appears on its own row. This simplified synthetic report is not the vendor’s confirmed export schema.</p></form>${messages()}<div id="cash-download" hidden></div>${previewMarkup()}`;
}
function hub() {
  return `<main class="hub"><div class="eyebrow">SPRINTHACK@ND · DATA INGESTION</div><h1>Two portals.<br>One reporting workflow.</h1><p class="hub-intro">Practice the report collection steps from Goodwill’s presentation using clickable replicas and downloadable synthetic data.</p><div class="portal-cards"><a href="/upright" class="portal-card"><span class="portal-number">01 / OPERATIONS</span><strong class="upright-brand">upright</strong><h2>Paid-order reporting</h2><p>Reports → Paid orders → Date range → Generate → Download</p><span class="card-action">Open Upright replica →</span></a><a href="/cash-monkey" class="portal-card cash-card"><span class="portal-number">02 / BOOKS</span><strong class="cash-brand">CashMonkey</strong><h2>Book-order reporting</h2><p>Reports → Orders → Dates & channels → Submit → CSV link</p><span class="card-action">Open Cash Monkey replica →</span></a></div><section class="hub-note"><h3>Ready for the team’s automation</h3><p>Real page controls. Observable report states. Repeatable files with date coverage and a separate verification manifest.</p><p>Demo dates: <b>September 30, 2026</b> and <b>October 1, 2026</b>. Other 2026 dates are supported, up to 31 days per request.</p></section></main>`;
}
if (path === '/') app.innerHTML = hub();
else if (isCash) app.innerHTML = `${cashHeader()}<div class="cash-layout">${cashSide()}<main class="cash-content">${isForm ? cashForm() : path === '/cash-monkey/reports' ? cashReports() : `<h1>Manager Dashboard</h1><h2 class="purple">The CashMonkey Console</h2>${consoleCharts()}<p class="muted">Illustrative dashboard using synthetic values.</p><a class="cash-open-reports" href="/cash-monkey/reports">Open Reports →</a>`}</main></div>`;
else if (path === '/upright') app.innerHTML = uprightHome();
else app.innerHTML = `${uprightHeader()}<div class="reports-title">Reports</div><div class="upright-layout">${uprightSide()}<main class="upright-content">${isForm ? uprightForm() : productivity()}</main></div>`;

function showMessage(text, kind = 'info') {
  const box = document.getElementById('messages');
  if (!box) return;
  box.hidden = false;
  box.className = `message ${kind}`;
  box.textContent = text;
}
function selectedValues(id) { return [...document.getElementById(id).selectedOptions].map(o => o.value); }
function textValues(id) { return document.getElementById(id).value.split(/[,\n]/).map(s => s.trim()).filter(Boolean); }
function currentSpec() {
  return {source, report_type: reportType,
    start_date: document.getElementById('start-date').value, end_date: document.getElementById('end-date').value,
    timezone: isCash ? 'UTC' : document.getElementById('timezone').value,
    channels: isCash ? selectedValues('channels') : document.getElementById('channel').value ? [document.getElementById('channel').value] : [],
    accounts: isCash ? selectedValues('accounts') : [],
    payment_status: isCash ? 'All' : document.getElementById('payment-status').value,
    order_ids: isCash ? textValues('order-ids') : [], skus: isCash ? textValues('skus') : [],
    format: 'CSV', mode: modeSelect.value};
}
async function fetchJson(url, options) {
  const response = await fetch(url, options);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `Request failed (${response.status}).`);
  return body;
}
function downloadLinks(job) {
  return `<a href="${job.download_url}" download data-testid="download-${job.id}">Download</a><a class="manifest-link" href="${job.manifest_url}" download>Manifest</a><button class="preview-button" data-job="${job.id}">Preview</button>`;
}
async function refreshHistory() {
  const body = document.getElementById('report-history');
  if (!body) return;
  const jobs = (await fetchJson('/api/reports')).filter(j => j.spec.source === source && j.spec.report_type === reportType);
  if (!jobs.length) return;
  body.innerHTML = jobs.map(job => `<tr data-report-id="${job.id}"><td>demo_operator</td><td>This session</td><td>${escapeHtml(job.spec.start_date)} — ${escapeHtml(job.spec.end_date)}</td><td><span class="status ${job.status}" data-testid="report-status">${job.status === 'ready' ? 'Complete' : job.status === 'pending' ? 'Generating' : 'Failed'}</span></td><td class="download-cell">${job.status === 'ready' ? downloadLinks(job) : job.status === 'failed' ? escapeHtml(job.error) : 'Waiting for report…'}</td></tr>`).join('');
}
async function watchReport(id, deadline = Date.now() + 15000) {
  try {
    const job = await fetchJson(`/api/reports/${id}`);
    if (!isCash) await refreshHistory();
    if (job.status === 'failed') throw new Error(job.error);
    if (job.status === 'ready') {
      requestBusy = false;
      document.getElementById('generate-report').disabled = false;
      showMessage(`Report complete. ${job.manifest.row_count} synthetic rows are ready to download.`, 'success');
      if (isCash) {
        const box = document.getElementById('cash-download');
        box.hidden = false;
        box.innerHTML = `<span class="green-note">Synthetic orders are reported in USD.</span><p>CSV file download: <a href="${job.download_url}" download data-testid="cash-download-link">${escapeHtml(job.manifest.file_name)}</a></p><p><a href="${job.manifest_url}" download>Download verification manifest</a> · <button class="preview-button" data-job="${job.id}">Preview report</button></p>`;
      }
      return;
    }
    if (Date.now() > deadline) throw new Error('Report generation timed out. Stop automation and review this run.');
    pollTimer = setTimeout(() => watchReport(id, deadline), 300);
  } catch (error) {
    requestBusy = false;
    document.getElementById('generate-report').disabled = false;
    showMessage(error.message, 'error');
  }
}
const form = document.getElementById('report-form');
if (form) {
  if (!isCash) refreshHistory().catch(error => showMessage(error.message, 'error'));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (requestBusy) return;
    const preview = document.getElementById('report-preview');
    preview.hidden = true;
    if (isCash) document.getElementById('cash-download').hidden = true;
    const spec = currentSpec();
    if (spec.start_date > spec.end_date) return showMessage('The start date must be on or before the end date.', 'error');
    requestBusy = true;
    document.getElementById('generate-report').disabled = true;
    clearTimeout(pollTimer);
    showMessage('Generating report. Please wait…');
    try {
      currentJob = await fetchJson('/api/reports', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(spec)});
      if (!isCash) await refreshHistory();
      watchReport(currentJob.id);
    } catch (error) {
      requestBusy = false;
      document.getElementById('generate-report').disabled = false;
      showMessage(error.message, 'error');
    }
  });
}
// Parse the replica's RFC-style CSV, including quoted commas and escaped quotes.
function parseCsv(text) {
  const rows = []; let row = [], cell = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '"') {
      if (quoted && text[i + 1] === '"') { cell += '"'; i++; } else quoted = !quoted;
    } else if (c === ',' && !quoted) { row.push(cell); cell = ''; }
    else if (c === '\n' && !quoted) { row.push(cell.replace(/\r$/, '')); rows.push(row); row = []; cell = ''; }
    else cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  return rows;
}
app.addEventListener('click', async event => {
  const button = event.target.closest('[data-job]');
  if (!button) return;
  try {
    const job = await fetchJson(`/api/reports/${button.dataset.job}`);
    if (job.status !== 'ready') throw new Error('Report is not ready.');
    const response = await fetch(job.download_url);
    if (!response.ok) throw new Error('Preview download failed.');
    const rows = parseCsv(await response.text());
    const [headers, ...records] = rows;
    const columns = isCash ? ['order_id', 'channel', 'title', 'quantity', 'item_revenue', 'refund_amount'] : ['paid_order_id', 'channel', 'item_title', 'gross_sales', 'refund_amount', 'net_sales'];
    document.querySelector('#preview-table thead').innerHTML = `<tr>${columns.map(c => `<th>${escapeHtml(c.replaceAll('_', ' '))}</th>`).join('')}</tr>`;
    document.querySelector('#preview-table tbody').innerHTML = records.slice(0, 20).map(row => `<tr>${columns.map(c => `<td>${escapeHtml(row[headers.indexOf(c)] || '')}</td>`).join('')}</tr>`).join('');
    const m = job.manifest;
    document.getElementById('preview-totals').innerHTML = `<span><b>${m.row_count}</b> report rows</span><span><b>${m.order_count}</b> orders</span><span><b>${money(m.demo_net_sales)}</b> demo net sales</span>`;
    document.getElementById('preview-note').textContent = `Showing the first ${Math.min(records.length, 20)} rows. ${isCash ? 'Cash Monkey rows represent units; do not use their count as customer count.' : 'The presentation counts report rows as customers; this replica identifies them as orders, not unique buyers.'} Net sales = item sales minus refunds, excluding shipping, tax and fees.`;
    const preview = document.getElementById('report-preview');
    preview.hidden = false;
    preview.scrollIntoView({behavior: 'smooth', block: 'start'});
  } catch (error) { showMessage(error.message, 'error'); }
});
