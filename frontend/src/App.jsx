import React, { useState } from 'react';
import './index.css';

function App() {
  const [formData, setFormData] = useState({
    model_name: 'iPhone 13',
    ram: 4,
    memory: 128,
    is_used: true
  });
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : 
              (name === 'ram' || name === 'memory') ? Number(value) : value
    }));
  };

  const getPrediction = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPrediction(null);
    
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });
      
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      
      const data = await response.json();
      setPrediction(data.price);
    } catch (err) {
      setError('Failed to get prediction. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="brand-title">Price Predictor</h1>
        <h2 className="brand-subtitle">Sri Lankan iPhone Market</h2>
        
        <form onSubmit={getPrediction}>
          <div className="form-group">
            <label htmlFor="model_name">iPhone Model</label>
            <select 
              id="model_name" 
              name="model_name" 
              value={formData.model_name}
              onChange={handleChange}
            >
              <option value="iPhone 11">iPhone 11</option>
              <option value="iPhone 11 Pro">iPhone 11 Pro</option>
              <option value="iPhone 11 Pro Max">iPhone 11 Pro Max</option>
              <option value="iPhone 12">iPhone 12</option>
              <option value="iPhone 12 Pro">iPhone 12 Pro</option>
              <option value="iPhone 12 Pro Max">iPhone 12 Pro Max</option>
              <option value="iPhone 13">iPhone 13</option>
              <option value="iPhone 13 Pro">iPhone 13 Pro</option>
              <option value="iPhone 13 Pro Max">iPhone 13 Pro Max</option>
              <option value="iPhone 14">iPhone 14</option>
              <option value="iPhone 14 Pro">iPhone 14 Pro</option>
              <option value="iPhone 14 Pro Max">iPhone 14 Pro Max</option>
              <option value="iPhone 15">iPhone 15</option>
              <option value="iPhone 15 Pro">iPhone 15 Pro</option>
              <option value="iPhone 15 Pro Max">iPhone 15 Pro Max</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="ram">RAM (GB)</label>
            <select 
              id="ram" 
              name="ram" 
              value={formData.ram} 
              onChange={handleChange}
            >
              <option value={4}>4 GB</option>
              <option value={6}>6 GB</option>
              <option value={8}>8 GB</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="memory">Storage (GB)</label>
            <select 
              id="memory" 
              name="memory" 
              value={formData.memory} 
              onChange={handleChange}
            >
              <option value={64}>64 GB</option>
              <option value={128}>128 GB</option>
              <option value={256}>256 GB</option>
              <option value={512}>512 GB</option>
              <option value={1024}>1 TB</option>
            </select>
          </div>
          
          <div className="form-group">
            <label className="checkbox-wrap">
              <input 
                type="checkbox" 
                name="is_used"
                checked={formData.is_used}
                onChange={handleChange}
              />
              <span>This is a used phone</span>
            </label>
          </div>

          <button 
            type="submit" 
            className="predict-btn" 
            disabled={loading}
          >
            {loading ? <span className="loader"></span> : 'Predict Price'}
          </button>
        </form>

        {error && (
          <div style={{color: '#ff4b4b', textAlign: 'center', marginTop: '1rem', fontSize: '0.9rem'}}>
            {error}
          </div>
        )}

        {prediction && (
          <div className="result-card">
            <div className="result-label">Estimated Value</div>
            <div className="result-price">
              Rs. {Number(prediction).toLocaleString('en-US', { maximumFractionDigits: 0 })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
