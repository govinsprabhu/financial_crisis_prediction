import base64
import json
import os
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests

def get_gemini_api_key():
    """
    Retrieves the API key from environment variables.
    Replace with your actual key if not using an environment variable.
    """
    return "AIzaSyC6S8773_1pIO3q81dH42VLcu6SbC28gzs"

def resize_image(image_bytes, max_size=(1024, 1024)):
    """
    Resizes an image to fit within a maximum size while maintaining aspect ratio.
    """
    img = Image.open(BytesIO(image_bytes))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    resized_buffer = BytesIO()
    img.save(resized_buffer, format="JPEG")
    return resized_buffer.getvalue()

def detect_objects_with_gemini(image_path, api_key):
    """
    Sends an image and a prompt to the Gemini API to detect objects.

    Args:
        image_path (str): The path to the image file.
        api_key (str): Your Gemini API key.

    Returns:
        list: A list of dictionaries with detected objects, or None on failure.
    """
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            
        # Resize image to a reasonable size to avoid API limits
        resized_image_bytes = resize_image(image_bytes)

        # Encode the resized image to base64
        base64_image = base64.b64encode(resized_image_bytes).decode("utf-8")

        # The prompt is critical for getting structured data.
        # We ask for a JSON array containing object names and normalized bounding boxes.
        prompt = "Return a JSON array of all objects in this image. For each object, include the 'object_name' and a 'bounding_box' with normalized coordinates [ymin, xmin, ymax, xmax]. Do not include any other text."

        headers = {
            "Content-Type": "application/json"
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
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
        
        # Check if the response contains valid content
        if 'candidates' in result and len(result['candidates']) > 0:
            content = result['candidates'][0]['content']
            if 'parts' in content and len(content['parts']) > 0 and 'text' in content['parts'][0]:
                json_string = content['parts'][0]['text']
                # The model might return a JSON string with markdown, so we need to clean it.
                json_string = json_string.strip('` \n').replace("```json", "").replace("```", "")
                try:
                    objects = json.loads(json_string)
                    return objects
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON: {e}")
                    print("Raw JSON string:", json_string)
                    return None
        return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return None

def get_image_description(image_path, api_key):
    """
    Sends an image to the Gemini API and gets a natural language description.

    Args:
        image_path (str): The path to the image file.
        api_key (str): Your Gemini API key.

    Returns:
        str: A text description of the image, or None on failure.
    """
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        resized_image_bytes = resize_image(image_bytes)
        base64_image = base64.b64encode(resized_image_bytes).decode("utf-8")

        prompt = "Describe this image in detail."

        headers = {
            "Content-Type": "application/json"
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
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
            ]
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            content = result['candidates'][0]['content']
            if 'parts' in content and len(content['parts']) > 0 and 'text' in content['parts'][0]:
                return content['parts'][0]['text']
        return "Failed to get a description."

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return "Failed to get a description due to an API error."
    except FileNotFoundError:
        print(f"Error: The file '{image_path}' was not found.")
        return "Failed to get a description because the image file was not found."


def draw_bounding_boxes(image_path, detected_objects):
    """
    Draws bounding boxes and labels on the image and saves it.

    Args:
        image_path (str): The path to the original image.
        detected_objects (list): A list of dictionaries with detected objects.
    """
    try:
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default() # Using a default font
        
        width, height = img.size

        # Define some colors for the boxes
        colors = ["red", "green", "blue", "purple", "orange"]

        for i, obj in enumerate(detected_objects):
            # The coordinates are normalized (0 to 1), so convert to pixel values
            ymin, xmin, ymax, xmax = obj["bounding_box"]
            
            # The model's normalized coordinates might be 0-1 or 0-1000.
            # We'll handle both cases by checking the values.
            if ymin > 1 or xmin > 1 or ymax > 1 or xmax > 1:
                # Assume 0-1000 scale and normalize to 0-1
                ymin /= 1000
                xmin /= 1000
                ymax /= 1000
                xmax /= 1000
                
            x1 = int(xmin * width)
            y1 = int(ymin * height)
            x2 = int(xmax * width)
            y2 = int(ymax * height)
            
            object_name = obj["object_name"]
            color = colors[i % len(colors)]

            # Draw the bounding box
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # Draw the label text
            text_position = (x1, y1 - 15)
            draw.text(text_position, object_name, fill=color, font=font)

        output_path = "detected_" + os.path.basename(image_path)
        img.save(output_path)
        print(f"Image with detected objects saved to '{output_path}'")

    except FileNotFoundError:
        print(f"Error: The image file '{image_path}' was not found.")
    except Exception as e:
        print(f"An error occurred while drawing: {e}")

if __name__ == "__main__":
    # Get the API key
    api_key = get_gemini_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set your API key and try again.")
    else:
        # Example usage:
        # 1. Replace 'your_image.jpg' with the path to your image file.
        # 2. Make sure the image file is in the same directory as this script.
        image_file = "/Users/govindprabhu/Downloads/sddefault.jpg"
        
        print(f"Detecting objects in '{image_file}'...")
        detected_objects = detect_objects_with_gemini(image_file, api_key)
        
        if detected_objects:
            print("Detected Objects:")
            for obj in detected_objects:
                print(f"- {obj['object_name']} at coordinates {obj['bounding_box']}")
            
            draw_bounding_boxes(image_file, detected_objects)
        else:
            print("Object detection failed.")
            
        print("\nGetting image description...")
        description = get_image_description(image_file, api_key)
        print("Image Description:")
        print(description)