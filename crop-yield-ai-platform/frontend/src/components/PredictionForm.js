import React, { useState } from 'react';

const PredictionForm = ({ onSubmit, loading, supportedData }) => {
  const [formData, setFormData] = useState({
    crop_type: 'rice',
    region: 'Odisha',
    temperature: 28.5,
    rainfall: 1200,
    humidity: 75,
    soil_ph: 6.5,
    nitrogen: 120,
    phosphorus: 40,
    potassium: 30,
    pesticide_usage: 2.5,
    irrigation_hours: 8
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: parseFloat(value) || value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="prediction-form">
      <h2>Enter Agricultural Data for Yield Prediction</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="crop_type">Crop Type</label>
            <select
              id="crop_type"
              name="crop_type"
              value={formData.crop_type}
              onChange={handleChange}
              required
            >
              <option value="rice">Rice (ଧାନ)</option>
              <option value="wheat">Wheat (ଗହମ)</option>
              <option value="maize">Maize (ମକା)</option>
              <option value="cotton">Cotton (କପା)</option>
              <option value="sugarcane">Sugarcane (ଆଖୁ)</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="region">Region</label>
            <select
              id="region"
              name="region"
              value={formData.region}
              onChange={handleChange}
              required
            >
              <option value="Odisha">Odisha</option>
              <option value="Punjab">Punjab</option>
              <option value="Gujarat">Gujarat</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Karnataka">Karnataka</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="temperature">Temperature (°C)</label>
            <input
              type="number"
              id="temperature"
              name="temperature"
              value={formData.temperature}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="rainfall">Rainfall (mm)</label>
            <input
              type="number"
              id="rainfall"
              name="rainfall"
              value={formData.rainfall}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="humidity">Humidity (%)</label>
            <input
              type="number"
              id="humidity"
              name="humidity"
              value={formData.humidity}
              onChange={handleChange}
              step="0.1"
              min="0"
              max="100"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="soil_ph">Soil pH</label>
            <input
              type="number"
              id="soil_ph"
              name="soil_ph"
              value={formData.soil_ph}
              onChange={handleChange}
              step="0.1"
              min="0"
              max="14"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="nitrogen">Nitrogen (kg/ha)</label>
            <input
              type="number"
              id="nitrogen"
              name="nitrogen"
              value={formData.nitrogen}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phosphorus">Phosphorus (kg/ha)</label>
            <input
              type="number"
              id="phosphorus"
              name="phosphorus"
              value={formData.phosphorus}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="potassium">Potassium (kg/ha)</label>
            <input
              type="number"
              id="potassium"
              name="potassium"
              value={formData.potassium}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="pesticide_usage">Pesticide Usage (kg/ha)</label>
            <input
              type="number"
              id="pesticide_usage"
              name="pesticide_usage"
              value={formData.pesticide_usage}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="irrigation_hours">Irrigation Hours per Day</label>
            <input
              type="number"
              id="irrigation_hours"
              name="irrigation_hours"
              value={formData.irrigation_hours}
              onChange={handleChange}
              step="0.1"
              required
            />
          </div>
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? (
            <>
              Predicting...
              <span className="loading-spinner"></span>
            </>
          ) : (
            'Predict Crop Yield'
          )}
        </button>
      </form>
    </div>
  );
};

export default PredictionForm;
