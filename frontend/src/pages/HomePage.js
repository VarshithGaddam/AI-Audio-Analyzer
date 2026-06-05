import React, { useEffect } from 'react';
import { Mic, Zap, Brain, TrendingUp, Music, Waves, BarChart3, Sparkles } from 'lucide-react';
import './HomePage.css';

const HomePage = ({ onGetStarted }) => {
  useEffect(() => {
    const handleScroll = () => {
      const cards = document.querySelectorAll('.feature-card-small');
      const viewportCenter = window.innerWidth / 2;

      cards.forEach(card => {
        const rect = card.getBoundingClientRect();
        const cardCenter = rect.left + rect.width / 2;
        const distanceFromCenter = Math.abs(viewportCenter - cardCenter);
        
        // If card is near center (within 250px), zoom it
        if (distanceFromCenter < 250) {
          const scale = 1.2 - (distanceFromCenter / 250) * 0.2;
          card.style.transform = `scale(${scale}) translateY(${-20 * scale}px)`;
          card.style.boxShadow = '0 28px 72px rgba(255, 45, 85, 0.6)';
          card.style.zIndex = '10';
        } else {
          card.style.transform = 'scale(1) translateY(0)';
          card.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.1)';
          card.style.zIndex = '1';
        }
      });
    };

    // Check position more frequently for smoother animation
    const interval = setInterval(handleScroll, 20);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="homepage">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <span className="hero-badge">
              <Sparkles size={16} />
              Powered by AI & Machine Learning
            </span>
            <h1 className="hero-title">
              Analyze Your Audio with
              <span className="gradient-text"> Advanced AI</span>
            </h1>
            <p className="hero-description">
              Extract 60+ audio metrics using YAMNet, deep learning, and advanced signal processing. 
              Get comprehensive analysis of pitch, voice quality, spectral features, and more.
            </p>
            <div className="hero-buttons">
              <button className="btn-primary" onClick={onGetStarted}>
                <Mic size={20} />
                Start Analyzing
              </button>
              <button className="btn-secondary">
                <Music size={20} />
                View Demo
              </button>
            </div>
            <div className="hero-stats">
              <div className="stat-item">
                <h3>60+</h3>
                <p>Audio Metrics</p>
              </div>
              <div className="stat-item">
                <h3>1024</h3>
                <p>YAMNet Features</p>
              </div>
              <div className="stat-item">
                <h3>5+</h3>
                <p>Analysis Categories</p>
              </div>
            </div>
          </div>
          <div className="hero-image">
            <div className="floating-card card-1">
              <Waves size={32} />
              <h4>Waveform Analysis</h4>
            </div>
            <div className="floating-card card-2">
              <BarChart3 size={32} />
              <h4>Real-time Charts</h4>
            </div>
            <div className="floating-card card-3">
              <Brain size={32} />
              <h4>AI Powered</h4>
            </div>
            <div className="hero-visual">
              <div className="sound-wave wave-1"></div>
              <div className="sound-wave wave-2"></div>
              <div className="sound-wave wave-3"></div>
              <div className="sound-wave wave-4"></div>
              <div className="sound-wave wave-5"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section - Carousel */}
      <section className="features-section">
        <div className="section-header">
          <h2>Comprehensive Audio Analysis</h2>
          <p>Extract professional-grade metrics from any audio file</p>
        </div>
        <div className="carousel-container">
          <div className="carousel-track">
            {/* First set */}
            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #6b21a8, #7e22ce)'}}>
                <Mic size={28} />
              </div>
              <h3>Voice Quality</h3>
              <p>Jitter, shimmer, harmonicity & formants</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #7e22ce, #9333ea)'}}>
                <Waves size={28} />
              </div>
              <h3>Prosodic Features</h3>
              <p>Pitch contours & energy dynamics</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #9333ea, #a855f7)'}}>
                <BarChart3 size={28} />
              </div>
              <h3>Spectral Analysis</h3>
              <p>MFCCs & mel spectrograms</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #a855f7, #c026d3)'}}>
                <TrendingUp size={28} />
              </div>
              <h3>Temporal Features</h3>
              <p>Tempo, beats & rhythm patterns</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #c026d3, #d946ef)'}}>
                <Brain size={28} />
              </div>
              <h3>YAMNet ML</h3>
              <p>1024-dim deep learning embeddings</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #d946ef, #ec4899)'}}>
                <Zap size={28} />
              </div>
              <h3>Real-time Viz</h3>
              <p>Interactive charts & graphs</p>
            </div>

            {/* Second set - duplicate for seamless loop */}
            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #6b21a8, #7e22ce)'}}>
                <Mic size={28} />
              </div>
              <h3>Voice Quality</h3>
              <p>Jitter, shimmer, harmonicity & formants</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #7e22ce, #9333ea)'}}>
                <Waves size={28} />
              </div>
              <h3>Prosodic Features</h3>
              <p>Pitch contours & energy dynamics</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #9333ea, #a855f7)'}}>
                <BarChart3 size={28} />
              </div>
              <h3>Spectral Analysis</h3>
              <p>MFCCs & mel spectrograms</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #a855f7, #c026d3)'}}>
                <TrendingUp size={28} />
              </div>
              <h3>Temporal Features</h3>
              <p>Tempo, beats & rhythm patterns</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #c026d3, #d946ef)'}}>
                <Brain size={28} />
              </div>
              <h3>YAMNet ML</h3>
              <p>1024-dim deep learning embeddings</p>
            </div>

            <div className="feature-card-small">
              <div className="feature-icon" style={{background: 'linear-gradient(135deg, #d946ef, #ec4899)'}}>
                <Zap size={28} />
              </div>
              <h3>Real-time Viz</h3>
              <p>Interactive charts & graphs</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works-section">
        <div className="section-header">
          <h2>How It Works</h2>
          <p>Simple 3-step process to analyze your audio</p>
        </div>
        <div className="steps-container">
          <div className="step-card">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Upload Audio File</h3>
              <p>Drag and drop or browse to upload your audio file. Supports WAV, MP3, FLAC, OGG, M4A formats.</p>
            </div>
          </div>
          <div className="step-arrow">→</div>
          <div className="step-card">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>AI Analysis</h3>
              <p>Our ML models extract features including YAMNet embeddings, prosodic, spectral, and temporal metrics.</p>
            </div>
          </div>
          <div className="step-arrow">→</div>
          <div className="step-card">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>View Results</h3>
              <p>Explore comprehensive metrics across 6 interactive tabs with beautiful visualizations.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Screenshots/Preview Section */}
      <section className="preview-section">
        <div className="section-header">
          <h2>See It In Action</h2>
          <p>Explore our intuitive interface and comprehensive visualizations</p>
        </div>
        <div className="preview-container">
          <div className="preview-large">
            <div className="preview-image main-preview">
              <img src="/screenshots/dashboard.png" alt="Main Dashboard" style={{width: '100%', height: 'auto', display: 'block'}} onError={(e) => {
                e.target.style.display = 'none';
                e.target.nextSibling.style.display = 'flex';
              }} />
              <div className="image-overlay" style={{display: 'flex'}}>
                <div className="overlay-content">
                  <h2>Experience Professional Audio Analysis</h2>
                  <p>Real-time metrics • AI-powered insights • Beautiful visualizations</p>
                </div>
              </div>
            </div>
            <div className="preview-caption">
              <h3>Comprehensive Dashboard</h3>
              <p>View all your audio metrics in one beautiful interface</p>
            </div>
          </div>

          <div className="preview-grid">
            <div className="preview-item">
              <div className="preview-image">
                <img src="/screenshots/waveform.png" alt="Waveform Analysis" onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }} />
                <div className="preview-placeholder" style={{display: 'none'}}>
                  <Waves size={48} />
                  <p>Waveform View</p>
                </div>
              </div>
              <h4>Waveform Analysis</h4>
            </div>

            <div className="preview-item">
              <div className="preview-image">
                <img src="/screenshots/pitch.png" alt="Pitch Tracking" onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }} />
                <div className="preview-placeholder" style={{display: 'none'}}>
                  <TrendingUp size={48} />
                  <p>Pitch Contour</p>
                </div>
              </div>
              <h4>Pitch Tracking</h4>
            </div>

            <div className="preview-item">
              <div className="preview-image">
                <img src="/screenshots/spectrogram.png" alt="Spectrogram" onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }} />
                <div className="preview-placeholder" style={{display: 'none'}}>
                  <BarChart3 size={48} />
                  <p>Spectrogram</p>
                </div>
              </div>
              <h4>Mel Spectrogram</h4>
            </div>

            <div className="preview-item">
              <div className="preview-image">
                <img src="/screenshots/metrics.png" alt="Voice Metrics" onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }} />
                <div className="preview-placeholder" style={{display: 'none'}}>
                  <Mic size={48} />
                  <p>Metrics Cards</p>
                </div>
              </div>
              <h4>Voice Quality Metrics</h4>
            </div>
          </div>
        </div>
      </section>

      {/* Visualization Showcase */}
      <section className="visualization-section">
        <div className="section-header">
          <h2>Rich Visualizations</h2>
          <p>Professional charts and graphs powered by advanced algorithms</p>
        </div>
        <div className="viz-grid">
          <div className="viz-card">
            <div className="viz-demo bars-demo">
              <div className="chart-bars">
                <div className="bar" style={{height: '60%', animationDelay: '0s'}}></div>
                <div className="bar" style={{height: '85%', animationDelay: '0.1s'}}></div>
                <div className="bar" style={{height: '45%', animationDelay: '0.2s'}}></div>
                <div className="bar" style={{height: '70%', animationDelay: '0.3s'}}></div>
                <div className="bar" style={{height: '90%', animationDelay: '0.4s'}}></div>
                <div className="bar" style={{height: '55%', animationDelay: '0.5s'}}></div>
              </div>
            </div>
            <h3>Time-Series Plots</h3>
            <p>Track audio features over time with interactive line charts</p>
          </div>

          <div className="viz-card">
            <div className="viz-demo heatmap-demo">
              <div className="heatmap-grid">
                {[...Array(48)].map((_, i) => (
                  <div key={i} className="heatmap-cell" style={{
                    opacity: Math.random() * 0.7 + 0.3,
                    animationDelay: `${i * 0.02}s`
                  }}></div>
                ))}
              </div>
            </div>
            <h3>Spectrograms</h3>
            <p>Visualize frequency content with mel spectrograms and MFCCs</p>
          </div>

          <div className="viz-card">
            <div className="viz-demo waveform-demo">
              <div className="waveform-display">
                {[...Array(60)].map((_, i) => (
                  <div key={i} className="wave-bar" style={{
                    height: `${Math.sin(i * 0.3) * 40 + 50}%`,
                    animationDelay: `${i * 0.02}s`
                  }}></div>
                ))}
              </div>
            </div>
            <h3>Waveforms</h3>
            <p>View audio signal amplitude with high-resolution waveform display</p>
          </div>

          <div className="viz-card">
            <div className="viz-demo metrics-demo">
              <div className="homepage-metrics-demo">
                <div className="metric-badge badge-1">Pitch</div>
                <div className="metric-badge badge-2">Energy</div>
                <div className="metric-badge badge-3">Tempo</div>
                <div className="metric-badge badge-4">Jitter</div>
              </div>
            </div>
            <h3>Metric Cards</h3>
            <p>Key metrics displayed in beautiful, easy-to-read cards</p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          <div className="stat-box">
            <div className="stat-icon">🎯</div>
            <h3>60+</h3>
            <p>Audio Metrics Extracted</p>
          </div>
          <div className="stat-box">
            <div className="stat-icon">⚡</div>
            <h3>10s</h3>
            <p>Average Analysis Time</p>
          </div>
          <div className="stat-box">
            <div className="stat-icon">📊</div>
            <h3>6</h3>
            <p>Analysis Categories</p>
          </div>
          <div className="stat-box">
            <div className="stat-icon">🎨</div>
            <h3>100%</h3>
            <p>Interactive Visualizations</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Analyze Your Audio?</h2>
          <p>Get started now and extract comprehensive metrics from your audio files</p>
          <button className="btn-cta" onClick={onGetStarted}>
            <Mic size={24} />
            Start Free Analysis
          </button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
