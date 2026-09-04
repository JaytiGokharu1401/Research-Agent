import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ConfigurationPage from './pages/ConfigurationPage';
import ResearchResults from './pages/ResearchResults';
import FullReport from './pages/FullReport';
import Reports from './pages/Reports';
import './App.css';

function App() {
  return (
    <Router basename="/Research-Agent">
      <Routes>
        <Route path="/" element={<ConfigurationPage />} />
        <Route path="/research/:configId" element={<ResearchResults />} />
        <Route path="/report/:configId" element={<FullReport />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Router>
  );
}

export default App;