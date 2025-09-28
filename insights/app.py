# insights/app.py
from flask import Flask
from insights.routes.insights_bp import insights_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(insights_bp, url_prefix='/api/insights')

    @app.route("/", methods=["GET"])
    def home():
        return "Welcome to Expense Insights API 🚀. Use Postman to test /api/insights/sms or /api/insights/csv."

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
