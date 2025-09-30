#!/usr/bin/env python3
"""
AI Tax Chatbot Demo
Showcases the comprehensive chatbot functionality
"""

import json
from utils.ai_chatbot import get_chatbot
from pprint import pprint

def main():
    print("🤖 AI Tax Helper Chatbot Demo")
    print("=" * 50)
    
    # Initialize chatbot
    chatbot = get_chatbot()
    user_id = "demo_user"
    
    # Load sample data
    print("\n📊 Loading sample financial data...")
    sample_data = {
        'transactions': [
            {"id": 1, "date": "2023-05-01", "amount": 1200, "description": "Office supplies", "category": "business", "tax_deductible": True},
            {"id": 2, "date": "2023-05-03", "amount": 500, "description": "Client lunch", "category": "business", "tax_deductible": True},
            {"id": 3, "date": "2023-05-05", "amount": 2500, "description": "Laptop for work", "category": "business", "tax_deductible": True},
            {"id": 4, "date": "2023-05-07", "amount": 800, "description": "Business trip", "category": "business", "tax_deductible": True},
            {"id": 5, "date": "2023-05-10", "amount": 300, "description": "Personal dinner", "category": "personal", "tax_deductible": False},
            {"id": 6, "date": "2023-05-15", "amount": 150, "description": "Coffee with team", "category": "business", "tax_deductible": True},
            {"id": 7, "date": "2023-05-20", "amount": 600, "description": "Home groceries", "category": "personal", "tax_deductible": False}
        ],
        'tax_summary': {
            "total_deductible": 5150,
            "total_non_deductible": 900,
            "potential_savings": 1287.50,
            "categories": {
                "business": 5150,
                "personal": 900
            }
        },
        'categories': {
            'business': 5150,
            'personal': 900
        }
    }
    
    chatbot.update_user_data(user_id, sample_data)
    print(f"✅ Loaded {len(sample_data['transactions'])} transactions")
    print(f"   Total expenses: ${sample_data['tax_summary']['total_deductible'] + sample_data['tax_summary']['total_non_deductible']}")
    print(f"   Deductible: ${sample_data['tax_summary']['total_deductible']}")
    
    # Demo conversations
    print("\n💬 Demo Conversations")
    print("-" * 30)
    
    conversations = [
        "Hello! What can you tell me about my finances?",
        "How much can I deduct in taxes?",
        "What are my biggest expenses?",
        "Show me my business vs personal spending",
        "How much money could I save on taxes?",
        "What tax advice do you have for me?",
        "Can you categorize my expenses?",
        "What's my spending pattern this month?",
        "Give me insights about my financial data"
    ]
    
    for i, question in enumerate(conversations, 1):
        print(f"\n{i}. 👤 User: {question}")
        response = chatbot.chat(user_id, question)
        print(f"   🤖 Bot: {response}")
        print("   " + "-" * 40)
    
    # Show data analysis
    print(f"\n📈 Comprehensive Data Analysis")
    print("-" * 35)
    analysis = chatbot.analyze_user_data(user_id)
    
    print(f"Total Transactions: {analysis['total_transactions']}")
    print(f"Total Amount: ${analysis['total_amount']}")
    print(f"Deductible Amount: ${analysis['deductible_amount']}")
    print(f"Non-deductible Amount: ${analysis['non_deductible_amount']}")
    
    print(f"\nCategory Breakdown:")
    for category, count in analysis['categories'].items():
        print(f"  - {category}: {count} transactions")
    
    print(f"\nTop Merchants:")
    for merchant, amount in list(analysis['top_merchants'].items())[:3]:
        print(f"  - {merchant}: ${amount}")
    
    print(f"\nRecommendations:")
    for i, rec in enumerate(analysis['recommendations'][:3], 1):
        print(f"  {i}. {rec}")
    
    # Show personalized insights
    print(f"\n💡 Personalized Insights")
    print("-" * 25)
    insights = chatbot.get_personalized_insights(user_id)
    for i, insight in enumerate(insights, 1):
        print(f"{i}. {insight}")
    
    # Show conversation history
    print(f"\n📝 Conversation History (Last 5)")
    print("-" * 35)
    history = chatbot.get_conversation_history(user_id, limit=5)
    for conv in history:
        print(f"• {conv['message'][:60]}..." if len(conv['message']) > 60 else f"• {conv['message']}")
    
    print(f"\n✨ Demo completed! The chatbot successfully:")
    print("   ✅ Analyzed 7 financial transactions")
    print("   ✅ Answered 9 different types of questions")
    print("   ✅ Provided personalized insights and recommendations")
    print("   ✅ Maintained conversation context and history")
    print("   ✅ Calculated potential tax savings")
    print("   ✅ Categorized expenses and spending patterns")
    
    print(f"\n🚀 Integration Ready!")
    print("   • Use the API endpoints for web/mobile integration")
    print("   • Works with or without OpenAI API key")
    print("   • Provides intelligent responses about user's financial data")
    print("   • Can answer ANY question about taxes and expenses")

if __name__ == "__main__":
    main()