import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import HomePage from './pages/HomePage';
import FileUpload from './components/FileUpload';
import MetricsDisplay from './components/MetricsDisplay';
import LoadingSpinner from './components/LoadingSpinner';

const API_URL = process.env.REACT_APP_API_URL || 'https://varshith800-yamee-audio-analyzer.hf.space';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showAnalyzer, setShowAnalyzer] = useState(false);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    setAnalysisData(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setAnalysisData(response.data);
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to analyze audio file';
      setError(errorMsg);
      console.error('Analysis error:', err);
      console.error('Error details:', err.response?.data);
    } finally {
      setLoading(false);
    }
  };

  const handleGetStarted = () => {
    setShowAnalyzer(true);
  };

  const handleBackToHome = () => {
    setShowAnalyzer(false);
    setAnalysisData(null);
    setError(null);
  };

  if (!showAnalyzer) {
    return (
      <div className="App">
        <header className="App-header">
          <div className="header-content">
            <div className="logo-section">
              <div className="logo-icon">🎤</div>
              <div>
                <h1>AI Voice Analyzer</h1>
                <p>Advanced audio analysis powered by machine learning</p>
              </div>
            </div>
          </div>
        </header>
        <HomePage onGetStarted={handleGetStarted} />
        <footer className="App-footer">
          <p>Powered by YAMNet, TensorFlow & React</p>
          <div className="footer-links">
            <a href="#features">Features</a>
            <a href="#about">About</a>
            <a href="#docs">Documentation</a>
          </div>
        </footer>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">🎤</div>
            <div>
              <h1>AI Voice Analyzer</h1>
              <p>Advanced audio analysis powered by machine learning</p>
            </div>
          </div>
          <button className="btn-back" onClick={handleBackToHome}>
            ← Back to Home
          </button>
        </div>
      </header>

      <main className="App-main">
        <FileUpload onFileUpload={handleFileUpload} disabled={loading} />

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        {loading && <LoadingSpinner />}

        {analysisData && !loading && (
          <MetricsDisplay data={analysisData} />
        )}
      </main>

      <footer className="App-footer">
        <p>Powered by YAMNet, TensorFlow & React</p>
        <div className="footer-links">
          <a href="#features">Features</a>
          <a href="#about">About</a>
          <a href="#docs">Documentation</a>
        </div>
      </footer>
    </div>
  );
}

export default App;
