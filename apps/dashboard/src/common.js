export const $ = id => document.getElementById(id);
export function el(tag, text, className) { const node = document.createElement(tag); if (text !== undefined) node.textContent = String(text); if (className) node.className = className; return node; }
export function badge(value) {return el('span', value.replaceAll('_', ' '), 'badge '+value);}
export function money(value) {if(value === null || value === undefined) return 'Unavailable'; const [whole, cents='00'] = value.split('.'); return '$'+whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',')+'.'+cents;}
export function timestamp(value) {return value ? new Date(value).toLocaleString(undefined, {timeZone:'America/New_York',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'})+' ET' : 'Not yet available';}
export async function api(path, body, signal) {
  const response = await fetch(path, {signal, ...(body === undefined ? {} : {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})});
  const result = await response.json();
  if(!response.ok) {const error = new Error(result.error?.detail || 'The request failed. Please try again.'); error.body=result; throw error;}
  if(result.contract_version !== 'goodwill-v1' || result.synthetic !== true) throw new Error('Unexpected report response. Refresh or contact the demo maintainer.');
  return result;
}
export function query(filters) {const params=new URLSearchParams(); for(const [key,value] of Object.entries(filters)) if(value!==null && value!==undefined && value!=='') params.set(key,String(value)); return params.toString();}
export function table(headers, rows) {const node=el('table');const head=el('thead');const tr=el('tr');for(const title of headers){const th=el('th',title);th.scope='col';tr.append(th);}head.append(tr);node.append(head);const body=el('tbody');for(const row of rows){const tr=el('tr');for(const value of row){const td=el('td');value instanceof Node ? td.append(value) : td.textContent=String(value ?? '—');tr.append(td);}body.append(tr);}node.append(body);return node;}
export function action(label, handler) {const button=el('button',label,'table-action');button.type='button';button.addEventListener('click',handler);return button;}
export function errorNotice(error) {$('global-error').textContent=error.message || String(error);$('global-error').hidden=false;}
export function clearError() {$('global-error').hidden=true;}
