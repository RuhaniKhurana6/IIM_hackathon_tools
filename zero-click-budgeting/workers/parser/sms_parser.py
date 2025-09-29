import re

def parse_sms(text: str) -> dict:
    r = { 'raw': text, 'amount': None, 'merchant': None, 'method': None }
    m = re.search(r'(\d+[\.,]?\d*)', text)
    if m: r['amount'] = float(m.group(1).replace(',', ''))
    low = text.lower()
    if 'upi' in low: r['method'] = 'UPI'
    for t in ['amazon','zomato','uber','ola','swiggy','myntra','flipkart']:
        if t in low: r['merchant'] = t.title(); break
    return r