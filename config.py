"""
Configuration file for Advanced Audio Analyzer
Customize analysis parameters here
"""

# Audio Loading
DEFAULT_SAMPLE_RATE = 22050  # Hz
YAMNET_SAMPLE_RATE = 16000   # YAMNet requires 16kHz

# Pitch Detection (pYIN algorithm)
PITCH_FMIN = 50   # Minimum frequency (Hz) - lower for male voices
PITCH_FMAX = 500  # Maximum frequency (Hz) - higher for female voices

# MFCC Configuration
N_MFCC = 20           # Number of MFCC coefficients
N_MELS = 128          # Number of mel bands
N_FFT = 2048          # FFT window size
HOP_LENGTH = 512      # Hop length for STFT

# Formant Analysis
LPC_ORDER = 12        # Linear Prediction Coding order
FORMANT_FRAME_LENGTH = 0.025  # Frame length in seconds
FORMANT_HOP_LENGTH = 0.010    # Hop length in seconds

# Tempo and Beat Tracking
TEMPO_MIN = 30        # Minimum tempo (BPM)
TEMPO_MAX = 300       # Maximum tempo (BPM)

# PCA Configuration
PCA_COMPONENTS = 10   # Number of PCA components to retain

# Visualization
PLOT_DPI = 300        # DPI for static plots
PLOT_STYLE = 'darkgrid'  # Seaborn style
PLOT_WIDTH = 15       # Default plot width
PLOT_HEIGHT = 10      # Default plot height

# Output
DEFAULT_OUTPUT_DIR = 'output'
PLOTS_SUBDIR = 'plots'
METRICS_FILENAME = 'audio_metrics.json'
REPORT_FILENAME = 'audio_analysis_report.html'

# Processing
ENABLE_GPU = True     # Use GPU if available
VERBOSE = True        # Print progress messages

# Advanced Settings
SPECTRAL_CONTRAST_BANDS = 6  # Number of spectral contrast bands
CHROMA_N_CHROMA = 12         # Number of chroma bins

# Feature Extraction Flags
EXTRACT_YAMNET = True
EXTRACT_PROSODIC = True
EXTRACT_SPECTRAL = True
EXTRACT_TEMPORAL = True
EXTRACT_VOICE_QUALITY = True
EXTRACT_FORMANTS = True
EXTRACT_STATISTICAL = True

# Audio Preprocessing
APPLY_PREEMPHASIS = True
PREEMPHASIS_COEF = 0.97

# Silence Detection (optional)
SILENCE_THRESHOLD = 0.01  # RMS threshold for silence
MIN_SILENCE_DURATION = 0.1  # Minimum silence duration (seconds)

# Export Settings
EXPORT_EMBEDDINGS = False  # Export raw YAMNet embeddings (large file)
EXPORT_SPECTROGRAMS = True
EXPORT_CONTOURS = True

# Streamlit App Settings
STREAMLIT_THEME = 'dark'
MAX_UPLOAD_SIZE = 200  # MB

# Model Cache
CACHE_DIR = '.model_cache'
YAMNET_MODEL_URL = 'https://tfhub.dev/google/yamnet/1'

# Supported Audio Formats
SUPPORTED_FORMATS = [
    'wav', 'mp3', 'flac', 'ogg', 'm4a', 'aac', 'wma'
]

# Metric Descriptions (for UI)
METRIC_DESCRIPTIONS = {
    'pitch_mean': 'Average fundamental frequency',
    'jitter': 'Pitch perturbation (voice quality)',
    'shimmer': 'Amplitude perturbation (voice quality)',
    'harmonicity': 'Harmonic-to-noise ratio',
    'tempo': 'Estimated beats per minute',
    'spectral_centroid': 'Spectral brightness measure',
    'formant_f1': 'First formant (vowel height)',
    'formant_f2': 'Second formant (vowel frontness)',
}

# Clinical Thresholds (for voice pathology screening)
CLINICAL_THRESHOLDS = {
    'jitter_normal': 1.0,      # % (below = normal)
    'jitter_mild': 2.0,        # % (above = abnormal)
    'shimmer_normal': 3.0,     # % (below = normal)
    'shimmer_mild': 5.0,       # % (above = abnormal)
    'hnr_normal': 15.0,        # dB (above = normal)
    'hnr_mild': 10.0,          # dB (below = abnormal)
}

# Gender-based pitch ranges (for classification)
PITCH_RANGES = {
    'male': (85, 180),      # Hz
    'female': (165, 255),   # Hz
    'child': (250, 350),    # Hz
}


def get_config():
    """Return configuration as dictionary"""
    return {
        'sample_rate': DEFAULT_SAMPLE_RATE,
        'pitch_range': (PITCH_FMIN, PITCH_FMAX),
        'n_mfcc': N_MFCC,
        'n_mels': N_MELS,
        'pca_components': PCA_COMPONENTS,
        'output_dir': DEFAULT_OUTPUT_DIR,
        'verbose': VERBOSE,
    }


def validate_config():
    """Validate configuration parameters"""
    assert PITCH_FMIN < PITCH_FMAX, "PITCH_FMIN must be less than PITCH_FMAX"
    assert N_MFCC > 0, "N_MFCC must be positive"
    assert N_MELS > 0, "N_MELS must be positive"
    assert PCA_COMPONENTS > 0, "PCA_COMPONENTS must be positive"
    assert 0 < PREEMPHASIS_COEF < 1, "PREEMPHASIS_COEF must be between 0 and 1"
    print("✓ Configuration validated")


if __name__ == '__main__':
    validate_config()
    config = get_config()
    print("Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
