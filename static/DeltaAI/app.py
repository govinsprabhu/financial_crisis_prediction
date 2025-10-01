import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
import io
import base64
import json
import requests

# Set up Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max

# Initialize Google Cloud Vision client (optional)
vision_client = None
try:
    from google.cloud import vision
    from google.oauth2 import service_account
    
    # Set your Google service account key path here
    GOOGLE_APPLICATION_CREDENTIALS = 'path/to/your/service-account.json'
    
    if os.path.exists(GOOGLE_APPLICATION_CREDENTIALS):
        credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
        vision_client = vision.ImageAnnotatorClient(credentials=credentials)
        print("Google Cloud Vision API initialized successfully")
    else:
        print("Google Cloud Vision credentials not found. Using Gemini API for vehicle detection.")
except ImportError:
    print("Google Cloud Vision library not installed. Using Gemini API for vehicle detection.")
except Exception as e:
    print(f"Error initializing Google Cloud Vision: {e}. Using Gemini API for vehicle detection.")

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyC6S8773_1pIO3q81dH42VLcu6SbC28gzs"

def resize_image(image_bytes, max_size=(1024, 1024)):
    """Resizes an image to fit within a maximum size while maintaining aspect ratio."""
    img = Image.open(io.BytesIO(image_bytes))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    resized_buffer = io.BytesIO()
    img.save(resized_buffer, format="JPEG")
    return resized_buffer.getvalue()

def detect_vehicles_with_gemini(image_path):
    """Detects vehicles and their types using Gemini API"""
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            
        # Resize image to a reasonable size to avoid API limits
        resized_image_bytes = resize_image(image_bytes)
        base64_image = base64.b64encode(resized_image_bytes).decode("utf-8")

        # Specific prompt for vehicle detection
        prompt = """Analyze this image and identify any vehicles present. 
        Focus on military vehicles, tanks, cars, trucks, aircraft, ships, or any other vehicles.
        Return a JSON array with each vehicle containing:
        - "vehicle_type": The specific type (e.g., "tank", "car", "truck", "aircraft", "ship")
        - "description": Brief description of the vehicle
        - "confidence": High/Medium/Low confidence level
        - "military": true/false if it's a military vehicle
        
        If no vehicles are detected, return an empty array.
        Return only the JSON array, no other text."""

        headers = {"Content-Type": "application/json"}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={GEMINI_API_KEY}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inlineData": {
                                "mimeType": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            content = result['candidates'][0]['content']
            if 'parts' in content and len(content['parts']) > 0 and 'text' in content['parts'][0]:
                json_string = content['parts'][0]['text']
                json_string = json_string.strip('` \n').replace("```json", "").replace("```", "")
                try:
                    vehicles = json.loads(json_string)
                    return vehicles
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON: {e}")
                    return []
        return []
        
    except Exception as e:
        print(f"Gemini API error: {e}")
        return []

def analyze_image_basic(image_path):
    """Basic image analysis using PIL"""
    try:
        with Image.open(image_path) as img:
            # Get basic image information
            width, height = img.size
            format_name = img.format
            mode = img.mode
            
            # Basic analysis based on image characteristics
            analysis = []
            analysis.append(f"Image Format: {format_name}")
            analysis.append(f"Dimensions: {width}x{height} pixels")
            analysis.append(f"Color Mode: {mode}")
            
            # Analyze image size
            if width > 2000 or height > 2000:
                analysis.append("High Resolution Image")
            elif width < 500 or height < 500:
                analysis.append("Low Resolution Image")
            else:
                analysis.append("Medium Resolution Image")
            
            # Analyze color mode
            if mode == 'RGB':
                analysis.append("Color Image")
            elif mode == 'L':
                analysis.append("Grayscale Image")
            elif mode == 'RGBA':
                analysis.append("Image with Transparency")
            
            # Basic thermal detection (very simple heuristic)
            if mode == 'L':  # Grayscale
                # Check if image has high contrast (potential thermal)
                img_array = img.convert('L')
                pixels = list(img_array.getdata())
                min_val = min(pixels)
                max_val = max(pixels)
                contrast = max_val - min_val
                if contrast > 100:
                    analysis.append("High Contrast - Possible Thermal Image")
                else:
                    analysis.append("Low Contrast Image")
            
            return analysis
    except Exception as e:
        return [f"Error analyzing image: {str(e)}"]

# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Always try vehicle detection with Gemini first
        vehicles = detect_vehicles_with_gemini(filepath)
        
        if vehicles:
            # Format vehicle detection results
            vehicle_results = []
            for vehicle in vehicles:
                vehicle_type = vehicle.get('vehicle_type', 'Unknown')
                description = vehicle.get('description', 'No description')
                confidence = vehicle.get('confidence', 'Unknown')
                military = vehicle.get('military', False)
                
                result_text = f"Vehicle Type: {vehicle_type}"
                if military:
                    result_text += " (Military)"
                result_text += f" - {description} (Confidence: {confidence})"
                vehicle_results.append(result_text)
            
            return jsonify({
                'labels': vehicle_results, 
                'method': 'Gemini Vehicle Detection',
                'vehicle_count': len(vehicles)
            })
        else:
            # Fallback to basic analysis if no vehicles detected
            if vision_client:
                # Use Google Cloud Vision API
                with open(filepath, 'rb') as image_file:
                    content = image_file.read()
                image = vision.Image(content=content)
                response = vision_client.label_detection(image=image)
                labels = [label.description for label in response.label_annotations]
                return jsonify({'labels': labels, 'method': 'Google Cloud Vision'})
            else:
                # Use basic image analysis
                analysis = analyze_image_basic(filepath)
                analysis.append("No vehicles detected in this image.")
                return jsonify({'labels': analysis, 'method': 'Basic Image Analysis'})
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
    
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    print("Starting Thermal Vehicle Analyzer...")
    print("Access the application at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
