import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/ResearchResults.css';

export default function ResearchResults() {
  const { configId } = useParams();
  const navigate = useNavigate();
  const [config, setConfig] = useState(null);
  const [research, setResearch] = useState(null);
  const [opportunities, setOpportunities] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchResearchData();
  }, [configId]);

  const fetchResearchData = async () => {
    try {
      setLoading(true);
      
      // Fetch configuration
      const configRes = await axios.get(`http://localhost:8000/api/v1/configs/${configId}`);
      setConfig(configRes.data);

      // Fetch research results from JSON file
      // Note: You'll need to add this endpoint
      const researchRes = await axios.get(`http://localhost:8000/api/v1/research/${configId}`);
      setResearch(researchRes.data);
      setOpportunities(researchRes.data.opportunities);
      
      setError(null);
    } catch (err) {
      console.error('Error fetching research:', err);
      setError('Failed to load research data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="results-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading research results...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-container">
        <div className="error-message">
          <h2>⚠️ Error</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            ← Back to Configuration
          </button>
        </div>
      </div>
    );
  }

  if (!research) {
    return (
      <div className="results-container">
        <div className="error-message">
          <h2>No research data found</h2>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            ← Back to Configuration
          </button>
        </div>
      </div>
    );
  }

  const marketResearch = research.levels?.market_research || {};
  const platformAnalysis = research.levels?.platform_analysis || {};
  const industryAnalysis = research.levels?.industry_analysis || {};

  return (
    <div className="results-container">
      {/* Header */}
      <div className="results-header">
        <div className="header-content">
          <h1>📊 {research.technology} Market Research Report</h1>
          <p className="subtitle">Research Agent - Market Intelligence & Opportunity Discovery</p>
          <p className="meta">
            Generated: {new Date(research.generated_at).toLocaleDateString()} | 
            Duration: {research.duration_seconds?.toFixed(2)}s
          </p>
        </div>
      </div>

      {/* Navigation */}
      <div className="results-nav">
        <button onClick={() => navigate('/')} className="nav-btn">← New Research</button>
        <button onClick={() => navigate('/reports')} className="nav-btn">📋 All Reports</button>
        <button onClick={() => navigate(`/report/${configId}`)} className="nav-btn">📄 Full Report</button>
        <button onClick={() => exportPDF()} className="nav-btn primary">📥 Download PDF</button>
      </div>

      {/* Executive Summary */}
      <section className="results-section">
        <h2>📌 Executive Summary</h2>
        <div className="summary-box">
          <p>
            {marketResearch.summary || 
            `The ${research.technology} market is experiencing high demand with steady growth.`}
          </p>
          <div className="key-findings">
            <h4>Key Findings:</h4>
            <ul>
              <li>Market consolidating around AI-augmented platforms</li>
              <li>Convergence with AI/LLM capabilities accelerating</li>
              <li>Strong enterprise adoption with growing SMB interest</li>
              <li>ROI expectations: 300-500% within 12-18 months</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Market Trends */}
      <section className="results-section">
        <h2>📈 Market Trends</h2>
        <div className="trends-grid">
          {marketResearch.trends?.slice(0, 4).map((trend, idx) => (
            <div key={idx} className="trend-card">
              <h4>{trend.title}</h4>
              <p>{trend.description}</p>
              <span className={`status ${trend.momentum || 'steady'}`}>
                {trend.momentum || 'Steady'}
              </span>
            </div>
          ))}
        </div>
      </section>

      {/* Industry Opportunities */}
      <section className="results-section">
        <h2>🏢 Industry Opportunities</h2>
        <div className="industries-grid">
          {industryAnalysis.industries?.slice(0, 5).map((ind, idx) => (
            <div key={idx} className="industry-card">
              <h4>{ind.industry}</h4>
              <div className="opportunity-item">
                <strong>Top Opportunity:</strong>
                <p>{ind.opportunities?.[0]?.title || 'Automation opportunity'}</p>
              </div>
              <div className="opportunity-item">
                <strong>Investment Trend:</strong>
                <p>{ind.investment_trends?.[0]?.trend || 'Steady growth'}</p>
              </div>
              <div className="metrics">
                <span className="badge">
                  {ind.opportunities?.length || 0} opportunities
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Project Opportunities */}
      <section className="results-section">
        <h2>💼 Project Opportunities</h2>
        <div className="opportunities-list">
          {opportunities?.project_opportunities?.slice(0, 5).map((opp, idx) => (
            <div key={idx} className="opportunity-box">
              <div className="opp-header">
                <h4>{opp.title}</h4>
                <span className="badge revenue">${opp.potential_revenue}</span>
              </div>
              <p className="opp-desc">{opp.description}</p>
              <div className="opp-meta">
                <span>📅 {opp.timeline}</span>
                <span>💰 {opp.potential_revenue}</span>
                <span>🎯 {opp.industry}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Recommended Actions */}
      <section className="results-section">
        <h2>🎯 Recommended Actions</h2>
        <div className="actions-grid">
          <div className="action-column">
            <h4>Immediate</h4>
            <ul>
              <li>✓ Establish {research.technology} Center of Excellence</li>
              <li>✓ Develop industry-specific playbooks</li>
              <li>✓ Build AI integration capabilities</li>
              <li>✓ Create training programs</li>
            </ul>
          </div>
          <div className="action-column">
            <h4>Short Term (3-6 months)</h4>
            <ul>
              <li>✓ Launch market campaigns</li>
              <li>✓ Build customer success stories</li>
              <li>✓ Expand certifications</li>
              <li>✓ Establish analyst relations</li>
            </ul>
          </div>
          <div className="action-column">
            <h4>Long Term (6-12 months)</h4>
            <ul>
              <li>✓ Achieve market leadership</li>
              <li>✓ Build ecosystem partnerships</li>
              <li>✓ Develop proprietary capabilities</li>
              <li>✓ Explore strategic opportunities</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Risks & Considerations */}
      <section className="results-section warning">
        <h2>⚠️ Risks & Considerations</h2>
        <div className="risks-grid">
          <div className="risk-column">
            <h4>Market Risks</h4>
            <ul>
              <li>Rapid vendor consolidation</li>
              <li>Cloud providers entering market</li>
              <li>ROI expectations may exceed reality</li>
            </ul>
          </div>
          <div className="risk-column">
            <h4>Execution Risks</h4>
            <ul>
              <li>Talent acquisition challenges</li>
              <li>Platform evolution requires R&D</li>
              <li>Customer education needed</li>
            </ul>
          </div>
          <div className="risk-column">
            <h4>Mitigation</h4>
            <ul>
              <li>Build compliance into solutions</li>
              <li>Maintain vendor partnerships</li>
              <li>Invest in customer enablement</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Bottom Navigation */}
      <div className="results-footer">
        <button onClick={() => navigate('/')} className="btn btn-secondary">
          ← New Research
        </button>
        <button onClick={() => navigate(`/report/${configId}`)} className="btn btn-primary">
          📄 View Full 15-Section Report →
        </button>
      </div>
    </div>
  );
}

// Helper function for PDF export
function exportPDF() {
  // Placeholder - we'll implement this with a library
  alert('PDF export will be available in the next update!');
}