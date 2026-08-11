# Medusa AI — Flexible Deployment Build

This package is designed for both Render and Heroku.

## Python compatibility
The project intentionally does not include a `.python-version` file. This allows the hosting platform to select an available supported Python 3 release.

## Render
- Uses `render.yaml`
- Build: `pip install -r requirements.txt`
- Start: `gunicorn main:app`

## Heroku
- Uses the root `Procfile`
- Process: `web: gunicorn main:app`
