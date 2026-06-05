import React, { useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './MetricsDisplay.css';

const CHART_TICK = { fill: 'rgba(255,255,255,0.75)', fontSize: 11 };
const CHART_GRID = 'rgba(168, 85, 247, 0.25)';
const TOOLTIP_STYLE = { background: '#1a0033', border: '1px solid #a855f7', borderRadius: 8, color: '#fff' };
const CHROMA_LABELS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
const BAND_LABELS = {
  sub_bass: 'Sub Bass', bass: 'Bass', low_mids: 'Low Mids',
  mids: 'Mids', high_mids: 'High Mids', highs: 'Highs',
};

const ChartWrapper = ({ children, height = 300 }) => (
  <div className="chart-wrapper" style={{ height }}>
    <ResponsiveContainer width="100%" height="100%">
      {children}
    </ResponsiveContainer>
  </div>
);

const MetricsDisplay = ({ data }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [activeSection, setActiveSection] = useState('statistical');

  const tabs = [
    { id: 'overview', name: '📊 Overview', icon: '📊' },
    { id: 'music', name: '🎼 Music Director', icon: '🎼' },
    { id: 'advanced', name: '🔬 Advanced', icon: '🔬' },
    { id: 'prosodic', name: '🎵 Prosodic', icon: '🎵' },
    { id: 'spectral', name: '🌈 Spectral', icon: '🌈' },
    { id: 'temporal', name: '⏱️ Temporal', icon: '⏱️' },
    { id: 'voice', name: '🎤 Voice Quality', icon: '🎤' },
    { id: 'ml', name: '🤖 ML Analysis', icon: '🤖' },
  ];

  const mp = data.music_production;
  const adv = data.advanced_analysis;

  const sections = [
    {
      id: 'statistical',
      icon: '📊',
      title: 'Statistical',
      metrics: [
        { label: 'Duration', value: `${data.duration.toFixed(2)}s` },
        { label: 'Sample Rate', value: `${data.sample_rate} Hz` },
        { label: 'RMS Energy', value: data.statistical.rms_energy.toFixed(4) },
        { label: 'Peak Amplitude', value: data.statistical.peak_amplitude.toFixed(4) },
        { label: 'Crest Factor', value: data.statistical.crest_factor.toFixed(2) },
        { label: 'Skewness', value: data.statistical.skewness.toFixed(4) },
        { label: 'Kurtosis', value: data.statistical.kurtosis.toFixed(4) },
      ]
    },
    {
      id: 'prosodic',
      icon: '🎵',
      title: 'Prosodic',
      metrics: [
        { label: 'Pitch Mean', value: `${data.prosodic.pitch_mean.toFixed(2)} Hz` },
        { label: 'Pitch Median', value: `${data.prosodic.pitch_median.toFixed(2)} Hz` },
        { label: 'Pitch Std', value: `${data.prosodic.pitch_std.toFixed(2)} Hz` },
        { label: 'Pitch Range', value: `${data.prosodic.pitch_range.toFixed(2)} Hz` },
        { label: 'Voiced %', value: `${data.prosodic.voiced_percentage.toFixed(2)}%` },
        { label: 'Energy Mean', value: data.prosodic.energy_mean.toFixed(4) },
        { label: 'Dynamic Range', value: `${data.prosodic.energy_dynamic_range.toFixed(2)} dB` },
      ]
    },
    {
      id: 'spectral',
      icon: '🌈',
      title: 'Spectral',
      metrics: [
        { label: 'Spectral Centroid', value: `${data.spectral.spectral_centroid_mean.toFixed(2)} Hz` },
        { label: 'Spectral Rolloff', value: `${data.spectral.spectral_rolloff_mean.toFixed(2)} Hz` },
        { label: 'Spectral Bandwidth', value: `${data.spectral.spectral_bandwidth_mean.toFixed(2)} Hz` },
        { label: 'Spectral Flatness', value: data.spectral.spectral_flatness_mean.toFixed(4) },
        { label: 'MFCC Dimensions', value: data.spectral.mfcc_mean.length },
        { label: 'Chroma Dimensions', value: data.spectral.chroma_mean.length },
      ]
    },
    {
      id: 'temporal',
      icon: '⏱️',
      title: 'Temporal',
      metrics: [
        { label: 'Tempo', value: `${data.temporal.tempo.toFixed(2)} BPM` },
        { label: 'Beat Count', value: data.temporal.beat_count },
        { label: 'ZCR Mean', value: data.temporal.zero_crossing_rate_mean.toFixed(4) },
        { label: 'ZCR Std', value: data.temporal.zero_crossing_rate_std.toFixed(4) },
        { label: 'Rhythm Complexity', value: data.temporal.rhythm_complexity.toFixed(4) },
      ]
    },
    {
      id: 'voice',
      icon: '🎤',
      title: 'Voice Quality',
      metrics: [
        { label: 'Harmonicity', value: `${data.voice_quality.harmonicity.toFixed(2)} dB` },
        { label: 'Harmonic Ratio', value: data.voice_quality.harmonic_ratio.toFixed(4) },
        { label: 'Jitter', value: `${data.voice_quality.jitter.toFixed(4)}%` },
        { label: 'Shimmer', value: `${data.voice_quality.shimmer.toFixed(4)}%` },
        { label: 'Spectral Flux', value: data.voice_quality.spectral_flux_mean.toFixed(6) },
      ]
    },
    {
      id: 'formants',
      icon: '📢',
      title: 'Formants',
      metrics: [
        { label: 'F1 (First Formant)', value: `${data.formants.f1_mean.toFixed(2)} Hz` },
        { label: 'F1 Std Dev', value: `${data.formants.f1_std.toFixed(2)} Hz` },
        { label: 'F2 (Second Formant)', value: `${data.formants.f2_mean.toFixed(2)} Hz` },
        { label: 'F2 Std Dev', value: `${data.formants.f2_std.toFixed(2)} Hz` },
        { label: 'F3 (Third Formant)', value: `${data.formants.f3_mean.toFixed(2)} Hz` },
      ]
    },
    {
      id: 'ml',
      icon: '🤖',
      title: 'ML Analysis',
      metrics: [
        { label: 'Embedding Shape', value: `${data.ml_analysis.embedding_shape[0]} × ${data.ml_analysis.embedding_shape[1]}` },
        { label: 'Audio Classes', value: data.ml_analysis.num_classes },
        { label: 'PCA Components', value: data.ml_analysis.pca_components[0].length },
        { label: 'Top 3 PC Variance', value: `${(data.ml_analysis.cumulative_variance[2] * 100).toFixed(2)}%` },
        { label: 'Total Variance', value: `${(data.ml_analysis.cumulative_variance[data.ml_analysis.cumulative_variance.length - 1] * 100).toFixed(2)}%` },
      ]
    },
    ...(mp ? [{
      id: 'music',
      icon: '🎼',
      title: 'Music Director',
      metrics: [
        { label: 'Estimated Key', value: `${mp.estimated_key} ${mp.key_mode}` },
        { label: 'Key Confidence', value: `${(mp.key_confidence * 100).toFixed(1)}%` },
        { label: 'Tempo', value: `${mp.tempo_bpm.toFixed(1)} BPM` },
        { label: 'Beat Regularity', value: `${(mp.beat_regularity * 100).toFixed(1)}%` },
        { label: 'Dominant Note', value: mp.dominant_note },
        { label: 'Loudness (LUFS est.)', value: `${mp.integrated_loudness_db.toFixed(1)} dB` },
        { label: 'Dynamic Range', value: `${mp.dynamic_range_db.toFixed(1)} dB` },
        { label: 'Harmonic Content', value: `${mp.harmonic_content_pct.toFixed(1)}%` },
        { label: 'Percussive Content', value: `${mp.percussive_content_pct.toFixed(1)}%` },
        { label: 'Onset Rate', value: `${mp.onset_rate_per_min.toFixed(1)}/min` },
        ...(mp.primary_instrument ? [
          { label: 'Primary Instrument', value: `${mp.primary_instrument} (${(mp.primary_instrument_confidence * 100).toFixed(1)}%)` },
        ] : []),
      ]
    }] : []),
    ...(adv ? [{
      id: 'advanced',
      icon: '🔬',
      title: 'Advanced',
      metrics: [
        { label: 'Time Signature', value: adv.time_signature },
        { label: 'SNR', value: `${adv.snr_db.toFixed(1)} dB` },
        { label: 'Syncopation', value: `${(adv.syncopation_index * 100).toFixed(1)}%` },
        { label: 'Harmonic Entropy', value: adv.harmonic_entropy.toFixed(3) },
        { label: 'Melodic Range', value: `${adv.melodic_range_semitones.toFixed(1)} semitones` },
        { label: 'Melodic Contour', value: adv.melodic_contour },
        { label: 'CPP (Voice Clarity)', value: `${adv.cepstral_peak_prominence_db.toFixed(2)} dB` },
        { label: 'Secondary Tempo', value: `${adv.secondary_tempo_bpm.toFixed(1)} BPM` },
        { label: 'Polyphony Density', value: adv.polyphony_density.toFixed(4) },
        { label: 'Embedding Stability', value: `${(adv.embedding_stability * 100).toFixed(1)}%` },
      ]
    }] : []),
  ];

  const pitchData = (data.prosodic.pitch_contour || [])
    .map((value, index) => ({ time: index, pitch: isNaN(value) ? null : value }))
    .filter(d => d.pitch !== null);

  const energyData = (data.prosodic.energy_contour || [])
    .map((value, index) => ({ time: index, energy: value }));

  const spectralData = (data.spectral.spectral_centroids || [])
    .map((centroid, index) => ({
      time: index,
      centroid,
      rolloff: data.spectral.spectral_rolloff?.[index] ?? 0,
    }));

  const onsetData = (data.temporal.onset_strength || [])
    .map((value, index) => ({ time: index, strength: value }));

  const waveformData = (data.waveform?.data || [])
    .map((value, index) => ({
      time: (index * (data.waveform?.time_step || 0.0045)).toFixed(2),
      amplitude: value,
    }));

  const qualityData = [
    { name: 'Harmonicity', value: data.voice_quality.harmonicity },
    { name: 'Jitter', value: data.voice_quality.jitter },
    { name: 'Shimmer', value: data.voice_quality.shimmer },
    { name: 'HNR Ratio', value: data.voice_quality.harmonic_ratio * 100 },
  ];

  const formantData = [
    { name: 'F1', value: data.formants.f1_mean },
    { name: 'F2', value: data.formants.f2_mean },
    { name: 'F3', value: data.formants.f3_mean },
  ];

  const pcaData = (data.ml_analysis.pca_components || [])
    .map((components, index) => ({
      frame: index,
      pc1: components[0],
      pc2: components[1] || 0,
      pc3: components[2] || 0,
    }));

  const varianceData = (data.ml_analysis.explained_variance || [])
    .map((value, index) => ({
      component: `PC${index + 1}`,
      variance: parseFloat((value * 100).toFixed(2)),
      cumulative: parseFloat((data.ml_analysis.cumulative_variance[index] * 100).toFixed(2)),
    }));

  const renderMetricCard = (metric, idx) => (
    <div key={idx} className="accordion-metric-card">
      <span className="metric-label">{metric.label}</span>
      <span className="metric-value-text">{metric.value}</span>
    </div>
  );

  const renderWaveformChart = () => (
    waveformData.length > 0 && (
      <div className="chart-container">
        <h3>Waveform</h3>
        <ChartWrapper>
          <LineChart data={waveformData}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="time" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Line type="monotone" dataKey="amplitude" stroke="#c084fc" strokeWidth={2} dot={false} />
          </LineChart>
        </ChartWrapper>
      </div>
    )
  );

  const renderProsodicCharts = () => (
    <>
      <div className="chart-container">
        <h3>Pitch Contour (F0)</h3>
        <ChartWrapper>
          <LineChart data={pitchData}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="time" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Line type="monotone" dataKey="pitch" stroke="#ff6b6b" strokeWidth={2} dot={false} />
          </LineChart>
        </ChartWrapper>
      </div>
      <div className="chart-container">
        <h3>Energy Contour</h3>
        <ChartWrapper>
          <LineChart data={energyData}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="time" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Line type="monotone" dataKey="energy" stroke="#51cf66" strokeWidth={2} dot={false} />
          </LineChart>
        </ChartWrapper>
      </div>
    </>
  );

  const renderSpectralChart = () => (
    <div className="chart-container">
      <h3>Spectral Features Over Time</h3>
      <ChartWrapper>
        <LineChart data={spectralData}>
          <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
          <XAxis dataKey="time" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
          <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
          <Tooltip contentStyle={TOOLTIP_STYLE} />
          <Legend wrapperStyle={{ color: '#fff' }} />
          <Line type="monotone" dataKey="centroid" stroke="#845ef7" strokeWidth={2} name="Centroid" dot={false} />
          <Line type="monotone" dataKey="rolloff" stroke="#ff922b" strokeWidth={2} name="Rolloff" dot={false} />
        </LineChart>
      </ChartWrapper>
    </div>
  );

  const renderTemporalChart = () => (
    <div className="chart-container">
      <h3>Onset Strength Envelope</h3>
      <ChartWrapper>
        <LineChart data={onsetData}>
          <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
          <XAxis dataKey="time" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
          <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
          <Tooltip contentStyle={TOOLTIP_STYLE} />
          <Line type="monotone" dataKey="strength" stroke="#f59f00" strokeWidth={2} dot={false} />
        </LineChart>
      </ChartWrapper>
    </div>
  );

  const renderVoiceCharts = () => (
    <div className="charts-row">
      <div className="chart-container half">
        <h3>Voice Quality Metrics</h3>
        <ChartWrapper>
          <BarChart data={qualityData}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="name" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" angle={-15} textAnchor="end" height={70} />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Bar dataKey="value" fill="#20c997" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ChartWrapper>
      </div>
      <div className="chart-container half">
        <h3>Formant Frequencies</h3>
        <ChartWrapper>
          <BarChart data={formantData}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="name" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Bar dataKey="value" fill="#4c6ef5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ChartWrapper>
      </div>
    </div>
  );

  const renderFormantChart = () => (
    <div className="chart-container">
      <h3>Formant Frequencies</h3>
      <ChartWrapper>
        <BarChart data={formantData}>
          <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
          <XAxis dataKey="name" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
          <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
          <Tooltip contentStyle={TOOLTIP_STYLE} />
          <Bar dataKey="value" fill="#4c6ef5" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ChartWrapper>
    </div>
  );

  const chromaData = mp?.chroma_profile?.map((v, i) => ({
    note: CHROMA_LABELS[i], energy: parseFloat((v * 100).toFixed(2)),
  })) || [];

  const balanceData = mp?.spectral_balance
    ? Object.entries(mp.spectral_balance).map(([k, v]) => ({
        band: BAND_LABELS[k] || k, pct: parseFloat(v.toFixed(2)),
      }))
    : [];

  const textureData = mp ? [
    { name: 'Harmonic', value: mp.harmonic_content_pct },
    { name: 'Percussive', value: mp.percussive_content_pct },
  ] : [];

  const dynamicsData = mp?.segment_loudness_db?.map((v, i) => ({
    section: `Seg ${i + 1}`, loudness: parseFloat(v.toFixed(2)),
  })) || [];

  const renderMusicCharts = () => {
    if (!mp) {
      return (
        <div className="chart-container">
          <p className="tab-hint">Restart the backend and re-analyze to load Music Director features.</p>
        </div>
      );
    }
    return (
      <>
        {mp.production_insights?.length > 0 && (
          <div className="chart-container production-insights">
            <h3>Production Insights</h3>
            <ul className="insights-list">
              {mp.production_insights.map((tip, i) => (
                <li key={i}>{tip}</li>
              ))}
            </ul>
          </div>
        )}

        {mp.primary_instrument && (
          <div className="primary-instrument-badge">
            Primary Instrument: <strong>{mp.primary_instrument}</strong>
            <span> ({(mp.primary_instrument_confidence * 100).toFixed(1)}% confidence)</span>
          </div>
        )}

        {mp.detected_instruments?.length > 0 && (
          <div className="chart-container">
            <h3>Detected Instruments (specific)</h3>
            <p className="tab-hint" style={{ margin: '0 0 1rem', padding: 0 }}>
              Scores are AI confidence levels, not percentages that add to 100%. Generic labels like &quot;Music&quot; are filtered out.
            </p>
            <div className="detected-classes-grid">
              {mp.detected_instruments.map((cls, idx) => (
                <div key={idx} className="detected-class-item">
                  <div className="class-rank">#{idx + 1}</div>
                  <div className="class-info">
                    <div className="class-name">{cls[0]}</div>
                    <div className="class-confidence">
                      <div className="confidence-bar">
                        <div className="confidence-fill" style={{ width: `${(cls[1] * 100).toFixed(1)}%` }} />
                      </div>
                      <span className="confidence-text">{(cls[1] * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="charts-row">
          <div className="chart-container half">
            <h3>Chroma / Harmonic Content (Key Analysis)</h3>
            <ChartWrapper>
              <BarChart data={chromaData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="note" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="energy" fill="#f59e00" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartWrapper>
          </div>
          <div className="chart-container half">
            <h3>Frequency Balance (Mix EQ)</h3>
            <ChartWrapper>
              <BarChart data={balanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="band" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" angle={-20} textAnchor="end" height={60} />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="pct" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartWrapper>
          </div>
        </div>

        <div className="charts-row">
          <div className="chart-container half">
            <h3>Harmonic vs Percussive Texture</h3>
            <ChartWrapper>
              <BarChart data={textureData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="name" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="value" fill="#ec4899" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartWrapper>
          </div>
          <div className="chart-container half">
            <h3>Dynamic Sections (Loudness Over Time)</h3>
            <ChartWrapper>
              <LineChart data={dynamicsData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="section" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Line type="monotone" dataKey="loudness" stroke="#fbbf24" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ChartWrapper>
          </div>
        </div>
      </>
    );
  };

  const renderMLCharts = () => (
    <>
      {data.ml_analysis.top_detected_classes && (
        <div className="chart-container">
          <h3>Top Detected Sounds & Instruments</h3>
          <div className="detected-classes-grid">
            {data.ml_analysis.top_detected_classes.map((cls, idx) => (
              <div key={idx} className="detected-class-item">
                <div className="class-rank">#{idx + 1}</div>
                <div className="class-info">
                  <div className="class-name">{cls[0]}</div>
                  <div className="class-confidence">
                    <div className="confidence-bar">
                      <div className="confidence-fill" style={{ width: `${(cls[1] * 100).toFixed(1)}%` }} />
                    </div>
                    <span className="confidence-text">{(cls[1] * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      <div className="chart-container">
        <h3>YAMNet Embeddings - PCA Projection</h3>
        <ChartWrapper>
          <LineChart data={pcaData}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="frame" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Legend wrapperStyle={{ color: '#fff' }} />
            <Line type="monotone" dataKey="pc1" stroke="#0ea5e9" strokeWidth={2} name="PC1" dot={false} />
            <Line type="monotone" dataKey="pc2" stroke="#ec4899" strokeWidth={2} name="PC2" dot={false} />
            <Line type="monotone" dataKey="pc3" stroke="#fbbf24" strokeWidth={2} name="PC3" dot={false} />
          </LineChart>
        </ChartWrapper>
      </div>
      <div className="chart-container">
        <h3>Explained Variance</h3>
        <ChartWrapper>
          <BarChart data={varianceData.slice(0, 10)}>
            <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
            <XAxis dataKey="component" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
            <Tooltip contentStyle={TOOLTIP_STYLE} />
            <Legend wrapperStyle={{ color: '#fff' }} />
            <Bar dataKey="variance" fill="#8b5cf6" name="Individual" radius={[4, 4, 0, 0]} />
            <Bar dataKey="cumulative" fill="#06b6d4" name="Cumulative" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ChartWrapper>
      </div>
    </>
  );

  const TONNETZ_LABELS = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'];

  const chordData = adv?.estimated_chords?.map(([name, score]) => ({
    chord: name.replace(' major', 'maj').replace(' minor', 'min'),
    score: parseFloat((score * 100).toFixed(2)),
  })) || [];

  const tonnetzData = adv?.tonnetz_mean?.map((v, i) => ({
    dim: TONNETZ_LABELS[i] || `T${i + 1}`, value: parseFloat(v.toFixed(4)),
  })) || [];

  const noveltyData = adv?.novelty_curve?.map((v, i) => ({
    frame: i, novelty: parseFloat(v.toFixed(4)),
  })) || [];

  const timbreData = adv?.timbre_labels?.map((label, i) => ({
    name: label, pct: parseFloat((adv.timbre_clusters_pct[i] || 0).toFixed(1)),
  })) || [];

  const renderAdvancedCharts = () => {
    if (!adv) {
      return (
        <div className="chart-container">
          <p className="tab-hint">Restart the backend and re-analyze to load Advanced analysis.</p>
        </div>
      );
    }
    return (
      <>
        {adv.advanced_insights?.length > 0 && (
          <div className="chart-container production-insights">
            <h3>Advanced Expert Insights</h3>
            <ul className="insights-list">
              {adv.advanced_insights.map((tip, i) => (
                <li key={i}>{tip}</li>
              ))}
            </ul>
          </div>
        )}

        {adv.structural_sections?.length > 0 && (
          <div className="chart-container">
            <h3>Structural Segmentation (Song Sections)</h3>
            <div className="section-timeline">
              {adv.structural_sections.map((sec, i) => (
                <div key={i} className="section-block">
                  <span className="section-label">{sec.label}</span>
                  <span className="section-time">{sec.start}s – {sec.end}s</span>
                  <span className="section-dur">({(sec.end - sec.start).toFixed(1)}s)</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="charts-row">
          <div className="chart-container half">
            <h3>Chord / Harmony Detection</h3>
            <ChartWrapper>
              <BarChart data={chordData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="chord" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" angle={-25} textAnchor="end" height={70} />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="score" fill="#a855f7" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartWrapper>
          </div>
          <div className="chart-container half">
            <h3>Tonnetz Harmonic Space</h3>
            <ChartWrapper>
              <BarChart data={tonnetzData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="dim" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartWrapper>
          </div>
        </div>

        <div className="charts-row">
          <div className="chart-container half">
            <h3>Spectral Novelty (Section Changes)</h3>
            <ChartWrapper>
              <LineChart data={noveltyData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="frame" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Line type="monotone" dataKey="novelty" stroke="#f472b6" strokeWidth={2} dot={false} />
              </LineChart>
            </ChartWrapper>
          </div>
          <div className="chart-container half">
            <h3>Timbre Clusters (K-Means on MFCC)</h3>
            <ChartWrapper>
              <BarChart data={timbreData}>
                <CartesianGrid strokeDasharray="3 3" stroke={CHART_GRID} />
                <XAxis dataKey="name" tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <YAxis tick={CHART_TICK} stroke="rgba(255,255,255,0.3)" />
                <Tooltip contentStyle={TOOLTIP_STYLE} />
                <Bar dataKey="pct" fill="#fb923c" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ChartWrapper>
          </div>
        </div>
      </>
    );
  };

  const renderSectionCharts = (sectionId) => {
    switch (sectionId) {
      case 'statistical': return renderWaveformChart();
      case 'prosodic': return renderProsodicCharts();
      case 'spectral': return renderSpectralChart();
      case 'temporal': return renderTemporalChart();
      case 'voice': return renderVoiceCharts();
      case 'formants': return renderFormantChart();
      case 'ml': return renderMLCharts();
      case 'music': return renderMusicCharts();
      case 'advanced': return renderAdvancedCharts();
      default: return null;
    }
  };

  const handleTabClick = (tabId) => {
    setActiveTab(tabId);
    if (tabId === 'voice') setActiveSection('voice');
    else if (tabId !== 'overview') setActiveSection(tabId);
  };

  const handleSectionClick = (sectionId) => {
    setActiveSection(sectionId);
    if (sectionId === 'formants') setActiveTab('voice');
    else if (['statistical', 'prosodic', 'spectral', 'temporal', 'voice', 'ml', 'music', 'advanced'].includes(sectionId)) {
      setActiveTab(sectionId === 'statistical' ? 'overview' : sectionId);
    }
  };

  const renderOverview = () => {
    const activeData = sections.find(s => s.id === activeSection);
    return (
      <div className="tab-content">
        <h2>Audio Overview</h2>
        <p className="tab-hint">Select a category below to see metrics and charts. Or use the top tabs.</p>

        <div className="accordion-container">
          <div className="accordion-headers">
            {sections.map(section => (
              <div
                key={section.id}
                className={`accordion-header ${activeSection === section.id ? 'active' : ''}`}
                onClick={() => handleSectionClick(section.id)}
              >
                <span className="accordion-icon">{section.icon}</span>
                <span className="accordion-title-text">{section.title}</span>
                <span className="metric-count">{section.metrics.length} metrics</span>
              </div>
            ))}
          </div>

          {activeData && (
            <div className="accordion-content">
              <div className="accordion-metrics">
                {activeData.metrics.map((metric, idx) => renderMetricCard(metric, idx))}
              </div>
              <div className="section-charts">
                {renderSectionCharts(activeSection)}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderProsodic = () => (
    <div className="tab-content">
      <h2>Prosodic Features</h2>
      <div className="accordion-metrics">
        {sections.find(s => s.id === 'prosodic').metrics.map((m, i) => renderMetricCard(m, i))}
      </div>
      {renderProsodicCharts()}
    </div>
  );

  const renderSpectral = () => (
    <div className="tab-content">
      <h2>Spectral Features</h2>
      <div className="accordion-metrics">
        {sections.find(s => s.id === 'spectral').metrics.map((m, i) => renderMetricCard(m, i))}
      </div>
      {renderSpectralChart()}
    </div>
  );

  const renderTemporal = () => (
    <div className="tab-content">
      <h2>Temporal & Rhythm Features</h2>
      <div className="accordion-metrics">
        {sections.find(s => s.id === 'temporal').metrics.map((m, i) => renderMetricCard(m, i))}
      </div>
      {renderTemporalChart()}
    </div>
  );

  const renderVoiceQuality = () => (
    <div className="tab-content">
      <h2>Voice Quality & Formants</h2>
      <div className="accordion-metrics">
        {[
          ...sections.find(s => s.id === 'voice').metrics,
          { label: 'F1 Formant', value: `${data.formants.f1_mean.toFixed(2)} Hz` },
          { label: 'F2 Formant', value: `${data.formants.f2_mean.toFixed(2)} Hz` },
        ].map((m, i) => renderMetricCard(m, i))}
      </div>
      {renderVoiceCharts()}
    </div>
  );

  const renderMLAnalysis = () => (
    <div className="tab-content">
      <h2>YAMNet & ML Analysis</h2>
      <div className="accordion-metrics">
        {sections.find(s => s.id === 'ml').metrics.slice(0, 4).map((m, i) => renderMetricCard(m, i))}
      </div>
      {renderMLCharts()}
    </div>
  );

  const renderMusicDirector = () => (
    <div className="tab-content">
      <h2>Music Director & Production</h2>
      <p className="tab-hint">Key, tempo, mix balance, dynamics, and instrument detection for composers and music directors.</p>
      {mp ? (
        <div className="accordion-metrics">
          {sections.find(s => s.id === 'music')?.metrics.map((m, i) => renderMetricCard(m, i))}
        </div>
      ) : null}
      {renderMusicCharts()}
    </div>
  );

  const renderAdvanced = () => (
    <div className="tab-content">
      <h2>Advanced Analysis</h2>
      <p className="tab-hint">Structure segmentation, harmony, timbre clustering, SNR, syncopation, and expert DSP techniques.</p>
      {adv ? (
        <div className="accordion-metrics">
          {sections.find(s => s.id === 'advanced')?.metrics.map((m, i) => renderMetricCard(m, i))}
        </div>
      ) : null}
      {renderAdvancedCharts()}
    </div>
  );

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview': return renderOverview();
      case 'music': return renderMusicDirector();
      case 'advanced': return renderAdvanced();
      case 'prosodic': return renderProsodic();
      case 'spectral': return renderSpectral();
      case 'temporal': return renderTemporal();
      case 'voice': return renderVoiceQuality();
      case 'ml': return renderMLAnalysis();
      default: return renderOverview();
    }
  };

  return (
    <div className="metrics-display">
      <div className="tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => handleTabClick(tab.id)}
          >
            {tab.name}
          </button>
        ))}
      </div>
      {renderTabContent()}
    </div>
  );
};

export default MetricsDisplay;
