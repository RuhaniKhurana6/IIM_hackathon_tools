import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.insights_bp import insights_bp

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(insights_bp, url_prefix='/api/insights')

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
