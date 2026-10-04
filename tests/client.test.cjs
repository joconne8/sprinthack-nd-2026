// Client boundary checks; product UI and independent acceptance are separate.
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const client = require(path.resolve(process.argv[2], 'client.js'));
const examples = path.resolve(__dirname, '../contracts/v1/examples');
const read = name => JSON.parse(fs.readFileSync(path.join(examples, name + '.json'), 'utf8'));

(async () => {
  const originalFetch = global.fetch;
  const calls = [];
  const metrics = read('metrics-available');
  global.fetch = async (url, options) => { calls.push({url, options}); return {ok: true, status: 200, json: async () => metrics}; };
  try {
    const signal = new AbortController().signal;
    const result = await client.getMetrics('http://127.0.0.1:8000/', {
      start_date: '2026-09-30', end_date: '2026-09-30', source: 'upright_replica', platform: null, store: null,
    }, signal);
    assert.deepEqual(result, metrics);
    assert.equal(result.metrics[0].value, '7127.78');
    assert.equal(calls[0].options.signal, signal);
    assert.equal(new URL(calls[0].url).pathname, '/api/v1/metrics');
    assert.equal(new URL(calls[0].url).searchParams.has('platform'), false);
    await client.getEvidence('http://localhost:8000', {start_date: '2026-09-30', end_date: '2026-09-30', source: 'upright_replica', run_id: 'shown-run', limit: 1});
    assert.equal(new URL(calls[1].url).searchParams.get('run_id'), 'shown-run');
    const failed = read('batch-failed');
    global.fetch = async () => ({ok: false, status: 422, json: async () => failed});
    await assert.rejects(client.importCsv('http://localhost:8000', {csv_text: 'headers\r\n', manifest: {}, allow_corrections: false}), err => {
      assert(err instanceof client.ApiError);
      assert.equal(err.status, 422);
      assert.deepEqual(err.body, failed);
      return true;
    });
    global.fetch = async () => ({ok: true, status: 200, json: async () => ({...metrics, contract_version: '1.0.0'})});
    await assert.rejects(client.getImports('http://localhost:8000'), /Unsupported/);
    global.fetch = async () => { throw new Error('connection refused'); };
    await assert.rejects(client.getImports('http://localhost:8000'), /connection refused/);
    console.log('PASS: client preserves API values, filters/run identity, cancellation signal, failed batches and errors.');
  } finally { global.fetch = originalFetch; }
})().catch(error => { console.error(error); process.exitCode = 1; });
