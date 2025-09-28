import re
from dateutil import parser as dtparser
from datetime import datetime
import pandas as pd

# Regex to capture amount like ₹500, Rs. 299, INR 1000 etc.
AMOUNT_REGEX = re.compile(r"(?:₹|Rs\.?|INR)\s?(\d+(?:\.\d{1,2})?)")

# Example: "ICICI Bank: Rs 500 spent at Uber on 25-Sep"
def parse_upi_sms(text: str, received_date=None):
    # Extract amount
    match = AMOUNT_REGEX.search(text)
    amount = float(match.group(1)) if match else None

    # Merchant heuristic: take the word after "at" if present
    merchant = None
    if " at " in text:
        merchant = text.split(" at ")[-1].split(" ")[0]

    # Parse date if provided or fallback to today
    try:
        date = dtparser.parse(text, fuzzy=True)
    except Exception:
        date = received_date or datetime.today()

    return {
        "date": date.strftime("%Y-%m-%d"),
        "amount": amount,
        "merchant": merchant,
        "raw_text": text
    }

def parse_bank_csv(file_or_buffer):
    # Example CSV headers: Date, Description, Amount
    df = pd.read_csv(file_or_buffer)
    transactions = []
    for _, row in df.iterrows():
        transactions.append({
            "date": str(row.get("Date")),
            "amount": float(row.get("Amount")),
            "merchant": row.get("Description"),
            "raw_text": str(row.to_dict())
        })
    return transactions
