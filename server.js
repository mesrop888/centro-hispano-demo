// Centro Hispano: a small static web server for the site/ folder.
// No dependencies; needs only Node.js 18+.
//
//   node server.js              → http://localhost:5173
//   node server.js 8080         → custom port
//   PORT=8080 node server.js    → custom port via environment

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.join(__dirname, 'site');
const PORT = Number(process.argv[2] || process.env.PORT || 5173);
const LANGS = ['en', 'es']; // Armenian lives at the root

const TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.avif': 'image/avif',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
};

// The 404 page matching the language folder of the requested path.
function notFoundPage(urlPath) {
  const lang = urlPath.split('/')[1];
  return path.join(ROOT, LANGS.includes(lang) ? lang : '', '404.html');
}

function send(res, status, file, body) {
  res.writeHead(status, {
    'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream',
    'Cache-Control': 'no-cache',
    'X-Content-Type-Options': 'nosniff',
  });
  res.end(body);
}

const server = http.createServer((req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    res.writeHead(405, { Allow: 'GET, HEAD' }).end();
    return;
  }

  let urlPath;
  try {
    urlPath = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  } catch {
    res.writeHead(400).end('Bad request');
    return;
  }

  // Folders serve their index.html; /en redirects to /en/
  let file = path.join(ROOT, urlPath);
  if (!file.startsWith(ROOT)) { res.writeHead(403).end('Forbidden'); return; }
  try {
    if (fs.statSync(file).isDirectory()) {
      if (!urlPath.endsWith('/')) { res.writeHead(301, { Location: urlPath + '/' }).end(); return; }
      file = path.join(file, 'index.html');
    }
  } catch { /* missing: handled below */ }

  fs.readFile(file, (err, data) => {
    if (!err) { send(res, 200, file, req.method === 'HEAD' ? undefined : data); return; }
    const page = notFoundPage(urlPath);
    fs.readFile(page, (err404, html) => {
      send(res, 404, page, err404 ? 'Not found' : html);
    });
    console.log(`404 ${urlPath}`);
  });
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE') {
    console.error(`Port ${PORT} is already in use. Try: node server.js ${PORT + 1}`);
  } else {
    console.error(err.message);
  }
  process.exit(1);
});

server.listen(PORT, () => {
  const base = `http://localhost:${PORT}`;
  console.log('\n  Centro Hispano is running\n');
  console.log(`  Armenian  ${base}/`);
  console.log(`  English   ${base}/en/`);
  console.log(`  Spanish   ${base}/es/`);
  console.log('\n  Press Ctrl+C to stop.\n');
});
