// usage: node capture.mjs <outdir> <width> <name=path>...
import { spawn } from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
const [outDir, width, ...pages] = process.argv.slice(2);
const chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'cap-'));
const port = 9333 + Math.floor(Math.random() * 500);
const proc = spawn(chrome, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--hide-scrollbars', 'about:blank']);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws;
for (let i = 0; i < 50; i++) { try { const j = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const t = j.find((x) => x.type === 'page'); if (t) { ws = new WebSocket(t.webSocketDebuggerUrl); break; } } catch {} await sleep(200); }
await new Promise((r) => ws.addEventListener('open', r));
let id = 0; const pend = {};
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d.result || d); delete pend[d.id]; } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const w = +width, mobile = w < 768;
await send('Emulation.setDeviceMetricsOverride', { width: w, height: mobile ? 844 : 900, deviceScaleFactor: 1, mobile });
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
for (const p of pages) {
  const [name, url] = p.split('=');
  await send('Page.enable');
  await send('Page.navigate', { url });
  await sleep(1500);
  await send('Runtime.evaluate', { expression: 'new Promise(async r=>{for(let y=0;y<document.documentElement.scrollHeight;y+=500){scrollTo(0,y);await new Promise(s=>setTimeout(s,300))}scrollTo(0,0);setTimeout(r,5000)})', awaitPromise: true });
  const r = await send('Runtime.evaluate', { expression: 'document.documentElement.scrollHeight', returnByValue: true });
  const h = r.result.value;
  const over = await send('Runtime.evaluate', { expression: `JSON.stringify([...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().right>${w}+1).map(e=>e.tagName+'.'+e.className).slice(0,8))`, returnByValue: true });
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, width: w, height: Math.min(h, +process.env.MAXH || h), y: +process.env.Y0 || 0, scale: 1 } });
  fs.writeFileSync(path.join(outDir, `${name}.png`), Buffer.from(shot.data, 'base64'));
  console.log(name, w, h, 'overflow:', over.result.value);
}
ws.close(); proc.kill();
