# insights/utils/analytics.py
from collections import defaultdict
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import math

def monthly_category_summary(transactions):
    # transactions: list of dicts with 'amount' and 'category'
    totals = defaultdict(float)
    for t in transactions:
        totals[t['category']] += float(t['amount'])
    return dict(totals)

def percent_change(prev, curr):
    # returns percentage change number (positive = increase); handles prev=0
    if prev == 0:
        if curr == 0:
            return 0.0
        return float('inf')  # indicate infinite increase; we'll handle in presentation
    return ((curr - prev) / prev) * 100.0

def summarize_monthly_comparison(conn, year, month):
    from .storage import query_transactions_month
    # get current month transactions
    cur_tx = query_transactions_month(conn, year, month)
    # previous month
    prev_dt = datetime(year, month, 1) - relativedelta(months=1)
    prev_tx = query_transactions_month(conn, prev_dt.year, prev_dt.month)
    cur_cat = monthly_category_summary(cur_tx)
    prev_cat = monthly_category_summary(prev_tx)

    categories = set(list(cur_cat.keys()) + list(prev_cat.keys()))
    diffs = {}
    for c in categories:
        prev_amt = prev_cat.get(c, 0.0)
        cur_amt = cur_cat.get(c, 0.0)
        pc = percent_change(prev_amt, cur_amt)
        diffs[c] = {
            "previous": prev_amt,
            "current": cur_amt,
            "percent_change": pc if math.isfinite(pc) else None
        }
    total_prev = sum(prev_cat.values())
    total_cur = sum(cur_cat.values())
    total_pc = percent_change(total_prev, total_cur)
    return {
        "category_comparison": diffs,
        "total_previous": total_prev,
        "total_current": total_cur,
        "total_percent_change": total_pc if math.isfinite(total_pc) else None
    }

def detect_recurring_subscriptions(conn, lookback_months=3, min_occurrences=2):
    from .storage import query_transactions_range
    from datetime import datetime
    now = datetime.utcnow().date()
    start = (now - relativedelta(months=lookback_months)).isoformat()
    end = (now + relativedelta(days=1)).isoformat()
    txs = query_transactions_range(conn, start, end)
    # group by merchant
    by_merchant = {}
    for t in txs:
        m = t.get('merchant') or "Unknown"
        if m not in by_merchant:
            by_merchant[m] = []
        by_merchant[m].append(t)
    recurring = []
    for merchant, items in by_merchant.items():
        if len(items) >= min_occurrences:
            avg = sum(i['amount'] for i in items) / len(items)
            recurring.append({
                "merchant": merchant,
                "count": len(items),
                "avg_amount": round(avg,2),
                "total": round(sum(i['amount'] for i in items),2)
            })
    # sort by avg_amount desc
    recurring.sort(key=lambda x: x['avg_amount'], reverse=True)
    # suggestion: propose cutting top recurring items as potential savings
    suggestions = []
    for r in recurring:
        suggestions.append({
            "merchant": r['merchant'],
            "monthly_avg": r['avg_amount'],
            "suggestion": f"Review subscription from {r['merchant']}. Potential monthly save: ₹{r['avg_amount']}"
        })
    return {
        "recurring": recurring,
        "suggestions": suggestions
    }
