import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const root = path.resolve(process.argv[2] || 'site'); const port = +process.argv[3] || 5173;
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg' };
const notFound = (p) => path.join(root, /^\/(en|es)\//.test(p) ? p.slice(1, 3) : '', '404.html');
http.createServer((req, res) => {
  let p = decodeURIComponent(new URL(req.url, 'http://x').pathname); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, p); if (!f.startsWith(root)) { res.writeHead(403).end(); return; }
  fs.readFile(f, (e, d) => {
    if (!e) { res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream', 'cache-control': 'no-store' }).end(d); return; }
    fs.readFile(notFound(p), (e2, d2) => res.writeHead(404, { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' }).end(e2 ? 'Not found' : d2));
  });
}).listen(port, () => console.log('serving', root, port));
