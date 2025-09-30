import os
import sys
import re
from typing import List, Dict, Any
from flask import Flask, jsonify, request
from flask_cors import CORS
from dateutil import parser as dtparser
from datetime import datetime, date
import random
import json

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory stores for demo purposes
TRANSACTIONS: List[Dict[str, Any]] = []
BUDGET_TRANSACTIONS: List[Dict[str, Any]] = []
MONTHLY_LIMIT = 50000

# In-memory chat sessions for demo
CHAT_SESSIONS: Dict[str, List[Dict[str, Any]]] = {}
# Optional user profiles keyed by user_id for personalization
USER_PROFILES: Dict[str, Dict[str, Any]] = {}
USERS: Dict[str, Dict[str, Any]] = {}
OTP_STORE: Dict[str, str] = {}

# In-memory uploaded transactions for Time Machine (very simple demo store)
TIME_MACHINE_TRANSACTIONS: List[Dict[str, Any]] = []

# Regex for amount parsing (from insights)
AMOUNT_REGEX = re.compile(r"(?:₹|Rs\.?|INR)\s?(\d+\.?\d*)")

# =============================================================================
# TAX HELPER ENDPOINTS
# =============================================================================

@app.route('/api/tax/categorized', methods=['GET'])
def get_categorized_transactions():
    """Get categorized transactions for tax purposes"""
    transactions = [
        {"id": 1, "date": "2024-01-15", "amount": 1200, "description": "Office supplies - Staples", "category": "business", "tax_deductible": True},
        {"id": 2, "date": "2024-01-18", "amount": 500, "description": "Restaurant - Lunch meeting", "category": "business", "tax_deductible": True},
        {"id": 3, "date": "2024-01-20", "amount": 2500, "description": "Laptop repair - Dell Service", "category": "business", "tax_deductible": True},
        {"id": 4, "date": "2024-01-22", "amount": 800, "description": "Personal groceries", "category": "personal", "tax_deductible": False},
        {"id": 5, "date": "2024-01-25", "amount": 1500, "description": "Home internet - business use", "category": "business", "tax_deductible": True},
        {"id": 6, "date": "2024-01-28", "amount": 3000, "description": "Professional software license", "category": "business", "tax_deductible": True},
        {"id": 7, "date": "2024-02-02", "amount": 450, "description": "Coffee shop - personal", "category": "personal", "tax_deductible": False},
        {"id": 8, "date": "2024-02-05", "amount": 2200, "description": "Business conference ticket", "category": "business", "tax_deductible": True},
    ]
    return jsonify(transactions)

@app.route('/api/tax/upload-receipt', methods=['POST'])
def upload_receipt():
    """Mock receipt processing"""
    # Generate a random transaction from uploaded receipt
    mock_transaction = {
        "id": random.randint(100, 999),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": random.randint(50, 1000),
        "description": "Receipt processed - " + random.choice(["Office supplies", "Business meal", "Software purchase", "Equipment rental"]),
        "category": "business",
        "tax_deductible": True
    }
    return jsonify({
        "success": True, 
        "message": "Receipt processed successfully",
        "transaction": mock_transaction
    })

@app.route('/api/tax/summary', methods=['GET'])
def get_tax_summary():
    """Get tax summary with potential savings"""
    summary = {
        "total_deductible": 10900,
        "total_non_deductible": 1250,
        "potential_savings": 3270,  # Assuming 30% tax bracket
        "categories": {
            "business": 10900,
            "personal": 1250
        },
        "deduction_breakdown": {
            "80C": 25000,  # Life insurance, PPF, etc.
            "80D": 15000,  # Health insurance
            "HRA": 12000,  # House rent allowance
            "Business Expenses": 10900
        }
    }
    return jsonify(summary)

# =============================================================================
# INSIGHTS ENDPOINTS
# =============================================================================

@app.route('/api/insights/spending-by-category', methods=['GET'])
def get_spending_by_category():
    """Get spending breakdown by category"""
    data = {
        "categories": ["Food & Dining", "Transportation", "Shopping", "Entertainment", "Utilities", "Healthcare"],
        "amounts": [8500, 4200, 6800, 3200, 2800, 1500],
        "percentages": [32.1, 15.9, 25.7, 12.1, 10.6, 5.7],
        "total_spent": 26500,
        "period": "This Month"
    }
    return jsonify(data)

@app.route('/api/insights/monthly-trends', methods=['GET'])
def get_monthly_trends():
    """Get monthly spending trends"""
    data = {
        "months": ["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024", "Jan 2025"],
        "spending": [18500, 22300, 19800, 26500, 24200, 21800],
        "income": [45000, 45000, 47000, 45000, 45000, 48000],
        "savings": [26500, 22700, 27200, 18500, 20800, 26200]
    }
    return jsonify(data)

@app.route('/api/insights/transactions', methods=['GET'])
def get_insight_transactions():
    """Get recent transactions for insights"""
    transactions = [
        {"id": 1, "date": "2024-01-28", "amount": 850, "merchant": "Zomato", "category": "Food & Dining", "method": "UPI"},
        {"id": 2, "date": "2024-01-28", "amount": 120, "merchant": "Metro Card", "category": "Transportation", "method": "Card"},
        {"id": 3, "date": "2024-01-27", "amount": 2500, "merchant": "Amazon", "category": "Shopping", "method": "Card"},
        {"id": 4, "date": "2024-01-27", "amount": 450, "merchant": "BookMyShow", "category": "Entertainment", "method": "UPI"},
        {"id": 5, "date": "2024-01-26", "amount": 1200, "merchant": "Electricity Board", "category": "Utilities", "method": "Net Banking"},
        {"id": 6, "date": "2024-01-25", "amount": 800, "merchant": "Apollo Pharmacy", "category": "Healthcare", "method": "Card"},
        {"id": 7, "date": "2024-01-24", "amount": 350, "merchant": "Uber", "category": "Transportation", "method": "UPI"},
        {"id": 8, "date": "2024-01-23", "amount": 1500, "merchant": "Big Bazaar", "category": "Shopping", "method": "Card"}
    ]
    return jsonify(transactions)

@app.route('/api/insights/ingest/sms', methods=['POST'])
def ingest_sms():
    """Process SMS transaction data"""
    data = request.get_json()
    text = data.get("text", "")

    # Parse amount
    amount_match = AMOUNT_REGEX.search(text)
    amount = float(amount_match.group(1)) if amount_match else None

    # Enhanced merchant and category logic
    merchant = "Other"
    category = "Misc"
    
    if "Uber" in text or "uber" in text:
        merchant = "Uber"
        category = "Transportation"
    elif "Zomato" in text or "zomato" in text:
        merchant = "Zomato"
        category = "Food & Dining"
    elif "Amazon" in text or "amazon" in text:
        merchant = "Amazon"
        category = "Shopping"
    elif "ATM" in text or "Cash" in text:
        merchant = "ATM"
        category = "Cash Withdrawal"

    # Parse date
    date_str = None
    try:
        parsed_date = dtparser.parse(text, fuzzy=True).date()
        date_str = parsed_date.isoformat()
    except Exception:
        date_str = datetime.now().date().isoformat()

    result = {
        "id": len(TRANSACTIONS) + 1,
        "amount": amount,
        "merchant": merchant,
        "category": category,
        "date": date_str,
        "raw_text": text,
        "method": "SMS"
    }

    TRANSACTIONS.append(result)
    return jsonify(result)

@app.route('/api/insights/chat', methods=['POST'])
def insights_chat():
    """Chat with your financial data - AI assistant for insights"""
    data = request.get_json()
    question = data.get("question", "").lower().strip()
    
    # Get current insights data
    spending_data = {
        "categories": ["Food & Dining", "Transportation", "Shopping", "Entertainment", "Utilities", "Healthcare"],
        "amounts": [8500, 4200, 6800, 3200, 2800, 1500],
        "percentages": [32.1, 15.9, 25.7, 12.1, 10.6, 5.7],
        "total_spent": 26500,
        "period": "This Month"
    }
    
    transactions = [
        {"id": 1, "date": "2024-01-28", "amount": 850, "merchant": "Zomato", "category": "Food & Dining", "method": "UPI"},
        {"id": 2, "date": "2024-01-28", "amount": 120, "merchant": "Metro Card", "category": "Transportation", "method": "Card"},
        {"id": 3, "date": "2024-01-27", "amount": 2500, "merchant": "Amazon", "category": "Shopping", "method": "Card"},
        {"id": 4, "date": "2024-01-27", "amount": 450, "merchant": "BookMyShow", "category": "Entertainment", "method": "UPI"},
        {"id": 5, "date": "2024-01-26", "amount": 1200, "merchant": "Electricity Board", "category": "Utilities", "method": "Net Banking"},
        {"id": 6, "date": "2024-01-25", "amount": 800, "merchant": "Apollo Pharmacy", "category": "Healthcare", "method": "Card"},
        {"id": 7, "date": "2024-01-24", "amount": 350, "merchant": "Uber", "category": "Transportation", "method": "UPI"},
        {"id": 8, "date": "2024-01-23", "amount": 1500, "merchant": "Big Bazaar", "category": "Shopping", "method": "Card"}
    ]
    
    monthly_trends = {
        "months": ["Aug 2024", "Sep 2024", "Oct 2024", "Nov 2024", "Dec 2024", "Jan 2025"],
        "spending": [18500, 22300, 19800, 26500, 24200, 21800],
        "income": [45000, 45000, 47000, 45000, 45000, 48000],
        "savings": [26500, 22700, 27200, 18500, 20800, 26200]
    }
    
    # Simple natural language processing
    response = generate_insights_response(question, spending_data, transactions, monthly_trends)
    
    return jsonify({
        "question": data.get("question", ""),
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "data_points": get_relevant_data_points(question, spending_data, transactions)
    })

# =============================================================================
# SIMPLE CHATBOT ENDPOINTS (for AIChatbot frontend component)
# =============================================================================

def _get_json_payload() -> Dict[str, Any]:
    """Best-effort JSON extraction from the incoming request.

    Accepts proper JSON, raw body JSON, or form data, returning an empty
    dict on failure. This makes the endpoint resilient to various clients
    (PowerShell, curl on Windows, browsers, etc.).
    """
    data: Dict[str, Any] = {}
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    if not data:
        try:
            raw = request.data.decode('utf-8', errors='ignore') if request.data else ''
            if raw:
                data = json.loads(raw)
        except Exception:
            pass
    if not data and request.form:
        data = {k: v for k, v in request.form.items()}
    return data

@app.route('/api/chatbot/initialize', methods=['POST'])
def chatbot_initialize():
    """Initialize a demo chat session for a given user id.

    The frontend calls this on mount. We create an in-memory session and
    return a simple success response.
    """
    payload = _get_json_payload()
    user_id = payload.get('user_id', 'anonymous')
    display_name = payload.get('name') or payload.get('display_name') or 'Ruhani'
    if user_id not in CHAT_SESSIONS:
        CHAT_SESSIONS[user_id] = []
    USER_PROFILES[user_id] = {"name": display_name}
    return jsonify({"initialized": True, "user_id": user_id, "name": display_name})


@app.route('/api/chatbot/chat', methods=['POST'])
def chatbot_chat():
    """Respond to a user message with deterministic, helpful text.

    This is a lightweight, rules-based stub designed to satisfy the
    AIChatbot.tsx expectations. It routes certain questions to the
    existing insights utilities to keep answers realistic.
    """
    payload = _get_json_payload()
    user_id = payload.get('user_id', 'anonymous')
    message: str = (payload.get('message') or '').strip()
    display_name = (USER_PROFILES.get(user_id, {}) or {}).get('name', 'Ruhani')

    if user_id not in CHAT_SESSIONS:
        CHAT_SESSIONS[user_id] = []

    # Store user message
    CHAT_SESSIONS[user_id].append({
        "role": "user",
        "content": message,
        "timestamp": datetime.now().isoformat()
    })

    # Build a response leveraging existing demo data functions
    lower = message.lower()
    response_text = None

    # Personalized greeting detection
    greeting_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    if any(kw in lower for kw in greeting_keywords):
        response_text = f"Hello {display_name}! How can I help you with taxes, spending, or budgeting today?"
    # Map to insights endpoints' underlying data to keep it consistent
    if any(k in lower for k in ["deduct", "tax", "save on taxes", "tax advice", "advice"]):
        summary = {
            "total_deductible": 10900,
            "potential_savings": 3270,
            "tip": "Maximize Section 80C (PPF/ELSS), claim business expenses, and keep receipts organized."
        }
        response_text = response_text or (
            f"Here's a quick tax snapshot: Potential savings about ₹{summary['potential_savings']:,}. "
            f"You currently have ₹{summary['total_deductible']:,} in deductible expenses. "
            f"Tip: {summary['tip']}"
        )
    elif any(k in lower for k in ["total expenses", "how much spent", "total spent", "spending this month"]):
        response_text = response_text or "You've spent ₹26,500 this month. Top categories: Food & Dining and Shopping."
    elif any(k in lower for k in ["spending categories", "categories", "breakdown"]):
        response_text = response_text or (
            "Spending breakdown this month: Food & Dining ₹8,500 (32%), Shopping ₹6,800 (26%), "
            "Transportation ₹4,200 (16%), Entertainment ₹3,200, Utilities ₹2,800, Healthcare ₹1,500."
        )
    else:
        # Generic answer falls back to insights summary language
        response_text = response_text or (
            f"I can help with taxes, spending trends, and budgeting, {display_name}. Ask e.g. "
            "'How much can I deduct?', 'Show my spending categories', or 'Give me tax advice'."
        )

    # Store assistant message
    CHAT_SESSIONS[user_id].append({
        "role": "assistant",
        "content": response_text,
        "timestamp": datetime.now().isoformat()
    })

    return jsonify({
        "response": response_text,
        "user_id": user_id,
        "messages": CHAT_SESSIONS[user_id][-6:]  # recent context preview
    })

# =============================================================================
# FINANCIAL DIGITAL TWIN - Simple Simulator
# =============================================================================

def _simulate_investment(principal: float, monthly: float, annual_rate_percent: float, months: int) -> Dict[str, Any]:
    annual_rate = annual_rate_percent / 100.0
    monthly_rate = annual_rate / 12.0
    balance = principal
    history = []
    for m in range(1, months + 1):
        balance = balance * (1 + monthly_rate) + monthly
        history.append(round(balance, 2))
    return {"final": round(balance, 2), "trajectory": history}


def _simulate_emi(purchase_amount: float, down_payment: float, annual_rate_percent: float, months: int) -> Dict[str, Any]:
    principal = max(purchase_amount - down_payment, 0)
    r = (annual_rate_percent / 100.0) / 12.0
    if r == 0 or months == 0:
        emi = principal / months if months else 0
    else:
        emi = principal * r * (1 + r) ** months / ((1 + r) ** months - 1)
    total_paid = round(emi * months + down_payment, 2)
    interest_paid = round(total_paid - purchase_amount, 2)
    schedule = [round(emi, 2)] * months
    return {"emi": round(emi, 2), "total_paid": total_paid, "interest_paid": interest_paid, "schedule": schedule}


@app.route('/api/digital-twin/simulate', methods=['POST'])
def digital_twin_simulate():
    payload = _get_json_payload()
    scenario = (payload.get('scenario') or 'compare_invest_vs_emi').lower()
    months = int(payload.get('months') or 12)

    result: Dict[str, Any] = {"scenario": scenario, "months": months}

    if scenario == 'compare_invest_vs_emi':
        # Inputs
        purchase_amount = float(payload.get('purchase_amount') or 80000)
        down_payment = float(payload.get('down_payment') or 10000)
        loan_apr = float(payload.get('loan_apr') or 16)
        investment_monthly = float(payload.get('investment_monthly') or 3000)
        invest_equity_apr = float(payload.get('invest_equity_apr') or 12)
        invest_gold_apr = float(payload.get('invest_gold_apr') or 6)

        emi = _simulate_emi(purchase_amount, down_payment, loan_apr, months)
        equity = _simulate_investment(0, investment_monthly, invest_equity_apr, months)
        gold = _simulate_investment(0, investment_monthly, invest_gold_apr, months)

        result.update({
            "emi": emi,
            "equity": equity,
            "gold": gold,
        })

        # Simple recommendation
        best_label = 'equity' if equity['final'] >= gold['final'] else 'gold'
        best_value = max(equity['final'], gold['final'])
        tip = (
            f"Investing ₹{int(investment_monthly)}/mo yields up to ₹{best_value:,.0f} in {months} months, "
            f"while EMI total paid is ₹{emi['total_paid']:,.0f} (interest ₹{emi['interest_paid']:,.0f})."
        )
        result["recommendation"] = {"best": best_label, "message": tip}

        # Financial health impact (needs user context; accept optional inputs)
        monthly_income = float(payload.get('monthly_income') or 45000)
        base_savings_rate = float(payload.get('base_savings_rate') or 0.25)  # 25% default
        base_savings_amount = monthly_income * base_savings_rate

        # Scenario A: Take EMI
        emi_payment = emi['emi'] if months > 0 else 0
        savings_with_emi = max(monthly_income - emi_payment - (monthly_income - base_savings_amount), 0)
        savings_rate_with_emi = savings_with_emi / monthly_income if monthly_income else 0

        # Scenario B: Invest monthly (investment_monthly)
        savings_with_invest = max(base_savings_amount - investment_monthly, 0)
        savings_rate_with_invest = savings_with_invest / monthly_income if monthly_income else 0

        # Simple affordability & emergency buffer score
        affordability_emi = 1.0 if emi_payment <= 0.3 * monthly_income else 0.5 if emi_payment <= 0.5 * monthly_income else 0.2
        buffer_months = (base_savings_amount * months) / (monthly_income or 1)
        buffer_score = 1.0 if buffer_months >= 6 else 0.6 if buffer_months >= 3 else 0.3

        health = {
            "income": monthly_income,
            "baseline": {
                "savings_rate": round(base_savings_rate, 2),
                "monthly_savings": round(base_savings_amount, 2)
            },
            "emi_path": {
                "monthly_emi": round(emi_payment, 2),
                "savings_rate": round(savings_rate_with_emi, 2),
                "affordability_score": affordability_emi
            },
            "invest_path": {
                "monthly_invest": investment_monthly,
                "savings_rate": round(savings_rate_with_invest, 2)
            },
            "resilience": {
                "emergency_buffer_score": buffer_score
            },
            "summary": "EMI reduces savings rate" if savings_rate_with_emi < base_savings_rate else "EMI manageable",
        }
        result["financial_health"] = health

    else:
        result["error"] = "unknown scenario"

    return jsonify(result)


@app.route('/api/digital-twin/interpret', methods=['POST'])
def digital_twin_interpret():
    """Very simple rule-based interpreter that converts a natural-language
    prompt into simulation parameters for compare_invest_vs_emi.
    """
    payload = _get_json_payload()
    prompt = str(payload.get('prompt') or '').lower()
    defaults = {
        "months": 12,
        "purchase_amount": 80000,
        "down_payment": 10000,
        "loan_apr": 16.0,
        "investment_monthly": 3000,
        "invest_equity_apr": 12.0,
        "invest_gold_apr": 6.0,
    }

    # Heuristics
    if "iphone" in prompt:
        defaults["purchase_amount"] = 79999
        defaults["down_payment"] = 10000 if "no down" not in prompt else 0
        defaults["months"] = 12 if "12" in prompt else 24 if "24" in prompt else defaults["months"]
    if "gold" in prompt:
        defaults["invest_gold_apr"] = 7.0
    if "mutual" in prompt or "mf" in prompt or "equity" in prompt or "sip" in prompt:
        defaults["invest_equity_apr"] = 12.0
    # Extract a rough monthly investment like "3000" or "3k"
    import re
    m = re.search(r"(\d{3,6})\s*(?:/mo|per month|monthly)?", prompt)
    if m:
        val = int(m.group(1))
        defaults["investment_monthly"] = val

    return jsonify({"scenario": "compare_invest_vs_emi", **defaults})


# =============================================================================
# FINANCIAL TIME MACHINE - Upload and Forecast
# =============================================================================

def _parse_csv_text(csv_text: str) -> List[Dict[str, Any]]:
    """Parse a simple CSV with headers: date,amount,description (amount +/-)."""
    import csv
    from io import StringIO
    rows: List[Dict[str, Any]] = []
    f = StringIO(csv_text)
    reader = csv.DictReader(f)
    for row in reader:
        try:
            rows.append({
                "date": row.get("date") or row.get("Date"),
                "amount": float(row.get("amount") or row.get("Amount") or 0),
                "description": row.get("description") or row.get("Description") or ""
            })
        except Exception:
            continue
    return rows


@app.route('/api/time-machine/upload', methods=['POST'])
def time_machine_upload():
    """Accept transaction history via multipart file or raw CSV text in body."""
    global TIME_MACHINE_TRANSACTIONS
    csv_text = ""
    if 'file' in request.files:
        csv_text = request.files['file'].read().decode('utf-8', errors='ignore')
    else:
        # Accept raw text or JSON {csv: "..."} for convenience
        payload = _get_json_payload()
        csv_text = str(payload.get('csv') or request.data.decode('utf-8', errors='ignore') or '')
    if not csv_text.strip():
        return jsonify({"error": "no CSV provided"}), 400
    rows = _parse_csv_text(csv_text)
    TIME_MACHINE_TRANSACTIONS = rows
    return jsonify({"ok": True, "count": len(rows)})


@app.route('/api/time-machine/forecast', methods=['POST'])
def time_machine_forecast():
    """Compute simple forward-looking projections from uploaded history.

    Inputs (JSON):
      current_balance (optional): current savings/cash
      horizon_years (optional): years to project (default 10)
      big_purchase (optional): amount user wants to afford
      expected_return_annual (optional): % return on savings (default 5)
    """
    payload = _get_json_payload()
    current_balance = float(payload.get('current_balance') or 50000)
    horizon_years = int(payload.get('horizon_years') or 10)
    big_purchase = float(payload.get('big_purchase') or 100000)
    expected_return = float(payload.get('expected_return_annual') or 5.0) / 100.0

    # Derive monthly net cashflow from history (average over last 3-6 months)
    from collections import defaultdict
    monthly_sum = defaultdict(float)
    for r in TIME_MACHINE_TRANSACTIONS:
        try:
            d = dtparser.parse(r["date"]).date()
            key = f"{d.year}-{d.month:02d}"
            monthly_sum[key] += float(r["amount"])
        except Exception:
            continue
    months_sorted = sorted(monthly_sum.keys())[-6:]
    avg_monthly_net = sum(monthly_sum[m] for m in months_sorted) / (len(months_sorted) or 1)

    # Project month by month
    months = horizon_years * 12
    monthly_rate = (1 + expected_return) ** (1/12) - 1 if expected_return > 0 else 0.0
    balance = current_balance
    timeline: List[Dict[str, Any]] = []
    run_out_month = None
    afford_month = None

    for i in range(1, months + 1):
        balance = balance * (1 + monthly_rate) + avg_monthly_net
        timeline.append({"month": i, "balance": round(balance, 2)})
        if run_out_month is None and balance <= 0:
            run_out_month = i
        if afford_month is None and balance >= big_purchase:
            afford_month = i

    # Basic retirement projection assuming constant net invest and return
    retirement_target = float(payload.get('retirement_target') or 5000000)
    retirement_month = None
    for t in timeline:
        if t["balance"] >= retirement_target:
            retirement_month = t["month"]
            break

    def to_years_months(m):
        if m is None:
            return None
        y = m // 12
        mm = m % 12
        return {"years": int(y), "months": int(mm)}

    # One-line recommendation
    reco = None
    if run_out_month is not None and run_out_month <= 12:
        reco = f"Warning: At your current trend you may run out of money in {run_out_month//12}y {run_out_month%12}m. Reduce expenses or increase income."
    elif afford_month is not None:
        reco = f"Stay the course: You can afford ₹{int(big_purchase):,} in {afford_month//12}y {afford_month%12}m assuming current trend and {int(expected_return*100)}% return."
    elif retirement_month is not None:
        reco = f"On track: Retirement target could be reached in {retirement_month//12}y {retirement_month%12}m."
    else:
        reco = "Consider increasing monthly surplus or return rate to meet goals within the horizon."

    return jsonify({
        "avg_monthly_net": round(avg_monthly_net, 2),
        "current_balance": round(current_balance, 2),
        "timeline": timeline[:120],  # cap to 10 years for payload size
        "run_out_in": to_years_months(run_out_month),
        "can_afford_in": to_years_months(afford_month),
        "retirement_in": to_years_months(retirement_month),
        "recommendation": reco,
        "assumptions": {
            "horizon_years": horizon_years,
            "expected_return_annual": expected_return * 100,
            "big_purchase": big_purchase,
            "retirement_target": retirement_target
        }
    })


@app.route('/api/time-machine/chat', methods=['POST'])
def time_machine_chat():
    """Answer questions about the uploaded data and forecast assumptions.

    This is a rules-based assistant that understands:
      - When will I run out of money?
      - When can I afford X?
      - What is my average monthly net?
      - How much should I save to hit retirement?
    """
    payload = _get_json_payload()
    question = str(payload.get('question') or '').lower()
    # Use a default forecast to answer
    forecast_req = {
        "current_balance": float(payload.get('current_balance') or 50000),
        "horizon_years": int(payload.get('horizon_years') or 10),
        "big_purchase": float(payload.get('big_purchase') or 100000),
        "expected_return_annual": float(payload.get('expected_return_annual') or 5.0),
        "retirement_target": float(payload.get('retirement_target') or 5000000),
    }

    with app.test_request_context(json=forecast_req):
        data = time_machine_forecast().json

    def fmt_period(v):
        if not v:
            return "not within the selected horizon"
        y = v.get('years', 0)
        m = v.get('months', 0)
        return f"{y} years {m} months"

    answer = None
    if any(k in question for k in ["run out", "bankrupt", "zero balance", "out of money"]):
        answer = f"You may run out of money in {fmt_period(data.get('run_out_in'))}."
    elif any(k in question for k in ["afford", "buy", "purchase"]):
        answer = f"You can afford your target in {fmt_period(data.get('can_afford_in'))}."
    elif any(k in question for k in ["average", "monthly net", "cash flow", "surplus"]):
        answer = f"Your average monthly net from history is ₹{int(data.get('avg_monthly_net') or 0):,}."
    elif any(k in question for k in ["retire", "retirement", "financial freedom"]):
        answer = f"Retirement target may be reached in {fmt_period(data.get('retirement_in'))}."
    elif any(k in question for k in ["recommend", "what should i do", "advice"]):
        answer = data.get('recommendation') or "Increase monthly surplus or adjust return assumptions to meet goals."
    else:
        answer = (
            "I can answer about run-out timing, affordability, average monthly net, and retirement timing. "
            "Ask e.g. 'When will I run out of money?' or 'When can I afford ₹1,00,000?'"
        )

    return jsonify({
        "question": payload.get('question', ''),
        "answer": answer,
        "assumptions": data.get('assumptions'),
    })

# =============================================================================
# AUTH ENDPOINTS (demo, in-memory)
# =============================================================================

@app.route('/auth/signup', methods=['POST'])
def auth_signup():
    payload = _get_json_payload()
    username = str(payload.get('username') or '').strip()
    password = str(payload.get('password') or '').strip()
    name = str(payload.get('name') or username or 'User').strip()
    email = str(payload.get('email') or '').strip().lower()

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400
    if username in USERS:
        return jsonify({"error": "username already exists"}), 409

    USERS[username] = {"password": password, "name": name, "user_id": username, "email": email, "email_verified": False}
    USER_PROFILES[username] = {"name": name}
    # Generate a demo OTP for email verification (logged and returned for demo)
    otp = f"{random.randint(100000, 999999)}"
    if email:
        OTP_STORE[email] = otp
        print(f"[DEV OTP] Email verification OTP for {email}: {otp}")
    return jsonify({"user_id": username, "name": name, "username": username, "email": email, "otp": otp})


@app.route('/auth/login', methods=['POST'])
def auth_login():
    payload = _get_json_payload()
    username = str(payload.get('username') or '').strip()
    password = str(payload.get('password') or '').strip()

    user = USERS.get(username)
    if not user or user.get('password') != password:
        return jsonify({"error": "invalid credentials"}), 401

    # Return a simple token (user_id) for demo; frontend can store it
    USER_PROFILES[username] = {"name": user.get('name') or username}
    return jsonify({"user_id": username, "name": user.get('name'), "username": username, "token": username})


@app.route('/auth/request-otp', methods=['POST'])
def auth_request_otp():
    payload = _get_json_payload()
    email = str(payload.get('email') or '').strip().lower()
    if not email:
        return jsonify({"error": "email required"}), 400
    otp = f"{random.randint(100000, 999999)}"
    OTP_STORE[email] = otp
    print(f"[DEV OTP] Email verification OTP for {email}: {otp}")
    return jsonify({"sent": True})


@app.route('/auth/verify-otp', methods=['POST'])
def auth_verify_otp():
    payload = _get_json_payload()
    email = str(payload.get('email') or '').strip().lower()
    code = str(payload.get('code') or '').strip()
    if not email or not code:
        return jsonify({"error": "email and code required"}), 400
    if OTP_STORE.get(email) != code:
        return jsonify({"error": "invalid code"}), 400
    # Mark any user with this email as verified
    for uname, info in USERS.items():
        if info.get('email') == email:
            info['email_verified'] = True
    OTP_STORE.pop(email, None)
    return jsonify({"verified": True})

def generate_insights_response(question, spending_data, transactions, monthly_trends):
    """Generate intelligent response based on user question and data"""
    question = question.lower()
    
    # Total spending questions
    if any(word in question for word in ['total', 'spent', 'how much']):
        if 'month' in question or 'monthly' in question:
            return f"You've spent ₹{spending_data['total_spent']:,} this month across all categories. Your highest spending is on {spending_data['categories'][0]} (₹{spending_data['amounts'][0]:,})."
        else:
            return f"Your total spending this month is ₹{spending_data['total_spent']:,}. This breaks down as: Food & Dining (₹8,500), Shopping (₹6,800), Transportation (₹4,200), Entertainment (₹3,200), Utilities (₹2,800), and Healthcare (₹1,500)."
    
    # Category-specific questions
    elif any(word in question for word in ['food', 'dining', 'restaurant', 'eat']):
        return f"Your food and dining expenses are ₹8,500 this month, which is 32.1% of your total spending. Recent transactions include Zomato (₹850). This is your largest spending category."
    
    elif any(word in question for word in ['transport', 'travel', 'uber', 'metro']):
        uber_amount = next((t['amount'] for t in transactions if 'uber' in t['merchant'].lower()), 0)
        metro_amount = next((t['amount'] for t in transactions if 'metro' in t['merchant'].lower()), 0)
        return f"Transportation costs are ₹4,200 this month (15.9% of spending). Recent: Uber ₹{uber_amount}, Metro ₹{metro_amount}. Consider using public transport more to save money."
    
    elif any(word in question for word in ['shopping', 'amazon', 'buy', 'purchase']):
        amazon_amount = next((t['amount'] for t in transactions if 'amazon' in t['merchant'].lower()), 0)
        return f"Shopping expenses total ₹6,800 this month (25.7% of spending). Your largest purchase was Amazon ₹{amazon_amount}. This is your second-highest category after food."
    
    # Trend questions
    elif any(word in question for word in ['trend', 'increasing', 'decreasing', 'pattern']):
        avg_spending = sum(monthly_trends['spending']) / len(monthly_trends['spending'])
        current_vs_avg = spending_data['total_spent'] - avg_spending
        if current_vs_avg > 0:
            return f"Your spending trend is increasing. This month (₹{spending_data['total_spent']:,}) is ₹{current_vs_avg:,.0f} above your 6-month average (₹{avg_spending:,.0f}). Consider reviewing your Food & Dining expenses."
        else:
            return f"Your spending is below average this month. Current: ₹{spending_data['total_spent']:,}, 6-month average: ₹{avg_spending:,.0f}. Good job controlling expenses!"
    
    # Savings questions
    elif any(word in question for word in ['save', 'saving', 'reduce', 'cut']):
        return f"To save money, consider reducing Food & Dining (₹8,500 - 32% of spending) and Shopping (₹6,800 - 26% of spending). Even a 20% reduction could save you ₹3,000+ monthly."
    
    # Budget questions
    elif any(word in question for word in ['budget', 'limit', 'afford']):
        monthly_income = monthly_trends['income'][-1]
        savings_rate = ((monthly_income - spending_data['total_spent']) / monthly_income) * 100
        return f"Based on your ₹{monthly_income:,} income and ₹{spending_data['total_spent']:,} spending, you're saving {savings_rate:.1f}% of your income. Aim for 20% savings rate for healthy finances."
    
    # Comparison questions
    elif any(word in question for word in ['compare', 'vs', 'versus', 'difference']):
        return f"Comparing your top categories: Food & Dining (₹8,500) vs Shopping (₹6,800) - you spend ₹1,700 more on food. Transportation (₹4,200) vs Entertainment (₹3,200) - ₹1,000 difference."
    
    # Recent transaction questions
    elif any(word in question for word in ['recent', 'latest', 'last', 'yesterday']):
        recent_transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)[:3]
        transaction_list = ', '.join([f"{t['merchant']} ₹{t['amount']}" for t in recent_transactions])
        return f"Your recent transactions: {transaction_list}. Total: ₹{sum(t['amount'] for t in recent_transactions)}."
    
    # Merchant-specific questions  
    elif any(merchant in question for merchant in ['zomato', 'amazon', 'uber', 'pharmacy']):
        for transaction in transactions:
            if any(merchant in transaction['merchant'].lower() for merchant in ['zomato', 'amazon', 'uber', 'pharmacy'] if merchant in question):
                return f"Found transaction: {transaction['merchant']} - ₹{transaction['amount']} on {transaction['date']} in {transaction['category']} category via {transaction['method']}."
    
    # General financial advice
    elif any(word in question for word in ['advice', 'recommend', 'suggest', 'tip']):
        return f"Based on your spending: 1) Food & Dining is 32% of spending - try cooking more at home. 2) Set category budgets: Food ₹7,000, Shopping ₹5,000. 3) Your savings rate looks healthy at {((45000-26500)/45000)*100:.1f}%."
    
    # Default response
    else:
        return f"I can help you analyze your financial data! You've spent ₹{spending_data['total_spent']:,} this month. Ask me about specific categories, trends, savings tips, or recent transactions. For example: 'How much did I spend on food?' or 'Show me my recent Amazon purchases.'"

def get_relevant_data_points(question, spending_data, transactions):
    """Extract relevant data points based on question context"""
    question = question.lower()
    data_points = []
    
    if 'food' in question or 'dining' in question:
        data_points.append({"category": "Food & Dining", "amount": 8500, "percentage": 32.1})
    
    if 'transport' in question:
        data_points.append({"category": "Transportation", "amount": 4200, "percentage": 15.9})
    
    if 'shop' in question or 'amazon' in question:
        data_points.append({"category": "Shopping", "amount": 6800, "percentage": 25.7})
    
    if 'total' in question:
        data_points.append({"metric": "Total Spending", "amount": spending_data['total_spent']})
    
    return data_points

# =============================================================================
# ZERO-CLICK BUDGETING ENDPOINTS
# =============================================================================

@app.route('/webhook/sms', methods=['POST'])
def webhook_sms():
    """Process SMS-based transaction for budgeting"""
    payload = request.get_json() or {}
    amount = float(payload.get("amount", 0))
    merchant = payload.get("merchant", "Unknown")
    method = "SMS"
    
    transaction = {
        "amount": amount, 
        "merchant": merchant, 
        "method": method,
        "timestamp": datetime.now().isoformat(),
        "category": categorize_merchant(merchant)
    }
    BUDGET_TRANSACTIONS.append(transaction)
    return jsonify({"queued": True, "count": len(BUDGET_TRANSACTIONS)})

@app.route('/webhook/upi', methods=['POST'])
def webhook_upi():
    """Process UPI-based transaction for budgeting"""
    payload = request.get_json() or {}
    amount = float(payload.get("amount", 0))
    merchant = payload.get("merchant", "Unknown")
    method = "UPI"
    
    transaction = {
        "amount": amount, 
        "merchant": merchant, 
        "method": method,
        "timestamp": datetime.now().isoformat(),
        "category": categorize_merchant(merchant)
    }
    BUDGET_TRANSACTIONS.append(transaction)
    return jsonify({"queued": True, "count": len(BUDGET_TRANSACTIONS)})

@app.route('/webhook/receipt', methods=['POST'])
def webhook_receipt():
    """Process receipt-based transaction for budgeting"""
    payload = request.get_json() or {}
    amount = float(payload.get("amount", 0))
    merchant = payload.get("merchant", "Unknown")
    method = "RECEIPT"
    
    transaction = {
        "amount": amount, 
        "merchant": merchant, 
        "method": method,
        "timestamp": datetime.now().isoformat(),
        "category": categorize_merchant(merchant)
    }
    BUDGET_TRANSACTIONS.append(transaction)
    return jsonify({"queued": True, "count": len(BUDGET_TRANSACTIONS)})

@app.route('/budget/gauge', methods=['GET'])
def budget_gauge():
    """Get current budget gauge status"""
    global MONTHLY_LIMIT
    
    # Calculate total spent this month
    total_spent = sum(t["amount"] for t in BUDGET_TRANSACTIONS)
    
    # Add some realistic demo spending if no transactions exist
    if not BUDGET_TRANSACTIONS:
        total_spent = 18750  # Demo amount
    
    percentage = (total_spent / MONTHLY_LIMIT) * 100
    remaining = MONTHLY_LIMIT - total_spent
    
    # Determine gauge color
    color = "green" if percentage < 50 else "orange" if percentage < 80 else "red"
    
    gauge = {
        "percentage": round(percentage, 1),
        "spent": total_spent,
        "limit": MONTHLY_LIMIT,
        "remaining": remaining,
        "color": color,
        "status": "Safe" if percentage < 80 else "Warning" if percentage < 100 else "Over Budget",
        "transactions_count": len(BUDGET_TRANSACTIONS)
    }
    return jsonify(gauge)

@app.route('/budget/transactions', methods=['GET'])
def get_budget_transactions():
    """Get all budget transactions"""
    return jsonify(BUDGET_TRANSACTIONS)

@app.route('/budget/set-limit', methods=['POST'])
def set_budget_limit():
    """Set monthly budget limit"""
    global MONTHLY_LIMIT
    data = request.get_json()
    new_limit = float(data.get('limit', 50000))
    MONTHLY_LIMIT = new_limit
    return jsonify({"success": True, "new_limit": MONTHLY_LIMIT})

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def categorize_merchant(merchant):
    """Categorize merchant for budget tracking"""
    merchant_lower = merchant.lower()
    
    if any(food in merchant_lower for food in ['zomato', 'swiggy', 'dominos', 'restaurant']):
        return 'Food & Dining'
    elif any(transport in merchant_lower for transport in ['uber', 'ola', 'metro', 'bus']):
        return 'Transportation'
    elif any(shop in merchant_lower for shop in ['amazon', 'flipkart', 'mall', 'store']):
        return 'Shopping'
    elif any(util in merchant_lower for util in ['electricity', 'water', 'gas', 'internet']):
        return 'Utilities'
    elif any(health in merchant_lower for health in ['hospital', 'pharmacy', 'doctor']):
        return 'Healthcare'
    else:
        return 'Others'

# =============================================================================
# GENERAL ENDPOINTS
# =============================================================================

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'services': {
            'tax_helper': 'running',
            'insights': 'running', 
            'budgeting': 'running'
        },
        'transactions_count': len(TRANSACTIONS),
        'budget_transactions_count': len(BUDGET_TRANSACTIONS)
    })

@app.route('/api/dashboard-summary')
def dashboard_summary():
    """Get summary data for dashboard"""
    # Calculate totals from budget transactions
    total_spent = sum(t["amount"] for t in BUDGET_TRANSACTIONS)
    if not BUDGET_TRANSACTIONS:
        total_spent = 18750  # Demo amount
        
    budget_percentage = (total_spent / MONTHLY_LIMIT) * 100
    
    summary = {
        "budget": {
            "spent": total_spent,
            "limit": MONTHLY_LIMIT,
            "percentage": round(budget_percentage, 1),
            "remaining": MONTHLY_LIMIT - total_spent
        },
        "tax_savings": 3270,
        "monthly_trend": "up",
        "top_category": "Food & Dining",
        "recent_transactions": len(BUDGET_TRANSACTIONS),
        "alerts": []
    }
    
    # Add alerts based on budget status
    if budget_percentage > 90:
        summary["alerts"].append("You're close to your monthly budget limit!")
    elif budget_percentage > 100:
        summary["alerts"].append("You've exceeded your monthly budget!")
        
    return jsonify(summary)

# Initialize with some demo data
def init_demo_data():
    """Initialize with demo transactions for testing"""
    global BUDGET_TRANSACTIONS
    
    demo_transactions = [
        {"amount": 850, "merchant": "Zomato", "method": "UPI", "timestamp": "2024-01-28T12:30:00", "category": "Food & Dining"},
        {"amount": 350, "merchant": "Uber", "method": "UPI", "timestamp": "2024-01-27T09:15:00", "category": "Transportation"},
        {"amount": 2500, "merchant": "Amazon", "method": "Card", "timestamp": "2024-01-26T16:45:00", "category": "Shopping"},
        {"amount": 1200, "merchant": "Electricity Board", "method": "Net Banking", "timestamp": "2024-01-25T14:20:00", "category": "Utilities"},
        {"amount": 450, "merchant": "BookMyShow", "method": "UPI", "timestamp": "2024-01-24T19:00:00", "category": "Entertainment"},
    ]
    
    BUDGET_TRANSACTIONS.extend(demo_transactions)

if __name__ == '__main__':
    init_demo_data()
    print("🚀 Starting FinHub Zen Unified Backend...")
    print("📊 Tax Helper: http://localhost:5000/api/tax/*")
    print("📈 Insights: http://localhost:5000/api/insights/*") 
    print("💰 Budgeting: http://localhost:5000/budget/* and /webhook/*")
    print("🏥 Health Check: http://localhost:5000/health")
    app.run(host='127.0.0.1', port=5000, debug=True)