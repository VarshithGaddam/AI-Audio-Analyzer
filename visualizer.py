import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import librosa.display
import pandas as pd


class AudioVisualizer:
    """Advanced visualization for audio analysis results"""
    
    def __init__(self):
        sns.set_style("darkgrid")
        plt.rcParams['figure.figsize'] = (15, 10)
        
    def create_comprehensive_report(self, results, output_path='audio_analysis_report.html'):
        """Create interactive HTML report with all visualizations"""
        
        audio = results['raw_audio']
        sr = results['sample_rate']
        
        # Create subplots
        fig = make_subplots(
            rows=5, cols=2,
            subplot_titles=(
                'Waveform', 'Mel Spectrogram',
                'Pitch Contour', 'Energy Contour',
                'MFCC Features', 'Spectral Features',
                'YAMNet Embedding PCA', 'Voice Quality',
                'Formants & Harmonics', 'Rhythm & Tempo'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "heatmap"}],
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "heatmap"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "scatter"}, {"type": "scatter"}]
            ],
            vertical_spacing=0.08,
            horizontal_spacing=0.1
        )
        
        # 1. Waveform
        time = np.linspace(0, len(audio)/sr, len(audio))
        fig.add_trace(
            go.Scatter(x=time, y=audio, mode='lines', name='Waveform', line=dict(color='blue', width=1)),
            row=1, col=1
        )
        
        # 2. Mel Spectrogram
        mel_spec = results['spectral']['mel_spectrogram']
        fig.add_trace(
            go.Heatmap(z=mel_spec, colorscale='Viridis', name='Mel Spec'),
            row=1, col=2
        )
        
        # 3. Pitch Contour
        pitch = results['prosodic']['pitch_contour']
        pitch_time = np.linspace(0, len(audio)/sr, len(pitch))
        pitch_clean = pitch.copy()
        pitch_clean[np.isnan(pitch_clean)] = 0
        fig.add_trace(
            go.Scatter(x=pitch_time, y=pitch_clean, mode='lines', name='Pitch (Hz)', 
                      line=dict(color='red', width=2)),
            row=2, col=1
        )
        
        # 4. Energy Contour
        energy = results['prosodic']['energy_contour']
        energy_time = np.linspace(0, len(audio)/sr, len(energy))
        fig.add_trace(
            go.Scatter(x=energy_time, y=energy, mode='lines', name='Energy',
                      line=dict(color='green', width=2)),
            row=2, col=2
        )
        
        # 5. MFCC Features
        mfcc = results['spectral']['mfcc_full']
        fig.add_trace(
            go.Heatmap(z=mfcc, colorscale='RdBu', name='MFCC'),
            row=3, col=1
        )
        
        # 6. Spectral Features
        spec_time = np.linspace(0, len(audio)/sr, len(results['spectral']['spectral_centroids']))
        fig.add_trace(
            go.Scatter(x=spec_time, y=results['spectral']['spectral_centroids'], 
                      name='Centroid', line=dict(color='purple')),
            row=3, col=2
        )
        fig.add_trace(
            go.Scatter(x=spec_time, y=results['spectral']['spectral_rolloff'], 
                      name='Rolloff', line=dict(color='orange')),
            row=3, col=2
        )
        
        # 7. YAMNet Embedding PCA
        pca_data = results['ml_analysis']['pca_components']
        pca_time = np.linspace(0, len(audio)/sr, pca_data.shape[0])
        fig.add_trace(
            go.Scatter(x=pca_time, y=pca_data[:, 0], name='PCA-1',
                      line=dict(color='cyan')),
            row=4, col=1
        )
        if pca_data.shape[1] > 1:
            fig.add_trace(
                go.Scatter(x=pca_time, y=pca_data[:, 1], name='PCA-2',
                          line=dict(color='magenta')),
                row=4, col=1
            )
        
        # 8. Voice Quality
        quality_metrics = ['harmonicity', 'jitter', 'shimmer', 'spectral_flux_mean']
        quality_values = [results['voice_quality'][m] for m in quality_metrics]
        fig.add_trace(
            go.Bar(x=quality_metrics, y=quality_values, name='Quality Metrics',
                  marker_color='teal'),
            row=4, col=2
        )
        
        # 9. Formants
        formant_labels = ['F1', 'F2', 'F3']
        formant_values = [
            results['formants']['formant_f1_mean'],
            results['formants']['formant_f2_mean'],
            results['formants']['formant_f3_mean']
        ]
        fig.add_trace(
            go.Scatter(x=formant_labels, y=formant_values, mode='markers+lines',
                      name='Formants', marker=dict(size=15, color='red')),
            row=5, col=1
        )
        
        # 10. Tempo and Rhythm
        onset = results['temporal']['onset_strength']
        onset_time = np.linspace(0, len(audio)/sr, len(onset))
        fig.add_trace(
            go.Scatter(x=onset_time, y=onset, mode='lines', name='Onset Strength',
                      line=dict(color='brown', width=2)),
            row=5, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text=f"<b>Comprehensive Audio Analysis Report</b>",
            title_font_size=24,
            showlegend=True,
            height=2000,
            template='plotly_dark'
        )
        
        # Save interactive HTML
        fig.write_html(output_path)
        print(f"\n✓ Interactive report saved: {output_path}")
        
        return fig
    
    def create_static_plots(self, results, output_dir='plots'):
        """Create static matplotlib plots"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        audio = results['raw_audio']
        sr = results['sample_rate']
        
        # Figure 1: Waveform and Spectrogram
        fig, axes = plt.subplots(3, 1, figsize=(15, 10))
        
        # Waveform
        librosa.display.waveshow(audio, sr=sr, ax=axes[0], color='blue')
        axes[0].set_title('Waveform', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Amplitude')
        
        # Mel Spectrogram
        mel_spec = results['spectral']['mel_spectrogram']
        img = librosa.display.specshow(mel_spec, sr=sr, x_axis='time', y_axis='mel', ax=axes[1], cmap='viridis')
        axes[1].set_title('Mel Spectrogram', fontsize=14, fontweight='bold')
        plt.colorbar(img, ax=axes[1], format='%+2.0f dB')
        
        # MFCC
        mfcc = results['spectral']['mfcc_full']
        img2 = librosa.display.specshow(mfcc, sr=sr, x_axis='time', ax=axes[2], cmap='RdBu_r')
        axes[2].set_title('MFCC Features', fontsize=14, fontweight='bold')
        plt.colorbar(img2, ax=axes[2])
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/spectral_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_dir}/spectral_analysis.png")
        plt.close()
        
        # Figure 2: Prosodic Features
        fig, axes = plt.subplots(2, 1, figsize=(15, 8))
        
        # Pitch
        pitch = results['prosodic']['pitch_contour']
        times = librosa.times_like(pitch, sr=sr)
        axes[0].plot(times, pitch, linewidth=2, color='red', label='Pitch')
        axes[0].set_title('Pitch Contour (F0)', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Frequency (Hz)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Energy
        energy = results['prosodic']['energy_contour']
        energy_times = librosa.times_like(energy, sr=sr)
        axes[1].plot(energy_times, energy, linewidth=2, color='green', label='Energy (RMS)')
        axes[1].set_title('Energy Contour', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Time (s)')
        axes[1].set_ylabel('RMS Energy')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/prosodic_features.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_dir}/prosodic_features.png")
        plt.close()
        
        # Figure 3: Voice Quality and Formants
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Voice quality metrics
        quality_data = {
            'Harmonicity': results['voice_quality']['harmonicity'],
            'Jitter (%)': results['voice_quality']['jitter'],
            'Shimmer (%)': results['voice_quality']['shimmer'],
            'Harmonic Ratio': results['voice_quality']['harmonic_ratio']
        }
        axes[0, 0].bar(quality_data.keys(), quality_data.values(), color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        axes[0, 0].set_title('Voice Quality Metrics', fontsize=14, fontweight='bold')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Formants
        formants = {
            'F1': results['formants']['formant_f1_mean'],
            'F2': results['formants']['formant_f2_mean'],
            'F3': results['formants']['formant_f3_mean']
        }
        axes[0, 1].bar(formants.keys(), formants.values(), color=['red', 'blue', 'green'])
        axes[0, 1].set_title('Formant Frequencies', fontsize=14, fontweight='bold')
        axes[0, 1].set_ylabel('Frequency (Hz)')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Spectral features
        spec_times = librosa.times_like(results['spectral']['spectral_centroids'], sr=sr)
        axes[1, 0].plot(spec_times, results['spectral']['spectral_centroids'], label='Centroid', linewidth=2)
        axes[1, 0].plot(spec_times, results['spectral']['spectral_rolloff'], label='Rolloff', linewidth=2)
        axes[1, 0].set_title('Spectral Features Over Time', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Frequency (Hz)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # YAMNet PCA
        pca_data = results['ml_analysis']['pca_components']
        axes[1, 1].scatter(pca_data[:, 0], pca_data[:, 1] if pca_data.shape[1] > 1 else np.zeros(len(pca_data)), 
                          c=np.arange(len(pca_data)), cmap='viridis', s=50, alpha=0.6)
        axes[1, 1].set_title('YAMNet Embeddings (PCA)', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('PC1')
        axes[1, 1].set_ylabel('PC2')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/voice_quality_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_dir}/voice_quality_analysis.png")
        plt.close()
        
        # Figure 4: Rhythm and Tempo
        fig, axes = plt.subplots(2, 1, figsize=(15, 8))
        
        # Onset strength
        onset = results['temporal']['onset_strength']
        onset_times = librosa.times_like(onset, sr=sr)
        axes[0].plot(onset_times, onset, linewidth=2, color='brown')
        axes[0].set_title(f"Onset Strength (Tempo: {results['temporal']['tempo']:.1f} BPM)", 
                         fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('Onset Strength')
        axes[0].grid(True, alpha=0.3)
        
        # Zero crossing rate
        zcr = results['temporal']['zcr_contour']
        zcr_times = librosa.times_like(zcr, sr=sr)
        axes[1].plot(zcr_times, zcr, linewidth=2, color='purple')
        axes[1].set_title('Zero Crossing Rate', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Time (s)')
        axes[1].set_ylabel('ZCR')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/rhythm_analysis.png', dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_dir}/rhythm_analysis.png")
        plt.close()
    
    def print_metrics_summary(self, results):
        """Print comprehensive metrics summary"""
        print("\n" + "="*80)
        print("COMPREHENSIVE AUDIO METRICS SUMMARY".center(80))
        print("="*80)
        
        # Statistical Features
        print("\n📊 STATISTICAL FEATURES:")
        print(f"  Duration: {results['statistical']['signal_duration']:.2f} seconds")
        print(f"  Mean Amplitude: {results['statistical']['signal_mean']:.6f}")
        print(f"  Std Deviation: {results['statistical']['signal_std']:.6f}")
        print(f"  RMS Energy: {results['statistical']['signal_rms']:.6f}")
        print(f"  Peak Amplitude: {results['statistical']['signal_peak']:.6f}")
        print(f"  Crest Factor: {results['statistical']['signal_crest_factor']:.2f}")
        print(f"  Skewness: {results['statistical']['signal_skewness']:.4f}")
        print(f"  Kurtosis: {results['statistical']['signal_kurtosis']:.4f}")
        
        # Prosodic Features
        print("\n🎵 PROSODIC FEATURES (Pitch & Energy):")
        print(f"  Pitch Mean: {results['prosodic']['pitch_mean']:.2f} Hz")
        print(f"  Pitch Median: {results['prosodic']['pitch_median']:.2f} Hz")
        print(f"  Pitch Std Dev: {results['prosodic']['pitch_std']:.2f} Hz")
        print(f"  Pitch Range: {results['prosodic']['pitch_range']:.2f} Hz")
        print(f"  Pitch IQR: {results['prosodic']['pitch_iqr']:.2f} Hz")
        print(f"  Voiced Percentage: {results['prosodic']['voiced_percentage']:.2f}%")
        print(f"  Energy Mean: {results['prosodic']['energy_mean']:.6f}")
        print(f"  Energy Std Dev: {results['prosodic']['energy_std']:.6f}")
        print(f"  Energy Dynamic Range: {results['prosodic']['energy_dynamic_range']:.2f} dB")
        
        # Spectral Features
        print("\n🌈 SPECTRAL FEATURES:")
        print(f"  Spectral Centroid Mean: {results['spectral']['spectral_centroid_mean']:.2f} Hz")
        print(f"  Spectral Centroid Std: {results['spectral']['spectral_centroid_std']:.2f} Hz")
        print(f"  Spectral Rolloff Mean: {results['spectral']['spectral_rolloff_mean']:.2f} Hz")
        print(f"  Spectral Bandwidth Mean: {results['spectral']['spectral_bandwidth_mean']:.2f} Hz")
        print(f"  Spectral Flatness Mean: {results['spectral']['spectral_flatness_mean']:.6f}")
        print(f"  MFCC Coefficients: {len(results['spectral']['mfcc_mean'])} dimensions")
        print(f"  Chroma Features: {len(results['spectral']['chroma_mean'])} dimensions")
        
        # Temporal Features
        print("\n⏱️ TEMPORAL & RHYTHM FEATURES:")
        print(f"  Tempo: {results['temporal']['tempo']:.2f} BPM")
        print(f"  Beat Frames Detected: {len(results['temporal']['beat_frames'])}")
        print(f"  Zero Crossing Rate Mean: {results['temporal']['zero_crossing_rate_mean']:.6f}")
        print(f"  Zero Crossing Rate Std: {results['temporal']['zero_crossing_rate_std']:.6f}")
        print(f"  Rhythm Complexity: {results['temporal']['rhythm_complexity']:.4f}")
        
        # Voice Quality
        print("\n🎤 VOICE QUALITY METRICS:")
        print(f"  Harmonicity: {results['voice_quality']['harmonicity']:.2f} dB")
        print(f"  Harmonic Ratio: {results['voice_quality']['harmonic_ratio']:.4f}")
        print(f"  Jitter: {results['voice_quality']['jitter']:.4f}%")
        print(f"  Shimmer: {results['voice_quality']['shimmer']:.4f}%")
        print(f"  Spectral Flux Mean: {results['voice_quality']['spectral_flux_mean']:.6f}")
        print(f"  Spectral Flux Std: {results['voice_quality']['spectral_flux_std']:.6f}")
        
        # Formants
        print("\n📢 FORMANT FREQUENCIES:")
        print(f"  F1 (First Formant): {results['formants']['formant_f1_mean']:.2f} Hz (±{results['formants']['formant_f1_std']:.2f})")
        print(f"  F2 (Second Formant): {results['formants']['formant_f2_mean']:.2f} Hz (±{results['formants']['formant_f2_std']:.2f})")
        print(f"  F3 (Third Formant): {results['formants']['formant_f3_mean']:.2f} Hz")
        
        # YAMNet ML Analysis
        print("\n🤖 YAMNET ML ANALYSIS:")
        print(f"  Embedding Dimensions: {results['yamnet']['embeddings'].shape}")
        print(f"  Audio Classes Analyzed: {results['yamnet']['scores'].shape[1]}")
        print(f"  PCA Components: {results['ml_analysis']['pca_components'].shape[1]}")
        print(f"  Explained Variance (top 3 PCs): {results['ml_analysis']['explained_variance'][:3].sum()*100:.2f}%")
        
        print("\n" + "="*80)
