import React from 'react';

const ResultsDisplay = ({ result }) => {
  if (!result) return null;

  const { predicted_yield, unit, recommendations, input_data } = result;

  const renderRecommendations = (items, title) => {
    if (!items || items.length === 0) return null;

    return (
      <div className="recommendation-card">
        <h3>{title}</h3>
        {items.map((item, index) => (
          <div key={index} className="recommendation-item">
            <strong>{item.action}</strong>
            <p>{item.detail}</p>
            {item.dosage && <p><em>Dosage: {item.dosage}</em></p>}
            {item.impact && <p className="impact">Impact: {item.impact}</p>}
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="results-display">
      <div className={`result-card priority-${recommendations.priority || 'medium'}`}>
        <h2>Predicted Crop Yield</h2>
        <div className="yield-value">
          {predicted_yield.toLocaleString()} {unit}
        </div>
        <p>For {input_data.crop_type} in {input_data.region}</p>
        
        {recommendations.optimization_score && (
          <div className="optimization-score">
            <h4>Optimization Score: {recommendations.optimization_score}%</h4>
            <div className="score-bar">
              <div 
                className="score-fill" 
                style={{
                  width: `${recommendations.optimization_score}%`,
                  background: recommendations.optimization_score > 80 ? '#48bb78' : 
                             recommendations.optimization_score > 60 ? '#ed8936' : '#f56565'
                }}
              />
            </div>
          </div>
        )}
      </div>

      <div className="recommendation-section">
        <h2>Personalized Recommendations</h2>
        
        {recommendations.priority && (
          <div className={`priority-badge priority-${recommendations.priority}`}>
            Priority Level: {recommendations.priority.toUpperCase()}
          </div>
        )}

        {renderRecommendations(recommendations.irrigation, '💧 Irrigation Optimization')}
        {renderRecommendations(recommendations.fertilization, '🌱 Fertilization Strategy')}
        {renderRecommendations(recommendations.pest_control, '🐛 Pest Control Measures')}
        {renderRecommendations(recommendations.general, '📋 General Recommendations')}

        {recommendations.timing && (
          <div className="recommendation-card">
            <h3>📅 Seasonal Timeline</h3>
            <div className="timing-info">
              <p><strong>Planting Time:</strong> {recommendations.timing.planting}</p>
              <p><strong>Critical Period:</strong> {recommendations.timing.critical_period}</p>
              <p><strong>Harvest Time:</strong> {recommendations.timing.harvest_time}</p>
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .optimization-score {
          margin-top: 1.5rem;
          padding: 1rem;
          background: white;
          border-radius: 8px;
        }

        .optimization-score h4 {
          margin-bottom: 0.5rem;
          color: #2d3748;
        }

        .score-bar {
          width: 100%;
          height: 20px;
          background: #e2e8f0;
          border-radius: 10px;
          overflow: hidden;
        }

        .score-fill {
          height: 100%;
          transition: width 1s ease;
        }

        .priority-badge {
          padding: 0.5rem 1rem;
          border-radius: 6px;
          margin-bottom: 1rem;
          font-weight: 600;
          text-align: center;
        }

        .priority-badge.priority-high {
          background: #fed7d7;
          color: #c53030;
        }

        .priority-badge.priority-medium {
          background: #feebc8;
          color: #c05621;
        }

        .priority-badge.priority-low {
          background: #c6f6d5;
          color: #22543d;
        }

        .timing-info p {
          margin: 0.5rem 0;
          padding: 0.5rem;
          background: #f7fafc;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
};

export default ResultsDisplay;
