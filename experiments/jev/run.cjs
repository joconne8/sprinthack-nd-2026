'use strict';
const path = require('node:path');
const {runSkill} = require('../../acquisition/run_skill.cjs');
const {observe, recheck} = require('./dom.cjs');
const {DecisionError} = require('./provider.cjs');

async function runJev(request, provider, emit = () => {}) {
  let decisionFailure;
  const result = await runSkill(request.skillPath || path.resolve(__dirname, '../../acquisition/skills/upright-paid-orders.skill.json'), {
    ...request, deadlineMs: 60000,
    pageSetup: async page => {
      if (request.pageSetup) await request.pageSetup(page);
      const originalLocator = page.locator.bind(page);
      const wrap = (locator, description, scope = page) => new Proxy(locator, {get(object, key) {
        if (['click', 'fill', 'selectOption'].includes(key)) return async (...args) => {
          try {
            let selector;
            let reportParametersVerified = false;
            let goal = description.name || description.label;
            if (key === 'fill') selector = 'input[type=date]';
            else if (key === 'selectOption') selector = 'select';
            else if (description.name === 'Generate report') {
              selector = '#report-form button[type=submit]';
              goal = 'Generate the paid-orders CSV report using the currently selected dates';
              const start = await originalLocator('#start-date').inputValue();
              const end = await originalLocator('#end-date').inputValue();
              if (start !== request.startDate || end !== request.endDate ||
                  await originalLocator('#timezone').inputValue() !== 'America/Indiana/Indianapolis' ||
                  await originalLocator('#payment-status').inputValue() !== 'All') {
                throw new DecisionError('wrong_parameters', 'Form parameters differ from requested report');
              }
              reportParametersVerified = true;
            } else if (description.selector) {
              // Download is bound to the deterministic job ID, never to newest/first.
              selector = description.selector;
              goal = 'Download the CSV for the verified current report job';
            } else selector = 'a[href="/upright/reports"], a[href="/upright/reports/paid-orders"]';
            const state = await observe(scope === page ? {locator: originalLocator} : scope, selector);
            emit('observe', {goal, action: key, controls: state.candidates});
            const decision = await provider.choose(`${key}: ${goal}`, state.candidates,
              {action: key, fieldLabel: description.label, reportParametersVerified,
                reportSubmission: description.name === 'Generate report'});
            const target = state.targets.get(decision.id);
            if (!target) throw new DecisionError('invalid_decision', 'Unknown control identity');
            // Field semantics are invariant even if control order changes.
            const chosen = state.candidates.find(c => c.id === decision.id);
            if ((key === 'fill' || key === 'selectOption') && chosen.label !== description.label)
              throw new DecisionError('wrong_control', 'Jev selected a different parameter field');
            if (description.name === 'Paid orders' && chosen.href !== '/upright/reports/paid-orders')
              throw new DecisionError('wrong_control', 'Jev selected a different report');
            if (description.name === '▥ Reports' && chosen.href !== '/upright/reports')
              throw new DecisionError('wrong_control', 'Jev selected a different destination');
            await recheck(target);
            if (request.approve && description.name === 'Generate report' && chosen.label !== description.name) {
              await target.locator.evaluate(el => {el.style.outline = '4px solid #7c3aed'; el.scrollIntoView({block:'center'});});
              await request.approve({goal, original: description.name, proposed: chosen, decision});
              await recheck(target);
            }
            emit('choose', {action: key, goal, decision, target: chosen, value: key === 'click' ? undefined : args[0]});
            await target.locator[key](...args);
            emit('act', {action: key, target: chosen.id, completed: true});
            if (request.headed) await page.waitForTimeout(450);
          } catch (error) {
            decisionFailure = {type: error.code || 'browser_action_failed', detail: error.code ? error.message : 'Browser action failed; inspect local trace'};
            throw error;
          }
        };
        if (key === 'getByRole') return (role, options) => wrap(object.getByRole(role, options), options, object);
        const value = object[key]; return typeof value === 'function' ? value.bind(object) : value;
      }});
      const role = page.getByRole.bind(page), label = page.getByLabel.bind(page);
      page.getByRole = (r, o) => wrap(role(r, o), o);
      page.getByLabel = (l, o) => wrap(label(l, o), {label: l});
      page.locator = (s, o) => wrap(originalLocator(s, o), {selector: s});
    }
  });
  return decisionFailure ? {...result, ok: false, ...decisionFailure} : result;
}
module.exports = {runJev};
