from flask import Flask, render_template, request
from transformers import pipeline
from PIL import Image
import requests
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the Hugging Face image classification model
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error="No image part")

        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', error="No selected file")

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                image = Image.open(filepath)
                results = classifier(image)
            except Exception as e:
                return render_template('index.html', error=f"Error processing image: {e}")

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
