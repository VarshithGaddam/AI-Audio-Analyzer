import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';
import './FileUpload.css';

const FileUpload = ({ onFileUpload, disabled }) => {
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    // Validate file type
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/flac', 'audio/ogg', 'audio/x-m4a'];
    const validExtensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a'];
    
    const isValid = validTypes.includes(file.type) || 
                    validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));

    if (!isValid) {
      alert('Please upload a valid audio file (WAV, MP3, FLAC, OGG, M4A)');
      return;
    }

    setSelectedFile(file);
    onFileUpload(file);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-area ${dragActive ? 'drag-active' : ''} ${disabled ? 'disabled' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".wav,.mp3,.flac,.ogg,.m4a,audio/*"
          onChange={handleChange}
          disabled={disabled}
          style={{ display: 'none' }}
        />
        
        <Upload size={56} className="upload-icon" strokeWidth={1.5} />
        <h3>Drop your audio file here or click to browse</h3>
        <p>Analyze your audio with advanced machine learning</p>
        
        <div className="format-badges">
          <span className="format-badge">WAV</span>
          <span className="format-badge">MP3</span>
          <span className="format-badge">FLAC</span>
          <span className="format-badge">OGG</span>
          <span className="format-badge">M4A</span>
        </div>
        
        {selectedFile && (
          <div className="selected-file">
            <div className="file-info">
              <div className="file-icon">🎵</div>
              <div className="file-details">
                <h4>{selectedFile.name}</h4>
                <p className="file-size">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUpload;
