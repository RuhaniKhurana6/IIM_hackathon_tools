from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from utils.ai_chatbot import get_chatbot
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/chatbot/chat', methods=['POST'])
def chat_with_ai():
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        chatbot = get_chatbot()
        response = chatbot.chat(user_id, message)
        
        return jsonify({
            'response': response,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)