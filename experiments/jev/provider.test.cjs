const {test} = require('node:test');
const assert = require('node:assert/strict');
const {JevProvider, validateAnswer} = require('./provider.cjs');
const controls = [{id: 'a', label: 'Build export', role: 'button'}];
const answer = () => ({model: 'jev-1.13.0', answers: {target: {type: 'choice', choice: 'a', confidence: 0.98, probabilities: {a: 0.99, STOP: 0.01}}}, usage: {input_tokens: 100, output_tokens: 10}});
test('accepts bounded high-confidence target', () => assert.equal(validateAnswer(answer(), controls).id, 'a'));
test('invalid IDs, probabilities, models and low confidence fail', () => {
  for (const change of [b => b.answers.target.choice = 'unknown', b => b.answers.target.confidence = 0.8,
    b => b.answers.target.probabilities.a = NaN, b => b.answers.target.probabilities.a = 0.5,
    b => b.model = 'another-model', b => b.answers.target.probabilities.extra = 0]) {
    const body = answer(); change(body); assert.throws(() => validateAnswer(body, controls));
  }
});
test('STOP fails closed', () => {
  const b = answer(); b.answers.target.choice = 'STOP'; b.answers.target.probabilities = {a: 0.01, STOP: 0.99};
  assert.throws(() => validateAnswer(b, controls), {code: 'model_stopped'});
});
test('missing key fails before network', () => assert.throws(() => new JevProvider({key: ''}), {code: 'missing_credentials'}));
test('API errors never retry or log error bodies/keys', async () => {
  let calls = 0; const events = [];
  const p = new JevProvider({key: 'test-secret', emit: (...e) => events.push(e), fetchFn: async () => {calls++; return {ok: false, status: 401};}});
  await assert.rejects(p.choose('Generate', controls), {code: 'api_error'});
  assert.equal(calls, 1); assert(!JSON.stringify(events).includes('test-secret'));
});
test('transport failures and malformed JSON stop', async () => {
  for (const fetchFn of [async () => {throw new Error('secret transport text');}, async () => ({ok: true, json: async () => {throw new Error('secret');}})]) {
    const p = new JevProvider({key: 'test', fetchFn});
    await assert.rejects(p.choose('Generate', controls)); assert.equal(p.calls, 1);
  }
});
test('tracks actual usage; enforces request and time caps', async () => {
  const p = new JevProvider({key: 'test', fetchFn: async () => ({ok: true, json: async () => answer()})});
  await p.choose('Generate', controls); assert.deepEqual(p.usage(), {model_calls: 1, input_tokens: 100, output_tokens: 10});
  p.calls = 20; await assert.rejects(p.choose('Generate', controls), {code: 'budget_exceeded'});
  p.calls = 0; p.deadline = 0; await assert.rejects(p.choose('Generate', controls), {code: 'budget_exceeded'});
});
test('field requests identify the literal label independently of current date values', async () => {
  let payload;
  const candidates = [{id:'a',label:'End date',value:'2026-09-30'}, {id:'b',label:'Start date',value:'2026-09-30'}];
  const p = new JevProvider({key:'test',fetchFn:async (_, options) => {
    payload=JSON.parse(options.body);
    const body=answer(); body.answers.target.probabilities={a:0.99,b:0,STOP:0.01};
    return {ok:true,json:async()=>body};
  }});
  await p.choose('fill: End date', candidates, {action:'fill',fieldLabel:'End date'});
  assert.equal(payload.state.requested_field_label,'End date');
  assert.match(payload.questions.target.instructions,/label exactly equals/);
  assert.match(payload.questions.target.instructions,/not deciding its value/);
  assert.match(payload.questions.target.instructions,/Do not compare or infer dates/);
});
test('generation asks for the next action after independently verified parameters', async () => {
  let payload;
  const p = new JevProvider({key:'test',fetchFn:async (_, options) => {
    payload=JSON.parse(options.body); return {ok:true,json:async()=>answer()};
  }});
  await p.choose('Generate the paid-orders report', controls, {action:'click',reportSubmission:true,reportParametersVerified:true});
  assert.equal(payload.state.report_parameters_verified_by_code,true);
  assert.match(payload.questions.target.instructions,/which button to click next/);
  assert.match(payload.questions.target.instructions,/not whether a report has already been generated/);
  assert.match(payload.questions.target.instructions,/Build export/);
  assert.equal(validateAnswer(answer(), controls).confidence,0.98);
});
