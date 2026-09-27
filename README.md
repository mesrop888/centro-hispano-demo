# Centro Hispano website

Static site in three languages: Armenian (main, at the root), English (`/en/`) and Spanish (`/es/`).

## Run it locally

Needs [Python](https://www.python.org) 3.8 or newer. No install step.

    python server.py

Another port: `python server.py 8080`. Then open http://localhost:5173 (Armenian), `/en/` or `/es/`. Stop with Ctrl+C.

## Folders

- `site/`: the website itself. Upload this folder's contents to any web host.
- `server.py`: the web server (Python standard library). It also shows the right-language 404 page.
- `tools/`: `build.py` regenerates the pages; `i18n_es.json` and `i18n_hy.json` hold the translations.

## Publishing

`site/_redirects` (Netlify) and `site/.htaccess` (Apache or shared hosting) send missing pages to the 404 page in the right language.

### Render (runs server.py)

`render.yaml` deploys the site as a free Render web service that runs `python server.py`; every push to `main` redeploys.
One-time setup: on https://render.com choose **New → Blueprint**, connect this GitHub repository, and apply.

### GitHub Pages (optional)

`.github/workflows/pages.yml` can publish `site/` to GitHub Pages instead. It runs only when started manually from the Actions tab, after setting **Settings → Pages → Source: GitHub Actions**.

### PythonAnywhere (runs wsgi.py)

PythonAnywhere runs WSGI apps, so it uses `wsgi.py` (same routing as `server.py`, standard library only).

1. In a **Bash console**: `git clone https://github.com/mesrop888/centro-hispano-demo.git`
2. **Web** tab → **Add a new web app** → **Manual configuration** → any Python 3 version.
3. Open the **WSGI configuration file** link, replace everything with:

   ```python
   import sys
   path = "/home/YOUR_USERNAME/centro-hispano-demo"
   if path not in sys.path:
       sys.path.insert(0, path)
   from wsgi import application
   ```

4. Optional, faster assets: **Static files** → URL `/assets/`, directory `/home/YOUR_USERNAME/centro-hispano-demo/site/assets`.
5. Click **Reload**. The site is at `https://YOUR_USERNAME.pythonanywhere.com/`.

To update later: `cd ~/centro-hispano-demo && git pull`, then **Reload** on the Web tab.
