import re

def parse_sms(text):
    amount = re.findall(r"Rs\s?(\d+)", text)
    merchant = re.findall(r"at\s([A-Za-z]+)", text)

    return {
        "merchant": merchant[0] if merchant else "Unknown",
        "amount": float(amount[0]) if amount else 0.0,
        "raw_text": text
    }
