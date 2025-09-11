"""
Flask API for Crop Yield Prediction Platform
MVP Implementation
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.crop_yield_model import quick_predict, CropYieldPredictor

app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Store model instance
predictor = None

# Crop types mapping
CROP_TYPES = {
    0: "Rice",
    1: "Wheat",
    2: "Maize",
    3: "Cotton",
    4: "Sugarcane",
    5: "Pulses",
    6: "Oilseeds",
    7: "Vegetables"
}

# Season mapping
SEASONS = {
    0: "Kharif (Monsoon)",
    1: "Rabi (Winter)",
    2: "Summer"
}

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Crop Yield Prediction API',
        'version': '1.0.0'
    })

@app.route('/api/predict', methods=['POST'])
def predict_yield():
    """
    Predict crop yield based on input parameters
    
    Expected JSON input:
    {
        "rainfall": 650,
        "temperature": 28,
        "humidity": 65,
        "soil_ph": 6.8,
        "nitrogen": 45,
        "phosphorus": 38,
        "potassium": 42,
        "crop_type": "Wheat",
        "season": "Kharif",
        "area_hectares": 2
    }
    """
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['rainfall', 'temperature', 'humidity', 'soil_ph', 
                          'nitrogen', 'phosphorus', 'potassium']
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Convert crop type and season to codes
        crop_type = data.get('crop_type', 'Wheat')
        season = data.get('season', 'Kharif')
        
        # Find crop type code
        crop_type_code = 1  # Default to Wheat
        for code, name in CROP_TYPES.items():
            if name.lower() == crop_type.lower():
                crop_type_code = code
                break
        
        # Find season code
        season_code = 0  # Default to Kharif
        for code, name in SEASONS.items():
            if season.lower() in name.lower():
                season_code = code
                break
        
        # Prepare prediction data
        prediction_data = {
            'rainfall': float(data['rainfall']),
            'temperature': float(data['temperature']),
            'humidity': float(data['humidity']),
            'soil_ph': float(data['soil_ph']),
            'nitrogen': float(data['nitrogen']),
            'phosphorus': float(data['phosphorus']),
            'potassium': float(data['potassium']),
            'crop_type_code': crop_type_code,
            'season_code': season_code,
            'area_hectares': float(data.get('area_hectares', 1))
        }
        
        # Get prediction
        result = quick_predict(prediction_data)
        
        # Add input summary to response
        result['input_summary'] = {
            'crop_type': crop_type,
            'season': season,
            'area': prediction_data['area_hectares'],
            'location': data.get('location', 'Odisha')
        }
        
        # Calculate potential increase
        result['potential_increase'] = {
            'percentage': '10-15%',
            'description': 'Expected yield increase by following recommendations'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/crop-types', methods=['GET'])
def get_crop_types():
    """Get list of supported crop types"""
    return jsonify({
        'crop_types': list(CROP_TYPES.values())
    })

@app.route('/api/seasons', methods=['GET'])
def get_seasons():
    """Get list of seasons"""
    return jsonify({
        'seasons': list(SEASONS.values())
    })

@app.route('/api/sample-data', methods=['GET'])
def get_sample_data():
    """Get sample data for testing"""
    samples = [
        {
            'name': 'Good Conditions - Rice',
            'data': {
                'rainfall': 1200,
                'temperature': 27,
                'humidity': 70,
                'soil_ph': 6.5,
                'nitrogen': 60,
                'phosphorus': 45,
                'potassium': 45,
                'crop_type': 'Rice',
                'season': 'Kharif',
                'area_hectares': 2
            }
        },
        {
            'name': 'Average Conditions - Wheat',
            'data': {
                'rainfall': 650,
                'temperature': 22,
                'humidity': 60,
                'soil_ph': 6.8,
                'nitrogen': 45,
                'phosphorus': 38,
                'potassium': 40,
                'crop_type': 'Wheat',
                'season': 'Rabi',
                'area_hectares': 1.5
            }
        },
        {
            'name': 'Challenging Conditions - Cotton',
            'data': {
                'rainfall': 400,
                'temperature': 35,
                'humidity': 45,
                'soil_ph': 7.8,
                'nitrogen': 30,
                'phosphorus': 25,
                'potassium': 30,
                'crop_type': 'Cotton',
                'season': 'Kharif',
                'area_hectares': 3
            }
        }
    ]
    return jsonify({'samples': samples})

@app.route('/api/recommendations/optimize', methods=['POST'])
def optimize_recommendations():
    """
    Get optimized recommendations for maximum yield
    """
    try:
        data = request.json
        current_yield = data.get('current_yield', 30)
        
        # Generate optimization plan
        optimization_plan = {
            'target_yield': round(current_yield * 1.15, 2),
            'timeline': '3-4 months',
            'steps': [
                {
                    'week': '1-2',
                    'action': 'Soil Testing',
                    'details': 'Conduct comprehensive soil analysis for pH, NPK, and micronutrients'
                },
                {
                    'week': '3-4',
                    'action': 'Soil Preparation',
                    'details': 'Add recommended amendments based on soil test results'
                },
                {
                    'week': '5-8',
                    'action': 'Implement Irrigation Plan',
                    'details': 'Set up drip irrigation or optimize watering schedule'
                },
                {
                    'week': '9-12',
                    'action': 'Monitor and Adjust',
                    'details': 'Regular monitoring of crop health and adjusting inputs'
                }
            ],
            'investment_required': {
                'low': '₹5,000 - ₹10,000 per hectare',
                'medium': '₹10,000 - ₹20,000 per hectare',
                'high': '₹20,000 - ₹35,000 per hectare'
            }
        }
        
        return jsonify(optimization_plan)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/historical-data', methods=['GET'])
def get_historical_data():
    """Get historical yield data for visualization"""
    # Simulated historical data
    historical_data = {
        'years': [2019, 2020, 2021, 2022, 2023],
        'average_yields': [28.5, 30.2, 29.8, 31.5, 32.8],
        'rainfall': [750, 820, 680, 900, 850],
        'region': 'Odisha'
    }
    return jsonify(historical_data)

if __name__ == '__main__':
    print("Starting Crop Yield Prediction API Server...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
