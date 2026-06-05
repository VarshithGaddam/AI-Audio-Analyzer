import numpy as np
import librosa
import tensorflow as tf
import tensorflow_hub as hub
from scipy import signal, stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
import os
warnings.filterwarnings('ignore')

PITCH_CLASSES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
INSTRUMENT_KEYWORDS = (
    'guitar', 'piano', 'drum', 'violin', 'cello', 'trumpet', 'saxophone', 'flute',
    'organ', 'synthesizer', 'bass', 'harp', 'clarinet', 'viola', 'trombone',
    'harmonica', 'ukulele', 'banjo', 'mandolin', 'choir', 'singing',
    'orchestra', 'brass', 'string', 'percussion', 'keyboard', 'cymbal', 'snare',
    'oboe', 'bassoon', 'piccolo', 'trumpet', 'horn', 'tuba', 'marimba', 'xylophone',
)
GENERIC_SOUND_LABELS = (
    'music', 'musical instrument', 'traditional music', 'folk music',
    'background music', 'theme music', 'soundtrack', 'melody',
)
SPECIFIC_INSTRUMENTS = (
    'flute', 'guitar', 'piano', 'drum', 'violin', 'cello', 'trumpet', 'saxophone',
    'clarinet', 'organ', 'synthesizer', 'bass', 'harp', 'viola', 'trombone',
    'oboe', 'bassoon', 'piccolo', 'harmonica', 'ukulele', 'banjo', 'mandolin',
    'marimba', 'xylophone', 'cymbal', 'snare', 'choir',
)


class AdvancedAudioAnalyzer:
    """Advanced audio analysis using YAMNet and ML techniques"""
    
    def __init__(self):
        print("Loading YAMNet model...")
        self.yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')
        print("YAMNet model loaded successfully!")
        
    def load_audio(self, audio_path, sr=22050):
        """Load audio file with proper resampling"""
        audio, sample_rate = librosa.load(audio_path, sr=sr, mono=True)
        return audio, sample_rate
    
    def extract_yamnet_features(self, audio, sr):
        """Extract embeddings and classifications from YAMNet"""
        # YAMNet expects 16kHz audio
        if sr != 16000:
            audio_16k = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        else:
            audio_16k = audio
        
        # Get YAMNet predictions
        scores, embeddings, spectrogram = self.yamnet_model(audio_16k)
        
        # Get class names
        class_names = self._get_yamnet_class_names()
        
        # Average scores across time
        mean_scores = np.mean(scores.numpy(), axis=0)
        
        # Get top 10 classes
        top_indices = mean_scores.argsort()[-10:][::-1]
        top_classes = [(class_names[i], float(mean_scores[i])) for i in top_indices]
        
        return {
            'embeddings': embeddings.numpy(),
            'scores': scores.numpy(),
            'spectrogram': spectrogram.numpy(),
            'top_classes': top_classes,
            'class_names': class_names
        }
    
    def _get_yamnet_class_names(self):
        """Get YAMNet class names from CSV"""
        import csv
        import urllib.request
        
        # Download class names if not cached
        class_map_path = 'yamnet_class_map.csv'
        if not os.path.exists(class_map_path):
            url = 'https://raw.githubusercontent.com/tensorflow/models/master/research/audioset/yamnet/yamnet_class_map.csv'
            urllib.request.urlretrieve(url, class_map_path)
        
        class_names = []
        with open(class_map_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                class_names.append(row[2])  # Display name is in column 2
        
        return class_names
    
    def extract_prosodic_features(self, audio, sr):
        """Extract prosodic features: pitch, energy, rhythm"""
        # Pitch extraction using pYIN algorithm (ML-based)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio, 
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr
        )
        
        # Remove NaN values
        f0_clean = f0[~np.isnan(f0)]
        
        prosodic = {
            'pitch_mean': np.mean(f0_clean) if len(f0_clean) > 0 else 0,
            'pitch_std': np.std(f0_clean) if len(f0_clean) > 0 else 0,
            'pitch_median': np.median(f0_clean) if len(f0_clean) > 0 else 0,
            'pitch_range': np.ptp(f0_clean) if len(f0_clean) > 0 else 0,
            'pitch_iqr': stats.iqr(f0_clean) if len(f0_clean) > 0 else 0,
            'voiced_percentage': np.mean(voiced_flag) * 100,
            'pitch_contour': f0,
            'voiced_probabilities': voiced_probs
        }
        
        # Energy/Intensity
        rms = librosa.feature.rms(y=audio)[0]
        prosodic.update({
            'energy_mean': np.mean(rms),
            'energy_std': np.std(rms),
            'energy_max': np.max(rms),
            'energy_dynamic_range': 20 * np.log10(np.max(rms) / (np.min(rms) + 1e-10)),
            'energy_contour': rms
        })
        
        return prosodic
    
    def extract_spectral_features(self, audio, sr):
        """Extract spectral characteristics using ML-friendly features"""
        # Mel-frequency cepstral coefficients (MFCC)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
        
        # Mel spectrogram
        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
        spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
        spectral_flatness = librosa.feature.spectral_flatness(y=audio)[0]
        
        return {
            'mfcc_mean': np.mean(mfcc, axis=1),
            'mfcc_std': np.std(mfcc, axis=1),
            'mfcc_delta_mean': np.mean(mfcc_delta, axis=1),
            'mfcc_delta2_mean': np.mean(mfcc_delta2, axis=1),
            'mfcc_full': mfcc,
            'mel_spectrogram': mel_spec_db,
            'chroma_mean': np.mean(chroma, axis=1),
            'chroma_std': np.std(chroma, axis=1),
            'spectral_centroid_mean': np.mean(spectral_centroids),
            'spectral_centroid_std': np.std(spectral_centroids),
            'spectral_rolloff_mean': np.mean(spectral_rolloff),
            'spectral_bandwidth_mean': np.mean(spectral_bandwidth),
            'spectral_contrast_mean': np.mean(spectral_contrast, axis=1),
            'spectral_flatness_mean': np.mean(spectral_flatness),
            'spectral_centroids': spectral_centroids,
            'spectral_rolloff': spectral_rolloff,
            'spectral_bandwidth': spectral_bandwidth,
        }
    
    def extract_temporal_features(self, audio, sr):
        """Extract temporal and rhythm features"""
        # Onset detection
        onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        
        # Tempo and rhythm
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
        
        return {
            'tempo': tempo,
            'beat_frames': beats,
            'onset_strength': onset_env,
            'zero_crossing_rate_mean': np.mean(zcr),
            'zero_crossing_rate_std': np.std(zcr),
            'rhythm_complexity': np.std(onset_env),
            'tempogram': tempogram,
            'zcr_contour': zcr
        }
    
    def extract_voice_quality_features(self, audio, sr):
        """Extract voice quality metrics"""
        # Harmonic-percussive separation
        harmonic, percussive = librosa.effects.hpss(audio)
        
        # Harmonicity ratio
        harmonic_ratio = np.sum(harmonic**2) / (np.sum(audio**2) + 1e-10)
        
        # Spectral flux
        spec = np.abs(librosa.stft(audio))
        spectral_flux = np.sqrt(np.sum(np.diff(spec, axis=1)**2, axis=0))
        
        # Jitter and shimmer approximation using signal processing
        f0, _, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=sr)
        f0_clean = f0[~np.isnan(f0)]
        
        jitter = 0
        shimmer = 0
        if len(f0_clean) > 1:
            # Period-to-period variation
            jitter = np.mean(np.abs(np.diff(f0_clean))) / np.mean(f0_clean) if np.mean(f0_clean) > 0 else 0
            
            # Amplitude variation
            rms = librosa.feature.rms(y=audio)[0]
            shimmer = np.mean(np.abs(np.diff(rms))) / np.mean(rms) if np.mean(rms) > 0 else 0
        
        return {
            'harmonic_ratio': harmonic_ratio,
            'harmonicity': 10 * np.log10(harmonic_ratio + 1e-10),
            'jitter': jitter * 100,  # percentage
            'shimmer': shimmer * 100,  # percentage
            'spectral_flux_mean': np.mean(spectral_flux),
            'spectral_flux_std': np.std(spectral_flux),
            'harmonic_component': harmonic,
            'percussive_component': percussive
        }
    
    def extract_statistical_features(self, audio, sr):
        """Extract statistical properties of the audio signal"""
        return {
            'signal_mean': np.mean(audio),
            'signal_std': np.std(audio),
            'signal_skewness': stats.skew(audio),
            'signal_kurtosis': stats.kurtosis(audio),
            'signal_rms': np.sqrt(np.mean(audio**2)),
            'signal_peak': np.max(np.abs(audio)),
            'signal_crest_factor': np.max(np.abs(audio)) / (np.sqrt(np.mean(audio**2)) + 1e-10),
            'signal_duration': len(audio) / sr
        }
    
    def extract_formant_features(self, audio, sr):
        """Extract formant frequencies using LPC analysis"""
        # Pre-emphasis filter
        pre_emphasized = librosa.effects.preemphasis(audio)
        
        # Linear Predictive Coding
        lpc_order = 12
        
        # Frame the signal
        frame_length = int(0.025 * sr)
        hop_length = int(0.010 * sr)
        
        frames = librosa.util.frame(pre_emphasized, frame_length=frame_length, hop_length=hop_length)
        
        formants_list = []
        for frame in frames.T:
            if np.sum(frame**2) > 1e-10:  # Only process non-silent frames
                # Calculate LPC coefficients
                lpc_coeffs = librosa.lpc(frame, order=lpc_order)
                
                # Find roots of LPC polynomial
                roots = np.roots(lpc_coeffs)
                roots = roots[np.imag(roots) >= 0]  # Keep only positive frequencies
                
                # Convert to frequencies
                angles = np.arctan2(np.imag(roots), np.real(roots))
                freqs = angles * (sr / (2 * np.pi))
                
                # Sort and take first 4 formants
                freqs = np.sort(freqs[freqs > 90])[:4]
                formants_list.append(freqs)
        
        # Average formants
        if len(formants_list) > 0:
            formants_array = np.array([f for f in formants_list if len(f) >= 3])
            if len(formants_array) > 0:
                return {
                    'formant_f1_mean': np.mean([f[0] for f in formants_array]),
                    'formant_f2_mean': np.mean([f[1] for f in formants_array]),
                    'formant_f3_mean': np.mean([f[2] for f in formants_array]) if len(formants_array[0]) > 2 else 0,
                    'formant_f1_std': np.std([f[0] for f in formants_array]),
                    'formant_f2_std': np.std([f[1] for f in formants_array]),
                }
        
        return {
            'formant_f1_mean': 0,
            'formant_f2_mean': 0,
            'formant_f3_mean': 0,
            'formant_f1_std': 0,
            'formant_f2_std': 0,
        }
    
    def _hz_to_note(self, freq):
        """Convert frequency in Hz to musical note name with octave."""
        if freq is None or freq <= 0 or np.isnan(freq):
            return 'N/A'
        midi = 12 * np.log2(freq / 440.0) + 69
        midi_round = int(round(midi))
        octave = midi_round // 12 - 1
        return f"{PITCH_CLASSES[midi_round % 12]}{octave}"

    def _estimate_key(self, chroma_mean):
        """Estimate musical key and mode from chroma profile."""
        chroma_norm = chroma_mean / (np.sum(chroma_mean) + 1e-10)
        best_corr = -2.0
        best_key = 'C'
        best_mode = 'major'

        for i in range(12):
            major_rotated = np.roll(MAJOR_PROFILE, i)
            minor_rotated = np.roll(MINOR_PROFILE, i)
            major_norm = major_rotated / (np.sum(major_rotated) + 1e-10)
            minor_norm = minor_rotated / (np.sum(minor_rotated) + 1e-10)
            major_corr = float(np.corrcoef(chroma_norm, major_norm)[0, 1])
            minor_corr = float(np.corrcoef(chroma_norm, minor_norm)[0, 1])
            if major_corr > best_corr:
                best_corr = major_corr
                best_key = PITCH_CLASSES[i]
                best_mode = 'major'
            if minor_corr > best_corr:
                best_corr = minor_corr
                best_key = PITCH_CLASSES[i]
                best_mode = 'minor'

        return best_key, best_mode, max(0.0, best_corr)

    def _spectral_balance(self, audio, sr):
        """Energy distribution across frequency bands (mix balance)."""
        S = np.abs(librosa.stft(audio))
        freqs = librosa.fft_frequencies(sr=sr)
        total = np.sum(S ** 2) + 1e-10
        bands = {
            'sub_bass': (20, 60),
            'bass': (60, 250),
            'low_mids': (250, 500),
            'mids': (500, 2000),
            'high_mids': (2000, 6000),
            'highs': (6000, min(12000, sr // 2)),
        }
        return {name: float(np.sum(S[mask] ** 2) / total * 100)
                for name, (lo, hi) in bands.items()
                if (mask := (freqs >= lo) & (freqs < hi)).any()}

    def _generate_production_insights(self, music):
        """Generate practical mixing notes for music directors."""
        insights = []
        tempo = music.get('tempo_bpm', 0)
        if tempo < 80:
            insights.append('Slow tempo — suitable for ballads, ambient, or emotional passages.')
        elif tempo > 140:
            insights.append('Fast tempo — energetic track; check transient clarity on drums.')
        else:
            insights.append('Mid-range tempo — versatile for pop, rock, and film scoring.')

        if music.get('beat_regularity', 0) > 0.85:
            insights.append('Very steady groove — strong rhythmic foundation for arrangement.')
        elif music.get('beat_regularity', 0) < 0.6:
            insights.append('Irregular rhythm — rubato or complex time feel detected.')

        dr = music.get('dynamic_range_db', 0)
        if dr < 8:
            insights.append('Low dynamic range — mix may sound heavily compressed; consider more contrast.')
        elif dr > 20:
            insights.append('Wide dynamics — preserve headroom; good for cinematic builds.')

        harmonic_pct = music.get('harmonic_content_pct', 0)
        if harmonic_pct > 65:
            insights.append('Harmonic-dominant — melodic instruments and vocals lead the texture.')
        elif harmonic_pct < 35:
            insights.append('Percussive-dominant — rhythm section drives the track; check punch in low-mids.')

        balance = music.get('spectral_balance', {})
        if balance.get('sub_bass', 0) > 25:
            insights.append('Heavy sub-bass — verify on full-range monitors and cinema systems.')
        if balance.get('high_mids', 0) + balance.get('highs', 0) > 40:
            insights.append('Bright mix — presence and air are strong; watch for harshness on vocals.')
        if balance.get('mids', 0) < 15:
            insights.append('Thin mids — body may be lacking; consider boosting 500 Hz–2 kHz region.')

        key = music.get('estimated_key', 'N/A')
        mode = music.get('key_mode', '')
        if key != 'N/A':
            insights.append(f'Estimated key: {key} {mode} — use for transposition and harmonic layering.')

        return insights[:6]

    def extract_music_production_features(self, audio, sr, results):
        """Features tailored for music directors and producers."""
        chroma = librosa.feature.chroma_cqt(y=audio, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        estimated_key, key_mode, key_confidence = self._estimate_key(chroma_mean)

        harmonic, percussive = librosa.effects.hpss(audio)
        harmonic_energy = np.sum(harmonic ** 2)
        percussive_energy = np.sum(percussive ** 2)
        total_energy = harmonic_energy + percussive_energy + 1e-10

        onset_env = results['temporal']['onset_strength']
        tempo_raw = results['temporal']['tempo']
        tempo_bpm = float(np.atleast_1d(tempo_raw)[0])
        beats = results['temporal']['beat_frames']
        duration = results['statistical']['signal_duration']

        beat_regularity = 0.0
        avg_beat_interval = 0.0
        if len(beats) > 2:
            beat_times = librosa.frames_to_time(beats, sr=sr)
            intervals = np.diff(beat_times)
            avg_beat_interval = float(np.mean(intervals))
            beat_regularity = float(max(0.0, min(1.0, 1 - (np.std(intervals) / (np.mean(intervals) + 1e-10)))))

        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        onset_rate = float(len(onsets) / (duration / 60.0)) if duration > 0 else 0.0

        rms = librosa.feature.rms(y=audio)[0]
        rms_db = 20 * np.log10(rms + 1e-10)
        integrated_loudness_db = float(np.mean(rms_db))
        peak_loudness_db = float(np.max(rms_db))
        dynamic_range_db = float(np.max(rms_db) - np.min(rms_db))

        segment_count = 8
        segment_len = max(1, len(rms) // segment_count)
        segment_levels = [
            float(np.mean(rms[i * segment_len:(i + 1) * segment_len]))
            for i in range(segment_count)
        ]
        segment_levels_db = (20 * np.log10(np.array(segment_levels) + 1e-10)).tolist()

        spectral_balance = self._spectral_balance(audio, sr)
        pitch_hz = results['prosodic']['pitch_mean']
        dominant_note = self._hz_to_note(pitch_hz)

        top_classes = results['yamnet']['top_classes']
        all_music_classes = [
            [name, score] for name, score in top_classes
            if any(kw in name.lower() for kw in INSTRUMENT_KEYWORDS)
            or name.lower() in GENERIC_SOUND_LABELS
        ]
        detected_instruments = [
            [name, score] for name, score in all_music_classes
            if not any(generic == name.lower() or generic in name.lower()
                       for generic in GENERIC_SOUND_LABELS
                       if generic not in ('background music',))
            and 'musical instrument' not in name.lower()
        ][:8]
        if not detected_instruments:
            detected_instruments = all_music_classes[:8]

        primary_instrument = None
        primary_confidence = 0.0
        for name, score in top_classes:
            name_lower = name.lower()
            if any(inst in name_lower for inst in SPECIFIC_INSTRUMENTS):
                if not any(generic in name_lower for generic in GENERIC_SOUND_LABELS):
                    primary_instrument = name
                    primary_confidence = float(score)
                    break

        music = {
            'estimated_key': estimated_key,
            'key_mode': key_mode,
            'key_confidence': key_confidence,
            'tempo_bpm': tempo_bpm,
            'beat_count': int(len(beats)),
            'beat_regularity': beat_regularity,
            'avg_beat_interval_sec': avg_beat_interval,
            'onset_rate_per_min': onset_rate,
            'dominant_pitch_hz': float(pitch_hz),
            'dominant_note': dominant_note,
            'integrated_loudness_db': integrated_loudness_db,
            'peak_loudness_db': peak_loudness_db,
            'dynamic_range_db': dynamic_range_db,
            'harmonic_content_pct': float(harmonic_energy / total_energy * 100),
            'percussive_content_pct': float(percussive_energy / total_energy * 100),
            'spectral_balance': spectral_balance,
            'chroma_profile': chroma_mean.tolist(),
            'segment_loudness_db': segment_levels_db,
            'detected_instruments': detected_instruments,
            'primary_instrument': primary_instrument,
            'primary_instrument_confidence': primary_confidence,
            'all_detected_sounds': all_music_classes[:10],
        }
        if primary_instrument:
            music['production_insights'] = [
                f'Primary instrument detected: {primary_instrument} ({primary_confidence * 100:.1f}% confidence).',
            ] + self._generate_production_insights(music)
        else:
            music['production_insights'] = self._generate_production_insights(music)
        return music

    def _estimate_time_signature(self, beats, onset_env, sr):
        """Estimate time signature from beat accent patterns."""
        if len(beats) < 8:
            return '4/4', 0.5
        strengths = onset_env[np.clip(beats, 0, len(onset_env) - 1)]
        scores = {}
        for beats_per_bar, label in [(3, '3/4'), (4, '4/4'), (6, '6/8')]:
            downbeats = strengths[::beats_per_bar]
            other = np.concatenate([strengths[i::beats_per_bar] for i in range(1, beats_per_bar)]) if beats_per_bar > 1 else strengths
            if len(downbeats) > 0 and len(other) > 0:
                scores[label] = float(np.mean(downbeats) / (np.mean(other) + 1e-10))
            else:
                scores[label] = 1.0
        best = max(scores, key=scores.get)
        confidence = min(0.95, max(0.4, scores[best] / (max(scores.values()) + 1e-10) * 0.7))
        return best, confidence

    def _estimate_chords(self, chroma_mean, top_n=5):
        """Match chroma profile to major/minor triad templates."""
        chroma_norm = chroma_mean / (np.sum(chroma_mean) + 1e-10)
        candidates = []
        for root in range(12):
            major = np.zeros(12)
            major[[root, (root + 4) % 12, (root + 7) % 12]] = 1.0
            minor = np.zeros(12)
            minor[[root, (root + 3) % 12, (root + 7) % 12]] = 1.0
            major_score = float(np.dot(chroma_norm, major / 3))
            minor_score = float(np.dot(chroma_norm, minor / 3))
            candidates.append((f'{PITCH_CLASSES[root]} major', major_score))
            candidates.append((f'{PITCH_CLASSES[root]} minor', minor_score))
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates[:top_n]

    def _analyze_melody(self, pitch_contour):
        """Melodic interval and contour analysis from pitch track."""
        f0 = pitch_contour[~np.isnan(pitch_contour)]
        if len(f0) < 4:
            return {
                'melodic_range_semitones': 0.0,
                'mean_interval_semitones': 0.0,
                'contour_type': 'insufficient_data',
                'ascending_pct': 0.0,
                'descending_pct': 0.0,
            }
        midi = 12 * np.log2(f0 / 440.0) + 69
        intervals = np.diff(midi)
        ascending = float(np.mean(intervals > 0.5) * 100)
        descending = float(np.mean(intervals < -0.5) * 100)
        if ascending > 55:
            contour = 'ascending'
        elif descending > 55:
            contour = 'descending'
        elif abs(ascending - descending) < 15:
            contour = 'stable'
        else:
            contour = 'varied'
        return {
            'melodic_range_semitones': float(np.ptp(midi)),
            'mean_interval_semitones': float(np.mean(np.abs(intervals))),
            'contour_type': contour,
            'ascending_pct': ascending,
            'descending_pct': descending,
        }

    def _estimate_snr(self, audio, sr):
        """Estimate signal-to-noise ratio in dB."""
        rms = librosa.feature.rms(y=audio, frame_length=2048, hop_length=512)[0]
        noise_floor = float(np.percentile(rms, 10))
        signal_level = float(np.percentile(rms, 90))
        if noise_floor <= 0:
            return 40.0
        return float(20 * np.log10(signal_level / noise_floor))

    def _estimate_cpp(self, audio, sr):
        """Cepstral Peak Prominence — voice clarity indicator."""
        spec = np.abs(librosa.stft(audio, n_fft=2048))
        log_spec = np.log(spec + 1e-10)
        cepstrum = np.fft.ifft(log_spec, axis=0).real
        quefrency = np.arange(cepstrum.shape[0])
        min_q = int(sr / 1000)
        max_q = int(sr / 80)
        region = cepstrum[min_q:max_q, :]
        if region.size == 0:
            return 0.0
        peak = np.max(region, axis=0)
        baseline = np.mean(region, axis=0)
        cpp = peak - baseline
        return float(np.median(cpp))

    def _detect_structural_sections(self, audio, sr, duration):
        """Segment audio into structural sections using chroma recurrence."""
        chroma = librosa.feature.chroma_cqt(y=audio, sr=sr)
        if chroma.shape[1] < 8:
            return [{'start': 0.0, 'end': duration, 'label': 'Full Track'}]
        k = min(6, max(2, int(duration / 30)))
        try:
            bound_frames = librosa.segment.agglomerative(chroma, k=k)
            bound_times = [0.0] + [float(t) for t in librosa.frames_to_time(bound_frames, sr=sr)]
            bound_times = sorted(set([t for t in bound_times if 0 <= t <= duration]))
            if bound_times[-1] < duration:
                bound_times.append(duration)
            sections = []
            for i in range(1, len(bound_times)):
                sections.append({
                    'start': round(bound_times[i - 1], 2),
                    'end': round(bound_times[i], 2),
                    'label': f'Section {i}',
                })
            return sections
        except Exception:
            return [{'start': 0.0, 'end': duration, 'label': 'Full Track'}]

    def _generate_advanced_insights(self, adv):
        """Expert-level production and analysis notes."""
        insights = []
        if adv.get('snr_db', 0) < 15:
            insights.append('Low SNR — noisy recording; consider denoising before mastering.')
        elif adv.get('snr_db', 0) > 35:
            insights.append('Clean signal — excellent source quality for mixing and mastering.')

        if adv.get('syncopation_index', 0) > 0.35:
            insights.append('High syncopation — off-beat accents create rhythmic complexity (jazz, funk, film scoring).')
        if adv.get('harmonic_entropy', 0) > 2.5:
            insights.append('Rich harmonic content — layered chords or polyphonic arrangement detected.')
        if adv.get('cepstral_peak_prominence_db', 0) > 8:
            insights.append('Strong cepstral peak — clear voiced signal; good for vocal-focused production.')

        contour = adv.get('melodic_contour', '')
        if contour == 'ascending':
            insights.append('Ascending melody — builds tension; effective for climactic scoring.')
        elif contour == 'descending':
            insights.append('Descending melody — resolving character; suits endings and cadences.')

        chords = adv.get('estimated_chords', [])
        if chords:
            insights.append(f"Likely harmonic center: {chords[0][0]} — anchor for arrangement and reharmonization.")

        sections = adv.get('structural_sections', [])
        if len(sections) > 2:
            insights.append(f'{len(sections)} structural sections detected — map verse/chorus/bridge for editing.')

        if adv.get('secondary_tempo_bpm', 0) > 0:
            ratio = adv.get('tempo_bpm', 0) / (adv['secondary_tempo_bpm'] + 1e-10)
            if 1.9 < ratio < 2.1:
                insights.append('Half-time feel detected — consider dual-tempo arrangement options.')

        return insights[:8]

    def extract_advanced_analysis(self, audio, sr, results):
        """Advanced DSP, music theory, and ML techniques for directors and engineers."""
        duration = results['statistical']['signal_duration']
        chroma = librosa.feature.chroma_cqt(y=audio, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        harmonic, _ = librosa.effects.hpss(audio)

        onset_env = results['temporal']['onset_strength']
        beats = results['temporal']['beat_frames']
        tempo_bpm = float(np.atleast_1d(results['temporal']['tempo'])[0])

        time_sig, time_sig_conf = self._estimate_time_signature(beats, onset_env, sr)
        estimated_chords = self._estimate_chords(chroma_mean)
        melody = self._analyze_melody(results['prosodic']['pitch_contour'])
        snr_db = self._estimate_snr(audio, sr)
        cpp = self._estimate_cpp(audio, sr)
        sections = self._detect_structural_sections(audio, sr, duration)

        tonnetz = librosa.feature.tonnetz(y=harmonic, sr=sr)
        tonnetz_mean = np.mean(tonnetz, axis=1).tolist()

        chroma_entropy = float(-np.sum(chroma_mean * np.log(chroma_mean + 1e-10)))
        polyphony_density = float(np.std(chroma, axis=1).mean())

        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        beat_set = set(int(b) for b in beats)
        off_beat_onsets = sum(1 for o in onsets if not any(abs(o - b) < 3 for b in beat_set))
        syncopation_index = float(off_beat_onsets / (len(onsets) + 1e-10))

        tempogram = results['temporal']['tempogram']
        tempogram_mean = np.mean(tempogram, axis=1)
        peak_idx = tempogram_mean.argsort()[-2:][::-1]
        tempi = librosa.tempo_frequencies(tempogram.shape[0], sr=sr)
        secondary_tempo = float(tempi[peak_idx[1]]) if len(peak_idx) > 1 else tempo_bpm

        novelty = librosa.onset.onset_strength(y=audio, sr=sr, aggregate=np.median)
        step = max(1, len(novelty) // 200)
        novelty_sampled = novelty[::step].tolist()

        mfcc = results['spectral']['mfcc_full'].T
        timbre_clusters_pct = [33.3, 33.3, 33.4]
        timbre_labels = ['Timbre A', 'Timbre B', 'Timbre C']
        if mfcc.shape[0] >= 12:
            k = min(3, mfcc.shape[0])
            km = KMeans(n_clusters=k, random_state=0, n_init=10)
            labels = km.fit_predict(mfcc)
            timbre_clusters_pct = [float(np.mean(labels == i) * 100) for i in range(k)]
            centroids = km.cluster_centers_[:, 0]
            order = np.argsort(centroids)
            label_names = ['Dark/Warm', 'Balanced', 'Bright/Sharp']
            timbre_labels = [label_names[i] if i < 3 else f'Cluster {i}' for i in order[:k]]

        embedding_var = float(np.var(results['yamnet']['embeddings']))
        embedding_stability = float(1.0 / (1.0 + embedding_var))

        advanced = {
            'time_signature': time_sig,
            'time_signature_confidence': time_sig_conf,
            'estimated_chords': estimated_chords,
            'tonnetz_mean': tonnetz_mean,
            'structural_sections': sections,
            'novelty_curve': novelty_sampled,
            'melodic_range_semitones': melody['melodic_range_semitones'],
            'mean_interval_semitones': melody['mean_interval_semitones'],
            'melodic_contour': melody['contour_type'],
            'ascending_pct': melody['ascending_pct'],
            'descending_pct': melody['descending_pct'],
            'snr_db': snr_db,
            'cepstral_peak_prominence_db': cpp,
            'harmonic_entropy': chroma_entropy,
            'polyphony_density': polyphony_density,
            'syncopation_index': syncopation_index,
            'tempo_bpm': tempo_bpm,
            'secondary_tempo_bpm': secondary_tempo,
            'timbre_clusters_pct': timbre_clusters_pct,
            'timbre_labels': timbre_labels,
            'embedding_stability': embedding_stability,
        }
        advanced['advanced_insights'] = self._generate_advanced_insights(advanced)
        return advanced

    def apply_ml_dimensionality_reduction(self, yamnet_embeddings):
        """Apply PCA to YAMNet embeddings for visualization"""
        scaler = StandardScaler()
        embeddings_scaled = scaler.fit_transform(yamnet_embeddings)
        
        pca = PCA(n_components=min(10, embeddings_scaled.shape[1]))
        embeddings_pca = pca.fit_transform(embeddings_scaled)
        
        return {
            'pca_components': embeddings_pca,
            'explained_variance': pca.explained_variance_ratio_,
            'cumulative_variance': np.cumsum(pca.explained_variance_ratio_)
        }
    
    def analyze(self, audio_path):
        """Perform complete analysis on audio file"""
        print(f"\nAnalyzing: {audio_path}")
        print("=" * 60)
        
        # Load audio
        audio, sr = self.load_audio(audio_path)
        print(f"✓ Audio loaded: {len(audio)/sr:.2f}s @ {sr}Hz")
        
        results = {}
        
        # YAMNet features
        print("✓ Extracting YAMNet embeddings...")
        results['yamnet'] = self.extract_yamnet_features(audio, sr)
        
        # Prosodic features
        print("✓ Extracting prosodic features (pitch, energy)...")
        results['prosodic'] = self.extract_prosodic_features(audio, sr)
        
        # Spectral features
        print("✓ Extracting spectral features (MFCC, mel-spectrogram)...")
        results['spectral'] = self.extract_spectral_features(audio, sr)
        
        # Temporal features
        print("✓ Extracting temporal features (tempo, rhythm)...")
        results['temporal'] = self.extract_temporal_features(audio, sr)
        
        # Voice quality
        print("✓ Extracting voice quality metrics...")
        results['voice_quality'] = self.extract_voice_quality_features(audio, sr)
        
        # Statistical features
        print("✓ Extracting statistical features...")
        results['statistical'] = self.extract_statistical_features(audio, sr)
        
        # Formant analysis
        print("✓ Extracting formant frequencies...")
        results['formants'] = self.extract_formant_features(audio, sr)
        
        # ML dimensionality reduction
        print("✓ Applying ML dimensionality reduction...")
        results['ml_analysis'] = self.apply_ml_dimensionality_reduction(results['yamnet']['embeddings'])

        # Music production analysis
        print("✓ Extracting music production features...")
        results['music_production'] = self.extract_music_production_features(audio, sr, results)

        # Advanced analysis (structure, harmony, timbre, DSP)
        print("✓ Running advanced analysis (structure, harmony, timbre)...")
        results['advanced_analysis'] = self.extract_advanced_analysis(audio, sr, results)
        
        # Store raw audio for visualization
        results['raw_audio'] = audio
        results['sample_rate'] = sr
        
        print("\n✓ Analysis complete!")
        print("=" * 60)
        
        return results
