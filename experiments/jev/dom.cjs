'use strict';
const {DecisionError} = require('./provider.cjs');
async function observe(scope, selector) {
  const locators = await scope.locator(selector).all();
  const candidates = [], targets = new Map();
  for (const locator of locators) {
    if (!await locator.isVisible() || !await locator.isEnabled()) continue;
    const metadata = await locator.evaluate(el => ({
      label: el.getAttribute('aria-label') || [...(el.labels || [])].map(l => l.textContent.trim()).join(' ') || el.textContent.trim(),
      role: el.getAttribute('role') || ({A: 'link', BUTTON: 'button', INPUT: 'input', SELECT: 'select'}[el.tagName]),
      value: el.value || '', enabled: !el.disabled, type: el.type || '', href: el.getAttribute('href') || ''
    }));
    if (metadata.type === 'password' || metadata.type === 'file') continue;
    const id = `control_${candidates.length + 1}`;
    candidates.push({id, ...metadata});
    targets.set(id, {locator, metadata: JSON.stringify(metadata), node: await locator.elementHandle()});
  }
  if (candidates.length > 254) throw new DecisionError('too_many_controls', 'Candidate set exceeds bounded Choice limit');
  return {candidates, targets};
}
async function recheck(target) {
  if (!target || !await target.locator.isVisible() || !await target.locator.isEnabled() ||
      !await target.node.evaluate(el => el.isConnected)) throw new DecisionError('stale_target', 'Control detached, hidden or disabled');
  const same = await target.locator.evaluate((el, original) => el === original, target.node);
  const current = await observe({locator: () => ({all: async () => [target.locator]})}, '');
  const metadata = current.candidates[0];
  if (!metadata) throw new DecisionError('stale_target', 'Control unavailable');
  const {id, ...fields} = metadata;
  if (!same || JSON.stringify(fields) !== target.metadata) throw new DecisionError('stale_target', 'Control changed after decision');
  await target.locator.click({trial: true});
}
module.exports = {observe, recheck};
