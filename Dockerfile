FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model files and dataset first
COPY african_crises.csv .
COPY logistic_regression_model.pkl .
COPY scaler.pkl .
COPY label_encoders.pkl .

# Copy the rest of the application
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=.

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--preload"]
