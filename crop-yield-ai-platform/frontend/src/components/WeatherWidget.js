import React, { useState, useEffect } from 'react';
import axios from 'axios';

const WeatherWidget = () => {
  const [weatherData, setWeatherData] = useState(null);
  const [soilData, setSoilData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEnvironmentalData();
  }, []);

  const fetchEnvironmentalData = async () => {
    try {
      const [weatherRes, soilRes] = await Promise.all([
        axios.get('/api/weather'),
        axios.get('/api/soil')
      ]);
      
      setWeatherData(weatherRes.data);
      setSoilData(soilRes.data);
    } catch (error) {
      console.error('Error fetching environmental data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="weather-widget">
        <div className="loading">Loading environmental data...</div>
      </div>
    );
  }

  return (
    <>
      <div className="weather-widget">
        <h3>🌤️ Current Weather</h3>
        {weatherData && (
          <>
            <p className="location">{weatherData.location}</p>
            <div className="weather-info">
              <div className="weather-item">
                <span>Temperature</span>
                <span>{weatherData.temperature}°C</span>
              </div>
              <div className="weather-item">
                <span>Humidity</span>
                <span>{weatherData.humidity}%</span>
              </div>
              <div className="weather-item">
                <span>Rainfall</span>
                <span>{weatherData.rainfall} mm</span>
              </div>
            </div>
          </>
        )}
      </div>

      <div className="weather-widget" style={{ marginTop: '1rem' }}>
        <h3>🌱 Soil Health</h3>
        {soilData && (
          <>
            <p className="location">{soilData.location}</p>
            <div className="weather-info">
              <div className="weather-item">
                <span>pH Level</span>
                <span>{soilData.ph}</span>
              </div>
              <div className="weather-item">
                <span>Nitrogen</span>
                <span>{soilData.nitrogen} kg/ha</span>
              </div>
              <div className="weather-item">
                <span>Phosphorus</span>
                <span>{soilData.phosphorus} kg/ha</span>
              </div>
              <div className="weather-item">
                <span>Potassium</span>
                <span>{soilData.potassium} kg/ha</span>
              </div>
            </div>
            <p className="last-tested">Last tested: {soilData.last_tested}</p>
          </>
        )}
      </div>

      <div className="weather-widget" style={{ marginTop: '1rem', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <h3 style={{ color: 'white' }}>💡 Quick Tips</h3>
        <ul className="tips-list">
          <li>Monitor weather patterns daily for optimal irrigation</li>
          <li>Test soil every season for accurate nutrient management</li>
          <li>Keep records of all agricultural inputs for better predictions</li>
          <li>Consult local agricultural officers for region-specific advice</li>
        </ul>
      </div>

      <style jsx>{`
        .location {
          color: #718096;
          font-size: 0.9rem;
          margin-bottom: 1rem;
        }

        .last-tested {
          margin-top: 1rem;
          font-size: 0.85rem;
          color: #718096;
          text-align: center;
        }

        .tips-list {
          list-style: none;
          padding: 0;
        }

        .tips-list li {
          padding: 0.5rem 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.2);
          font-size: 0.9rem;
          line-height: 1.4;
        }

        .tips-list li:last-child {
          border-bottom: none;
        }

        .loading {
          text-align: center;
          padding: 1rem;
          color: #718096;
        }
      `}</style>
    </>
  );
};

export default WeatherWidget;
