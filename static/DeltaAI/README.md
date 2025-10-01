# Vehicle Detection & Classification System

A web-based application that uses AI to detect and classify vehicles in images, including military vehicles like tanks, civilian vehicles, aircraft, and ships.

## Features

- **Vehicle Detection**: Identifies various types of vehicles in uploaded images
- **Military Vehicle Classification**: Specifically detects military vehicles (tanks, armored vehicles, etc.)
- **Multiple Vehicle Types**: Supports detection of cars, trucks, aircraft, ships, and more
- **Confidence Levels**: Provides confidence ratings for each detection
- **Modern Web Interface**: Clean, responsive UI with real-time analysis
- **Fallback Analysis**: Basic image analysis when no vehicles are detected

## Vehicle Types Detected

- **Military Vehicles**: Tanks, armored personnel carriers, military trucks
- **Civilian Vehicles**: Cars, trucks, motorcycles, buses
- **Aircraft**: Planes, helicopters, drones
- **Maritime**: Ships, boats, submarines
- **Other**: Construction vehicles, emergency vehicles, etc.

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 app.py
   ```

4. **Access the application**:
   Open your browser and go to: `http://localhost:5001`

## Usage

1. **Upload an Image**: Click "Choose File" and select an image containing vehicles
2. **Analyze**: Click "Analyze Vehicles" to process the image
3. **View Results**: See detailed vehicle detection results with:
   - Vehicle type classification
   - Description of each vehicle
   - Confidence levels
   - Military vs civilian classification

## Technical Details

### AI Models Used

- **Primary**: Google Gemini 2.5 Flash API for vehicle detection and classification
- **Fallback**: Google Cloud Vision API (if credentials available)
- **Basic Analysis**: PIL/Pillow for image properties when no vehicles detected

### API Configuration

The application uses the Gemini API key from the `THermal.py` file. To use your own API key:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Replace the API key in `app.py` line 25:
   ```python
   GEMINI_API_KEY = "your-api-key-here"
   ```

### File Structure

```
DeltaAI/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── style.css         # Styling
│   └── script.js         # Frontend JavaScript
├── uploads/              # Temporary file storage
├── THermal.py           # Original Gemini integration
└── test_vehicle_detection.py  # Test script
```

## Example Output

When you upload an image with vehicles, you'll see results like:

```
Vehicle Detection Results
Analysis Method: Gemini Vehicle Detection
Vehicles Detected: 2

Detected Items:
🛡️ Vehicle Type: tank (Military) - Main battle tank with turret and tracks (Confidence: High)
🚗 Vehicle Type: car - Civilian sedan parked nearby (Confidence: Medium)
```

## Troubleshooting

### Common Issues

1. **"Server not running"**: Make sure to run `python3 app.py` first
2. **"No vehicles detected"**: Try uploading a clearer image with visible vehicles
3. **API errors**: Check your internet connection and API key validity

### Port Conflicts

If port 5001 is in use, the application will automatically try alternative ports. Check the console output for the correct URL.

## Development

### Adding New Vehicle Types

To extend vehicle detection capabilities, modify the prompt in the `detect_vehicles_with_gemini()` function in `app.py`.

### Customizing the UI

- Edit `templates/index.html` for layout changes
- Modify `static/style.css` for styling
- Update `static/script.js` for frontend behavior

## License

This project is for educational and research purposes. Please ensure you have proper permissions for any images you analyze.

## Support

For issues or questions, check the console output for error messages and ensure all dependencies are properly installed.
