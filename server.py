"""Centro Hispano: a small static web server for the site/ folder.

Standard library only; needs Python 3.8+.

    python server.py              -> http://localhost:5173
    python server.py 8080         -> custom port
    PORT=8080 python server.py    -> custom port via environment (used by hosts like Render)
"""

import os
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = (Path(__file__).parent / "site").resolve()
LANGS = ("en", "es")  # Armenian lives at the root


class SiteHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "text/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
        ".webp": "image/webp",
        ".avif": "image/avif",
        ".woff2": "font/woff2",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    # Only GET and HEAD are served
    def do_POST(self):
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED)
        self.send_header("Allow", "GET, HEAD")
        self.send_header("Content-Length", "0")
        self.end_headers()

    do_PUT = do_DELETE = do_PATCH = do_POST

    def send_head(self):
        url_path = unquote(urlsplit(self.path).path)
        target = (ROOT / url_path.lstrip("/")).resolve()

        # Never serve anything outside site/
        if target != ROOT and ROOT not in target.parents:
            self.send_error(HTTPStatus.FORBIDDEN, "Forbidden")
            return None

        # Folders: redirect /en to /en/, then serve index.html
        if target.is_dir():
            if not url_path.endswith("/"):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", url_path + "/")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return None
            target = target / "index.html"

        if target.is_file():
            return super().send_head()

        return self.send_not_found(url_path)

    def send_not_found(self, url_path):
        """Serve the 404 page matching the language folder of the request."""
        first = url_path.strip("/").split("/")[0]
        page = ROOT / (first if first in LANGS else "") / "404.html"
        body = page.read_bytes() if page.is_file() else b"Not found"
        self.send_response(HTTPStatus.NOT_FOUND)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)
        return None

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, fmt % args))


class SiteServer(ThreadingHTTPServer):
    # On Windows, address reuse lets two servers share a port silently; refuse instead.
    allow_reuse_address = os.name != "nt"
    daemon_threads = True


def main():
    port = int(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("PORT", 5173))
    try:
        server = SiteServer(("0.0.0.0", port), SiteHandler)
    except OSError:
        sys.exit(f"Port {port} is already in use. Try: python server.py {port + 1}")

    base = f"http://localhost:{port}"
    print("\n  Centro Hispano is running\n")
    print(f"  Armenian  {base}/")
    print(f"  English   {base}/en/")
    print(f"  Spanish   {base}/es/")
    print("\n  Press Ctrl+C to stop.\n", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")


if __name__ == "__main__":
    main()
