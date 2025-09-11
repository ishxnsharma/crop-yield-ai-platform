from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

app = Flask(__name__)
CORS(app)

# Global model variable
model = None

def create_sample_data():
    """Create sample agricultural data for training"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'temperature': np.random.normal(25, 5, n_samples),  # Average temp in Celsius
        'rainfall': np.random.normal(150, 50, n_samples),   # Monthly rainfall in mm
        'humidity': np.random.normal(70, 15, n_samples),    # Humidity percentage
        'ph_level': np.random.normal(6.5, 0.5, n_samples), # Soil pH
        'nitrogen': np.random.normal(40, 10, n_samples),    # Nitrogen content
        'phosphorus': np.random.normal(20, 5, n_samples),   # Phosphorus content
        'potassium': np.random.normal(30, 8, n_samples),    # Potassium content
    }
    
    df = pd.DataFrame(data)
    
    # Create a realistic yield formula (tons per hectare)
    df['yield'] = (
        2.0 +  # Base yield
        0.1 * df['temperature'] +
        0.02 * df['rainfall'] +
        0.05 * df['humidity'] +
        0.5 * df['ph_level'] +
        0.03 * df['nitrogen'] +
        0.04 * df['phosphorus'] +
        0.02 * df['potassium'] +
        np.random.normal(0, 0.5, n_samples)  # Add some noise
    )
    
    # Ensure yield is positive
    df['yield'] = np.maximum(df['yield'], 0.5)
    
    return df

def train_model():
    """Train the crop yield prediction model"""
    global model
    
    # Check if model already exists
    if os.path.exists('crop_yield_model.joblib'):
        model = joblib.load('crop_yield_model.joblib')
        print("Model loaded from file")
        return
    
    # Create sample data
    df = create_sample_data()
    
    # Prepare features and target
    features = ['temperature', 'rainfall', 'humidity', 'ph_level', 'nitrogen', 'phosphorus', 'potassium']
    X = df[features]
    y = df['yield']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, 'crop_yield_model.joblib')
    
    # Print model performance
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Model trained! Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_yield():
    """Predict crop yield based on input parameters"""
    try:
        data = request.json
        
        # Extract features
        features = [
            data.get('temperature', 25),
            data.get('rainfall', 150),
            data.get('humidity', 70),
            data.get('ph_level', 6.5),
            data.get('nitrogen', 40),
            data.get('phosphorus', 20),
            data.get('potassium', 30)
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        # Generate recommendations
        recommendations = generate_recommendations(data, prediction)
        
        return jsonify({
            'predicted_yield': round(prediction, 2),
            'unit': 'tons per hectare',
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def generate_recommendations(data, predicted_yield):
    """Generate farming recommendations based on input data"""
    recommendations = []
    
    temp = data.get('temperature', 25)
    rainfall = data.get('rainfall', 150)
    ph = data.get('ph_level', 6.5)
    nitrogen = data.get('nitrogen', 40)
    
    if temp < 20:
        recommendations.append("Consider using row covers or greenhouse protection for better temperature control")
    elif temp > 35:
        recommendations.append("Provide shade or increase irrigation during hot periods")
    
    if rainfall < 100:
        recommendations.append("Increase irrigation frequency - crops need more water")
    elif rainfall > 250:
        recommendations.append("Ensure proper drainage to prevent waterlogging")
    
    if ph < 6.0:
        recommendations.append("Add lime to increase soil pH for better nutrient availability")
    elif ph > 7.5:
        recommendations.append("Add organic matter to lower soil pH")
    
    if nitrogen < 30:
        recommendations.append("Apply nitrogen fertilizer to boost crop growth")
    
    if predicted_yield < 3.0:
        recommendations.append("Consider soil testing and consulting with local agricultural extension office")
    elif predicted_yield > 6.0:
        recommendations.append("Great conditions! Focus on pest monitoring and timely harvesting")
    
    if not recommendations:
        recommendations.append("Current conditions look good for healthy crop growth")
    
    return recommendations

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    # Train model on startup
    train_model()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
