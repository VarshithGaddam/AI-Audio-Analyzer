import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = () => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <h3>Analyzing Your Audio</h3>
      <p>Extracting features using advanced ML algorithms</p>
      <div className="loading-steps">
        <p>Loading audio signal</p>
        <p>Extracting YAMNet embeddings</p>
        <p>Computing prosodic features</p>
        <p>Analyzing spectral characteristics</p>
        <p>Calculating voice quality metrics</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;
