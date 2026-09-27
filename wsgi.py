"""Centro Hispano as a WSGI app, for hosts such as PythonAnywhere.

Serves the site/ folder with the same rules as server.py:
folder redirects, language-matched 404 pages, nothing outside site/.
Standard library only.

Local test:  python wsgi.py   -> http://localhost:8000
"""

import mimetypes
from pathlib import Path
from urllib.parse import unquote

ROOT = (Path(__file__).parent / "site").resolve()
LANGS = ("en", "es")  # Armenian lives at the root

TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
}


def _headers(content_type, length):
    return [
        ("Content-Type", content_type),
        ("Content-Length", str(length)),
        ("Cache-Control", "no-cache"),
        ("X-Content-Type-Options", "nosniff"),
    ]


def _not_found(url_path, start_response, head):
    first = url_path.strip("/").split("/")[0]
    page = ROOT / (first if first in LANGS else "") / "404.html"
    body = page.read_bytes() if page.is_file() else b"Not found"
    start_response("404 Not Found", _headers("text/html; charset=utf-8", len(body)))
    return [b"" if head else body]


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    if method not in ("GET", "HEAD"):
        start_response("405 Method Not Allowed", [("Allow", "GET, HEAD"), ("Content-Length", "0")])
        return [b""]
    head = method == "HEAD"

    # PATH_INFO arrives decoded as latin-1 per PEP 3333; recover the UTF-8 path
    raw = environ.get("PATH_INFO", "/") or "/"
    try:
        url_path = unquote(raw.encode("latin-1").decode("utf-8"))
    except UnicodeError:
        url_path = raw

    target = (ROOT / url_path.lstrip("/")).resolve()
    if target != ROOT and ROOT not in target.parents:
        body = b"Forbidden"
        start_response("403 Forbidden", _headers("text/plain; charset=utf-8", len(body)))
        return [body]

    if target.is_dir():
        if not url_path.endswith("/"):
            query = environ.get("QUERY_STRING")
            location = url_path + "/" + (f"?{query}" if query else "")
            start_response("301 Moved Permanently", [("Location", location), ("Content-Length", "0")])
            return [b""]
        target = target / "index.html"

    if not target.is_file():
        return _not_found(url_path, start_response, head)

    body = target.read_bytes()
    ctype = TYPES.get(target.suffix.lower()) or mimetypes.guess_type(target.name)[0] or "application/octet-stream"
    start_response("200 OK", _headers(ctype, len(body)))
    return [b"" if head else body]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    print("Centro Hispano (WSGI) on http://localhost:8000  (Ctrl+C to stop)")
    make_server("", 8000, application).serve_forever()
