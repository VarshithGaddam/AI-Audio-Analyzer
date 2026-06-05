#!/usr/bin/env python3
"""
Example usage of the Advanced Audio Analyzer
"""

from audio_analyzer import AdvancedAudioAnalyzer
from visualizer import AudioVisualizer
import sys


def analyze_audio_example(audio_path):
    """
    Example function showing how to use the analyzer
    """
    print("="*80)
    print("ADVANCED AI VOICE ANALYZER - EXAMPLE")
    print("="*80)
    
    # Step 1: Initialize the analyzer (loads YAMNet model)
    print("\n1️⃣ Initializing analyzer...")
    analyzer = AdvancedAudioAnalyzer()
    
    # Step 2: Analyze the audio file
    print("\n2️⃣ Analyzing audio file...")
    results = analyzer.analyze(audio_path)
    
    # Step 3: Access specific metrics
    print("\n3️⃣ Accessing metrics:")
    print(f"\n   📏 Duration: {results['statistical']['signal_duration']:.2f} seconds")
    print(f"   🎵 Average Pitch: {results['prosodic']['pitch_mean']:.2f} Hz")
    print(f"   🎼 Tempo: {results['temporal']['tempo']:.1f} BPM")
    print(f"   🎤 Harmonicity: {results['voice_quality']['harmonicity']:.2f} dB")
    print(f"   🔊 Energy (RMS): {results['prosodic']['energy_mean']:.4f}")
    
    # Step 4: Access advanced metrics
    print("\n4️⃣ Advanced metrics:")
    print(f"   • Jitter: {results['voice_quality']['jitter']:.4f}%")
    print(f"   • Shimmer: {results['voice_quality']['shimmer']:.4f}%")
    print(f"   • F1 Formant: {results['formants']['formant_f1_mean']:.2f} Hz")
    print(f"   • F2 Formant: {results['formants']['formant_f2_mean']:.2f} Hz")
    print(f"   • Spectral Centroid: {results['spectral']['spectral_centroid_mean']:.2f} Hz")
    
    # Step 5: YAMNet embeddings
    print("\n5️⃣ YAMNet ML Analysis:")
    print(f"   • Embedding shape: {results['yamnet']['embeddings'].shape}")
    print(f"   • Number of frames analyzed: {results['yamnet']['embeddings'].shape[0]}")
    print(f"   • PCA components: {results['ml_analysis']['pca_components'].shape[1]}")
    print(f"   • Top 3 PC variance: {results['ml_analysis']['explained_variance'][:3].sum()*100:.2f}%")
    
    # Step 6: Create visualizations
    print("\n6️⃣ Creating visualizations...")
    visualizer = AudioVisualizer()
    
    # Print comprehensive summary
    visualizer.print_metrics_summary(results)
    
    # Create interactive report
    visualizer.create_comprehensive_report(results, 'example_report.html')
    
    # Create static plots
    visualizer.create_static_plots(results, 'example_plots')
    
    print("\n✅ Analysis complete!")
    print("\n📂 Output files:")
    print("   • example_report.html (interactive)")
    print("   • example_plots/ (static images)")
    
    # Step 7: Example of accessing time-series data
    print("\n7️⃣ Time-series data available:")
    print(f"   • Pitch contour: {len(results['prosodic']['pitch_contour'])} points")
    print(f"   • Energy contour: {len(results['prosodic']['energy_contour'])} points")
    print(f"   • MFCC matrix: {results['spectral']['mfcc_full'].shape}")
    print(f"   • Mel spectrogram: {results['spectral']['mel_spectrogram'].shape}")
    
    return results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <audio_file>")
        print("\nExample:")
        print("  python example_usage.py sample.wav")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    results = analyze_audio_example(audio_file)
    
    # You can now use 'results' for further analysis
    print("\n💡 Tip: Import this module to use in your own scripts!")
