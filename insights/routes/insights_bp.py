from flask import Blueprint, request, jsonify
from dateutil import parser as dtparser
import re

insights_bp = Blueprint("insights", __name__)

# Regex for amount
AMOUNT_REGEX = re.compile(r"(?:₹|Rs\.?|INR)\s?(\d+\.?\d*)")

@insights_bp.route("/ingest/sms", methods=["POST"])
def ingest_sms():
    data = request.get_json()
    text = data.get("text", "")

    # Parse amount
    amount_match = AMOUNT_REGEX.search(text)
    amount = float(amount_match.group(1)) if amount_match else None

    # Dummy merchant & category logic
    merchant = "Uber" if "Uber" in text else "Other"
    category = "Travel" if "Uber" in text else "Misc"

    # Parse date correctly
    date = None
    try:
        date = dtparser.parse(text, fuzzy=True).date().isoformat()
    except Exception:
        date = None

    result = {
        "id": 1,
        "amount": amount,
        "merchant": merchant,
        "category": category,
        "date": date,
        "raw_text": text
    }

    return jsonify(result)
