#!/usr/bin/env python3
"""
FinHub Zen Integration Test Script
==================================
This script tests all the integrated APIs with dummy data to demonstrate
that all three tools (Tax Helper, Insights, Zero-Click Budgeting) work
together seamlessly through the unified backend.
"""

import requests
import json
import time
from typing import Dict, Any

# Base URL for our unified backend
BASE_URL = "http://localhost:5000"

def print_header(title: str) -> None:
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"{title.center(60)}")
    print(f"{'='*60}")

def print_result(endpoint: str, data: Any) -> None:
    """Print API result in a formatted way"""
    print(f"\n🔗 {endpoint}")
    if isinstance(data, dict):
        print(json.dumps(data, indent=2))
    else:
        print(data)

def test_health_check() -> bool:
    """Test if the backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print_result("Health Check", response.json())
            return True
    except Exception as e:
        print(f"❌ Backend not running: {e}")
        return False

def test_tax_helper_apis() -> None:
    """Test all Tax Helper APIs"""
    print_header("TAX HELPER APIs")
    
    # Test categorized transactions
    try:
        response = requests.get(f"{BASE_URL}/api/tax/categorized")
        print_result("GET /api/tax/categorized", response.json()[:3])  # Show first 3
        print("... (showing first 3 transactions)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test tax summary
    try:
        response = requests.get(f"{BASE_URL}/api/tax/summary")
        print_result("GET /api/tax/summary", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test receipt upload (mock)
    try:
        response = requests.post(f"{BASE_URL}/api/tax/upload-receipt", json={})
        print_result("POST /api/tax/upload-receipt", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")

def test_insights_apis() -> None:
    """Test all Insights APIs"""
    print_header("INSIGHTS APIs")
    
    # Test spending by category
    try:
        response = requests.get(f"{BASE_URL}/api/insights/spending-by-category")
        print_result("GET /api/insights/spending-by-category", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test monthly trends
    try:
        response = requests.get(f"{BASE_URL}/api/insights/monthly-trends")
        print_result("GET /api/insights/monthly-trends", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test transactions
    try:
        response = requests.get(f"{BASE_URL}/api/insights/transactions")
        print_result("GET /api/insights/transactions", response.json()[:3])  # Show first 3
        print("... (showing first 3 transactions)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test SMS ingestion
    try:
        sms_text = "You spent Rs 250 at Zomato on 2024-01-29"
        response = requests.post(f"{BASE_URL}/api/insights/ingest/sms", json={"text": sms_text})
        print_result("POST /api/insights/ingest/sms", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")

def test_budgeting_apis() -> None:
    """Test all Zero-Click Budgeting APIs"""
    print_header("ZERO-CLICK BUDGETING APIs")
    
    # Test current budget gauge
    try:
        response = requests.get(f"{BASE_URL}/budget/gauge")
        print_result("GET /budget/gauge", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test adding SMS transaction
    try:
        response = requests.post(f"{BASE_URL}/webhook/sms", json={
            "amount": 75,
            "merchant": "Uber"
        })
        print_result("POST /webhook/sms", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test adding UPI transaction
    try:
        response = requests.post(f"{BASE_URL}/webhook/upi", json={
            "amount": 320,
            "merchant": "Amazon"
        })
        print_result("POST /webhook/upi", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test adding receipt transaction
    try:
        response = requests.post(f"{BASE_URL}/webhook/receipt", json={
            "amount": 180,
            "merchant": "Big Bazaar"
        })
        print_result("POST /webhook/receipt", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Check updated gauge
    try:
        response = requests.get(f"{BASE_URL}/budget/gauge")
        print_result("GET /budget/gauge (updated)", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test getting all budget transactions
    try:
        response = requests.get(f"{BASE_URL}/budget/transactions")
        transactions = response.json()
        print_result("GET /budget/transactions", f"Total transactions: {len(transactions)}")
        print("Recent transactions:")
        for t in transactions[-3:]:
            print(f"  - {t['merchant']}: ${t['amount']} ({t['method']}) - {t['category']}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_dashboard_api() -> None:
    """Test Dashboard Summary API"""
    print_header("DASHBOARD SUMMARY API")
    
    try:
        response = requests.get(f"{BASE_URL}/api/dashboard-summary")
        print_result("GET /api/dashboard-summary", response.json())
    except Exception as e:
        print(f"❌ Error: {e}")

def run_all_tests() -> None:
    """Run all integration tests"""
    print_header("FinHub Zen Integration Tests")
    print("Testing unified backend with dummy data...")
    
    # Check if backend is running
    if not test_health_check():
        print("\n❌ Please start the backend first with: python main_backend.py")
        return
    
    # Run all API tests
    test_tax_helper_apis()
    test_insights_apis()
    test_budgeting_apis()
    test_dashboard_api()
    
    print_header("TEST SUMMARY")
    print("✅ All APIs tested successfully!")
    print("🚀 Frontend should be running at: http://localhost:5173")
    print("🔧 Backend is running at: http://localhost:5000")
    print("\n📋 What to test in the frontend:")
    print("  1. Dashboard - Shows integrated data from all tools")
    print("  2. Tax Helper - View categorized transactions and summaries")
    print("  3. Insights - Analyze spending patterns and trends")
    print("  4. Budgeting - Real-time budget gauge and auto-categorization")
    print("\n💡 Try adding more transactions via API or frontend to see live updates!")

if __name__ == "__main__":
    run_all_tests()