import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const Dashboard = () => {
  const [statistics, setStatistics] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, historicalRes] = await Promise.all([
        axios.get('/api/statistics'),
        axios.get('/api/historical')
      ]);
      
      setStatistics(statsRes.data);
      setHistoricalData(historicalRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const cropYieldChartData = historicalData ? {
    labels: Object.keys(historicalData.average_yields),
    datasets: [{
      label: 'Average Yield (kg/ha)',
      data: Object.values(historicalData.average_yields),
      backgroundColor: [
        'rgba(102, 126, 234, 0.8)',
        'rgba(118, 75, 162, 0.8)',
        'rgba(237, 137, 54, 0.8)',
        'rgba(72, 187, 120, 0.8)',
        'rgba(245, 101, 101, 0.8)'
      ],
      borderColor: [
        'rgba(102, 126, 234, 1)',
        'rgba(118, 75, 162, 1)',
        'rgba(237, 137, 54, 1)',
        'rgba(72, 187, 120, 1)',
        'rgba(245, 101, 101, 1)'
      ],
      borderWidth: 2
    }]
  } : null;

  return (
    <div className="dashboard">
      <h2>Agricultural Analytics Dashboard</h2>
      
      {statistics && (
        <div className="dashboard-grid">
          <div className="stat-card">
            <h3>Total Predictions</h3>
            <div className="value">{statistics.total_predictions}</div>
          </div>
          
          <div className="stat-card">
            <h3>Average Yield</h3>
            <div className="value">{Math.round(statistics.average_yield)} kg/ha</div>
          </div>
          
          <div className="stat-card">
            <h3>Best Crop</h3>
            <div className="value">{statistics.best_performing_crop}</div>
          </div>
          
          <div className="stat-card">
            <h3>Regions Covered</h3>
            <div className="value">{statistics.regions_covered}</div>
          </div>
        </div>
      )}

      <div className="charts-section">
        {cropYieldChartData && (
          <div className="chart-container">
            <h3>Average Crop Yields by Type</h3>
            <Bar 
              data={cropYieldChartData}
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    display: false
                  },
                  tooltip: {
                    callbacks: {
                      label: (context) => `${context.parsed.y.toLocaleString()} kg/ha`
                    }
                  }
                },
                scales: {
                  y: {
                    beginAtZero: true,
                    title: {
                      display: true,
                      text: 'Yield (kg/ha)'
                    }
                  }
                }
              }}
            />
          </div>
        )}

        {historicalData && (
          <div className="recent-predictions">
            <h3>Recent Predictions</h3>
            <div className="predictions-list">
              {historicalData.recent_predictions.slice(0, 5).map((pred, index) => (
                <div key={index} className="prediction-item">
                  <div className="pred-info">
                    <strong>{pred.crop_type}</strong> in {pred.region}
                  </div>
                  <div className="pred-yield">
                    {pred.yield_per_hectare.toLocaleString()} kg/ha
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <style jsx>{`
        .dashboard {
          animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .charts-section {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
          margin-top: 2rem;
        }

        .chart-container {
          background: #f7fafc;
          padding: 1.5rem;
          border-radius: 12px;
        }

        .chart-container h3 {
          margin-bottom: 1rem;
          color: #2d3748;
        }

        .recent-predictions {
          background: #f7fafc;
          padding: 1.5rem;
          border-radius: 12px;
        }

        .recent-predictions h3 {
          margin-bottom: 1rem;
          color: #2d3748;
        }

        .predictions-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .prediction-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem;
          background: white;
          border-radius: 6px;
          border-left: 3px solid #667eea;
        }

        .pred-info strong {
          color: #2d3748;
          text-transform: capitalize;
        }

        .pred-yield {
          font-weight: 600;
          color: #48bb78;
        }

        .loading {
          text-align: center;
          padding: 2rem;
          color: #718096;
        }

        @media (max-width: 768px) {
          .charts-section {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default Dashboard;
