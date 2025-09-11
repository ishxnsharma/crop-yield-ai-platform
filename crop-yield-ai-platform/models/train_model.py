import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import os

def load_and_preprocess_data(data_path):
    """Load and preprocess the agricultural data"""
    df = pd.read_csv(data_path)
    
    # Encode categorical variables
    le_crop = LabelEncoder()
    le_region = LabelEncoder()
    
    df['crop_type_encoded'] = le_crop.fit_transform(df['crop_type'])
    df['region_encoded'] = le_region.fit_transform(df['region'])
    
    # Save encoders for later use
    joblib.dump(le_crop, 'models/crop_encoder.pkl')
    joblib.dump(le_region, 'models/region_encoder.pkl')
    
    return df, le_crop, le_region

def prepare_features(df):
    """Prepare feature matrix and target variable"""
    feature_columns = [
        'crop_type_encoded', 'region_encoded', 'temperature', 'rainfall',
        'humidity', 'soil_ph', 'nitrogen', 'phosphorus', 'potassium',
        'pesticide_usage', 'irrigation_hours'
    ]
    
    X = df[feature_columns]
    y = df['yield_per_hectare']
    
    return X, y, feature_columns

def train_model(X, y):
    """Train Random Forest model for crop yield prediction"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("Model Performance Metrics:")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    print(f"R² Score: {r2:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Most Important Features:")
    print(feature_importance.head())
    
    return model, scaler

def save_model(model, scaler, feature_columns):
    """Save trained model and preprocessors"""
    joblib.dump(model, 'models/crop_yield_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(feature_columns, 'models/feature_columns.pkl')
    print("\nModel and preprocessors saved successfully!")

if __name__ == "__main__":
    # Check if data file exists
    data_path = 'data/sample_crop_data.csv'
    
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        exit(1)
    
    # Load and preprocess data
    df, le_crop, le_region = load_and_preprocess_data(data_path)
    
    # Prepare features
    X, y, feature_columns = prepare_features(df)
    
    # Train model
    model, scaler = train_model(X, y)
    
    # Save model
    save_model(model, scaler, feature_columns)
    
    print("\nModel training completed successfully!")
    print(f"Crops supported: {list(le_crop.classes_)}")
    print(f"Regions supported: {list(le_region.classes_)}")
