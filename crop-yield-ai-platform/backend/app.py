from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
import requests
from datetime import datetime
from recommendation_engine import generate_recommendations

app = Flask(__name__)
CORS(app)

# Load model and preprocessors
model = None
scaler = None
crop_encoder = None
region_encoder = None
feature_columns = None

def load_models():
    """Load all trained models and encoders"""
    global model, scaler, crop_encoder, region_encoder, feature_columns
    
    model_path = '../models/'
    
    try:
        model = joblib.load(os.path.join(model_path, 'crop_yield_model.pkl'))
        scaler = joblib.load(os.path.join(model_path, 'scaler.pkl'))
        crop_encoder = joblib.load(os.path.join(model_path, 'crop_encoder.pkl'))
        region_encoder = joblib.load(os.path.join(model_path, 'region_encoder.pkl'))
        feature_columns = joblib.load(os.path.join(model_path, 'feature_columns.pkl'))
        print("Models loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading models: {e}")
        return False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': model is not None
    })

@app.route('/api/predict', methods=['POST'])
def predict_yield():
    """Predict crop yield based on input parameters"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['crop_type', 'region', 'temperature', 'rainfall', 
                          'humidity', 'soil_ph', 'nitrogen', 'phosphorus', 
                          'potassium', 'pesticide_usage', 'irrigation_hours']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Encode categorical variables
        try:
            crop_encoded = crop_encoder.transform([data['crop_type']])[0]
            region_encoded = region_encoder.transform([data['region']])[0]
        except ValueError as e:
            return jsonify({
                'error': f'Unknown crop type or region. Supported crops: {list(crop_encoder.classes_)}, Supported regions: {list(region_encoder.classes_)}'
            }), 400
        
        # Prepare features
        features = np.array([[
            crop_encoded,
            region_encoded,
            data['temperature'],
            data['rainfall'],
            data['humidity'],
            data['soil_ph'],
            data['nitrogen'],
            data['phosphorus'],
            data['potassium'],
            data['pesticide_usage'],
            data['irrigation_hours']
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Generate recommendations
        recommendations = generate_recommendations(data, prediction)
        
        return jsonify({
            'success': True,
            'predicted_yield': round(prediction, 2),
            'unit': 'kg per hectare',
            'input_data': data,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/weather', methods=['GET'])
def get_weather():
    """Get current weather data (mock data for MVP)"""
    # In production, integrate with real weather API
    mock_weather = {
        'temperature': 28.5,
        'humidity': 75,
        'rainfall': 12.5,
        'location': 'Bhubaneswar, Odisha',
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(mock_weather)

@app.route('/api/soil', methods=['GET'])
def get_soil_data():
    """Get soil data (mock data for MVP)"""
    # In production, integrate with soil testing database
    mock_soil = {
        'ph': 6.5,
        'nitrogen': 120,
        'phosphorus': 40,
        'potassium': 30,
        'organic_matter': 2.5,
        'location': 'Bhubaneswar, Odisha',
        'last_tested': '2024-01-15'
    }
    return jsonify(mock_soil)

@app.route('/api/crops', methods=['GET'])
def get_supported_crops():
    """Get list of supported crops and regions"""
    return jsonify({
        'crops': list(crop_encoder.classes_) if crop_encoder else [],
        'regions': list(region_encoder.classes_) if region_encoder else []
    })

@app.route('/api/historical', methods=['GET'])
def get_historical_data():
    """Get historical yield data"""
    try:
        df = pd.read_csv('../data/sample_crop_data.csv')
        
        # Group by crop type and calculate average yield
        avg_yield = df.groupby('crop_type')['yield_per_hectare'].mean().to_dict()
        
        # Get recent trends
        recent_data = df.tail(10).to_dict('records')
        
        return jsonify({
            'average_yields': avg_yield,
            'recent_predictions': recent_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get agricultural statistics"""
    try:
        df = pd.read_csv('../data/sample_crop_data.csv')
        
        stats = {
            'total_predictions': len(df),
            'average_yield': df['yield_per_hectare'].mean(),
            'best_performing_crop': df.groupby('crop_type')['yield_per_hectare'].mean().idxmax(),
            'regions_covered': df['region'].nunique(),
            'crops_analyzed': df['crop_type'].nunique()
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load models on startup
    if load_models():
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load models. Please train the model first.")
