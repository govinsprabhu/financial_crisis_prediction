# 🚀 Quick Start Guide - Vehicle Detection App

## For New Users - Simple Setup

### Step 1: Prerequisites
Make sure you have Python 3.7+ installed on your computer.

**Check if Python is installed:**
```bash
python3 --version
```

If you don't have Python, download it from [python.org](https://www.python.org/downloads/)

### Step 2: Download/Clone the Project
- Download all the project files to a folder on your computer
- Or if you have Git: `git clone <repository-url>`

### Step 3: Open Terminal/Command Prompt
- **Mac/Linux**: Open Terminal
- **Windows**: Open Command Prompt or PowerShell

### Step 4: Navigate to Project Folder
```bash
cd /path/to/your/DeltaAI/folder
```

### Step 5: Install Dependencies (One-time setup)
```bash
pip3 install -r requirements.txt
```

### Step 6: Run the Application
```bash
python3 app.py
```

### Step 7: Open in Browser
- Open your web browser
- Go to: `http://localhost:5001`
- You should see the Vehicle Detection interface

### Step 8: Test the Application
1. Click "Choose File" and select an image with vehicles
2. Click "Analyze Vehicles"
3. Wait for the results to appear

## 🎯 What You'll See

The app will detect and classify vehicles like:
- 🛡️ Military vehicles (tanks, armored vehicles)
- 🚗 Civilian vehicles (cars, trucks)
- ✈️ Aircraft (planes, helicopters)
- 🚢 Ships and boats

## ❗ Common Issues & Solutions

### "Command not found: python3"
- **Mac**: Install Python from python.org
- **Windows**: Use `python` instead of `python3`

### "pip3 not found"
- **Mac**: Install pip: `python3 -m ensurepip --upgrade`
- **Windows**: Use `pip` instead of `pip3`

### "Port already in use"
- The app will automatically try different ports
- Check the console output for the correct URL

### "Module not found" errors
- Run: `pip3 install -r requirements.txt` again
- Make sure you're in the correct project folder

## 🆘 Need Help?

1. Check the console output for error messages
2. Make sure all files are in the same folder
3. Try running the test script: `python3 test_vehicle_detection.py`

## 📱 Example Usage

1. **Upload a photo** of a parking lot → Detect cars
2. **Upload a military image** → Detect tanks, armored vehicles
3. **Upload an airport photo** → Detect planes, helicopters

The app works best with clear, high-quality images where vehicles are clearly visible!
