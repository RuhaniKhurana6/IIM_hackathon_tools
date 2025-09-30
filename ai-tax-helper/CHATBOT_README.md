# 🤖 AI Tax Helper Chatbot

A comprehensive AI-powered chatbot that can analyze user financial data and answer any questions about taxes, expenses, and financial insights.

## ✨ Features

### 🧠 Intelligent Conversational AI
- **Natural Language Processing**: Understands and responds to questions about tax and financial data
- **Context-Aware**: Maintains conversation context across multiple interactions
- **Personalized Responses**: Provides tailored advice based on user's specific financial data

### 📊 Data Analysis Capabilities
- **Transaction Analysis**: Automatically categorizes and analyzes financial transactions
- **Tax Deduction Identification**: Identifies potential tax-deductible expenses
- **Spending Pattern Insights**: Provides insights into spending habits and patterns
- **Real-time Calculations**: Calculates potential tax savings and financial metrics

### 💬 Conversation Features
- **Multi-turn Conversations**: Maintains conversation history and context
- **Memory System**: Remembers user preferences and previous discussions
- **Question Variety**: Can answer any question about user's financial data including:
  - "How much can I deduct in taxes?"
  - "What are my total business expenses?"
  - "Show me my spending categories"
  - "What's my biggest expense this month?"
  - "Give me tax planning advice"
  - "How much could I save in taxes?"

### 🔧 Technical Features
- **Fallback Mode**: Works with or without OpenAI API (uses intelligent mock responses)
- **Robust Error Handling**: Gracefully handles missing dependencies
- **RESTful API**: Complete API for integration with web/mobile applications
- **Data Privacy**: User data is processed locally and not shared externally

## 🚀 Quick Start

### Prerequisites
```bash
# Basic requirements (always needed)
pip install flask flask-cors

# Optional AI dependencies (for advanced features)
pip install openai langchain langchain-openai pandas numpy
```

### Running the Application
1. **Start the Flask server:**
   ```bash
   cd ai-tax-helper
   python app.py
   ```

2. **The server will start on http://localhost:5000**

3. **Test the chatbot directly:**
   ```bash
   python test_chatbot.py
   ```

## 📡 API Endpoints

### Core Chatbot Endpoints

#### 1. Chat with AI
**POST** `/api/chatbot/chat`
```json
{
  "user_id": "user123",
  "message": "How much can I deduct in taxes?"
}
```
**Response:**
```json
{
  "response": "Based on your data, you have $4800 in tax-deductible expenses...",
  "user_id": "user123",
  "timestamp": "2023-05-01T10:30:00"
}
```

#### 2. Initialize with Data
**POST** `/api/chatbot/initialize`
```json
{
  "user_id": "user123"
}
```
Loads sample data for demonstration purposes.

#### 3. Update User Data
**POST** `/api/chatbot/update-data`
```json
{
  "user_id": "user123",
  "data": {
    "transactions": [...],
    "categories": {...},
    "tax_summary": {...}
  }
}
```

#### 4. Get Data Analysis
**POST** `/api/chatbot/analyze`
```json
{
  "user_id": "user123"
}
```
**Response:**
```json
{
  "total_transactions": 5,
  "total_amount": 5300,
  "deductible_amount": 4800,
  "non_deductible_amount": 500,
  "categories": {...},
  "monthly_breakdown": {...},
  "recommendations": [...]
}
```

#### 5. Get Personalized Insights
**GET** `/api/chatbot/insights?user_id=user123`
```json
{
  "insights": [
    "You could save approximately $1200.00 in taxes this year",
    "Your highest expense category is 'business'",
    "Your spending in 2023-05 was $5300"
  ],
  "user_id": "user123"
}
```

#### 6. Conversation Management
- **GET** `/api/chatbot/history?user_id=user123` - Get conversation history
- **POST** `/api/chatbot/clear-history` - Clear conversation history

## 🛠️ Integration Examples

### JavaScript/Web Integration
```javascript
// Initialize chatbot with user data
async function initializeChatbot(userId) {
  const response = await fetch('/api/chatbot/initialize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId })
  });
  return response.json();
}

// Chat with the AI
async function sendMessage(userId, message) {
  const response = await fetch('/api/chatbot/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      user_id: userId, 
      message: message 
    })
  });
  const data = await response.json();
  return data.response;
}

// Get insights
async function getInsights(userId) {
  const response = await fetch(`/api/chatbot/insights?user_id=${userId}`);
  const data = await response.json();
  return data.insights;
}
```

### Python Integration
```python
from utils.ai_chatbot import get_chatbot

# Get the chatbot instance
chatbot = get_chatbot()

# Update user data
user_data = {
    'transactions': [
        {"amount": 1200, "description": "Office supplies", "tax_deductible": True},
        {"amount": 500, "description": "Personal meal", "tax_deductible": False}
    ],
    'tax_summary': {"total_deductible": 1200, "potential_savings": 300}
}
chatbot.update_user_data("user123", user_data)

# Chat with the bot
response = chatbot.chat("user123", "What are my tax deductions?")
print(response)

# Get analysis
analysis = chatbot.analyze_user_data("user123")
print(analysis)
```

## 💡 Example Conversations

### Basic Tax Questions
```
User: "Hello, what can you help me with?"
Bot: "Hello! I'm your AI tax assistant. I can help you understand your tax situation, categorize expenses, and provide personalized financial insights. I have access to 5 of your transactions. What would you like to know?"

User: "How much can I deduct in taxes?"
Bot: "Based on your data, you have $4800 in tax-deductible expenses. This includes business expenses like office supplies, professional services, and business travel. Would you like me to explain which specific expenses are deductible?"

User: "What are my total expenses?"
Bot: "You have $5300 in total expenses from 5 transactions. Of these, $4800 are business expenses that may be tax-deductible. Your top spending categories appear to be related to your business operations."
```

### Advanced Analysis
```
User: "Can you analyze my spending patterns?"
Bot: "Based on your transaction data: Your highest expense category is 'business' with $4800. You could save approximately $1200.00 in taxes from your deductible expenses. Your spending in 2023-05 was $5300. I recommend keeping detailed records of all business-related expenses and consider using a business credit card for easier expense tracking."

User: "Give me some tax planning advice"
Bot: "Here are some personalized tax planning recommendations: 1) You could save approximately $1200.00 in taxes this year, 2) Keep detailed records of all business-related expenses, 3) Consider using a business credit card for easier expense tracking, 4) Review your expenses monthly to identify tax-saving opportunities."
```

## 🏗️ Architecture

### Core Components

1. **TaxChatbot Class** (`utils/ai_chatbot.py`)
   - Main chatbot intelligence
   - Data analysis and insights
   - Conversation memory management
   - OpenAI integration (when available)

2. **Flask API** (`app.py`)
   - RESTful endpoints
   - Request handling
   - Error management
   - CORS support

3. **Fallback System**
   - Intelligent mock responses when AI APIs unavailable
   - Maintains full functionality without external dependencies
   - Seamless degradation

### Data Flow
```
User Question → API Endpoint → Chatbot Instance → Context Analysis → Response Generation → User
     ↑                                                     ↓
User Data ← Data Analysis ← Transaction Processing ← Data Update
```

## 🔒 Privacy & Security

- **Local Processing**: All data analysis happens locally
- **No External Data Sharing**: User data stays on your server
- **Optional AI Integration**: Works without external AI services
- **Secure API**: Standard Flask security practices

## 🧪 Testing

### Run All Tests
```bash
python test_chatbot.py
```

### Test Individual Components
```bash
# Test direct chatbot functionality
python -c "from utils.ai_chatbot import get_chatbot; bot = get_chatbot(); print(bot.chat('test', 'Hello'))"

# Test API endpoints (server must be running)
python simple_test.py
```

### Sample Test Output
```
🚀 Starting AI Tax Chatbot Tests

🔧 Testing chatbot functionality directly...
✅ Direct data update successful
Q: Hello!
A: Hello! I'm your AI tax assistant. I can help you understand your tax situation...

Q: What are my tax deductions?
A: Based on your data, you have $1200 in tax-deductible expenses...

✨ Testing completed!
```

## 📝 Customization

### Adding Custom Tax Knowledge
Edit `setup_tax_knowledge_base()` in `ai_chatbot.py`:
```python
tax_knowledge = [
    "Your custom tax information here...",
    "Additional business expense categories...",
    "Specific tax rules for your region..."
]
```

### Custom Response Logic
Modify `_generate_mock_response()` for specialized responses:
```python
def _generate_mock_response(self, user_id: str, message: str) -> str:
    # Add your custom logic here
    if "custom_keyword" in message.lower():
        return "Your custom response"
    # ... existing logic
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the AI Tax Helper application. See the main project license for details.

## 🆘 Support

For support, please check:
1. This README for common issues
2. Run the test scripts to diagnose problems
3. Check server logs for detailed error messages
4. Ensure all dependencies are properly installed

---

**Built with ❤️ for smart tax management**