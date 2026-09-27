import { spawn } from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'au-')); const port = 9800 + Math.floor(Math.random() * 90);
const proc = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank']);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms)); let ws;
for (let i = 0; i < 50; i++) { try { const j = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const t = j.find((x) => x.type === 'page'); if (t) { ws = new WebSocket(t.webSocketDebuggerUrl); break; } } catch {} await sleep(200); }
await new Promise((r) => ws.addEventListener('open', r)); let id = 0; const pend = {}; const logs = [];
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d.result || d); delete pend[d.id]; } if (d.method === 'Runtime.exceptionThrown') logs.push('EXC ' + d.params.exceptionDetails.text); if (d.method === 'Log.entryAdded' && d.params.entry.level === 'error') logs.push('LOG ' + d.params.entry.text + ' ' + (d.params.entry.url || '')); });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send('Runtime.enable'); await send('Log.enable'); await send('Page.enable');
const pages = ['index', 'cursos', 'eventos', 'nosotros', 'contacto'];
const urls = []; for (const l of ['', 'en/', 'es/']) for (const p of pages) urls.push(`http://localhost:5173/${l}${p}.html`); urls.push('http://localhost:5173/x/y', 'http://localhost:5173/en/nope', 'http://localhost:5173/es/nope');
const CHECK = `(async()=>{const W=ms=>new Promise(r=>setTimeout(r,ms));for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await W(60)}scrollTo(0,0);await W(1500);
const r={};const vw=innerWidth;
r.overflowX=document.documentElement.scrollWidth>vw+1?document.documentElement.scrollWidth:0;
r.brokenImg=[...document.images].filter(i=>i.complete&&i.naturalWidth===0&&i.src&&!i.src.startsWith('data:')).map(i=>i.src.split('/').pop()).slice(0,5);
r.noAlt=[...document.images].filter(i=>!i.hasAttribute('alt')).length;
r.noDims=[...document.querySelectorAll('main img')].filter(i=>!i.getAttribute('width')&&!i.closest('.wall')).length;
const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);r.dupIds=[...new Set(ids.filter((x,i)=>ids.indexOf(x)!==i))];
const hs=[...document.querySelectorAll('h1,h2,h3')].map(h=>+h.tagName[1]);r.h1=hs.filter(x=>x===1).length;r.headSkip=hs.some((h,i)=>i&&h-hs[i-1]>1);
r.smallTargets=[...document.querySelectorAll('a,button,input,textarea')].filter(e=>{const b=e.getBoundingClientRect();return b.width&&b.height&&(b.height<24||b.width<24)&&getComputedStyle(e).display!=='inline'}).map(e=>(e.className||e.tagName)+':'+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height)).slice(0,6);
r.emptyLinks=[...document.querySelectorAll('a')].filter(a=>!a.textContent.trim()&&!a.querySelector('img[alt]:not([alt=""])')&&!a.getAttribute('aria-label')).length;
r.deadHref=[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href')).filter(h=>!/^(https?:|mailto:|tel:|#)/.test(h));
r.lang=document.documentElement.lang;r.title=document.title.slice(0,40);
const low=[];document.querySelectorAll('main p, main li, main dd, main dt, main span, main a, main h1, main h2, main h3').forEach(e=>{if(!e.childNodes.length||![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;const cs=getComputedStyle(e);if(parseFloat(cs.fontSize)<12.5)low.push(e.className||e.tagName)});r.tinyText=[...new Set(low)].slice(0,6);
return r})()`;
const lvl = process.argv[2] || 1440; const out = {};
await send('Emulation.setDeviceMetricsOverride', { width: +lvl, height: 900, deviceScaleFactor: 1, mobile: +lvl < 768 });
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
const hrefs = new Set();
for (const u of urls) { logs.length = 0; await send('Page.navigate', { url: u }); await sleep(1200);
  const v = (await send('Runtime.evaluate', { expression: CHECK, awaitPromise: true, returnByValue: true })).result.value;
  v.deadHref.forEach((h) => hrefs.add(new URL(h, u).href.split('#')[0].split('?')[0])); delete v.deadHref;
  v.console = [...logs]; const k = u.replace('http://localhost:5173/', '');
  const bad = Object.entries(v).filter(([kk, x]) => !['lang', 'title', 'h1'].includes(kk) && (Array.isArray(x) ? x.length : x));
  out[k] = { lang: v.lang, h1: v.h1, ...Object.fromEntries(bad) }; }
const dead = []; for (const h of hrefs) { const s = (await fetch(h)).status; if (s !== 200) dead.push(s + ' ' + h); }
console.log(JSON.stringify(out, null, 0).replace(/\},"/g, '},\n"')); console.log('internal links checked', hrefs.size, 'dead:', dead);
ws.close(); proc.kill();
