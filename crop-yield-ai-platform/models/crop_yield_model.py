"""
Crop Yield Prediction Model
Simple MVP implementation using Random Forest and Neural Network
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

class CropYieldPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.is_trained = False
        
    def prepare_features(self, data):
        """Prepare features for training/prediction"""
        # Feature engineering for agricultural data
        features = pd.DataFrame()
        
        # Basic features
        features['rainfall'] = data.get('rainfall', 0)  # mm
        features['temperature'] = data.get('temperature', 25)  # Celsius
        features['humidity'] = data.get('humidity', 60)  # percentage
        features['soil_ph'] = data.get('soil_ph', 6.5)
        features['nitrogen'] = data.get('nitrogen', 50)  # kg/ha
        features['phosphorus'] = data.get('phosphorus', 40)  # kg/ha
        features['potassium'] = data.get('potassium', 40)  # kg/ha
        features['crop_type_code'] = data.get('crop_type_code', 0)  # encoded crop type
        features['season_code'] = data.get('season_code', 0)  # 0: Kharif, 1: Rabi, 2: Summer
        features['area_hectares'] = data.get('area_hectares', 1)
        
        # Derived features
        features['npk_ratio'] = (features['nitrogen'] + features['phosphorus'] + features['potassium']) / 3
        features['temp_humidity_index'] = features['temperature'] * features['humidity'] / 100
        
        return features
    
    def train(self, training_data):
        """Train the model with historical data"""
        if isinstance(training_data, str):
            # Load from CSV file
            df = pd.read_csv(training_data)
        else:
            df = training_data
            
        # Prepare features
        X = self.prepare_features(df)
        y = df['yield_quintal_per_hectare']
        
        # Store feature columns for consistency
        self.feature_columns = X.columns.tolist()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.is_trained = True
        
        return {
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2_score': r2,
            'feature_importance': dict(zip(self.feature_columns, self.model.feature_importances_))
        }
    
    def predict(self, input_data):
        """Predict crop yield for given conditions"""
        if not self.is_trained:
            raise ValueError("Model not trained yet. Please train the model first.")
        
        # Prepare features
        features = self.prepare_features(input_data)
        
        # Ensure same columns as training
        features = features[self.feature_columns]
        
        # Scale and predict
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return prediction
    
    def get_recommendations(self, input_data, predicted_yield):
        """Generate farming recommendations based on predictions"""
        recommendations = []
        
        # Irrigation recommendations
        rainfall = input_data.get('rainfall', 0)
        if rainfall < 500:
            recommendations.append({
                'category': 'Irrigation',
                'priority': 'High',
                'action': 'Increase irrigation frequency',
                'details': f'Current rainfall ({rainfall}mm) is below optimal. Consider drip irrigation or scheduled watering.'
            })
        
        # Soil health recommendations
        soil_ph = input_data.get('soil_ph', 6.5)
        if soil_ph < 6.0:
            recommendations.append({
                'category': 'Soil Health',
                'priority': 'Medium',
                'action': 'Add lime to increase soil pH',
                'details': f'Current pH ({soil_ph}) is acidic. Add agricultural lime to reach optimal pH (6.0-7.0).'
            })
        elif soil_ph > 7.5:
            recommendations.append({
                'category': 'Soil Health',
                'priority': 'Medium',
                'action': 'Add organic matter or sulfur',
                'details': f'Current pH ({soil_ph}) is alkaline. Add organic matter or sulfur to lower pH.'
            })
        
        # Nutrient recommendations
        nitrogen = input_data.get('nitrogen', 50)
        phosphorus = input_data.get('phosphorus', 40)
        potassium = input_data.get('potassium', 40)
        
        if nitrogen < 40:
            recommendations.append({
                'category': 'Fertilization',
                'priority': 'High',
                'action': 'Increase nitrogen fertilizer',
                'details': f'Nitrogen levels ({nitrogen} kg/ha) are low. Apply urea or ammonium nitrate.'
            })
        
        if phosphorus < 30:
            recommendations.append({
                'category': 'Fertilization',
                'priority': 'Medium',
                'action': 'Add phosphorus fertilizer',
                'details': f'Phosphorus levels ({phosphorus} kg/ha) are low. Apply DAP or superphosphate.'
            })
        
        # Temperature and season recommendations
        temperature = input_data.get('temperature', 25)
        if temperature > 35:
            recommendations.append({
                'category': 'Climate Management',
                'priority': 'High',
                'action': 'Implement heat stress management',
                'details': 'Use shade nets, mulching, and increase watering during peak heat hours.'
            })
        
        # Yield optimization suggestion
        if predicted_yield < 30:  # Below average yield
            recommendations.append({
                'category': 'Yield Optimization',
                'priority': 'High',
                'action': 'Review farming practices',
                'details': 'Consider crop rotation, improved seeds, and integrated pest management.'
            })
        
        return recommendations
    
    def save_model(self, filepath='models/trained_model.pkl'):
        """Save the trained model"""
        if not self.is_trained:
            raise ValueError("Model not trained yet.")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_columns': self.feature_columns
            }, f)
    
    def load_model(self, filepath='models/trained_model.pkl'):
        """Load a trained model"""
        with open(filepath, 'rb') as f:
            saved_data = pickle.load(f)
            self.model = saved_data['model']
            self.scaler = saved_data['scaler']
            self.feature_columns = saved_data['feature_columns']
            self.is_trained = True

# Utility function for quick predictions
def quick_predict(crop_data):
    """Quick prediction function for API use"""
    predictor = CropYieldPredictor()
    
    # Check if model exists, otherwise use default predictions
    model_path = 'models/trained_model.pkl'
    if os.path.exists(model_path):
        predictor.load_model(model_path)
        prediction = predictor.predict(crop_data)
    else:
        # Return a simulated prediction for MVP
        base_yield = 35  # quintal per hectare baseline
        
        # Simple rule-based adjustments
        rainfall_factor = min(crop_data.get('rainfall', 800) / 800, 1.5)
        nutrient_factor = (crop_data.get('nitrogen', 50) + 
                          crop_data.get('phosphorus', 40) + 
                          crop_data.get('potassium', 40)) / 130
        
        prediction = base_yield * rainfall_factor * nutrient_factor
    
    recommendations = predictor.get_recommendations(crop_data, prediction)
    
    return {
        'predicted_yield': round(prediction, 2),
        'unit': 'quintal/hectare',
        'recommendations': recommendations
    }

if __name__ == "__main__":
    # Test the model with sample data
    sample_data = {
        'rainfall': 650,
        'temperature': 28,
        'humidity': 65,
        'soil_ph': 6.8,
        'nitrogen': 45,
        'phosphorus': 38,
        'potassium': 42,
        'crop_type_code': 1,
        'season_code': 0,
        'area_hectares': 2
    }
    
    result = quick_predict(sample_data)
    print(f"Predicted Yield: {result['predicted_yield']} {result['unit']}")
    print("\nRecommendations:")
    for rec in result['recommendations']:
        print(f"- {rec['category']}: {rec['action']}")
