#!/usr/bin/env python3
"""
Test script for AI Chatbot functionality
Demonstrates how the chatbot can answer questions about user's tax data
"""

import requests
import json
from pprint import pprint

# Configuration
BASE_URL = "http://localhost:5000"
TEST_USER_ID = "test_user_123"

def test_chatbot_apis():
    """Test all chatbot API endpoints"""
    
    print("🤖 Testing AI Tax Chatbot APIs")
    print("=" * 50)
    
    # 1. Initialize chatbot with sample data
    print("\n1️⃣  Initializing chatbot with sample data...")
    init_response = requests.post(f"{BASE_URL}/api/chatbot/initialize", 
                                 json={"user_id": TEST_USER_ID})
    
    if init_response.status_code == 200:
        print("✅ Chatbot initialized successfully")
        pprint(init_response.json())
    else:
        print(f"❌ Failed to initialize: {init_response.status_code}")
        print(init_response.text)
        return
    
    # 2. Test various chat queries
    chat_tests = [
        "Hello! What can you help me with?",
        "How much can I deduct in taxes?",
        "What are my total expenses?",
        "Show me my spending categories",
        "Can you give me a summary of my tax situation?",
        "What business expenses do I have?",
        "How much money could I save on taxes?",
        "What's the difference between business and personal expenses?",
        "Can you analyze my spending patterns?",
        "Give me some tax planning advice"
    ]
    
    print(f"\n2️⃣  Testing {len(chat_tests)} different chat queries...")
    
    for i, message in enumerate(chat_tests, 1):
        print(f"\n--- Query {i}: {message} ---")
        
        chat_response = requests.post(f"{BASE_URL}/api/chatbot/chat", 
                                     json={
                                         "user_id": TEST_USER_ID,
                                         "message": message
                                     })
        
        if chat_response.status_code == 200:
            response_data = chat_response.json()
            print(f"🤖 Response: {response_data['response']}")
        else:
            print(f"❌ Chat failed: {chat_response.status_code}")
    
    # 3. Test data analysis
    print(f"\n3️⃣  Testing data analysis...")
    analysis_response = requests.post(f"{BASE_URL}/api/chatbot/analyze", 
                                     json={"user_id": TEST_USER_ID})
    
    if analysis_response.status_code == 200:
        print("✅ Data analysis successful:")
        pprint(analysis_response.json())
    else:
        print(f"❌ Analysis failed: {analysis_response.status_code}")
    
    # 4. Test personalized insights
    print(f"\n4️⃣  Testing personalized insights...")
    insights_response = requests.get(f"{BASE_URL}/api/chatbot/insights", 
                                    params={"user_id": TEST_USER_ID})
    
    if insights_response.status_code == 200:
        print("✅ Insights generated successfully:")
        insights_data = insights_response.json()
        for i, insight in enumerate(insights_data['insights'], 1):
            print(f"   {i}. {insight}")
    else:
        print(f"❌ Insights failed: {insights_response.status_code}")
    
    # 5. Test conversation history
    print(f"\n5️⃣  Testing conversation history...")
    history_response = requests.get(f"{BASE_URL}/api/chatbot/history", 
                                   params={"user_id": TEST_USER_ID})
    
    if history_response.status_code == 200:
        history_data = history_response.json()
        print(f"✅ Found {history_data['count']} conversation entries")
        print("Recent conversations:")
        for conv in history_data['history'][-3:]:  # Show last 3
            print(f"   - {conv['message'][:50]}...")
    else:
        print(f"❌ History failed: {history_response.status_code}")
    
    print(f"\n6️⃣  Testing custom data update...")
    # Test updating with custom data
    custom_data = {
        "user_id": TEST_USER_ID,
        "data": {
            "transactions": [
                {"id": 6, "date": "2023-05-15", "amount": 1500, "description": "New laptop", "category": "business", "tax_deductible": True},
                {"id": 7, "date": "2023-05-16", "amount": 250, "description": "Client dinner", "category": "business", "tax_deductible": True}
            ],
            "categories": {
                "business": 6550,  # Updated with new transactions
                "personal": 500
            }
        }
    }
    
    update_response = requests.post(f"{BASE_URL}/api/chatbot/update-data", 
                                   json=custom_data)
    
    if update_response.status_code == 200:
        print("✅ Custom data updated successfully")
        
        # Test a query with the new data
        new_query_response = requests.post(f"{BASE_URL}/api/chatbot/chat", 
                                          json={
                                              "user_id": TEST_USER_ID,
                                              "message": "What's my latest transaction?"
                                          })
        
        if new_query_response.status_code == 200:
            print("🤖 Response to new data query:")
            print(f"   {new_query_response.json()['response']}")
    else:
        print(f"❌ Custom data update failed: {update_response.status_code}")

def test_direct_chatbot():
    """Test chatbot functionality directly (without API)"""
    print("\n🔧 Testing chatbot functionality directly...")
    
    try:
        from utils.ai_chatbot import get_chatbot
        
        chatbot = get_chatbot()
        
        # Test data update
        test_data = {
            'transactions': [
                {"id": 1, "date": "2023-05-01", "amount": 1200, "description": "Office supplies", "category": "business", "tax_deductible": True},
                {"id": 2, "date": "2023-05-03", "amount": 500, "description": "Restaurant", "category": "personal", "tax_deductible": False}
            ],
            'tax_summary': {
                "total_deductible": 1200,
                "total_non_deductible": 500,
                "potential_savings": 300
            }
        }
        
        chatbot.update_user_data("direct_test_user", test_data)
        print("✅ Direct data update successful")
        
        # Test chat
        test_messages = [
            "Hello!",
            "What are my tax deductions?",
            "How much did I spend on business expenses?"
        ]
        
        for message in test_messages:
            response = chatbot.chat("direct_test_user", message)
            print(f"Q: {message}")
            print(f"A: {response}")
            print()
        
        # Test analysis
        analysis = chatbot.analyze_user_data("direct_test_user")
        print("📊 Analysis results:")
        pprint(analysis)
        
    except ImportError as e:
        print(f"❌ Could not import chatbot: {e}")
    except Exception as e:
        print(f"❌ Direct test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting AI Tax Chatbot Tests")
    
    # Test direct functionality first
    test_direct_chatbot()
    
    # Test API endpoints (requires server to be running)
    try:
        health_check = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_check.status_code == 200:
            test_chatbot_apis()
        else:
            print(f"❌ Server not responding correctly: {health_check.status_code}")
    except requests.exceptions.ConnectionError:
        print("⚠️  Server is not running. Start the Flask app to test API endpoints:")
        print("   python app.py")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    print(f"\n✨ Testing completed!")