from src.budget_engine import compute_gauge

def test_basic_gauge():
    tx = [{ 'amount': 1000 }, { 'amount': 900 }]
    limits = { 'monthly': 5000 }
    g = compute_gauge(tx, limits)
    assert g['percent'] == 38
    assert g['status'] in ('green','orange','red')