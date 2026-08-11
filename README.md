# Medusa ♾️ AI

Render-ready Flask web application for a Medusa AI subscription dashboard.

## Structure

```text
MedusaAI/
├── main.py
├── subscription_config.json
├── requirements.txt
├── render.yaml
├── .python-version
├── .gitignore
├── Profile
├── README.md
├── templates/
│   ├── SplashScreen.html
│   └── dashboard.html
└── static/
    └── media/
        ├── logo.png
        └── intro.mp4
```

## Local run

```bash
pip install -r requirements.txt
python main.py
```

Open `http://127.0.0.1:5000/`.

## Render

Recommended settings:

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn main:app`
- Health Check Path: `/health`

`render.yaml` already contains these settings.

> The wallet balances and swap/payment routes in this package are application examples stored in memory. They are not connected to a blockchain, custody system, or payment processor.
