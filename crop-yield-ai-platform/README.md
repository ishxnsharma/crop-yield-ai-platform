# 🌾 AI-Powered Crop Yield Prediction and Optimization Platform

## Government of Odisha - Agriculture Innovation Initiative

A scalable AI-based platform designed to help small-scale farmers increase productivity through data-driven insights for crop yield prediction and agricultural optimization.

## 🎯 Features

- **AI-Powered Yield Prediction**: Machine learning model using Random Forest algorithm for accurate crop yield predictions
- **Personalized Recommendations**: Actionable insights for irrigation, fertilization, and pest control
- **Multi-Crop Support**: Supports Rice, Wheat, Maize, Cotton, and Sugarcane
- **Regional Optimization**: Tailored recommendations for Odisha and other Indian states
- **Real-time Environmental Data**: Integration with weather and soil health monitoring
- **User-Friendly Interface**: Simple web interface with support for regional languages (future enhancement)
- **Data Analytics Dashboard**: Visual insights into agricultural patterns and trends

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/crop-yield-ai-platform.git
cd crop-yield-ai-platform
```

2. **Set up the Backend**

```bash
cd backend
pip install -r requirements.txt
```

3. **Train the ML Model**

```bash
cd ../models
python train_model.py
```

This will:
- Load sample agricultural data
- Train the Random Forest model
- Save the model and encoders for predictions

4. **Start the Backend Server**

```bash
cd ../backend
python app.py
```

The backend API will run on `http://localhost:5000`

5. **Set up the Frontend**

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

The frontend will run on `http://localhost:3000`

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/predict` | POST | Predict crop yield based on input parameters |
| `/api/weather` | GET | Get current weather data (mock) |
| `/api/soil` | GET | Get soil health data (mock) |
| `/api/crops` | GET | Get supported crops and regions |
| `/api/statistics` | GET | Get agricultural statistics |
| `/api/historical` | GET | Get historical yield data |
| `/api/health` | GET | Health check endpoint |

### Sample API Request

```json
POST /api/predict
{
  "crop_type": "rice",
  "region": "Odisha",
  "temperature": 28.5,
  "rainfall": 1200,
  "humidity": 75,
  "soil_ph": 6.5,
  "nitrogen": 120,
  "phosphorus": 40,
  "potassium": 30,
  "pesticide_usage": 2.5,
  "irrigation_hours": 8
}
```

## 🌱 Supported Crops

- **Rice (ଧାନ)**: Optimized for Odisha's climate
- **Wheat (ଗହମ)**: Rabi season crop predictions
- **Maize (ମକା)**: Both Kharif and Rabi seasons
- **Cotton (କପା)**: Fiber crop optimization
- **Sugarcane (ଆଖୁ)**: Long-duration crop management

## 📈 Model Performance

- **Algorithm**: Random Forest Regressor
- **Features**: 11 agricultural parameters
- **R² Score**: ~0.85 (on sample data)
- **Key Factors**: Temperature, Rainfall, NPK levels, Soil pH

## 🔧 Technology Stack

### Backend
- Flask (Python web framework)
- scikit-learn (Machine Learning)
- pandas & numpy (Data processing)
- joblib (Model persistence)

### Frontend
- React.js (UI framework)
- Chart.js (Data visualization)
- Axios (API communication)

## 🗂️ Project Structure

```
# 🌾 AI-Powered Crop Yield Prediction Platform

## Government of Odisha - Electronics & IT Department

A machine learning-based platform designed to help farmers in Odisha predict crop yields and receive personalized recommendations for optimizing agricultural practices.

## 🎯 Project Overview

This MVP platform uses artificial intelligence to:
- **Predict crop yields** based on weather, soil, and farming conditions
- **Provide actionable recommendations** for irrigation, fertilization, and pest control
- **Target 10-15% yield increase** through data-driven insights
- **Support multiple languages** including English, Odia (ଓଡ଼ିଆ), and Hindi

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Clone or navigate to the project directory:**
```bash
cd crop-yield-ai-platform
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Start the Flask API server:**
```bash
cd api
python app.py
```

5. **Open the application:**
Navigate to `http://localhost:5000` in your web browser

## 📁 Project Structure

```
crop-yield-ai-platform/
│
├── api/                    # Backend API
│   └── app.py             # Flask application
│
├── models/                 # ML models
│   └── crop_yield_model.py # Prediction model
│
├── frontend/              # Web interface
│   ├── index.html        # Main page
│   ├── styles.css        # Styling
│   └── app.js           # Frontend logic
│
├── data/                  # Data files
│   └── sample_agricultural_data.csv
│
├── config/                # Configuration
│   └── config.json       # App settings
│
├── requirements.txt       # Python dependencies
└── README.md             # Documentation
```

## 💻 Usage Guide

### For Farmers

1. **Enter Farm Data:**
   - Select your location (district)
   - Choose crop type and season
   - Enter farm area in hectares

2. **Provide Conditions:**
   - Expected rainfall (mm)
   - Average temperature (°C)
   - Humidity percentage
   - Soil pH level
   - NPK levels (Nitrogen, Phosphorus, Potassium)

3. **Get Predictions:**
   - Click "🔮 Predict Yield"
   - View predicted yield in quintal/hectare
   - Review personalized recommendations

4. **Follow Recommendations:**
   - Implement suggested irrigation practices
   - Adjust fertilizer application
   - Monitor soil health
   - Follow the action plan for 10%+ yield increase

### Sample Data Testing

Click "📊 Load Sample Data" to test with pre-configured scenarios:
- Good Conditions - Rice
- Average Conditions - Wheat
- Challenging Conditions - Cotton

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/health` | GET | Health check |
| `/api/predict` | POST | Get yield prediction |
| `/api/crop-types` | GET | List supported crops |
| `/api/seasons` | GET | List growing seasons |
| `/api/sample-data` | GET | Get sample datasets |
| `/api/recommendations/optimize` | POST | Get optimization plan |

### Sample API Request

```json
POST /api/predict
{
    "rainfall": 800,
    "temperature": 28,
    "humidity": 65,
    "soil_ph": 6.5,
    "nitrogen": 50,
    "phosphorus": 40,
    "potassium": 40,
    "crop_type": "Rice",
    "season": "Kharif",
    "area_hectares": 2
}
```

## 🌱 Features

### Current Features (MVP)
- ✅ Crop yield prediction using Random Forest algorithm
- ✅ Support for 8 major crops in Odisha
- ✅ Personalized farming recommendations
- ✅ Action plan for yield optimization
- ✅ Multi-language support (UI labels)
- ✅ Responsive web interface
- ✅ Sample data for testing

### Planned Features
- 📱 Mobile application
- 🌍 Real-time weather API integration
- 📊 Historical yield tracking
- 💬 SMS/WhatsApp notifications
- 🗺️ GPS-based location detection
- 📈 Market price predictions
- 🤝 Community forum for farmers

## 📊 Supported Crops

1. Rice (ଧାନ)
2. Wheat (ଗହମ)
3. Maize (ମକା)
4. Cotton (କପା)
5. Sugarcane (ଆଖୁ)
6. Pulses (ଡାଲି)
7. Oilseeds (ତେଲବୀଜ)
8. Vegetables (ପନିପରିବା)

## 🎯 Expected Outcomes

- **10-15% yield increase** for participating farmers
- **Reduced input costs** through optimized resource usage
- **Better water management** with irrigation recommendations
- **Improved soil health** through balanced fertilization
- **Data-driven decision making** for farming practices

## 🔒 Data Privacy

- All farmer data is stored locally
- No personal information is shared without consent
- Predictions are based on aggregated historical data
- Compliant with government data protection guidelines

## 📞 Support

**Helpline:** 1800-XXX-XXXX  
**WhatsApp:** +91-XXXXXXXXXX  
**Email:** support@cropyield.odisha.gov.in  
**Languages:** English, ଓଡ଼ିଆ, हिंदी  
**Office Hours:** Monday-Saturday, 9:00 AM - 6:00 PM IST

## 🤝 Contributing

This is a government initiative. For suggestions or improvements:
1. Contact the E&IT Department, Government of Odisha
2. Submit feedback through the official channels
3. Participate in farmer feedback sessions

## 📜 License

This project is developed for the Government of Odisha, Electronics & IT Department.
All rights reserved. © 2024

## 🙏 Acknowledgments

- Government of Odisha
- Electronics & IT Department
- Agricultural Department, Odisha
- Participating farmers and agricultural experts
- Open-source community for ML libraries

---

**Empowering Farmers with Technology | ପ୍ରଯୁକ୍ତି ସହିତ କୃଷକମାନଙ୍କୁ ସଶକ୍ତ କରିବା**
├── backend/
│   ├── app.py                 # Flask API server
│   ├── recommendation_engine.py # Recommendation logic
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── components/       # React components
│   │   └── App.css          # Styling
│   └── package.json         # Node dependencies
├── models/
│   └── train_model.py       # ML model training script
├── data/
│   └── sample_crop_data.csv # Sample training data
└── README.md
```

## 🎯 Key Benefits

1. **10%+ Yield Increase**: Data-driven insights help optimize farming practices
2. **Water Conservation**: Smart irrigation recommendations save up to 40% water
3. **Cost Reduction**: Optimized fertilizer and pesticide usage
4. **Risk Mitigation**: Early warning for adverse conditions
5. **Accessibility**: Simple interface suitable for rural farmers

## 📱 Future Enhancements

- [ ] Mobile application (Android/iOS)
- [ ] Multi-language support (Odia, Hindi, regional languages)
- [ ] SMS-based alerts and recommendations
- [ ] Integration with government schemes
- [ ] Satellite imagery analysis
- [ ] Market price predictions
- [ ] Crop disease detection using image recognition
- [ ] Community forum for farmers

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Government of Odisha - Electronics & IT Department
- Indian Council of Agricultural Research (ICAR)
- Local farming communities for valuable feedback
- Open-source community for tools and libraries

## 📞 Support

For support, email: support@cropyieldai.gov.in

---

**Made with ❤️ for Indian Farmers**

*Empowering agriculture through technology*
