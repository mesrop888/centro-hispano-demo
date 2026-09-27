# Centro Hispano website

Static site in three languages: Armenian (main, at the root), English (`/en/`) and Spanish (`/es/`).

## Run it locally

Needs [Node.js](https://nodejs.org) 18 or newer. No install step.

- **Windows:** double-click `start.bat`. The site opens in your browser.
- **Any system:** `npm start` or `node server.js`
- **Another port:** `node server.js 8080`

Then open http://localhost:5173 (Armenian), `/en/` or `/es/`. Stop with Ctrl+C.

## Folders

- `site/`: the website itself. Upload this folder's contents to any web host.
- `server.js`: the local web server. It also shows the right-language 404 page.
- `tools/`: `build.py` regenerates the pages; `i18n_es.json` and `i18n_hy.json` hold the translations.

## Publishing

`site/_redirects` (Netlify) and `site/.htaccess` (Apache or shared hosting) send missing pages to the 404 page in the right language.

### Render (runs server.js)

`render.yaml` deploys the site as a free Render web service that runs `node server.js`; every push to `main` redeploys.
One-time setup: on https://render.com choose **New → Blueprint**, connect this GitHub repository, and apply.

### GitHub Pages (optional)

`.github/workflows/pages.yml` can publish `site/` to GitHub Pages instead. It runs only when started manually from the Actions tab, after setting **Settings → Pages → Source: GitHub Actions**.
