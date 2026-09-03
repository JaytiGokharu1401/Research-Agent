import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import '../styles/ConfigurationPage.css';

export default function ConfigurationPage() {
  const { register, handleSubmit, formState: { errors }, reset } = useForm();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [configs, setConfigs] = useState([]);

  const onSubmit = async (data) => {
    setLoading(true);
    setMessage('');
    try {
      const response = await axios.post('http://localhost:8000/api/v1/configs', data);
      console.log('✅ Config created:', response.data);
     setMessage(`✅ SUCCESS! Configuration saved! Redirecting to results...`);
     reset();

// Redirect to research results after 2 seconds
    setTimeout(() => {
    window.location.href = `/research/${response.data.id}`;
}, 2000);


    } catch (error) {
      console.error('❌ Error:', error);
      setMessage(`❌ Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fetchConfigs = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/configs');
      setConfigs(response.data.configs);
    } catch (error) {
      console.error('Error fetching configs:', error);
    }
  };

  React.useEffect(() => {
    fetchConfigs();
  }, []);

  return (
    <div className="config-container">
      <div className="config-header">
        <h1>🔍 Research Agent</h1>
        <p>Market Intelligence + Business Opportunity Discovery for PalTech</p>
      </div>

      <div className="config-content">
        <div className="config-form-section">
          <h2>Create Research Configuration</h2>
          
          <form onSubmit={handleSubmit(onSubmit)}>
            <div className="form-group">
              <label>🏷️ Technology / Category *</label>
              <input
                type="text"
                placeholder="e.g., RPA, AI, Kubernetes, Blockchain"
                {...register('technology', { required: 'Technology is required' })}
              />
              <small>What technology/market do you want to research?</small>
              {errors.technology && <span className="error">{errors.technology.message}</span>}
            </div>

            <div className="form-group">
              <label>📊 Search Strategy *</label>
              <select {...register('search_strategy', { required: 'Required' })}>
                <option value="">-- Select Strategy --</option>
                <option value="market">Market Analysis Only</option>
                <option value="technology">Technology Deep Dive</option>
                <option value="opportunity">Business Opportunity Focus</option>
                <option value="comprehensive">Comprehensive (All)</option>
              </select>
              {errors.search_strategy && <span className="error">{errors.search_strategy.message}</span>}
            </div>

            <div className="form-group">
              <label>🔑 Search Terms *</label>
              <textarea
                placeholder="e.g., RPA automation, UiPath, Power Automate, market trends"
                rows="3"
                {...register('search_terms', { required: 'Required' })}
              />
              <small>Key terms to search for (comma-separated)</small>
              {errors.search_terms && <span className="error">{errors.search_terms.message}</span>}
            </div>

            <div className="form-group">
              <label>👥 Target Audience *</label>
              <select {...register('target_audience', { required: 'Required' })}>
                <option value="">-- Select Audience --</option>
                <option value="manager">Manager / Organization Level</option>
                <option value="employee">Employee / Domain Expert</option>
                <option value="both">Both</option>
              </select>
              <small>Output will be customized for this audience</small>
              {errors.target_audience && <span className="error">{errors.target_audience.message}</span>}
            </div>

            <div className="form-group">
              <label>📅 Timeline Scope *</label>
              <select {...register('timeline_scope', { required: 'Required' })}>
                <option value="">-- Select Timeline --</option>
                <option value="7days">Last 7 Days</option>
                <option value="30days">Last 30 Days</option>
                <option value="90days">Last 90 Days</option>
                <option value="1year">Last 12 Months</option>
                <option value="all">All Time</option>
              </select>
              {errors.timeline_scope && <span className="error">{errors.timeline_scope.message}</span>}
            </div>

            <div className="form-group">
              <label>💬 Detailed Prompt (Optional)</label>
              <textarea
                placeholder="Any specific focus? e.g., Focus on emerging opportunities for PalTech..."
                rows="4"
                {...register('detailed_prompt')}
              />
              <small>Customize the research focus (optional)</small>
            </div>

            {message && (
              <div className={`message ${message.includes('❌') ? 'error' : 'success'}`}>
                {message}
              </div>
            )}

            <div className="form-buttons">
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? '⏳ Starting Research...' : '🚀 Run Research'}
              </button>
              <button type="reset" className="btn btn-secondary">
                🔄 Clear Form
              </button>
            </div>
          </form>
        </div>

        <div className="config-info-section">
          <h3>📚 How It Works</h3>
          <div className="info-card">
            <h4>📊 Level 1: Market Research</h4>
            <p>Analyzes technology trends, market growth, and industry direction.</p>
          </div>
          <div className="info-card">
            <h4>🔧 Level 2: Platform Analysis</h4>
            <p>Discovers and analyzes relevant platforms.</p>
          </div>
          <div className="info-card">
            <h4>🏢 Level 3: Industry Analysis</h4>
            <p>Identifies industry-specific opportunities and use cases.</p>
          </div>
          <div className="info-card">
            <h4>🎯 Opportunity Detection</h4>
            <p>Highlights business opportunities for PalTech.</p>
          </div>
        </div>
      </div>

      {configs.length > 0 && (
        <div className="saved-configs-section">
          <h2>📋 Saved Configurations ({configs.length})</h2>
          <div className="configs-grid">
            {configs.map(config => (
              <div key={config.id} className="config-card">
                <h4>{config.technology}</h4>
                <p><strong>Audience:</strong> {config.target_audience}</p>
                <p><strong>Timeline:</strong> {config.timeline_scope}</p>
                <p><strong>Created:</strong> {new Date(config.created_at).toLocaleDateString()}</p>
                <small>ID: {config.id.substring(0, 8)}...</small>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}