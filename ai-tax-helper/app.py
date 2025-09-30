import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.categorizer import classify_expense
from utils.ai_chatbot import get_chatbot

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Tax helper routes
@app.route('/api/tax/categorized', methods=['GET'])
def get_categorized_transactions():
    # Mock data for demo
    transactions = [
        {"id": 1, "date": "2023-05-01", "amount": 1200, "description": "Office supplies", "category": "business", "tax_deductible": True},
        {"id": 2, "date": "2023-05-03", "amount": 500, "description": "Restaurant", "category": "personal", "tax_deductible": False},
        {"id": 3, "date": "2023-05-05", "amount": 2500, "description": "Laptop repair", "category": "business", "tax_deductible": True},
    ]
    return jsonify(transactions)

@app.route('/api/tax/upload-receipt', methods=['POST'])
def upload_receipt():
    # Mock receipt processing
    return jsonify({"success": True, "message": "Receipt processed successfully"})

@app.route('/api/tax/summary', methods=['GET'])
def get_tax_summary():
    # Mock tax summary data
    summary = {
        "total_deductible": 3700,
        "total_non_deductible": 500,
        "potential_savings": 740,
        "categories": {
            "business": 3700,
            "personal": 500
        }
    }
    return jsonify(summary)

# AI Chatbot routes
@app.route('/api/chatbot/chat', methods=['POST'])
def chat_with_ai():
    """
    Main chatbot endpoint - can answer any question about user's data
    """
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
            'timestamp': chatbot.conversation_history[-1]['timestamp'] if chatbot.conversation_history else None
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@app.route('/api/chatbot/update-data', methods=['POST'])
def update_user_data():
    """
    Update user data for personalized chatbot responses
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        user_data = data.get('data', {})
        
        chatbot = get_chatbot()
        chatbot.update_user_data(user_id, user_data)
        
        return jsonify({
            'success': True,
            'message': 'User data updated successfully',
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Update error: {str(e)}'}), 500

@app.route('/api/chatbot/analyze', methods=['POST'])
def analyze_user_data():
    """
    Get comprehensive analysis of user's financial data
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        
        chatbot = get_chatbot()
        analysis = chatbot.analyze_user_data(user_id)
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@app.route('/api/chatbot/insights', methods=['GET'])
def get_personalized_insights():
    """
    Get personalized insights based on user data
    """
    try:
        user_id = request.args.get('user_id', 'default_user')
        
        chatbot = get_chatbot()
        insights = chatbot.get_personalized_insights(user_id)
        
        return jsonify({
            'insights': insights,
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Insights error: {str(e)}'}), 500

@app.route('/api/chatbot/history', methods=['GET'])
def get_conversation_history():
    """
    Get conversation history for a user
    """
    try:
        user_id = request.args.get('user_id', 'default_user')
        limit = int(request.args.get('limit', 10))
        
        chatbot = get_chatbot()
        history = chatbot.get_conversation_history(user_id, limit)
        
        return jsonify({
            'history': history,
            'user_id': user_id,
            'count': len(history)
        })
        
    except Exception as e:
        return jsonify({'error': f'History error: {str(e)}'}), 500

@app.route('/api/chatbot/clear-history', methods=['POST'])
def clear_conversation_history():
    """
    Clear conversation history for a user
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        
        chatbot = get_chatbot()
        chatbot.clear_conversation_history(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared',
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({'error': f'Clear history error: {str(e)}'}), 500

@app.route('/api/chatbot/initialize', methods=['POST'])
def initialize_chatbot_with_existing_data():
    """
    Initialize chatbot with existing tax data from the app
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        
        # Get existing tax data from the app
        transactions = [
            {"id": 1, "date": "2023-05-01", "amount": 1200, "description": "Office supplies", "category": "business", "tax_deductible": True},
            {"id": 2, "date": "2023-05-03", "amount": 500, "description": "Restaurant", "category": "personal", "tax_deductible": False},
            {"id": 3, "date": "2023-05-05", "amount": 2500, "description": "Laptop repair", "category": "business", "tax_deductible": True},
            {"id": 4, "date": "2023-05-07", "amount": 800, "description": "Business travel", "category": "business", "tax_deductible": True},
            {"id": 5, "date": "2023-05-10", "amount": 300, "description": "Office rent", "category": "business", "tax_deductible": True}
        ]
        
        tax_summary = {
            "total_deductible": 4800,
            "total_non_deductible": 500,
            "potential_savings": 1200,
            "categories": {
                "business": 4800,
                "personal": 500
            }
        }
        
        user_data = {
            'transactions': transactions,
            'tax_summary': tax_summary,
            'categories': {
                'business': 4800,
                'personal': 500
            }
        }
        
        chatbot = get_chatbot()
        chatbot.update_user_data(user_id, user_data)
        
        return jsonify({
            'success': True,
            'message': 'Chatbot initialized with existing data',
            'user_id': user_id,
            'data_loaded': {
                'transactions': len(transactions),
                'total_deductible': tax_summary['total_deductible']
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Initialization error: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting AI Tax Helper Chatbot Server...")
    print("Available endpoints:")
    print("   - POST /api/chatbot/chat - Main chat interface")
    print("   - POST /api/chatbot/initialize - Load sample data")
    print("   - GET /api/chatbot/insights - Get insights")
    print("   - GET /health - Health check")
    print("Server will be available at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting server: {e}")
