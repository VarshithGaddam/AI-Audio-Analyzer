#!/usr/bin/env python3
"""
Streamlit Web Application for Audio Analysis
Run with: streamlit run app.py
"""

import streamlit as st
import os
import tempfile
from audio_analyzer import AdvancedAudioAnalyzer
from visualizer import AudioVisualizer
import plotly.graph_objects as go
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="AI Voice Analyzer",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🎤 AI Voice Analyzer</div>', unsafe_allow_html=True)
st.markdown("### Advanced Audio Analysis using YAMNet & ML Techniques")

# Initialize session state
if 'analyzer' not in st.session_state:
    with st.spinner("Loading YAMNet model..."):
        st.session_state.analyzer = AdvancedAudioAnalyzer()
        st.session_state.visualizer = AudioVisualizer()
    st.success("✅ Model loaded successfully!")

# File upload
uploaded_file = st.file_uploader(
    "Upload an audio file (WAV, MP3, FLAC, OGG, etc.)",
    type=['wav', 'mp3', 'flac', 'ogg', 'm4a', 'aac']
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    st.audio(uploaded_file)
    
    # Analyze button
    if st.button("🚀 Analyze Audio", type="primary"):
        with st.spinner("Analyzing audio... This may take a moment..."):
            try:
                # Perform analysis
                results = st.session_state.analyzer.analyze(tmp_path)
                st.session_state.results = results
                st.success("✅ Analysis complete!")
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")
                st.stop()
    
    # Display results if available
    if 'results' in st.session_state:
        results = st.session_state.results
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview", "🎵 Prosodic", "🌈 Spectral", 
            "⏱️ Temporal", "🎤 Voice Quality", "🤖 ML Analysis"
        ])
        
        with tab1:
            st.header("Statistical & Overall Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Duration", f"{results['statistical']['signal_duration']:.2f}s")
                st.metric("RMS Energy", f"{results['statistical']['signal_rms']:.4f}")
            
            with col2:
                st.metric("Peak Amplitude", f"{results['statistical']['signal_peak']:.4f}")
                st.metric("Crest Factor", f"{results['statistical']['signal_crest_factor']:.2f}")
            
            with col3:
                st.metric("Skewness", f"{results['statistical']['signal_skewness']:.4f}")
                st.metric("Kurtosis", f"{results['statistical']['signal_kurtosis']:.4f}")
            
            with col4:
                st.metric("Mean Pitch", f"{results['prosodic']['pitch_mean']:.2f} Hz")
                st.metric("Tempo", f"{results['temporal']['tempo']:.1f} BPM")
            
            # Waveform
            st.subheader("Waveform")
            audio = results['raw_audio']
            sr = results['sample_rate']
            time = np.linspace(0, len(audio)/sr, len(audio))
            
            fig_wave = go.Figure()
            fig_wave.add_trace(go.Scatter(x=time, y=audio, mode='lines', name='Amplitude', line=dict(width=1)))
            fig_wave.update_layout(xaxis_title='Time (s)', yaxis_title='Amplitude', height=300)
            st.plotly_chart(fig_wave, use_container_width=True)
        
        with tab2:
            st.header("Prosodic Features (Pitch & Energy)")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Pitch Mean", f"{results['prosodic']['pitch_mean']:.2f} Hz")
                st.metric("Pitch Median", f"{results['prosodic']['pitch_median']:.2f} Hz")
                st.metric("Pitch Std Dev", f"{results['prosodic']['pitch_std']:.2f} Hz")
            
            with col2:
                st.metric("Pitch Range", f"{results['prosodic']['pitch_range']:.2f} Hz")
                st.metric("Pitch IQR", f"{results['prosodic']['pitch_iqr']:.2f} Hz")
                st.metric("Voiced %", f"{results['prosodic']['voiced_percentage']:.2f}%")
            
            with col3:
                st.metric("Energy Mean", f"{results['prosodic']['energy_mean']:.4f}")
                st.metric("Energy Std", f"{results['prosodic']['energy_std']:.4f}")
                st.metric("Dynamic Range", f"{results['prosodic']['energy_dynamic_range']:.2f} dB")
            
            # Pitch contour
            st.subheader("Pitch Contour (F0)")
            pitch = results['prosodic']['pitch_contour']
            pitch_time = np.linspace(0, len(audio)/sr, len(pitch))
            
            fig_pitch = go.Figure()
            fig_pitch.add_trace(go.Scatter(x=pitch_time, y=pitch, mode='lines', name='Pitch', line=dict(color='red', width=2)))
            fig_pitch.update_layout(xaxis_title='Time (s)', yaxis_title='Frequency (Hz)', height=300)
            st.plotly_chart(fig_pitch, use_container_width=True)
            
            # Energy contour
            st.subheader("Energy Contour")
            energy = results['prosodic']['energy_contour']
            energy_time = np.linspace(0, len(audio)/sr, len(energy))
            
            fig_energy = go.Figure()
            fig_energy.add_trace(go.Scatter(x=energy_time, y=energy, mode='lines', name='Energy', line=dict(color='green', width=2)))
            fig_energy.update_layout(xaxis_title='Time (s)', yaxis_title='RMS Energy', height=300)
            st.plotly_chart(fig_energy, use_container_width=True)
        
        with tab3:
            st.header("Spectral Features")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Spectral Centroid", f"{results['spectral']['spectral_centroid_mean']:.2f} Hz")
                st.metric("Spectral Rolloff", f"{results['spectral']['spectral_rolloff_mean']:.2f} Hz")
            
            with col2:
                st.metric("Spectral Bandwidth", f"{results['spectral']['spectral_bandwidth_mean']:.2f} Hz")
                st.metric("Spectral Flatness", f"{results['spectral']['spectral_flatness_mean']:.4f}")
            
            with col3:
                st.metric("MFCC Dimensions", len(results['spectral']['mfcc_mean']))
                st.metric("Chroma Dimensions", len(results['spectral']['chroma_mean']))
            
            # Mel Spectrogram
            st.subheader("Mel Spectrogram")
            mel_spec = results['spectral']['mel_spectrogram']
            
            fig_mel = go.Figure(data=go.Heatmap(z=mel_spec, colorscale='Viridis'))
            fig_mel.update_layout(xaxis_title='Time', yaxis_title='Mel Frequency', height=400)
            st.plotly_chart(fig_mel, use_container_width=True)
            
            # MFCC
            st.subheader("MFCC Features")
            mfcc = results['spectral']['mfcc_full']
            
            fig_mfcc = go.Figure(data=go.Heatmap(z=mfcc, colorscale='RdBu'))
            fig_mfcc.update_layout(xaxis_title='Time', yaxis_title='MFCC Coefficient', height=400)
            st.plotly_chart(fig_mfcc, use_container_width=True)
            
            # Spectral features over time
            st.subheader("Spectral Features Over Time")
            spec_time = np.linspace(0, len(audio)/sr, len(results['spectral']['spectral_centroids']))
            
            fig_spec = go.Figure()
            fig_spec.add_trace(go.Scatter(x=spec_time, y=results['spectral']['spectral_centroids'], 
                                         name='Centroid', line=dict(color='purple')))
            fig_spec.add_trace(go.Scatter(x=spec_time, y=results['spectral']['spectral_rolloff'], 
                                         name='Rolloff', line=dict(color='orange')))
            fig_spec.add_trace(go.Scatter(x=spec_time, y=results['spectral']['spectral_bandwidth'], 
                                         name='Bandwidth', line=dict(color='blue')))
            fig_spec.update_layout(xaxis_title='Time (s)', yaxis_title='Frequency (Hz)', height=400)
            st.plotly_chart(fig_spec, use_container_width=True)
        
        with tab4:
            st.header("Temporal & Rhythm Features")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Tempo", f"{results['temporal']['tempo']:.2f} BPM")
                st.metric("Beat Count", len(results['temporal']['beat_frames']))
            
            with col2:
                st.metric("ZCR Mean", f"{results['temporal']['zero_crossing_rate_mean']:.4f}")
                st.metric("ZCR Std", f"{results['temporal']['zero_crossing_rate_std']:.4f}")
            
            with col3:
                st.metric("Rhythm Complexity", f"{results['temporal']['rhythm_complexity']:.4f}")
            
            # Onset strength
            st.subheader("Onset Strength Envelope")
            onset = results['temporal']['onset_strength']
            onset_time = np.linspace(0, len(audio)/sr, len(onset))
            
            fig_onset = go.Figure()
            fig_onset.add_trace(go.Scatter(x=onset_time, y=onset, mode='lines', name='Onset', line=dict(color='brown', width=2)))
            fig_onset.update_layout(xaxis_title='Time (s)', yaxis_title='Onset Strength', height=300)
            st.plotly_chart(fig_onset, use_container_width=True)
            
            # Zero crossing rate
            st.subheader("Zero Crossing Rate")
            zcr = results['temporal']['zcr_contour']
            zcr_time = np.linspace(0, len(audio)/sr, len(zcr))
            
            fig_zcr = go.Figure()
            fig_zcr.add_trace(go.Scatter(x=zcr_time, y=zcr, mode='lines', name='ZCR', line=dict(color='purple', width=2)))
            fig_zcr.update_layout(xaxis_title='Time (s)', yaxis_title='Zero Crossing Rate', height=300)
            st.plotly_chart(fig_zcr, use_container_width=True)
        
        with tab5:
            st.header("Voice Quality & Formants")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Harmonicity", f"{results['voice_quality']['harmonicity']:.2f} dB")
                st.metric("Harmonic Ratio", f"{results['voice_quality']['harmonic_ratio']:.4f}")
            
            with col2:
                st.metric("Jitter", f"{results['voice_quality']['jitter']:.4f}%")
                st.metric("Shimmer", f"{results['voice_quality']['shimmer']:.4f}%")
            
            with col3:
                st.metric("Spectral Flux", f"{results['voice_quality']['spectral_flux_mean']:.6f}")
            
            # Voice quality bar chart
            st.subheader("Voice Quality Metrics")
            quality_data = {
                'Harmonicity (dB)': results['voice_quality']['harmonicity'],
                'Jitter (%)': results['voice_quality']['jitter'],
                'Shimmer (%)': results['voice_quality']['shimmer'],
                'Harmonic Ratio': results['voice_quality']['harmonic_ratio'] * 100
            }
            
            fig_quality = go.Figure(data=[
                go.Bar(x=list(quality_data.keys()), y=list(quality_data.values()),
                       marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
            ])
            fig_quality.update_layout(xaxis_title='Metric', yaxis_title='Value', height=400)
            st.plotly_chart(fig_quality, use_container_width=True)
            
            # Formants
            st.subheader("Formant Frequencies")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("F1 (First Formant)", f"{results['formants']['formant_f1_mean']:.2f} Hz",
                         delta=f"±{results['formants']['formant_f1_std']:.2f}")
            
            with col2:
                st.metric("F2 (Second Formant)", f"{results['formants']['formant_f2_mean']:.2f} Hz",
                         delta=f"±{results['formants']['formant_f2_std']:.2f}")
            
            with col3:
                st.metric("F3 (Third Formant)", f"{results['formants']['formant_f3_mean']:.2f} Hz")
            
            formant_data = {
                'F1': results['formants']['formant_f1_mean'],
                'F2': results['formants']['formant_f2_mean'],
                'F3': results['formants']['formant_f3_mean']
            }
            
            fig_formants = go.Figure(data=[
                go.Bar(x=list(formant_data.keys()), y=list(formant_data.values()),
                       marker_color=['red', 'blue', 'green'])
            ])
            fig_formants.update_layout(xaxis_title='Formant', yaxis_title='Frequency (Hz)', height=400)
            st.plotly_chart(fig_formants, use_container_width=True)
        
        with tab6:
            st.header("YAMNet & ML Analysis")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Embedding Shape", str(results['yamnet']['embeddings'].shape))
                st.metric("Audio Classes", results['yamnet']['scores'].shape[1])
            
            with col2:
                st.metric("PCA Components", results['ml_analysis']['pca_components'].shape[1])
                variance_3 = results['ml_analysis']['explained_variance'][:3].sum() * 100
                st.metric("Top 3 PC Variance", f"{variance_3:.2f}%")
            
            with col3:
                st.metric("Total Frames", results['yamnet']['embeddings'].shape[0])
            
            # PCA visualization
            st.subheader("YAMNet Embeddings - PCA Projection")
            pca_data = results['ml_analysis']['pca_components']
            pca_time = np.linspace(0, len(audio)/sr, pca_data.shape[0])
            
            fig_pca = go.Figure()
            fig_pca.add_trace(go.Scatter(x=pca_time, y=pca_data[:, 0], name='PC1', line=dict(color='cyan')))
            if pca_data.shape[1] > 1:
                fig_pca.add_trace(go.Scatter(x=pca_time, y=pca_data[:, 1], name='PC2', line=dict(color='magenta')))
            if pca_data.shape[1] > 2:
                fig_pca.add_trace(go.Scatter(x=pca_time, y=pca_data[:, 2], name='PC3', line=dict(color='yellow')))
            fig_pca.update_layout(xaxis_title='Time (s)', yaxis_title='PCA Component Value', height=400)
            st.plotly_chart(fig_pca, use_container_width=True)
            
            # PCA 2D scatter
            if pca_data.shape[1] > 1:
                st.subheader("PCA 2D Projection")
                fig_pca_2d = go.Figure(data=go.Scatter(
                    x=pca_data[:, 0], 
                    y=pca_data[:, 1],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=np.arange(len(pca_data)),
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Time")
                    )
                ))
                fig_pca_2d.update_layout(xaxis_title='PC1', yaxis_title='PC2', height=500)
                st.plotly_chart(fig_pca_2d, use_container_width=True)
            
            # Explained variance
            st.subheader("PCA Explained Variance")
            variance = results['ml_analysis']['explained_variance']
            cumulative = results['ml_analysis']['cumulative_variance']
            
            fig_var = go.Figure()
            fig_var.add_trace(go.Bar(x=list(range(1, len(variance)+1)), y=variance*100, name='Individual'))
            fig_var.add_trace(go.Scatter(x=list(range(1, len(cumulative)+1)), y=cumulative*100, 
                                        name='Cumulative', mode='lines+markers', line=dict(color='red', width=3)))
            fig_var.update_layout(xaxis_title='Principal Component', yaxis_title='Explained Variance (%)', height=400)
            st.plotly_chart(fig_var, use_container_width=True)
        
        # Download section
        st.header("📥 Download Results")
        
        # Create metrics dictionary for download
        metrics_dict = {
            'duration_seconds': float(results['statistical']['signal_duration']),
            'pitch_mean_hz': float(results['prosodic']['pitch_mean']),
            'pitch_std_hz': float(results['prosodic']['pitch_std']),
            'energy_mean': float(results['prosodic']['energy_mean']),
            'tempo_bpm': float(results['temporal']['tempo']),
            'harmonicity_db': float(results['voice_quality']['harmonicity']),
            'jitter_percent': float(results['voice_quality']['jitter']),
            'shimmer_percent': float(results['voice_quality']['shimmer']),
            'spectral_centroid_hz': float(results['spectral']['spectral_centroid_mean']),
            'f1_hz': float(results['formants']['formant_f1_mean']),
            'f2_hz': float(results['formants']['formant_f2_mean']),
            'f3_hz': float(results['formants']['formant_f3_mean']),
        }
        
        import json
        json_str = json.dumps(metrics_dict, indent=2)
        st.download_button(
            label="Download Metrics (JSON)",
            data=json_str,
            file_name="audio_metrics.json",
            mime="application/json"
        )
    
    # Clean up temp file
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)

else:
    st.info("👆 Upload an audio file to get started!")
    
    # Feature showcase
    st.markdown("### 🚀 Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎵 Prosodic Analysis**
        - Pitch (F0) extraction
        - Energy & dynamics
        - Voiced/unvoiced detection
        """)
    
    with col2:
        st.markdown("""
        **🌈 Spectral Analysis**
        - MFCC features
        - Mel spectrograms
        - Spectral characteristics
        """)
    
    with col3:
        st.markdown("""
        **🤖 ML Analysis**
        - YAMNet embeddings
        - PCA dimensionality reduction
        - Advanced voice metrics
        """)
