import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';
import Dashboard from './components/Dashboard';
import WeatherWidget from './components/WeatherWidget';

function App() {
  const [activeTab, setActiveTab] = useState('predict');
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [supportedData, setSupportedData] = useState({ crops: [], regions: [] });

  useEffect(() => {
    // Fetch supported crops and regions
    fetchSupportedData();
  }, []);

  const fetchSupportedData = async () => {
    try {
      const response = await axios.get('/api/crops');
      setSupportedData(response.data);
    } catch (error) {
      console.error('Error fetching supported data:', error);
    }
  };

  const handlePrediction = async (formData) => {
    setLoading(true);
    try {
      const response = await axios.post('/api/predict', formData);
      setPredictionResult(response.data);
      setActiveTab('results');
    } catch (error) {
      console.error('Prediction error:', error);
      alert('Error making prediction. Please check your inputs.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌾 AI-Powered Crop Yield Prediction Platform</h1>
        <p>Smart Farming Solutions for Odisha Farmers</p>
      </header>

      <nav className="nav-tabs">
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button 
          className={activeTab === 'predict' ? 'active' : ''}
          onClick={() => setActiveTab('predict')}
        >
          Predict Yield
        </button>
        <button 
          className={activeTab === 'results' ? 'active' : ''}
          onClick={() => setActiveTab('results')}
          disabled={!predictionResult}
        >
          Results & Recommendations
        </button>
      </nav>

      <div className="content-container">
        <div className="main-content">
          {activeTab === 'dashboard' && (
            <Dashboard />
          )}
          
          {activeTab === 'predict' && (
            <PredictionForm 
              onSubmit={handlePrediction}
              loading={loading}
              supportedData={supportedData}
            />
          )}
          
          {activeTab === 'results' && predictionResult && (
            <ResultsDisplay 
              result={predictionResult}
            />
          )}
        </div>
        
        <div className="sidebar">
          <WeatherWidget />
        </div>
      </div>

      <footer className="App-footer">
        <p>© 2024 Crop Yield AI Platform | Government of Odisha Initiative</p>
        <p>Empowering farmers with data-driven insights</p>
      </footer>
    </div>
  );
}

export default App;
