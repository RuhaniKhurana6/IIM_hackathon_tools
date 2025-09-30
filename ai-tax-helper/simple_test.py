#!/usr/bin/env python3
"""
Simple test script for the AI Chatbot APIs
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    return response.status_code == 200

def test_chatbot_initialize():
    print("\n--- Testing chatbot initialization ---")
    response = requests.post(f"{BASE_URL}/api/chatbot/initialize", 
                           json={"user_id": "test_user"})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
        return True
    else:
        print(f"Error: {response.text}")
        return False

def test_chatbot_chat():
    print("\n--- Testing chatbot chat ---")
    messages = [
        "Hello, what can you help me with?",
        "How much can I deduct in taxes?",
        "What are my total expenses?"
    ]
    
    for message in messages:
        print(f"\nSending: {message}")
        response = requests.post(f"{BASE_URL}/api/chatbot/chat", 
                               json={"user_id": "test_user", "message": message})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data['response']}")
        else:
            print(f"Error: {response.text}")

def test_chatbot_insights():
    print("\n--- Testing chatbot insights ---")
    response = requests.get(f"{BASE_URL}/api/chatbot/insights?user_id=test_user")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Insights:")
        for i, insight in enumerate(data['insights'], 1):
            print(f"  {i}. {insight}")
    else:
        print(f"Error: {response.text}")

def test_chatbot_analysis():
    print("\n--- Testing chatbot analysis ---")
    response = requests.post(f"{BASE_URL}/api/chatbot/analyze", 
                           json={"user_id": "test_user"})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Analysis: {json.dumps(data, indent=2)}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("🚀 Testing AI Tax Chatbot APIs")
    
    if not test_health():
        print("❌ Server is not responding")
        exit(1)
    
    if test_chatbot_initialize():
        test_chatbot_chat()
        test_chatbot_insights() 
        test_chatbot_analysis()
    else:
        print("❌ Failed to initialize chatbot")
    
    print("\n✨ Testing completed!")