from flask import Flask, request, jsonify

app = Flask(__name__)
# app.py (top)
from insights.routes.insights_bp import insights_bp
app.register_blueprint(insights_bp, url_prefix="/insights")



@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    text = data.get("text")

    # Dummy parsing logic (replace with your ML/regex later)
    amount = 500.0
    merchant = "Uber"
    category = "Deductible"
    date = "25-Sep"

    result = {
        "amount": amount,
        "category": category,
        "merchant": merchant,
        "raw_text": text,
        "summary": f"You spent Rs {amount} at {merchant} on {date}"
    }

    return jsonify(result)
@app.route('/')
def home():
    return "✅ Flask Tax Helper API is running! Use POST /classify"


if __name__ == '__main__':
    app.run(debug=True)
