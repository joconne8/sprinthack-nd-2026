#!/usr/bin/env node
'use strict';
// A visible scripted DOM replay, not a Jev model or a general-purpose agent.
const fs = require('node:fs');
const path = require('node:path');
const {runSkill} = require('../../acquisition/run_skill.cjs');

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log('Usage: mockup.cjs START_DATE [END_DATE] [--provider scripted-mock|jev] [--headed] [--mode normal|session-expired|changed-label|missing-report|delayed]\nJev requires TYPESAFE_API_KEY. BASE_URL defaults to http://127.0.0.1:4173; OUTPUT_DIR defaults to .runtime/jev-mockup');
    return;
  }
  const startDate = args[0] || '2026-09-30';
  const endDate = args[1] && !args[1].startsWith('--') ? args[1] : startDate;
  const modeIndex = args.indexOf('--mode');
  const mode = modeIndex >= 0 ? args[modeIndex + 1] : 'normal';
  const providerIndex = args.indexOf('--provider');
  const providerName = providerIndex < 0 ? 'scripted-mock' : args[providerIndex + 1];
  if (!['scripted-mock', 'jev'].includes(providerName)) throw new Error('Provider must be scripted-mock or jev');
  const outputDir = path.resolve(process.env.OUTPUT_DIR || '.runtime/jev-mockup', new Date().toISOString().replace(/[:.]/g, '-') + '-' + process.pid);
  fs.mkdirSync(outputDir, {recursive: true});
  const events = [];
  const began = Date.now();
  const emit = (phase, detail) => {
    const event = {elapsed_ms: Date.now() - began, phase, provider: providerName, ...detail};
    events.push(event);
    fs.appendFileSync(path.join(outputDir, 'trace.jsonl'), JSON.stringify(event) + '\n');
    console.log(JSON.stringify(event));
  };
  emit('disclosure', {message: providerName === 'jev' ? 'Actual Jev decisions; synthetic local portal only.' : 'Scripted decisions; synthetic local portal; zero model calls.'});
  const {chromium} = require('playwright');
  let browser;
  let provider;
  try {
    if (providerName === 'jev') provider = new (require('./provider.cjs').JevProvider)({emit, deadline: began + 60000});
    // Let the existing runner validate URL/dates before any navigation.
    if (args.includes('--headed')) browser = await chromium.launch({headless: false,
      ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
    const run = provider ? (_, request) => require('./run.cjs').runJev({...request, headed: args.includes('--headed'), pageSetup: undefined}, provider, emit) : runSkill;
    let result = await run(path.resolve(__dirname, '../../acquisition/skills/upright-paid-orders.skill.json'), {
      baseUrl: process.env.BASE_URL || 'http://127.0.0.1:4173', startDate, endDate,
      outputDir, mode, browser,
      pageSetup: async page => {
        // Observe the actual locator at action time; never execute page text as instructions.
        const wrap = (locator, target) => new Proxy(locator, {
          get(object, key) {
            if (['click', 'fill', 'selectOption'].includes(key)) return async (...params) => {
              await object.waitFor({state: 'visible'});
              const count = await object.count();
              emit('observe', {target, count, visible: await object.isVisible(), enabled: await object.isEnabled(),
                dom: (await object.ariaSnapshot()).slice(0, 2000)});
              if (count !== 1 || !await object.isEnabled()) throw new Error('Ambiguous or disabled control; human review required');
              emit('choose', {action: key, target, value: key === 'click' ? undefined : params[0],
                basis: 'Versioned replay selects this exact observed control; no AI inference.'});
              await object[key](...params);
              emit('act', {action: key, target, completed: true});
              if (args.includes('--headed')) await page.waitForTimeout(450);
            };
            if (['getByRole', 'getByLabel', 'locator'].includes(key)) return (...params) => wrap(object[key](...params), {parent: target, locator: key, arguments: params});
            const value = object[key];
            return typeof value === 'function' ? value.bind(object) : value;
          }
        });
        for (const name of ['getByRole', 'getByLabel', 'locator']) {
          const original = page[name].bind(page);
          page[name] = (...params) => wrap(original(...params), {locator: name, arguments: params});
        }
      }
    });
    if (result.ok) {
      try { result.verification = require('./verify.cjs').verifyFile(result, startDate, endDate); }
      catch { result = {...result, ok: false, type: 'content_validation_failed', detail: 'Downloaded CSV failed deterministic content checks'}; }
    }
    emit(result.ok ? 'verify' : 'stop', {result, message: result.ok ? 'Download checksum, source, report type, dates and CSV rows verified.' : 'Replay stopped; no success claimed.'});
    if (result.ok) fs.writeFileSync(path.join(outputDir, 'source.manifest.json'), JSON.stringify(result.manifest, null, 2) + '\n');
    fs.writeFileSync(path.join(outputDir, 'result.json'), JSON.stringify({provider: providerName, ...(provider ? provider.usage() : {model_calls: 0}),
      synthetic: true, elapsed_ms: Date.now() - began, result}, null, 2) + '\n');
    console.log(`Evidence: ${outputDir}`);
    process.exitCode = result.ok ? 0 : 1;
  } catch (error) {
    const result = {ok: false, type: error.code || 'runtime_error', detail: error.code ? error.message : 'Runtime failed; check browser/dependency setup'};
    emit('stop', {result});
    fs.writeFileSync(path.join(outputDir, 'result.json'), JSON.stringify({provider: providerName, ...(provider ? provider.usage() : {model_calls: 0}), synthetic: true, result}, null, 2));
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
  }
}
if (require.main === module) main().catch(error => {console.error(error.message); process.exitCode = 1;});
