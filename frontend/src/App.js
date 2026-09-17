import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ConfigurationPage from './pages/ConfigurationPage';
import ResearchResults from './pages/ResearchResults';
import FullReport from './pages/FullReport';
import Reports from './pages/Reports';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ConfigurationPage />} />
        <Route path="/research/:configId" element={<ResearchResults />} />
        <Route path="/report/:configId" element={<FullReport />} />
        <Route path="/reports" element={<Reports />} />
        {/* Catch all - redirect to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;