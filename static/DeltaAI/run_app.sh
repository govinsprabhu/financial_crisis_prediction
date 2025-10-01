#!/bin/bash

echo "========================================"
echo "   Vehicle Detection App Launcher"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python from https://www.python.org/downloads/"
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: requirements.txt not found"
    echo "Make sure you're in the correct project folder"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Run the application
echo
echo "Starting Vehicle Detection App..."
echo "Open your browser and go to: http://localhost:5001"
echo "Press Ctrl+C to stop the application"
echo
python3 app.py
