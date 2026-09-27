// prints the page Y of a selector at a width: node find.mjs url width selector
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
const [url, w, sel] = process.argv.slice(2);
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'fd-')); const port = 9600 + Math.floor(Math.random() * 90);
const proc = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank']);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms)); let ws;
for (let i = 0; i < 50; i++) { try { const j = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const t = j.find((x) => x.type === 'page'); if (t) { ws = new WebSocket(t.webSocketDebuggerUrl); break; } } catch {} await sleep(200); }
await new Promise((r) => ws.addEventListener('open', r)); let id = 0; const pend = {};
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d.result || d); delete pend[d.id]; } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
await send('Emulation.setDeviceMetricsOverride', { width: +w, height: 900, deviceScaleFactor: 1, mobile: +w < 768 });
await send('Page.enable'); await send('Page.navigate', { url }); await sleep(2500);
const r = await send('Runtime.evaluate', { expression: `(()=>{const e=document.querySelector(${JSON.stringify(sel)});const b=e.getBoundingClientRect();const p=e.querySelector('p');return JSON.stringify({y:Math.round(b.top+scrollY),h:Math.round(b.height),w:Math.round(b.width),scrollH:e.scrollHeight,pFont:getComputedStyle(p).fontSize,overflow:e.scrollHeight>e.clientHeight+1})})()`, returnByValue: true });
console.log(r.result.value); ws.close(); proc.kill();
