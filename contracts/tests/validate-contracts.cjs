#!/usr/bin/env node
// GOV-03 contract checks for contracts/v1.
//
// Dependency-free on purpose: no package manifest exists yet and ENG-01 owns dependencies.
// It implements only the JSON Schema draft-07 keywords this bundle uses, and refuses to run
// if the bundle uses anything else. Once ENG-01 adds a validator such as ajv, run both.
//
//   node contracts/tests/validate-contracts.cjs
//   # without Node, VS Code's bundled runtime works:
//   ELECTRON_RUN_AS_NODE=1 "<path to VS Code>/Code.exe" contracts/tests/validate-contracts.cjs
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..');
const V1 = path.join(REPO, 'contracts', 'v1');
const bundle = JSON.parse(fs.readFileSync(path.join(V1, 'goodwill-contracts.schema.json'), 'utf8'));

// ---------------------------------------------------------------- schema checker
const KNOWN = new Set([
  '$schema', '$id', '$ref', '$comment', 'title', 'description', 'definitions', 'type', 'properties',
  'required', 'additionalProperties', 'enum', 'const', 'pattern', 'format', 'minimum', 'maximum',
  'minLength', 'maxLength', 'items', 'minItems', 'maxItems', 'anyOf', 'oneOf', 'allOf', 'not', 'if',
  'then', 'else',
]);
const REF_SIBLINGS = new Set(['$ref', 'description', '$comment']);

function resolve(ref) {
  const m = /^#\/definitions\/([A-Za-z0-9_]+)$/.exec(ref);
  if (!m || !(m[1] in bundle.definitions)) throw new Error(`Unresolvable $ref ${ref}`);
  return bundle.definitions[m[1]];
}

function kind(v) {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  if (Number.isInteger(v)) return 'integer';
  return typeof v;
}

function isType(t, v) {
  switch (t) {
    case 'null': return v === null;
    case 'array': return Array.isArray(v);
    case 'object': return v !== null && typeof v === 'object' && !Array.isArray(v);
    case 'integer': return Number.isInteger(v);
    case 'number': return typeof v === 'number' && Number.isFinite(v);
    case 'string': return typeof v === 'string';
    case 'boolean': return typeof v === 'boolean';
    default: throw new Error(`Unknown type ${t}`);
  }
}

function equal(a, b) {
  return JSON.stringify(a) === JSON.stringify(b);
}

const FORMATS = {
  date: (s) => {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return false;
    const d = new Date(`${s}T00:00:00Z`);
    return !Number.isNaN(d.getTime()) && d.toISOString().slice(0, 10) === s;
  },
  'date-time': (s) =>
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$/.test(s) && !Number.isNaN(Date.parse(s)),
};

function check(schema, value, at, errors) {
  if (schema === true) return;
  if (schema === false) {
    errors.push(`${at}: not allowed`);
    return;
  }
  for (const key of Object.keys(schema)) {
    if (!KNOWN.has(key)) throw new Error(`Unsupported schema keyword "${key}" near ${at}`);
  }
  if ('$ref' in schema) {
    for (const key of Object.keys(schema)) {
      if (!REF_SIBLINGS.has(key)) throw new Error(`"${key}" beside $ref is ignored by draft-07 validators (near ${at})`);
    }
    check(resolve(schema.$ref), value, at, errors);
    return;
  }
  if (schema.type !== undefined) {
    const types = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!types.some((t) => isType(t, value))) {
      errors.push(`${at}: expected ${types.join('|')}, got ${kind(value)}`);
      return;
    }
  }
  if ('const' in schema && !equal(schema.const, value)) errors.push(`${at}: must equal ${JSON.stringify(schema.const)}`);
  if (schema.enum && !schema.enum.some((e) => equal(e, value))) errors.push(`${at}: ${JSON.stringify(value)} is not an allowed value`);
  if (typeof value === 'string') {
    if (schema.pattern && !new RegExp(schema.pattern, 'u').test(value)) errors.push(`${at}: "${value}" does not match ${schema.pattern}`);
    if (schema.minLength !== undefined && [...value].length < schema.minLength) errors.push(`${at}: shorter than ${schema.minLength}`);
    if (schema.maxLength !== undefined && [...value].length > schema.maxLength) errors.push(`${at}: longer than ${schema.maxLength}`);
    if (schema.format && FORMATS[schema.format] && !FORMATS[schema.format](value)) errors.push(`${at}: invalid ${schema.format} "${value}"`);
  }
  if (typeof value === 'number') {
    if (schema.minimum !== undefined && value < schema.minimum) errors.push(`${at}: below minimum ${schema.minimum}`);
    if (schema.maximum !== undefined && value > schema.maximum) errors.push(`${at}: above maximum ${schema.maximum}`);
  }
  if (Array.isArray(value)) {
    if (schema.minItems !== undefined && value.length < schema.minItems) errors.push(`${at}: fewer than ${schema.minItems} items`);
    if (schema.maxItems !== undefined && value.length > schema.maxItems) errors.push(`${at}: more than ${schema.maxItems} items`);
    if (schema.items) value.forEach((item, i) => check(schema.items, item, `${at}/${i}`, errors));
  }
  if (isType('object', value)) {
    for (const req of schema.required || []) {
      if (!(req in value)) errors.push(`${at}: missing required "${req}"`);
    }
    const props = schema.properties || {};
    for (const [k, v] of Object.entries(value)) {
      if (k in props) check(props[k], v, `${at}/${k}`, errors);
      else if (schema.additionalProperties === false) errors.push(`${at}: unexpected property "${k}"`);
      else if (schema.additionalProperties && typeof schema.additionalProperties === 'object') {
        check(schema.additionalProperties, v, `${at}/${k}`, errors);
      }
    }
  }
  for (const sub of schema.allOf || []) check(sub, value, at, errors);
  if (schema.anyOf && !schema.anyOf.some((sub) => passes(sub, value))) errors.push(`${at}: matches none of the allowed shapes`);
  if (schema.oneOf) {
    const n = schema.oneOf.filter((sub) => passes(sub, value)).length;
    if (n !== 1) errors.push(`${at}: matches ${n} oneOf shapes, needs exactly 1`);
  }
  if (schema.not && passes(schema.not, value)) errors.push(`${at}: matches a forbidden shape`);
  if (schema.if) {
    if (passes(schema.if, value)) {
      if (schema.then) check(schema.then, value, at, errors);
    } else if (schema.else) {
      check(schema.else, value, at, errors);
    }
  }
}

function passes(schema, value) {
  const errors = [];
  check(schema, value, '', errors);
  return errors.length === 0;
}

function validate(def, value) {
  const errors = [];
  check({ $ref: `#/definitions/${def}` }, value, def, errors);
  return errors;
}

// Walk every schema node once so unsupported keywords or dangling $refs fail even if no example reaches them.
function lint(node, at) {
  if (typeof node === 'boolean') return;
  for (const key of Object.keys(node)) {
    if (!KNOWN.has(key)) throw new Error(`Unsupported schema keyword "${key}" at ${at}`);
  }
  if ('$ref' in node) {
    for (const key of Object.keys(node)) {
      if (!REF_SIBLINGS.has(key)) throw new Error(`"${key}" beside $ref at ${at}`);
    }
    resolve(node.$ref);
  }
  if (node.pattern) new RegExp(node.pattern, 'u');
  for (const key of ['properties', 'definitions']) {
    for (const [k, sub] of Object.entries(node[key] || {})) lint(sub, `${at}/${key}/${k}`);
  }
  for (const key of ['items', 'not', 'if', 'then', 'else']) {
    if (node[key] && typeof node[key] === 'object') lint(node[key], `${at}/${key}`);
  }
  if (node.additionalProperties && typeof node.additionalProperties === 'object') lint(node.additionalProperties, `${at}/additionalProperties`);
  for (const key of ['allOf', 'anyOf', 'oneOf']) (node[key] || []).forEach((sub, i) => lint(sub, `${at}/${key}/${i}`));
}

// ---------------------------------------------------------------- integer-cent arithmetic
function cents(s) {
  const negative = s.startsWith('-');
  const [whole, frac] = s.replace('-', '').split('.');
  const value = BigInt(whole) * 100n + BigInt(frac);
  return negative ? -value : value;
}

function money(c) {
  const negative = c < 0n;
  const abs = negative ? -c : c;
  return `${negative ? '-' : ''}${abs / 100n}.${String(abs % 100n).padStart(2, '0')}`;
}

// ---------------------------------------------------------------- semantic rules (planning/contracts.md §5)
function semantic(def, x) {
  const e = [];
  const need = (cond, msg) => { if (!cond) e.push(`${def}: ${msg}`); };
  const terminalFailures = ['needs_human', 'failed_retriable_exhausted', 'failed_permanent'];

  if (def === 'SourcePackageManifest' || def === 'AcquisitionRun') {
    need(x.requested_start_date <= x.requested_end_date, 'requested_start_date is after requested_end_date');
  }
  if (def === 'SourcePackageManifest') {
    if (x.row_count === 0) need(x.coverage_start_date === null && x.coverage_end_date === null, 'empty file must have null coverage');
    if (x.coverage_start_date !== null) {
      need(x.coverage_start_date >= x.requested_start_date && x.coverage_end_date <= x.requested_end_date, 'coverage lies outside the requested period');
    }
    const t = x.source_reported_totals;
    if (t && t.item_sales && t.refunds && t.demo_net_sales) {
      need(cents(t.item_sales) - cents(t.refunds) === cents(t.demo_net_sales), 'source_reported_totals.demo_net_sales != item_sales - refunds');
    }
  }
  if (def === 'AcquisitionRun') {
    x.attempts.forEach((a, i) => need(a.attempt_number === i + 1, `attempts must be numbered 1..n (attempt ${i})`));
    const delivered = x.attempts.filter((a) => a.outcome === 'delivered').length;
    if (x.status === 'succeeded') need(delivered === 1 && x.attempts[x.attempts.length - 1].outcome === 'delivered', 'succeeded run must end with exactly one delivered attempt');
    if (terminalFailures.includes(x.status)) {
      need(delivered === 0, 'failed run cannot contain a delivered attempt');
      need(x.attempts.length > 0 && x.attempts[x.attempts.length - 1].outcome === x.failure_type, 'failure_type must equal the last attempt outcome');
    }
  }
  if (def === 'IntakeResult' && x.intake_state === 'acquired_verified') {
    const m = x.manifest;
    need(x.source_file_id === m.file_checksum, 'source_file_id must equal manifest.file_checksum');
    need(x.run_id === m.run_id, 'run_id must equal manifest.run_id');
    for (const k of ['byte_size', 'row_count', 'coverage_start_date', 'coverage_end_date']) need(x[k] === m[k], `${k} must equal manifest.${k}`);
  }
  if (def === 'ImportBatch') {
    const c = x.counts;
    need(x.idempotency_key === x.source_file_id, 'idempotency_key must equal source_file_id');
    need(x.rejected_rows.length === c.rejected, 'rejected_rows length must equal counts.rejected');
    if (x.outcome === 'duplicate_noop') {
      need(c.accepted === 0 && c.rejected === 0 && c.unchanged_duplicates === c.rows_in_file, 'duplicate_noop accepts and rejects nothing');
    } else if (x.outcome !== 'failed') {
      need(c.accepted + c.rejected === c.rows_in_file, 'accepted + rejected must equal rows_in_file');
      need(c.replaced_by_correction + c.unchanged_duplicates <= c.accepted, 'replaced + unchanged cannot exceed accepted');
    }
    if (x.outcome === 'imported') need(c.rejected === 0, 'outcome imported cannot have rejected rows');
    const r = x.reconciliation;
    if (r.state === 'reconciled') {
      const parts = [r.source_reported, r.accepted, r.rejected];
      const complete = parts.every((p) => p && p.item_sales !== null && p.refunds !== null);
      need(complete, 'reconciled requires every amount to be known');
      if (complete) {
        for (const f of ['item_sales', 'refunds']) {
          need(cents(r.source_reported[f]) === cents(r.accepted[f]) + cents(r.rejected[f]), `reconciled but source_reported.${f} != accepted + rejected`);
        }
      }
    }
  }
  if (def === 'MetricResult') {
    const f = x.filters;
    const cov = x.coverage;
    need(f.start_date <= f.end_date, 'filters.start_date is after end_date');
    need(cov.received_reports <= cov.expected_reports, 'received_reports exceeds expected_reports');
    if (cov.state === 'complete') need(cov.missing.length === 0 && cov.received_reports === cov.expected_reports, 'complete coverage cannot list missing reports');
    if (cov.state === 'partial' || cov.state === 'missing') need(cov.missing.length > 0, `${cov.state} coverage must list missing reports`);
    if (x.availability === 'available') need(cov.state === 'complete' || cov.state === 'not_applicable', 'available metric requires complete coverage');
    if (x.evidence) need(x.evidence.metric_run_id === x.freshness.metric_run_id, 'evidence and freshness must name the same metric run');
    if (x.freshness.publication_state === 'published') need(x.freshness.published_at !== null, 'published requires published_at');
    if (x.freshness.publication_state === 'stale_last_good') need(Boolean(x.freshness.stale_reason), 'stale_last_good requires stale_reason');
  }
  if (def === 'SupportingRows') {
    let items = 0n;
    let refunds = 0n;
    let contribution = 0n;
    x.rows.forEach((row, i) => {
      need(cents(row.item_sales) - cents(row.refunds) === cents(row.contribution), `row ${i} contribution != item_sales - refunds`);
      items += cents(row.item_sales);
      refunds += cents(row.refunds);
      contribution += cents(row.contribution);
    });
    const t = x.totals;
    if (x.page.offset === 0 && x.rows.length === x.page.total_rows) {
      need(items === cents(t.sum_item_sales), `sum_item_sales ${t.sum_item_sales} != rows ${money(items)}`);
      need(refunds === cents(t.sum_refunds), `sum_refunds ${t.sum_refunds} != rows ${money(refunds)}`);
      need(contribution === cents(t.sum_contribution), `sum_contribution ${t.sum_contribution} != rows ${money(contribution)}`);
    }
    need(cents(t.sum_item_sales) - cents(t.sum_refunds) === cents(t.sum_contribution), 'sum_contribution != sum_item_sales - sum_refunds');
    need(t.matches_displayed_value === (cents(t.sum_contribution) === cents(t.displayed_value)), 'matches_displayed_value contradicts the totals');
  }
  if (def === 'SourceCoverage') {
    need(x.period.start_date <= x.period.end_date, 'period start is after end');
    x.sources.forEach((s) => {
      need(s.received_dates <= s.expected_dates, `${s.source_name}: received exceeds expected`);
      need(s.missing_dates.length === s.expected_dates - s.received_dates, `${s.source_name}: missing_dates must list every expected date not received`);
      if (s.connection_state === 'connected_synthetic') {
        need((s.status === 'complete') === (s.missing_dates.length === 0), `${s.source_name}: status contradicts missing_dates`);
      }
    });
  }
  if (def === 'ExpectedReports') {
    const seen = new Set();
    x.reports.forEach((r) => {
      const key = `${r.source_name}/${r.report_type}`;
      need(!seen.has(key), `duplicate report ${key}`);
      seen.add(key);
      if (r.p0) need(r.connection_state === 'connected_synthetic' && r.expected_cadence === 'daily', `${key}: P0 reports must be connected and daily`);
      if (r.connection_state === 'not_connected') need(r.expected_cadence === 'none', `${key}: not_connected reports cannot be expected`);
    });
  }
  if (def === 'MetricComparison') {
    const bothAvailable = x.current.availability !== 'unavailable' && x.previous.availability !== 'unavailable';
    if (!bothAvailable) need(x.change === null, 'change must be null when either side is unavailable');
    if (bothAvailable && x.change && x.change.amount) {
      need(cents(x.current.value.amount) - cents(x.previous.value.amount) === cents(x.change.amount), 'change != current - previous');
    }
  }
  return e;
}

// Semantic rules assume a schema-valid shape (for example decimal strings), so they only run after the schema passes.
function allErrors(def, value) {
  const schemaErrors = validate(def, value);
  return schemaErrors.length ? schemaErrors : semantic(def, value);
}

// ---------------------------------------------------------------- replica compatibility (ING-01/02 output -> v1)
function replicaCompatibility() {
  const base = path.join(REPO, 'data ingestion', 'examples', 'upright_paid_orders_2026-09-30_2026-09-30_synthetic');
  const replica = JSON.parse(fs.readFileSync(`${base}.manifest.json`, 'utf8'));
  const bytes = fs.readFileSync(`${base}.csv`);
  const skill = JSON.parse(fs.readFileSync(path.join(REPO, 'acquisition', 'skills', 'upright-paid-orders.skill.json'), 'utf8'));
  const sha = crypto.createHash('sha256').update(bytes).digest('hex');
  // Documented translation: reports/GOV-03/compatibility-notes.md, table 1.
  // run_id and downloaded_at come from the ING-02 runner; fixed placeholders stand in for them here.
  const moved = [
    'source_name', 'report_type', 'requested_start_date', 'requested_end_date', 'reporting_timezone', 'file_name',
    'file_checksum', 'checksum_algorithm', 'row_count', 'coverage_start_date', 'coverage_end_date', 'synthetic',
    'currency', 'source_package_id', 'item_sales', 'refunds', 'demo_net_sales',
  ];
  const sourceMetadata = Object.fromEntries(Object.entries(replica).filter(([k]) => !moved.includes(k)));
  const translated = {
    contract_version: '1.0.0',
    run_id: 'compat-check-run',
    acquisition_class: 'portal_export',
    source_name: replica.source_name,
    report_type: replica.report_type,
    requested_start_date: replica.requested_start_date,
    requested_end_date: replica.requested_end_date,
    reporting_timezone: replica.reporting_timezone,
    file_name: replica.file_name,
    file_checksum: replica.file_checksum,
    checksum_algorithm: replica.checksum_algorithm,
    byte_size: bytes.length,
    row_count: replica.row_count,
    coverage_start_date: replica.coverage_start_date,
    coverage_end_date: replica.coverage_end_date,
    downloaded_at: '2026-10-04T01:14:05Z',
    skill_or_adapter_version: `${skill.skill_id}@${skill.skill_version}`,
    synthetic: replica.synthetic,
    currency: replica.currency,
    source_package_id: replica.source_package_id,
    source_reported_totals: { item_sales: replica.item_sales, refunds: replica.refunds, demo_net_sales: replica.demo_net_sales },
    source_metadata: sourceMetadata,
  };
  const errors = allErrors('SourcePackageManifest', translated);
  return { sha, checksumMatches: sha === replica.file_checksum, byteSize: bytes.length, zone: replica.reporting_timezone, errors };
}

// ---------------------------------------------------------------- runner
const results = { pass: 0, fail: 0 };
function report(ok, label, detail) {
  results[ok ? 'pass' : 'fail'] += 1;
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? `  -- ${detail}` : ''}`);
}

const selfTests = [
  ['null type rejects object', () => !passes({ type: 'null' }, {})],
  ['type list accepts null', () => passes({ type: ['string', 'null'] }, null)],
  ['integer rejects 1.5', () => !passes({ type: 'integer' }, 1.5)],
  ['oneOf rejects two matches', () => !passes({ oneOf: [{ type: 'string' }, { minLength: 0 }] }, 'x')],
  ['if/then enforced', () => !passes({ if: { const: 1 }, then: { const: 2 } }, 1)],
  ['if false skips then', () => passes({ if: { const: 1 }, then: { const: 2 } }, 3)],
  ['additionalProperties false', () => !passes({ type: 'object', additionalProperties: false, properties: {} }, { a: 1 })],
  ['required enforced', () => !passes({ type: 'object', required: ['a'] }, {})],
  ['pattern enforced', () => !passes({ type: 'string', pattern: '^a$' }, 'b')],
  ['date rejects 2026-02-30', () => !passes({ type: 'string', format: 'date' }, '2026-02-30')],
  ['date-time requires an offset', () => !passes({ type: 'string', format: 'date-time' }, '2026-10-01T13:05:12')],
  ['not enforced', () => !passes({ not: { type: 'null' } }, null)],
  ['anyOf accepts one match', () => passes({ anyOf: [{ type: 'string' }, { type: 'null' }] }, null)],
  ['minimum enforced', () => !passes({ type: 'integer', minimum: 1 }, 0)],
  ['$ref sibling rejected', () => { try { check({ $ref: '#/definitions/Date', minLength: 1 }, 'x', '', []); return false; } catch (err) { return true; } }],
  ['cents round-trip', () => money(cents('-12.05') + cents('7.10')) === '-4.95'],
];
console.log('# validator self-tests');
for (const [name, fn] of selfTests) report(fn(), `self-test: ${name}`);

console.log('\n# schema lint');
try {
  lint(bundle, '#');
  report(true, `bundle lint (${Object.keys(bundle.definitions).length} definitions)`);
} catch (err) {
  report(false, 'bundle lint', err.message);
}

function load(dir) {
  const full = path.join(V1, dir);
  return fs.readdirSync(full).filter((f) => f.endsWith('.json')).sort().map((f) => ({ file: `${dir}/${f}`, def: f.split('.')[0], data: JSON.parse(fs.readFileSync(path.join(full, f), 'utf8')) }));
}

const valid = load('examples/valid');
valid.push({ file: 'expected-reports.json', def: 'ExpectedReports', data: JSON.parse(fs.readFileSync(path.join(V1, 'expected-reports.json'), 'utf8')) });
console.log('\n# valid examples: must pass schema and semantic rules');
for (const ex of valid) {
  if (!(ex.def in bundle.definitions)) { report(false, ex.file, `no definition named ${ex.def}`); continue; }
  const errors = allErrors(ex.def, ex.data);
  report(errors.length === 0, `${ex.file} as ${ex.def}`, errors.slice(0, 3).join('; '));
}

console.log('\n# cross-example rules');
const supporting = valid.filter((ex) => ex.def === 'SupportingRows');
for (const metric of valid.filter((ex) => ex.def === 'MetricResult' && ex.data.evidence)) {
  const rows = supporting.find((s) => s.data.metric_run_id === metric.data.evidence.metric_run_id);
  if (!rows) continue;
  const same = metric.data.value && metric.data.value.amount === rows.data.totals.displayed_value;
  report(same, `${metric.file} value equals ${rows.file} displayed_value`);
}

console.log('\n# invalid examples: must be rejected by schema or semantic rules');
for (const ex of load('examples/invalid')) {
  const errors = allErrors(ex.def, ex.data);
  report(errors.length > 0, `${ex.file} rejected`, errors.length ? errors[0] : 'was accepted');
}

console.log('\n# replica output compatibility (data ingestion/examples, upright 2026-09-30)');
const compat = replicaCompatibility();
report(compat.checksumMatches, 'replica CSV SHA-256 equals its manifest', compat.sha);
const onlyZone = compat.errors.length === 1 && compat.errors[0].includes('/reporting_timezone');
if (compat.errors.length === 0) {
  report(true, 'translated replica manifest satisfies SourcePackageManifest v1');
} else if (onlyZone) {
  report(true, `translated replica manifest fails ONLY on reporting_timezone (${compat.zone}) -- KNOWN GAP until ING-02 requests America/New_York`);
} else {
  report(false, 'translated replica manifest needs undocumented translation', compat.errors.join('; '));
}

console.log('\n# top-level contracts with no valid example');
const topLevel = ['SourcePackageManifest', 'AcquisitionRun', 'IntakeResult', 'ImportBatch', 'MetricResult', 'MetricComparison', 'SupportingRows', 'SourceCoverage', 'ExpectedReports', 'ErrorResponse', 'ToolRequest', 'RerunProposal'];
const missing = topLevel.filter((d) => !valid.some((ex) => ex.def === d));
console.log(missing.length ? `none for: ${missing.join(', ')}` : 'none missing');

console.log(`\n${results.pass} passed, ${results.fail} failed`);
process.exitCode = results.fail === 0 ? 0 : 1;
