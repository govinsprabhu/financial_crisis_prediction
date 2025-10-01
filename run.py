#!/usr/bin/env python3
"""
Startup script for the Financial Crisis Prediction Web Application.
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        import pandas
        import numpy
        import sklearn
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_dataset():
    """Check if the dataset file exists."""
    if os.path.exists('african_crises.csv'):
        print("✅ Dataset file found")
        return True
    else:
        print("❌ Dataset file 'african_crises.csv' not found")
        return False

def start_application():
    """Start the Flask application."""
    print("🚀 Starting Financial Crisis Prediction Web Application...")
    print("=" * 60)
    
    # Check prerequisites
    if not check_dependencies():
        return False
    
    if not check_dataset():
        return False
    
    print("\n📊 Loading machine learning model...")
    print("⏳ This may take a few moments on first run...")
    
    try:
        # Start the Flask application
        from app import app
        print("\n✅ Application started successfully!")
        print("🌐 Open your browser and go to: http://localhost:5000")
        print("📱 The application is responsive and works on mobile devices")
        print("\n" + "=" * 60)
        print("Press Ctrl+C to stop the application")
        print("=" * 60)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        return False

if __name__ == "__main__":
    start_application() 