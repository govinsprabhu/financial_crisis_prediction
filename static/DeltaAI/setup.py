#!/usr/bin/env python3
"""
Setup script for Vehicle Detection Application
Automatically installs dependencies and checks system requirements
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_files():
    """Check if all required files are present"""
    required_files = [
        "app.py",
        "requirements.txt",
        "templates/index.html",
        "static/style.css",
        "static/script.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def create_uploads_folder():
    """Create uploads folder if it doesn't exist"""
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        print("✅ Created uploads folder")
    else:
        print("✅ Uploads folder exists")

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing imports...")
    try:
        import flask
        import PIL
        import requests
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Vehicle Detection App Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Check files
    if not check_files():
        return False
    
    # Create uploads folder
    create_uploads_folder()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: python3 app.py")
    print("2. Open your browser and go to: http://localhost:5001")
    print("3. Upload an image with vehicles to test")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
