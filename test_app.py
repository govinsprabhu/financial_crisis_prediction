#!/usr/bin/env python3
"""
Simple test script to verify the Flask application works correctly.
"""

import requests
import json
import time

def test_flask_app():
    """Test the Flask application endpoints."""
    
    base_url = "http://localhost:5000"
    
    print("Testing Financial Crisis Prediction Web Application...")
    print("=" * 50)
    
    # Test 1: Check if the main page loads
    print("1. Testing main page...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("   ✅ Main page loads successfully")
        else:
            print(f"   ❌ Main page failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Main page failed: {e}")
        return False
    
    # Test 2: Check if the about page loads
    print("2. Testing about page...")
    try:
        response = requests.get(f"{base_url}/about", timeout=10)
        if response.status_code == 200:
            print("   ✅ About page loads successfully")
        else:
            print(f"   ❌ About page failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ About page failed: {e}")
        return False
    
    # Test 3: Check if the data endpoint works
    print("3. Testing data endpoint...")
    try:
        response = requests.get(f"{base_url}/data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'crisis_distribution' in data:
                print("   ✅ Data endpoint works successfully")
                print(f"   📊 Crisis distribution: {data['crisis_distribution']}")
            else:
                print("   ❌ Data endpoint returned invalid data")
        else:
            print(f"   ❌ Data endpoint failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Data endpoint failed: {e}")
        return False
    
    # Test 4: Test prediction endpoint
    print("4. Testing prediction endpoint...")
    test_data = {
        "country": "Algeria",
        "year": "2020",
        "inflation_annual_cpi": "5.0",
        "exch_usd": "1.0",
        "systemic_crisis": "0",
        "currency_crises": "0",
        "inflation_crises": "0"
    }
    
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("   ✅ Prediction endpoint works successfully")
                print(f"   🎯 Prediction: {result['prediction']}")
                print(f"   📈 Confidence: {result['probability']}%")
            else:
                print(f"   ❌ Prediction failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Prediction endpoint failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Prediction endpoint failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! The application is working correctly.")
    print(f"🌐 Open your browser and go to: {base_url}")
    return True

if __name__ == "__main__":
    # Wait a moment for the Flask app to start
    print("Waiting for Flask app to start...")
    time.sleep(2)
    
    success = test_flask_app()
    if not success:
        print("\n❌ Some tests failed. Please check if the Flask app is running.")
        print("To start the app, run: python app.py") 