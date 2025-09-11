@echo off
echo.
echo ========================================
echo AI CROP YIELD PREDICTION PLATFORM
echo Government of Odisha - E&IT Department  
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt -q

REM Start the Flask server
echo.
echo ========================================
echo Starting Flask API Server...
echo ========================================
echo.
echo The application will be available at:
echo.
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd api
python app.py

pause
