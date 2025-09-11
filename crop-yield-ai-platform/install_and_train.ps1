# PowerShell script to help install Python and train the model

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Crop Yield AI - Model Training Assistant" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonInstalled = $false
$pythonCmd = ""

# Try different Python commands
$pythonCommands = @("python", "py", "python3")
foreach ($cmd in $pythonCommands) {
    try {
        $version = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonInstalled = $true
            $pythonCmd = $cmd
            Write-Host "✓ Python found: $version" -ForegroundColor Green
            break
        }
    } catch {
        # Continue to next command
    }
}

if (-not $pythonInstalled) {
    Write-Host "❌ Python is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Python:" -ForegroundColor Yellow
    Write-Host "1. Visit: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. Download Python 3.8 or higher" -ForegroundColor White
    Write-Host "3. During installation, CHECK the box 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "4. After installation, restart PowerShell and run this script again" -ForegroundColor White
    Write-Host ""
    
    # Offer to open Python download page
    $openBrowser = Read-Host "Would you like to open the Python download page? (Y/N)"
    if ($openBrowser -eq 'Y' -or $openBrowser -eq 'y') {
        Start-Process "https://www.python.org/downloads/"
    }
    
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "Installing required Python packages..." -ForegroundColor Yellow

# Navigate to project root
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

# Install requirements
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
& $pythonCmd -m pip install --upgrade pip
& $pythonCmd -m pip install pandas numpy scikit-learn joblib flask flask-cors requests python-dotenv matplotlib seaborn

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Try running: $pythonCmd -m pip install -r backend/requirements.txt" -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""

# Train the model
Write-Host "Training the ML model..." -ForegroundColor Yellow
Write-Host "This will use the sample data in data/sample_crop_data.csv" -ForegroundColor Cyan
Write-Host ""

# Navigate to models directory
Set-Location models

# Run the training script
& $pythonCmd train_model.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ MODEL TRAINING COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Model files created:" -ForegroundColor Cyan
    Write-Host "  • crop_yield_model.pkl" -ForegroundColor White
    Write-Host "  • scaler.pkl" -ForegroundColor White
    Write-Host "  • crop_encoder.pkl" -ForegroundColor White
    Write-Host "  • region_encoder.pkl" -ForegroundColor White
    Write-Host "  • feature_columns.pkl" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Start backend: Run start-backend.bat" -ForegroundColor White
    Write-Host "2. Start frontend: Run start-frontend.bat" -ForegroundColor White
    Write-Host "3. Open browser: http://localhost:3000" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Model training failed" -ForegroundColor Red
    Write-Host "Check the error messages above for details" -ForegroundColor Yellow
    
    # Try the standalone script
    Write-Host ""
    Write-Host "Trying standalone training script..." -ForegroundColor Yellow
    Set-Location ..
    & $pythonCmd train_model_standalone.py
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
