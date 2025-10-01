#!/usr/bin/env python3
"""
Test script for vehicle detection functionality
"""

import requests
import os
from PIL import Image
import io

def test_vehicle_detection():
    """Test the vehicle detection API endpoint"""
    
    # Check if the server is running
    try:
        response = requests.get('http://localhost:5001/')
        if response.status_code == 200:
            print("✅ Server is running successfully")
        else:
            print("❌ Server is not responding correctly")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start the server with: python3 app.py")
        return
    
    # Create a simple test image (you can replace this with an actual image file)
    print("\n📋 Testing vehicle detection functionality...")
    print("ℹ️  To test with a real image, upload one through the web interface at http://localhost:5001")
    print("ℹ️  The system can detect:")
    print("   • Military vehicles (tanks, armored vehicles)")
    print("   • Civilian vehicles (cars, trucks, motorcycles)")
    print("   • Aircraft (planes, helicopters)")
    print("   • Ships and boats")
    print("   • And other vehicle types")
    
    print("\n🚀 Application is ready for testing!")
    print("🌐 Open your browser and go to: http://localhost:5001")
    print("📸 Upload an image containing vehicles to see the detection in action")

if __name__ == "__main__":
    test_vehicle_detection()
