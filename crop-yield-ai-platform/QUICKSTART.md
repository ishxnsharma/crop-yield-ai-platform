# 🚀 Quick Start Guide - Crop Yield AI Platform

## Prerequisites Installation

### 1. Install Python (3.8 or higher)
- Download from: https://www.python.org/downloads/
- **Important**: Check ✅ "Add Python to PATH" during installation

### 2. Install Node.js (14 or higher)
- Download from: https://nodejs.org/
- This will also install npm

## One-Click Setup

After installing prerequisites, simply run:

```batch
setup.bat
```

This will automatically:
1. Install all Python dependencies
2. Train the ML model with sample data
3. Install all frontend dependencies

## Running the Application

### Option 1: Using Batch Scripts

1. **Start Backend Server**
   - Double-click `start-backend.bat`
   - Backend will run on http://localhost:5000

2. **Start Frontend (in new window)**
   - Double-click `start-frontend.bat`
   - Frontend will open at http://localhost:3000

### Option 2: Manual Commands

1. **Start Backend**
```bash
cd backend
python app.py
```

2. **Start Frontend (new terminal)**
```bash
cd frontend
npm start
```

## 🎯 Testing the Application

1. Open http://localhost:3000 in your browser
2. Navigate to "Predict Yield" tab
3. Enter sample data:
   - Crop: Rice
   - Region: Odisha
   - Temperature: 28.5°C
   - Rainfall: 1200mm
   - Humidity: 75%
   - Soil pH: 6.5
   - Nitrogen: 120 kg/ha
   - Phosphorus: 40 kg/ha
   - Potassium: 30 kg/ha
   - Pesticide: 2.5 kg/ha
   - Irrigation: 8 hours
4. Click "Predict Crop Yield"
5. View predictions and recommendations

## 📊 Key Features to Explore

1. **Dashboard**: View agricultural statistics and trends
2. **Yield Prediction**: Get AI-powered crop yield forecasts
3. **Recommendations**: Receive personalized farming advice
4. **Weather Widget**: Check current environmental conditions
5. **Soil Health**: Monitor soil nutrient levels

## 🔧 Troubleshooting

### Python not found
- Ensure Python is installed and added to PATH
- Try using `py` instead of `python` command

### npm not found
- Install Node.js from https://nodejs.org/
- Restart terminal after installation

### Port already in use
- Backend: Change port in `backend/app.py` (line 184)
- Frontend: Set PORT environment variable

### Module not found errors
- Run `pip install -r requirements.txt` in backend folder
- Run `npm install` in frontend folder

## 📱 Access from Mobile

To access from mobile devices on same network:
1. Find your computer's IP address: `ipconfig`
2. Access: `http://[YOUR-IP]:3000`

## 🌟 Next Steps

1. **Add Real Weather API**
   - Sign up at OpenWeatherMap
   - Add API key to backend

2. **Connect Real Database**
   - Set up PostgreSQL/MySQL
   - Update backend configuration

3. **Deploy to Cloud**
   - Consider Heroku, AWS, or DigitalOcean
   - Update CORS settings for production

## 📞 Support

For issues or questions:
- Check README.md for detailed documentation
- Review API endpoints in backend/app.py
- Examine recommendation logic in backend/recommendation_engine.py

---

**Happy Farming! 🌾**
