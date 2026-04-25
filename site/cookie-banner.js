(function(){
  if(localStorage.getItem('wr_cookies')==='1')return;
  var b=document.createElement('div');
  b.id='cookie-banner';
  b.innerHTML='<div style="max-width:900px;margin:0 auto;display:flex;align-items:center;gap:16px;flex-wrap:wrap"><span style="flex:1;min-width:200px">We use essential cookies for site functionality. No tracking or advertising cookies. <a href="/privacy.html" style="color:#4f8cff">Privacy Policy</a></span><button onclick="document.getElementById(\'cookie-banner\').remove();localStorage.setItem(\'wr_cookies\',\'1\')" style="padding:8px 20px;background:#4f8cff;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:600;font-size:13px;white-space:nowrap">Accept</button><button onclick="document.getElementById(\'cookie-banner\').remove();localStorage.setItem(\'wr_cookies\',\'1\')" style="padding:8px 16px;background:none;color:#8b94a8;border:1px solid #2e3a52;border-radius:6px;cursor:pointer;font-size:13px;white-space:nowrap">Dismiss</button></div>';
  b.style.cssText='position:fixed;bottom:0;left:0;right:0;background:rgba(11,15,26,.95);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-top:1px solid #1f2738;padding:16px 24px;z-index:9999;font-family:Inter,system-ui,sans-serif;font-size:13px;color:#8b94a8;animation:cbSlide .3s ease';
  var s=document.createElement('style');s.textContent='@keyframes cbSlide{from{transform:translateY(100%)}to{transform:translateY(0)}}';
  document.head.appendChild(s);
  document.body.appendChild(b);
})();
