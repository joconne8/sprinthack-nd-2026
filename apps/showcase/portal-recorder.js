/* Local replica instrumentation. Page text is observed data, never executable instructions. */
'use strict';
(() => {
  const prefix = '/showcase/portal';
  const params = new URLSearchParams(location.search);
  if (params.get('recording_id') && params.get('recorder_nonce')) {
    sessionStorage.setItem('showcase-recorder', JSON.stringify({id: params.get('recording_id'), nonce: params.get('recorder_nonce')}));
  }
  let session;
  try { session = JSON.parse(sessionStorage.getItem('showcase-recorder')); } catch { session = null; }
  const path = location.pathname.slice(prefix.length) || '/';
  const observe = () => [...document.querySelectorAll('h1, label, button, #messages')].filter(e => e.getClientRects().length).map(e => e.textContent.trim()).join(' | ').slice(0, 1500);
  const emit = event => {
    if (!session || parent === window) return;
    parent.postMessage({type: 'showcase-recorder', recording_id: session.id, nonce: session.nonce,
      event: {...event, path, observation: observe()}}, location.origin);
  };
  const anchors = () => document.querySelectorAll('a[href^="/"]').forEach(a => {
    if (!a.getAttribute('href').startsWith(prefix)) a.setAttribute('href', prefix + a.getAttribute('href'));
  });
  let ready = false;
  const update = () => {
    anchors();
    if (!ready && document.querySelector('#messages.success')) { ready = true; emit({op: 'ready'}); }
  };
  new MutationObserver(update).observe(document.body, {childList: true, subtree: true, attributes: true, attributeFilter: ['class']});
  update();
  emit({op: 'navigate'});
  document.addEventListener('click', event => {
    const element = event.target.closest('a,button');
    if (!element) return;
    const name = element.textContent.trim().replace(/\s+/g, ' ');
    const download = (element.getAttribute('href') || '').match(/\/api\/reports\/([a-f0-9]{32})\/download/);
    if (element.tagName === 'A' && download) emit({op: 'download', role: 'link', name, value: download[1]});
    else if ((element.tagName === 'A' && ['▥ Reports', 'Paid orders', 'Orders'].includes(name)) ||
      (element.tagName === 'BUTTON' && ['Generate report', 'Build export', 'Submit'].includes(name))) {
      emit({op: 'click', role: element.tagName === 'A' ? 'link' : 'button', name});
    }
  }, true);
  document.addEventListener('change', event => {
    const element = event.target;
    if (!['INPUT', 'SELECT'].includes(element.tagName) || element.type === 'password') return;
    const label = element.labels?.[0]?.textContent.trim();
    if (!['Start date', 'End date', 'Timezone', 'Payment status', 'Channel', 'Order Date From:', 'Order Date To:', 'Format:'].includes(label)) return;
    emit({op: element.tagName === 'SELECT' ? 'select' : 'fill', label, value: element.value});
  }, true);
})();
