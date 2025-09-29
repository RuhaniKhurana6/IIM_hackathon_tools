def compute_gauge(transactions, limits):
    total_spend = sum(float(t.get('amount', 0) or 0) for t in transactions)
    monthly_limit = limits.get('monthly', 1) or 1
    pct = min(100, round(100 * total_spend / monthly_limit))
    status = 'green' if pct < 70 else 'orange' if pct < 90 else 'red'
    return { 'percent': pct, 'status': status, 'monthly_limit': monthly_limit, 'spend': total_spend }