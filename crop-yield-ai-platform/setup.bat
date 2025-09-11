@echo off
echo ========================================
echo AI Crop Yield Prediction Platform Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo Training ML model...
cd ../models
python train_model.py
if %errorlevel% neq 0 (
    echo Failed to train model
    pause
    exit /b 1
)

echo.
echo Installing frontend dependencies...
cd ../frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application:
echo 1. Start backend: cd backend && python app.py
echo 2. Start frontend: cd frontend && npm start
echo.
pause
