from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({"status": "Flask is working!", "message": "Test successful"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("Starting minimal Flask test...")
    app.run(host='localhost', port=5000, debug=False)