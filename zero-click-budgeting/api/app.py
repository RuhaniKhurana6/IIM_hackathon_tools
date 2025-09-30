import os
import sys
from typing import List, Dict, Any
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Ensure budget-engine is importable
CUR_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CUR_DIR, ".."))
ENGINE_SRC = os.path.join(PROJECT_ROOT, "budget-engine", "src")
if ENGINE_SRC not in sys.path:
    sys.path.insert(0, ENGINE_SRC)

load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from budget_engine import compute_gauge  # type: ignore

app = Flask(__name__, static_folder=os.path.join(CUR_DIR, "static"))
CORS(app)  # Enable CORS for all routes

# In-memory store to keep demo simple
TRANSACTIONS: List[Dict[str, Any]] = []


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.post("/webhook/sms")
def webhook_sms():
    payload = request.get_json() or {}
    amount = float(payload.get("amount") or 0)
    merchant = payload.get("merchant")
    method = payload.get("method", "SMS")
    TRANSACTIONS.append({"amount": amount, "merchant": merchant, "method": method})
    return jsonify({"queued": True, "count": len(TRANSACTIONS)})


@app.post("/webhook/upi")
def webhook_upi():
    payload = request.get_json() or {}
    amount = float(payload.get("amount") or 0)
    merchant = payload.get("merchant")
    method = payload.get("method", "UPI")
    TRANSACTIONS.append({"amount": amount, "merchant": merchant, "method": method})
    return jsonify({"queued": True, "count": len(TRANSACTIONS)})


@app.post("/webhook/receipt")
def webhook_receipt():
    payload = request.get_json() or {}
    amount = float(payload.get("amount") or 0)
    merchant = payload.get("merchant")
    method = payload.get("method", "RECEIPT")
    TRANSACTIONS.append({"amount": amount, "merchant": merchant, "method": method})
    return jsonify({"queued": True, "count": len(TRANSACTIONS)})


@app.get("/budget/gauge")
def budget_gauge():
    monthly_limit = float(os.getenv("MONTHLY_LIMIT", "50000"))
    limits = {"monthly": monthly_limit}
    gauge = compute_gauge(TRANSACTIONS, limits)
    return jsonify(gauge)


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.getenv("API_PORT", "5050"))
    app.run(host="127.0.0.1", port=port, debug=True)