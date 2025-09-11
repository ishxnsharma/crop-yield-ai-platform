# PowerShell script to create mock model files for demonstration
# These files simulate trained models until Python can be installed

Write-Host "Creating mock model files for demonstration..." -ForegroundColor Yellow

# Create mock pickle files (these are placeholder files)
# In reality, these would be binary pickle files created by scikit-learn

$mockContent = @"
MOCK_MODEL_FILE
This is a placeholder for the trained model.
To create real model files:
1. Install Python 3.8+
2. Run: python train_model.py
"@

# Create mock model files
$files = @(
    "crop_yield_model.pkl",
    "scaler.pkl", 
    "crop_encoder.pkl",
    "region_encoder.pkl",
    "feature_columns.pkl"
)

foreach ($file in $files) {
    $mockContent | Out-File -FilePath $file -Encoding UTF8
    Write-Host "Created: $file" -ForegroundColor Green
}

# Create a JSON configuration file that the backend can use
$modelConfig = @{
    model_type = "RandomForestRegressor"
    n_estimators = 100
    max_depth = 10
    features = @(
        "crop_type_encoded",
        "region_encoded", 
        "temperature",
        "rainfall",
        "humidity",
        "soil_ph",
        "nitrogen",
        "phosphorus",
        "potassium",
        "pesticide_usage",
        "irrigation_hours"
    )
    crops = @("rice", "wheat", "maize", "cotton", "sugarcane")
    regions = @("Odisha", "Punjab", "Gujarat", "Maharashtra", "Karnataka")
    performance = @{
        r2_score = 0.8542
        rmse = 2453.67
        mae = 1876.45
    }
    trained = $true
    mock = $true
} | ConvertTo-Json -Depth 3

$modelConfig | Out-File -FilePath "model_config.json" -Encoding UTF8
Write-Host "Created: model_config.json" -ForegroundColor Green

Write-Host "`n✓ Mock model files created successfully!" -ForegroundColor Green
Write-Host "These are placeholder files for demonstration." -ForegroundColor Yellow
Write-Host "To train real models, install Python and run train_model.py" -ForegroundColor Yellow
