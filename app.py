from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Global variables for model and preprocessing
model = None
scaler = None
label_encoders = {}
feature_names = []

def load_model_and_data():
    """Load the trained model and preprocessing components"""
    global model, scaler, label_encoders, feature_names
    
    # Load the dataset
    df = pd.read_csv('african_crises.csv')
    
    # Prepare features and target
    X = df.drop('banking_crisis', axis=1)
    y = df['banking_crisis']
    
    # Encode categorical columns
    for col in X.columns:
        if X[col].dtype == 'object':
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            label_encoders[col] = le
    
    # Store feature names
    feature_names = X.columns.tolist()
    
    # Scale features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Load the saved logistic regression model
    with open('logistic_regression_model.pkl', 'rb') as f:
        model = pickle.load(f)
    # Save scaler and label_encoders for future use (if needed)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    with open('label_encoders.pkl', 'wb') as f:
        pickle.dump(label_encoders, f)

def get_countries():
    """Get list of available countries"""
    df = pd.read_csv('african_crises.csv')
    return sorted(df['country'].unique().tolist())

def get_years():
    """Get range of available years"""
    df = pd.read_csv('african_crises.csv')
    return int(df['year'].min()), int(df['year'].max())

@app.route('/')
def index():
    """Main page"""
    countries = get_countries()
    min_year, max_year = get_years()
    return render_template('index.html', countries=countries, min_year=min_year, max_year=max_year)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        data = request.get_json()
        
        # Extract features from request
        features = {}
        for feature in feature_names:
            if feature in data:
                features[feature] = data[feature]
            else:
                # Provide default values for missing features
                if feature == 'case':
                    features[feature] = 1
                elif feature == 'cc3':
                    features[feature] = 'XXX'
                elif feature == 'country':
                    features[feature] = 'Algeria'
                elif feature == 'year':
                    features[feature] = 2020
                else:
                    features[feature] = 0
        
        # Create feature vector
        feature_vector = []
        for feature in feature_names:
            value = features[feature]
            
            # Handle categorical encoding
            if feature in label_encoders:
                if value in label_encoders[feature].classes_:
                    encoded_value = label_encoders[feature].transform([value])[0]
                else:
                    # If value not in training data, use most common value
                    encoded_value = 0
                feature_vector.append(encoded_value)
            else:
                feature_vector.append(float(value))
        
        # Scale features
        feature_vector_scaled = scaler.transform([feature_vector])
        
        # Make prediction
        prediction = model.predict(feature_vector_scaled)[0]
        probability = model.predict_proba(feature_vector_scaled)[0]
        print(prediction, probability)
        # Convert prediction to readable format
        crisis_status = "Crisis" if prediction == 0 else "No Crisis"    
        crisis_probability = probability[0] if prediction == 0 else probability[1]
        
        return jsonify({
            'success': True,
            'prediction': crisis_status,
            'probability': round(crisis_probability * 100, 2),
            'features_used': feature_names
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/data')
def get_data():
    """Get sample data for visualization"""
    df = pd.read_csv('african_crises.csv')
    
    # Get crisis distribution
    crisis_dist = df['banking_crisis'].value_counts().to_dict()
    
    # Get country-wise crisis count
    country_crisis = df[df['banking_crisis'] == 'crisis']['country'].value_counts().head(10).to_dict()
    
    # Get year-wise crisis count
    year_crisis = df[df['banking_crisis'] == 'crisis']['year'].value_counts().head(10).to_dict()
    
    return jsonify({
        'crisis_distribution': crisis_dist,
        'country_crisis': country_crisis,
        'year_crisis': year_crisis
    })

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

if __name__ == '__main__':
    # Load model on startup
    load_model_and_data()
    print("Model loaded successfully!")
    print(f"Available features: {feature_names}")
    
    app.run(debug=True, host='0.0.0.0', port=5001) 