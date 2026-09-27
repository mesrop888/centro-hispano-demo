import { spawn } from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
const [url, outDir] = process.argv.slice(2);
const prof = fs.mkdtempSync(path.join(os.tmpdir(), 'bt-')); const port = 9700 + Math.floor(Math.random() * 90);
const proc = spawn('C:/Program Files/Google/Chrome/Application/chrome.exe', ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, 'about:blank']);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms)); let ws;
for (let i = 0; i < 50; i++) { try { const j = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const t = j.find((x) => x.type === 'page'); if (t) { ws = new WebSocket(t.webSocketDebuggerUrl); break; } } catch {} await sleep(200); }
await new Promise((r) => ws.addEventListener('open', r)); let id = 0; const pend = {};
ws.addEventListener('message', (m) => { const d = JSON.parse(m.data); if (d.id && pend[d.id]) { pend[d.id](d.result || d); delete pend[d.id]; } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => (await send('Runtime.evaluate', { expression: e, returnByValue: true })).result.value;
const shot = async (n) => { const s = await send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: 390, height: 330, scale: 1 } }); fs.writeFileSync(path.join(outDir, n + '.png'), Buffer.from(s.data, 'base64')); };
await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 700, deviceScaleFactor: 2, mobile: true });
await send('Page.enable'); await send('Page.navigate', { url }); await sleep(2500);
const state = () => ev("document.querySelector('.menu-btn').getAttribute('aria-expanded') + ' | ' + document.querySelector('.menu-btn').getAttribute('aria-label')");
console.log('closed:', await state());
await ev("document.querySelector('.menu-btn').click()"); await sleep(500); await shot('burger-open'); console.log('open:  ', await state());
await ev("document.querySelector('.menu-btn').click()"); await sleep(500); console.log('closed:', await state());
ws.close(); proc.kill();
