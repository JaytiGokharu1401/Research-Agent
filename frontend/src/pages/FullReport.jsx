import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/FullReport.css';

export default function FullReport() {
  const { configId } = useParams();
  const navigate = useNavigate();
  const [research, setResearch] = useState(null);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedSection, setExpandedSection] = useState('1_executive_summary');

  useEffect(() => {
    fetchReport();
  }, [configId]);

  const fetchReport = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`http://localhost:8000/api/v1/research/${configId}`);
      setResearch(res.data);
      setReport(res.data.report);
      setError(null);
    } catch (err) {
      console.error('Error fetching report:', err);
      setError('Failed to load report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="report-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading full report...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="report-container">
        <div className="error-message">
          <h2>⚠️ Error</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            ← Back
          </button>
        </div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="report-container">
        <div className="error-message">
          <h2>No report data found</h2>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            ← Back
          </button>
        </div>
      </div>
    );
  }

  const sections = report.sections || {};
  const sectionKeys = Object.keys(sections).sort();

  return (
    <div className="report-container">
      {/* Header */}
      <div className="report-header">
        <h1>📄 {research?.technology} - Complete Market Research Report</h1>
        <p className="subtitle">All 15 Sections - Executive Details</p>
      </div>

      {/* Navigation */}
      <div className="report-nav">
        <button onClick={() => navigate(`/research/${configId}`)} className="nav-btn">
          ← Back to Summary
        </button>
        <button onClick={() => navigate('/reports')} className="nav-btn">
          📋 All Reports
        </button>
      </div>

      <div className="report-content">
        {/* Table of Contents */}
        <aside className="report-toc">
          <h3>Table of Contents</h3>
          <nav className="toc-list">
            {sectionKeys.map((key, idx) => (
              <button
                key={key}
                className={`toc-item ${expandedSection === key ? 'active' : ''}`}
                onClick={() => setExpandedSection(key)}
              >
                {idx + 1}. {key.replace(/_/g, ' ').replace(/^\d+_/, '')}
              </button>
            ))}
          </nav>
        </aside>

        {/* Report Sections */}
        <main className="report-main">
          {sectionKeys.map((key) => (
            <section
              key={key}
              className={`report-section ${expandedSection === key ? 'expanded' : ''}`}
            >
              <button
                className="section-toggle"
                onClick={() =>
                  setExpandedSection(expandedSection === key ? null : key)
                }
              >
                <span className="toggle-icon">
                  {expandedSection === key ? '▼' : '▶'}
                </span>
                <h2>{key.replace(/_/g, ' ').replace(/^\d+_/, '')}</h2>
              </button>

              {expandedSection === key && (
                <div className="section-content">
                  <SectionRenderer section={sections[key]} />
                </div>
              )}
            </section>
          ))}
        </main>
      </div>

      {/* Footer */}
      <div className="report-footer">
        <button onClick={() => navigate(`/research/${configId}`)} className="btn btn-secondary">
          ← Back to Summary
        </button>
        <button onClick={() => navigate('/reports')} className="btn btn-primary">
          📋 All Reports →
        </button>
      </div>
    </div>
  );
}

// Component to render different section types
function SectionRenderer({ section }) {
  if (!section) {
    return <p>No data available for this section.</p>;
  }

  if (typeof section === 'string') {
    return <p>{section}</p>;
  }

  if (section.content) {
    return <div className="section-prose">{section.content}</div>;
  }

  if (Array.isArray(section.trends)) {
    return (
      <div className="trends-list">
        {section.trends.map((trend, idx) => (
          <div key={idx} className="trend-item">
            <h4>{trend}</h4>
          </div>
        ))}
      </div>
    );
  }

  if (section.summary) {
    return (
      <div>
        <p>{section.summary}</p>
        {section.trends && (
          <div className="trends-list">
            {section.trends.map((t, idx) => (
              <p key={idx}>• {t}</p>
            ))}
          </div>
        )}
      </div>
    );
  }

  if (section.opportunities) {
    return (
      <div className="opportunities-section">
        {Array.isArray(section.opportunities) &&
          section.opportunities.map((opp, idx) => (
            <div key={idx} className="opp-item">
              <h4>{opp.title || opp.name || `Opportunity ${idx + 1}`}</h4>
              <p>{opp.description || opp.description}</p>
            </div>
          ))}
      </div>
    );
  }

  // Default: render as pretty JSON
  return (
    <pre className="section-json">
      {JSON.stringify(section, null, 2)}
    </pre>
  );
}