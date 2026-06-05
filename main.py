#!/usr/bin/env python3
"""
Advanced AI Voice Analyzer
Using YAMNet, ML approaches, and comprehensive audio feature extraction
"""

import argparse
from audio_analyzer import AdvancedAudioAnalyzer
from visualizer import AudioVisualizer
import json
import os


def save_metrics_to_json(results, output_file='audio_metrics.json'):
    """Save all metrics to JSON file"""
    metrics = {
        'statistical': results['statistical'],
        'prosodic': {
            'pitch_mean': float(results['prosodic']['pitch_mean']),
            'pitch_median': float(results['prosodic']['pitch_median']),
            'pitch_std': float(results['prosodic']['pitch_std']),
            'pitch_range': float(results['prosodic']['pitch_range']),
            'pitch_iqr': float(results['prosodic']['pitch_iqr']),
            'voiced_percentage': float(results['prosodic']['voiced_percentage']),
            'energy_mean': float(results['prosodic']['energy_mean']),
            'energy_std': float(results['prosodic']['energy_std']),
            'energy_dynamic_range': float(results['prosodic']['energy_dynamic_range']),
        },
        'spectral': {
            'spectral_centroid_mean': float(results['spectral']['spectral_centroid_mean']),
            'spectral_centroid_std': float(results['spectral']['spectral_centroid_std']),
            'spectral_rolloff_mean': float(results['spectral']['spectral_rolloff_mean']),
            'spectral_bandwidth_mean': float(results['spectral']['spectral_bandwidth_mean']),
            'spectral_flatness_mean': float(results['spectral']['spectral_flatness_mean']),
            'mfcc_mean': results['spectral']['mfcc_mean'].tolist(),
            'chroma_mean': results['spectral']['chroma_mean'].tolist(),
        },
        'temporal': {
            'tempo': float(results['temporal']['tempo']),
            'beat_count': int(len(results['temporal']['beat_frames'])),
            'zero_crossing_rate_mean': float(results['temporal']['zero_crossing_rate_mean']),
            'zero_crossing_rate_std': float(results['temporal']['zero_crossing_rate_std']),
            'rhythm_complexity': float(results['temporal']['rhythm_complexity']),
        },
        'voice_quality': {
            'harmonicity': float(results['voice_quality']['harmonicity']),
            'harmonic_ratio': float(results['voice_quality']['harmonic_ratio']),
            'jitter': float(results['voice_quality']['jitter']),
            'shimmer': float(results['voice_quality']['shimmer']),
            'spectral_flux_mean': float(results['voice_quality']['spectral_flux_mean']),
        },
        'formants': results['formants'],
        'yamnet_analysis': {
            'embedding_shape': results['yamnet']['embeddings'].shape,
            'num_classes': results['yamnet']['scores'].shape[1],
            'pca_explained_variance': results['ml_analysis']['explained_variance'].tolist(),
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"\n✓ Metrics saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Advanced AI Voice Analyzer')
    parser.add_argument('audio_file', help='Path to audio file (wav, mp3, etc.)')
    parser.add_argument('--output-dir', default='output', help='Output directory for results')
    parser.add_argument('--no-plots', action='store_true', help='Skip static plot generation')
    parser.add_argument('--no-html', action='store_true', help='Skip interactive HTML report')
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Initialize analyzer
    analyzer = AdvancedAudioAnalyzer()
    
    # Analyze audio
    results = analyzer.analyze(args.audio_file)
    
    # Initialize visualizer
    visualizer = AudioVisualizer()
    
    # Print metrics summary
    visualizer.print_metrics_summary(results)
    
    # Save metrics to JSON
    json_path = os.path.join(args.output_dir, 'audio_metrics.json')
    save_metrics_to_json(results, json_path)
    
    # Create visualizations
    if not args.no_plots:
        plots_dir = os.path.join(args.output_dir, 'plots')
        visualizer.create_static_plots(results, plots_dir)
    
    if not args.no_html:
        html_path = os.path.join(args.output_dir, 'audio_analysis_report.html')
        visualizer.create_comprehensive_report(results, html_path)
    
    print(f"\n✅ Analysis complete! Results saved to: {args.output_dir}")
    print(f"\nNext steps:")
    print(f"  - View JSON metrics: {json_path}")
    if not args.no_html:
        print(f"  - Open interactive report: {html_path}")
    if not args.no_plots:
        print(f"  - View static plots in: {plots_dir}")


if __name__ == '__main__':
    main()
