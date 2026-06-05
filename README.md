# 🎤 AI Voice Analyzer

> Advanced audio analysis powered by YAMNet deep learning and comprehensive signal processing

Extract **60+ professional-grade audio metrics** from any audio file using cutting-edge AI, machine learning, and advanced signal processing techniques.

![AI Voice Analyzer](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15.0-FF6F00?style=for-the-badge&logo=tensorflow)

---

## ✨ Features

### 🧠 **YAMNet Deep Learning**
- 1024-dimensional audio embeddings
- Audio classification across 521 classes
- Intelligent instrument detection
- PCA analysis and dimensionality reduction

### 🎵 **Prosodic Analysis**
- Pitch (F0) extraction using pYIN algorithm
- Energy and RMS contours
- Voiced/unvoiced detection
- Dynamic range analysis

### 🌈 **Spectral Features**
- 20 MFCC coefficients
- Mel spectrograms
- 12 Chroma features
- Spectral centroid, rolloff, bandwidth, flatness

### ⏱️ **Temporal Features**
- Tempo and BPM detection
- Beat tracking and onset detection
- Rhythm complexity analysis
- Zero-crossing rate

### 🎤 **Voice Quality**
- Jitter and shimmer
- Harmonicity (HNR)
- Formant extraction (F1, F2, F3)
- Spectral flux and harmonic-percussive separation

### 🎼 **Music Production Insights**
- Key and mode detection (major/minor)
- Loudness (LUFS)
- Spectral balance across 6 frequency bands
- Harmonic vs percussive content ratio
- Production recommendations

### 🔬 **Advanced Analysis**
- Time signature estimation
- Chord detection
- Structural segmentation
- Melodic contour analysis
- Syncopation and polyphony metrics

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+** and npm
- **2GB** free disk space

### Installation

**Windows (One-Click Setup):**
```bash
setup.bat
```

**Manual Setup:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### Running the Application

**Windows (One-Click Start):**
```bash
start.bat
```

**Manual Start:**
```bash
# Terminal 1: Start Backend API
cd backend
python api.py

# Terminal 2: Start Frontend
cd frontend
npm start
```

The application will automatically open at **http://localhost:3000**

- **Backend API:** http://localhost:8000
- **Frontend UI:** http://localhost:3000

---

## 📊 Metrics Extracted

### Statistical Metrics (8)
Duration, RMS energy, peak amplitude, crest factor, skewness, kurtosis

### Prosodic Features (9)
Pitch mean/median/std/range/IQR, voiced percentage, energy mean/std/dynamic range

### Spectral Features (38)
Spectral centroid, rolloff, bandwidth, flatness, 20 MFCCs, 12 chroma coefficients

### Temporal Features (5)
Tempo, beat count, zero-crossing rate mean/std, rhythm complexity

### Voice Quality (5)
Harmonicity, HNR, jitter, shimmer, spectral flux

### Formants (5)
F1, F2, F3 frequencies and standard deviations

### ML Analysis (1034+)
1024 YAMNet embeddings, 10 PCA components, explained variance, top 10 audio classes

### Music Production (15+)
Key, mode, tempo, beat regularity, loudness, dynamic range, harmonic/percussive ratio, spectral balance (6 bands), chroma profile, detected instruments

### Advanced Analysis (20+)
Time signature, chords, structural sections, tonnetz, novelty curve, melodic contour, SNR, cepstral peak prominence, harmonic entropy, syncopation, polyphony density, timbre clusters

**Total: 60+ comprehensive metrics**

---

## 🎨 User Interface

### Modern Design
- Dark purple gradient theme
- Glassmorphism cards with glowing borders
- Smooth animations and transitions
- Responsive layout

### 8 Interactive Tabs
1. **Overview** - All metrics in organized sections
2. **Music Director** - Production insights and recommendations
3. **Advanced** - Structural and harmonic analysis
4. **Prosodic** - Pitch and energy visualizations
5. **Spectral** - Frequency domain analysis
6. **Temporal** - Rhythm and timing features
7. **Voice Quality** - Harmonicity and formant charts
8. **ML Analysis** - YAMNet classifications and PCA

### Visualizations
- Line charts for time-series data (Recharts)
- Bar charts for comparative metrics
- Interactive tooltips and legends
- Real-time analysis feedback

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **TensorFlow 2.15.0** - Deep learning framework
- **TensorFlow Hub 0.15.0** - YAMNet model hosting
- **librosa 0.10.1** - Audio analysis library
- **FastAPI 0.104.1** - Modern async web framework
- **uvicorn 0.24.0** - ASGI server
- **NumPy, SciPy, scikit-learn** - Scientific computing
- **matplotlib, seaborn, plotly** - Visualization

### Frontend
- **React 18.2.0** - UI framework
- **Axios 1.6.0** - HTTP client
- **Recharts 2.10.0** - Chart library
- **Lucide React** - Icon system

---

## 📁 Project Structure

```
yamee/
├── backend/
│   ├── api.py                  # FastAPI server
│   ├── requirements.txt        # Backend dependencies
│   └── yamnet_class_map.csv    # YAMNet class labels
├── frontend/
│   ├── public/
│   │   └── screenshots/        # App screenshots
│   └── src/
│       ├── components/         # React components
│       │   ├── FileUpload.js
│       │   ├── MetricsDisplay.js
│       │   └── LoadingSpinner.js
│       ├── pages/
│       │   └── HomePage.js     # Landing page
│       └── App.js              # Main app
├── audio_analyzer.py           # Core analysis engine
├── visualizer.py               # Report generation
├── config.py                   # Configuration settings
├── main.py                     # CLI interface
├── example_usage.py            # Usage examples
├── requirements.txt            # Full Python dependencies
├── setup.bat                   # Windows setup script
├── start.bat                   # Windows start script
└── README.md                   # This file
```

---

## 🎯 Supported Audio Formats

- **WAV** - Waveform Audio File Format
- **MP3** - MPEG Audio Layer 3
- **FLAC** - Free Lossless Audio Codec
- **OGG** - Ogg Vorbis
- **M4A** - MPEG-4 Audio

---

## 🔧 Advanced Usage

### Command Line Interface (CLI)

```bash
# Analyze audio file and generate reports
python main.py path/to/audio.wav

# Use example script
python example_usage.py
```

### Python API

```python
from audio_analyzer import AdvancedAudioAnalyzer

# Initialize analyzer
analyzer = AdvancedAudioAnalyzer()

# Analyze audio file
results = analyzer.analyze('path/to/audio.wav')

# Access metrics
print(results['prosodic']['pitch_mean'])
print(results['ml_analysis']['top_classes'])
```

### REST API

```bash
# Health check
curl http://localhost:8000/health

# Analyze audio file
curl -X POST http://localhost:8000/analyze \
  -F "file=@path/to/audio.wav"

# Get available metrics info
curl http://localhost:8000/metrics-info
```

---

## 🚨 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is not in use

### Frontend won't start
- Ensure Node.js 16+ is installed: `node --version`
- Install dependencies: `cd frontend && npm install`
- Check port 3000 is not in use

### Model download issues
- YAMNet downloads automatically on first run
- Requires stable internet connection
- ~30MB download from TensorFlow Hub

### Restart backend server
```bash
restart_backend.bat
```

### Check backend status
```bash
check_status.bat
```

---

## 📝 Configuration

Edit `config.py` to customize analysis parameters:

```python
# Audio parameters
DEFAULT_SAMPLE_RATE = 22050
PITCH_FMIN = 50  # Minimum pitch (Hz)
PITCH_FMAX = 500  # Maximum pitch (Hz)

# MFCC configuration
N_MFCC = 20
N_MELS = 128

# Tempo detection
TEMPO_MIN = 30
TEMPO_MAX = 300
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is open source and available for educational and research purposes.

---

## 🌟 Acknowledgments

- **YAMNet** - Google Research (TensorFlow Hub)
- **librosa** - Audio analysis library
- **React** - UI framework
- **FastAPI** - Modern Python web framework

---

## 📧 Contact

For questions, issues, or feedback, please open an issue on the repository.

---

<div align="center">

**Made with ❤️ and 🎵**

*Analyze Your Audio with Advanced AI*

</div>
