# 🚀 Getting Started - Vehicle Detection App

## Quick Start Options

### Option 1: Automated Setup (Recommended)
```bash
python3 setup.py
python3 app.py
```

### Option 2: Manual Setup
```bash
pip3 install -r requirements.txt
python3 app.py
```

### Option 3: Platform-Specific Scripts
- **Mac/Linux**: `./run_app.sh`
- **Windows**: Double-click `run_app.bat`

## 📋 What You Need

### Prerequisites
- **Python 3.7 or higher** (Download from [python.org](https://www.python.org/downloads/))
- **Internet connection** (for AI vehicle detection)

### Files You Should Have
```
DeltaAI/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── setup.py              # Automated setup
├── run_app.sh            # Mac/Linux launcher
├── run_app.bat           # Windows launcher
├── templates/index.html  # Web interface
├── static/style.css      # Styling
├── static/script.js      # Frontend logic
└── README.md             # Documentation
```

## 🎯 Step-by-Step Instructions

### For Complete Beginners

1. **Download Python** (if not installed)
   - Go to [python.org](https://www.python.org/downloads/)
   - Download and install Python 3.7+

2. **Download the Project**
   - Download all files to a folder on your computer

3. **Open Terminal/Command Prompt**
   - **Mac**: Press `Cmd + Space`, type "Terminal", press Enter
   - **Windows**: Press `Win + R`, type "cmd", press Enter

4. **Navigate to Project Folder**
   ```bash
   cd /path/to/your/DeltaAI/folder
   ```

5. **Run Setup**
   ```bash
   python3 setup.py
   ```

6. **Start the App**
   ```bash
   python3 app.py
   ```

7. **Open in Browser**
   - Open your web browser
   - Go to: `http://localhost:5001`

## 🧪 Testing the Application

1. **Find a Test Image**
   - Use any image with vehicles (cars, trucks, tanks, etc.)
   - Clear, high-quality images work best

2. **Upload and Analyze**
   - Click "Choose File" and select your image
   - Click "Analyze Vehicles"
   - Wait for results (usually 5-10 seconds)

3. **Expected Results**
   ```
   Vehicle Detection Results
   Analysis Method: Gemini Vehicle Detection
   Vehicles Detected: 2

   Detected Items:
   🛡️ Vehicle Type: tank (Military) - Main battle tank (Confidence: High)
   🚗 Vehicle Type: car - Civilian sedan (Confidence: Medium)
   ```

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "python3 not found" | Install Python from python.org |
| "pip3 not found" | Run: `python3 -m ensurepip --upgrade` |
| "Module not found" | Run: `pip3 install -r requirements.txt` |
| "Port in use" | Check console for correct URL |
| "No vehicles detected" | Try a clearer image with visible vehicles |

### Getting Help

1. **Check Console Output**: Look for error messages in the terminal
2. **Verify Files**: Make sure all project files are in the same folder
3. **Test Setup**: Run `python3 setup.py` to check everything
4. **Check Internet**: The AI detection requires internet connection

## 📱 Example Use Cases

- **Parking Lot Photos** → Detect cars, trucks
- **Military Images** → Detect tanks, armored vehicles
- **Airport Photos** → Detect planes, helicopters
- **Harbor Images** → Detect ships, boats
- **Construction Sites** → Detect construction vehicles

## 🎉 Success!

Once you see the web interface and can upload images, you're all set! The app will:

- ✅ Detect various vehicle types
- ✅ Classify military vs civilian vehicles
- ✅ Provide confidence levels
- ✅ Give detailed descriptions
- ✅ Work with most image formats (JPEG, PNG, etc.)

## 📞 Need More Help?

- Check the `README.md` for detailed documentation
- Look at `QUICK_START.md` for simplified instructions
- Run `python3 test_vehicle_detection.py` to test the system
- Check console output for specific error messages

Happy vehicle detecting! 🚗🛡️✈️🚢
