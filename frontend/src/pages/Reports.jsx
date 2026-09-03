import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Reports.css';

export default function Reports() {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setLoading(true);
      const res = await axios.get('http://localhost:8000/api/v1/research');
      setReports(res.data.research || []);
      setError(null);
    } catch (err) {
      console.error('Error fetching reports:', err);
      setError('Failed to load reports');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="reports-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading reports...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="reports-container">
      {/* Header */}
      <div className="reports-header">
        <h1>📋 All Research Reports</h1>
        <p className="subtitle">View your research history</p>
      </div>

      {/* Navigation */}
      <div className="reports-nav">
        <button onClick={() => navigate('/')} className="nav-btn">
          ➕ New Research
        </button>
      </div>

      {/* Reports List */}
      {error && <div className="error-message">{error}</div>}

      {reports.length === 0 ? (
        <div className="empty-state">
          <h2>No reports yet</h2>
          <p>Create a new research to see it here</p>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            ➕ Create First Research
          </button>
        </div>
      ) : (
        <div className="reports-grid">
          {reports.map((report) => (
            <div key={report.config_id} className="report-card">
              <div className="card-header">
                <h3>{report.technology}</h3>
                <span className={`status ${report.status}`}>
                  {report.status}
                </span>
              </div>

              <div className="card-body">
                <p className="date">
                  📅 {new Date(report.generated_at).toLocaleDateString()}
                </p>
                <p className="id">ID: {report.config_id.substring(0, 8)}...</p>
              </div>

              <div className="card-actions">
                <button
                  onClick={() => navigate(`/research/${report.config_id}`)}
                  className="action-btn summary"
                >
                  📊 Summary
                </button>
                <button
                  onClick={() => navigate(`/report/${report.config_id}`)}
                  className="action-btn full"
                >
                  📄 Full Report
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Footer */}
      <div className="reports-footer">
        <button onClick={() => navigate('/')} className="btn btn-secondary">
          ← Back Home
        </button>
      </div>
    </div>
  );
}