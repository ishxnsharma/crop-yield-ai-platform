#!/usr/bin/env python3
"""
Standalone Model Training Script for Crop Yield Prediction
Can be run independently once Python and dependencies are installed
"""

import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'pandas': 'pandas',
        'numpy': 'numpy', 
        'sklearn': 'scikit-learn',
        'joblib': 'joblib'
    }
    
    missing_packages = []
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall them using:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False
    return True

def train_model():
    """Main training function"""
    print("=" * 50)
    print("CROP YIELD PREDICTION MODEL TRAINING")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies first!")
        return False
    
    # Import required libraries
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
    import joblib
    
    # Check for data file
    data_path = 'data/sample_crop_data.csv'
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return False
    
    print("\n1. Loading data...")
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} samples with {len(df.columns)} columns")
    
    # Encode categorical variables
    print("\n2. Encoding categorical variables...")
    le_crop = LabelEncoder()
    le_region = LabelEncoder()
    
    df['crop_type_encoded'] = le_crop.fit_transform(df['crop_type'])
    df['region_encoded'] = le_region.fit_transform(df['region'])
    
    print(f"   Encoded {len(le_crop.classes_)} crop types")
    print(f"   Encoded {len(le_region.classes_)} regions")
    
    # Prepare features
    print("\n3. Preparing features...")
    feature_columns = [
        'crop_type_encoded', 'region_encoded', 'temperature', 'rainfall',
        'humidity', 'soil_ph', 'nitrogen', 'phosphorus', 'potassium',
        'pesticide_usage', 'irrigation_hours'
    ]
    
    X = df[feature_columns]
    y = df['yield_per_hectare']
    print(f"   Feature matrix shape: {X.shape}")
    print(f"   Target variable shape: {y.shape}")
    
    # Split data
    print("\n4. Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Testing samples: {len(X_test)}")
    
    # Scale features
    print("\n5. Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\n6. Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    print("   Model training completed!")
    
    # Evaluate model
    print("\n7. Evaluating model performance...")
    y_pred = model.predict(X_test_scaled)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"   RMSE: {rmse:.2f}")
    print(f"   MAE: {mae:.2f}")
    print(f"   R² Score: {r2:.4f}")
    
    # Cross-validation
    print("\n8. Performing cross-validation...")
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, 
                               scoring='r2')
    print(f"   CV R² Scores: {cv_scores}")
    print(f"   Average CV R²: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Feature importance
    print("\n9. Analyzing feature importance...")
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("   Top 5 most important features:")
    for idx, row in feature_importance.head().iterrows():
        print(f"   - {row['feature']}: {row['importance']:.3f}")
    
    # Save models
    print("\n10. Saving model files...")
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model, 'models/crop_yield_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(le_crop, 'models/crop_encoder.pkl')
    joblib.dump(le_region, 'models/region_encoder.pkl')
    joblib.dump(feature_columns, 'models/feature_columns.pkl')
    
    print("    ✓ Model files saved successfully!")
    
    # Display supported crops and regions
    print("\n" + "=" * 50)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"\nSupported Crops: {', '.join(le_crop.classes_)}")
    print(f"Supported Regions: {', '.join(le_region.classes_)}")
    print("\nModel is ready for predictions!")
    
    # Save training results
    with open('models/training_results.txt', 'w') as f:
        f.write(f"Model Training Results\n")
        f.write(f"=====================\n")
        f.write(f"Date: {pd.Timestamp.now()}\n")
        f.write(f"R² Score: {r2:.4f}\n")
        f.write(f"RMSE: {rmse:.2f}\n")
        f.write(f"MAE: {mae:.2f}\n")
        f.write(f"\nSupported Crops: {', '.join(le_crop.classes_)}\n")
        f.write(f"Supported Regions: {', '.join(le_region.classes_)}\n")
    
    return True

if __name__ == "__main__":
    success = train_model()
    sys.exit(0 if success else 1)
