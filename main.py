import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)

with (BASE_DIR / "subscription_config.json").open("r", encoding="utf-8") as f:
    subscription_data = json.load(f)

# Demo/in-memory wallet state. Replace with a database before handling real funds.
user_wallets = {
    "default_user": {
        "BTC": 0.25,
        "ETH": 1.5,
        "USDT": 1200.0,
        "tag": "@medusa.default",
    }
}


@app.get("/")
def splash():
    return render_template("SplashScreen.html")


@app.get("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        project=subscription_data["project"],
        wallets=user_wallets["default_user"],
        terms=subscription_data["subscription_terms"]["access"],
        renewal=subscription_data["subscription_terms"]["payment"]["renewal"],
        address=subscription_data["subscription_terms"]["payment"]["recipient_address"],
        benefits=subscription_data.get("benefits", []),
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "Medusa AI"})


@app.get("/api/wallets")
def api_wallets():
    return jsonify(user_wallets)


@app.post("/api/swap")
def swap_tokens():
    data = request.get_json(silent=True) or {}
    user = "default_user"
    from_token = str(data.get("from", "")).upper()
    to_token = str(data.get("to", "")).upper()

    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"status": "failed", "reason": "Invalid amount"}), 400

    supported = {"BTC", "ETH", "USDT"}
    if from_token not in supported or to_token not in supported:
        return jsonify({"status": "failed", "reason": "Unsupported token"}), 400
    if from_token == to_token:
        return jsonify({"status": "failed", "reason": "Choose two different tokens"}), 400
    if amount <= 0:
        return jsonify({"status": "failed", "reason": "Amount must be greater than zero"}), 400
    if user_wallets[user][from_token] < amount:
        return jsonify({"status": "failed", "reason": "Insufficient balance"}), 400

    # Simplified 1:1 demonstration swap. No real blockchain transaction occurs.
    user_wallets[user][from_token] -= amount
    user_wallets[user][to_token] += amount

    return jsonify({"status": "success", "wallets": user_wallets[user]})


@app.post("/api/pay")
def pay_user():
    data = request.get_json(silent=True) or {}
    sender = "default_user"
    recipient_tag = str(data.get("recipient", "")).strip()
    token = str(data.get("token", "")).upper()

    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"status": "failed", "reason": "Invalid amount"}), 400

    supported = {"BTC", "ETH", "USDT"}
    if token not in supported or not recipient_tag:
        return jsonify({"status": "failed", "reason": "Invalid recipient or token"}), 400
    if amount <= 0:
        return jsonify({"status": "failed", "reason": "Amount must be greater than zero"}), 400
    if user_wallets[sender][token] < amount:
        return jsonify({"status": "failed", "reason": "Insufficient balance"}), 400

    user_wallets[sender][token] -= amount
    return jsonify(
        {
            "status": "success",
            "message": f"Sent {amount:g} {token} to {recipient_tag}",
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
