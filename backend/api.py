"""
FastAPI Backend for AI Voice Analyzer
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from audio_analyzer import AdvancedAudioAnalyzer
from visualizer import AudioVisualizer
import numpy as np
import base64
import io
import json

app = FastAPI(title="AI Voice Analyzer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global analyzer instance
analyzer = None

@app.on_event("startup")
async def startup_event():
    """Initialize analyzer on startup"""
    global analyzer
    print("Loading YAMNet model...")
    analyzer = AdvancedAudioAnalyzer()
    print("Model loaded successfully!")

@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "AI Voice Analyzer API"}

@app.get("/health")
async def health():
    """Check if model is loaded"""
    return {
        "status": "ok",
        "model_loaded": analyzer is not None
    }

def safe_float(value):
    """Convert to float, handling NaN and Inf"""
    if isinstance(value, (np.floating, float)):
        if np.isnan(value) or np.isinf(value):
            return 0.0
    return float(value)

def numpy_to_json(obj):
    """Convert numpy types to JSON serializable types, handling NaN and Inf"""
    if isinstance(obj, np.ndarray):
        # Replace NaN and Inf with None or 0
        obj_clean = np.nan_to_num(obj, nan=0.0, posinf=0.0, neginf=0.0)
        return obj_clean.tolist()
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        # Handle NaN and Inf for scalar floats
        if np.isnan(obj) or np.isinf(obj):
            return 0.0
        return float(obj)
    elif isinstance(obj, dict):
        return {key: numpy_to_json(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [numpy_to_json(item) for item in obj]
    return obj

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Analyze uploaded audio file and return comprehensive metrics
    """
    if not analyzer:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    # Validate file type
    allowed_types = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/flac', 
                     'audio/ogg', 'audio/x-wav', 'audio/x-m4a']
    
    if file.content_type not in allowed_types and not any(
        file.filename.endswith(ext) for ext in ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
    ):
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Please upload audio files."
        )
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Analyze audio
        print(f"Analyzing: {file.filename}")
        results = analyzer.analyze(tmp_path)
        
        # Prepare response with serializable data
        response_data = {
            "filename": file.filename,
            "duration": safe_float(results['statistical']['signal_duration']),
            "sample_rate": int(results['sample_rate']),
            
            "statistical": {
                "duration": safe_float(results['statistical']['signal_duration']),
                "rms_energy": safe_float(results['statistical']['signal_rms']),
                "peak_amplitude": safe_float(results['statistical']['signal_peak']),
                "crest_factor": safe_float(results['statistical']['signal_crest_factor']),
                "skewness": safe_float(results['statistical']['signal_skewness']),
                "kurtosis": safe_float(results['statistical']['signal_kurtosis']),
            },
            
            "prosodic": {
                "pitch_mean": safe_float(results['prosodic']['pitch_mean']),
                "pitch_median": safe_float(results['prosodic']['pitch_median']),
                "pitch_std": safe_float(results['prosodic']['pitch_std']),
                "pitch_range": safe_float(results['prosodic']['pitch_range']),
                "pitch_iqr": safe_float(results['prosodic']['pitch_iqr']),
                "voiced_percentage": safe_float(results['prosodic']['voiced_percentage']),
                "energy_mean": safe_float(results['prosodic']['energy_mean']),
                "energy_std": safe_float(results['prosodic']['energy_std']),
                "energy_dynamic_range": safe_float(results['prosodic']['energy_dynamic_range']),
                "pitch_contour": numpy_to_json(results['prosodic']['pitch_contour'][:1000]),
                "energy_contour": numpy_to_json(results['prosodic']['energy_contour'][:1000]),
            },
            
            "spectral": {
                "spectral_centroid_mean": safe_float(results['spectral']['spectral_centroid_mean']),
                "spectral_centroid_std": safe_float(results['spectral']['spectral_centroid_std']),
                "spectral_rolloff_mean": safe_float(results['spectral']['spectral_rolloff_mean']),
                "spectral_bandwidth_mean": safe_float(results['spectral']['spectral_bandwidth_mean']),
                "spectral_flatness_mean": safe_float(results['spectral']['spectral_flatness_mean']),
                "mfcc_mean": numpy_to_json(results['spectral']['mfcc_mean']),
                "chroma_mean": numpy_to_json(results['spectral']['chroma_mean']),
                "spectral_centroids": numpy_to_json(results['spectral']['spectral_centroids'][:1000]),
                "spectral_rolloff": numpy_to_json(results['spectral']['spectral_rolloff'][:1000]),
            },
            
            "temporal": {
                "tempo": safe_float(results['temporal']['tempo']),
                "beat_count": int(len(results['temporal']['beat_frames'])),
                "zero_crossing_rate_mean": safe_float(results['temporal']['zero_crossing_rate_mean']),
                "zero_crossing_rate_std": safe_float(results['temporal']['zero_crossing_rate_std']),
                "rhythm_complexity": safe_float(results['temporal']['rhythm_complexity']),
                "onset_strength": numpy_to_json(results['temporal']['onset_strength'][:1000]),
            },
            
            "voice_quality": {
                "harmonicity": safe_float(results['voice_quality']['harmonicity']),
                "harmonic_ratio": safe_float(results['voice_quality']['harmonic_ratio']),
                "jitter": safe_float(results['voice_quality']['jitter']),
                "shimmer": safe_float(results['voice_quality']['shimmer']),
                "spectral_flux_mean": safe_float(results['voice_quality']['spectral_flux_mean']),
            },
            
            "formants": {
                "f1_mean": safe_float(results['formants']['formant_f1_mean']),
                "f2_mean": safe_float(results['formants']['formant_f2_mean']),
                "f3_mean": safe_float(results['formants']['formant_f3_mean']),
                "f1_std": safe_float(results['formants']['formant_f1_std']),
                "f2_std": safe_float(results['formants']['formant_f2_std']),
            },
            
            "ml_analysis": {
                "embedding_shape": [int(x) for x in results['yamnet']['embeddings'].shape],
                "num_classes": int(results['yamnet']['scores'].shape[1]),
                "pca_components": numpy_to_json(results['ml_analysis']['pca_components'][:100]),  # First 100 frames
                "explained_variance": numpy_to_json(results['ml_analysis']['explained_variance']),
                "cumulative_variance": numpy_to_json(results['ml_analysis']['cumulative_variance']),
                "top_detected_classes": results['yamnet']['top_classes'][:10]  # Top 10 instruments/sounds
            },

            "music_production": {
                "estimated_key": results['music_production']['estimated_key'],
                "key_mode": results['music_production']['key_mode'],
                "key_confidence": safe_float(results['music_production']['key_confidence']),
                "tempo_bpm": safe_float(results['music_production']['tempo_bpm']),
                "beat_count": int(results['music_production']['beat_count']),
                "beat_regularity": safe_float(results['music_production']['beat_regularity']),
                "avg_beat_interval_sec": safe_float(results['music_production']['avg_beat_interval_sec']),
                "onset_rate_per_min": safe_float(results['music_production']['onset_rate_per_min']),
                "dominant_pitch_hz": safe_float(results['music_production']['dominant_pitch_hz']),
                "dominant_note": results['music_production']['dominant_note'],
                "integrated_loudness_db": safe_float(results['music_production']['integrated_loudness_db']),
                "peak_loudness_db": safe_float(results['music_production']['peak_loudness_db']),
                "dynamic_range_db": safe_float(results['music_production']['dynamic_range_db']),
                "harmonic_content_pct": safe_float(results['music_production']['harmonic_content_pct']),
                "percussive_content_pct": safe_float(results['music_production']['percussive_content_pct']),
                "spectral_balance": results['music_production']['spectral_balance'],
                "chroma_profile": numpy_to_json(results['music_production']['chroma_profile']),
                "segment_loudness_db": numpy_to_json(results['music_production']['segment_loudness_db']),
                "detected_instruments": results['music_production']['detected_instruments'],
                "primary_instrument": results['music_production'].get('primary_instrument'),
                "primary_instrument_confidence": safe_float(results['music_production'].get('primary_instrument_confidence', 0)),
                "all_detected_sounds": results['music_production'].get('all_detected_sounds', []),
                "production_insights": results['music_production']['production_insights'],
            },

            "advanced_analysis": {
                "time_signature": results['advanced_analysis']['time_signature'],
                "time_signature_confidence": safe_float(results['advanced_analysis']['time_signature_confidence']),
                "estimated_chords": results['advanced_analysis']['estimated_chords'],
                "tonnetz_mean": numpy_to_json(results['advanced_analysis']['tonnetz_mean']),
                "structural_sections": results['advanced_analysis']['structural_sections'],
                "novelty_curve": numpy_to_json(results['advanced_analysis']['novelty_curve']),
                "melodic_range_semitones": safe_float(results['advanced_analysis']['melodic_range_semitones']),
                "mean_interval_semitones": safe_float(results['advanced_analysis']['mean_interval_semitones']),
                "melodic_contour": results['advanced_analysis']['melodic_contour'],
                "ascending_pct": safe_float(results['advanced_analysis']['ascending_pct']),
                "descending_pct": safe_float(results['advanced_analysis']['descending_pct']),
                "snr_db": safe_float(results['advanced_analysis']['snr_db']),
                "cepstral_peak_prominence_db": safe_float(results['advanced_analysis']['cepstral_peak_prominence_db']),
                "harmonic_entropy": safe_float(results['advanced_analysis']['harmonic_entropy']),
                "polyphony_density": safe_float(results['advanced_analysis']['polyphony_density']),
                "syncopation_index": safe_float(results['advanced_analysis']['syncopation_index']),
                "tempo_bpm": safe_float(results['advanced_analysis']['tempo_bpm']),
                "secondary_tempo_bpm": safe_float(results['advanced_analysis']['secondary_tempo_bpm']),
                "timbre_clusters_pct": numpy_to_json(results['advanced_analysis']['timbre_clusters_pct']),
                "timbre_labels": results['advanced_analysis']['timbre_labels'],
                "embedding_stability": safe_float(results['advanced_analysis']['embedding_stability']),
                "advanced_insights": results['advanced_analysis']['advanced_insights'],
            },
            
            # Waveform data (sampled)
            "waveform": {
                "data": numpy_to_json(results['raw_audio'][::100][:5000]),  # Downsample for display
                "time_step": 100 / results['sample_rate']
            }
        }
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        # Clean up on error
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        
        # Print detailed error for debugging
        import traceback
        print("=" * 60)
        print("ERROR during analysis:")
        print(str(e))
        print("-" * 60)
        traceback.print_exc()
        print("=" * 60)
        
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/metrics-info")
async def get_metrics_info():
    """Get information about all available metrics"""
    return {
        "categories": {
            "statistical": [
                "duration", "rms_energy", "peak_amplitude", "crest_factor", 
                "skewness", "kurtosis"
            ],
            "prosodic": [
                "pitch_mean", "pitch_median", "pitch_std", "pitch_range", 
                "pitch_iqr", "voiced_percentage", "energy_mean", "energy_std",
                "energy_dynamic_range"
            ],
            "spectral": [
                "spectral_centroid", "spectral_rolloff", "spectral_bandwidth",
                "spectral_flatness", "mfcc", "chroma"
            ],
            "temporal": [
                "tempo", "beat_count", "zero_crossing_rate", "rhythm_complexity"
            ],
            "voice_quality": [
                "harmonicity", "harmonic_ratio", "jitter", "shimmer", 
                "spectral_flux"
            ],
            "formants": [
                "f1_mean", "f2_mean", "f3_mean"
            ],
            "ml_analysis": [
                "yamnet_embeddings", "pca_components", "explained_variance"
            ],
            "music_production": [
                "estimated_key", "tempo_bpm", "beat_regularity", "dynamic_range_db",
                "harmonic_content_pct", "spectral_balance", "chroma_profile",
                "detected_instruments", "production_insights"
            ],
            "advanced_analysis": [
                "time_signature", "estimated_chords", "structural_sections",
                "novelty_curve", "tonnetz_mean", "timbre_clusters",
                "snr_db", "syncopation_index", "melodic_contour", "advanced_insights"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
