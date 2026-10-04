'use strict';
// Injected only into the synthetic portal controlled by our isolated browser.
function recorderScript() {
  const describe = el => ({label:el.getAttribute('aria-label') || [...(el.labels||[])].map(l=>l.textContent.trim()).join(' ') || el.textContent.trim(),
    role:el.tagName==='A'?'link':el.tagName==='BUTTON'?'button':el.tagName==='SELECT'?'select':'input',
    href:el.getAttribute('href')||'',value:el.value||'',page:location.pathname});
  const snapshot=()=>[...document.querySelectorAll('a,button,input[type=date],select')]
    .filter(el=>el.getClientRects().length && !el.disabled)
    .map(describe).slice(0,60);
  document.addEventListener('click',event=>{
    const el=event.target.closest('a,button');
    if(el) window.recordStep({op:'click',...describe(el),before:snapshot()}).catch(()=>{});
  },true);
  document.addEventListener('change',event=>{
    const el=event.target;
    if(el.matches('input[type=date],select')) window.recordStep({op:el.tagName==='SELECT'?'select':'fill',...describe(el),before:snapshot()}).catch(()=>{});
  },true);
}
module.exports={recorderScript};
