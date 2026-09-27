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

### GitHub Pages

Every push to `main` deploys `site/` through `.github/workflows/pages.yml`.
One-time setup: repository **Settings → Pages → Build and deployment → Source: GitHub Actions**.
Live at https://mesrop888.github.io/centro-hispano-demo/
