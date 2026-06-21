import React, { useState, useRef, useCallback } from 'react';
import { getDemoFile } from '../utils/api';

const ACCEPTED_EXTENSIONS = ['.py', '.js', '.ts', '.java', '.go'];

const LANG_LABELS = {
  '.py': 'Python',
  '.js': 'JavaScript',
  '.ts': 'TypeScript',
  '.java': 'Java',
  '.go': 'Go',
};

export default function UploadScreen({ onScan }) {
  const [file, setFile] = useState(null);
  const [code, setCode] = useState('');
  const [dragActive, setDragActive] = useState(false);
  const [loadingDemo, setLoadingDemo] = useState(false);
  const fileInputRef = useRef(null);

  const getExtension = (name) => {
    const dot = name.lastIndexOf('.');
    return dot !== -1 ? name.substring(dot).toLowerCase() : '';
  };

  const handleFile = useCallback((f) => {
    const ext = getExtension(f.name);
    if (!ACCEPTED_EXTENSIONS.includes(ext)) {
      alert(`Unsupported file type: ${ext}\nAccepted: ${ACCEPTED_EXTENSIONS.join(', ')}`);
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      setFile(f);
      setCode(e.target.result);
    };
    reader.readAsText(f);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files?.[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, [handleFile]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setDragActive(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setDragActive(false);
  }, []);

  const handleDemoFile = useCallback(async () => {
    setLoadingDemo(true);
    try {
      const data = await getDemoFile();
      setFile({ name: data.filename, size: new Blob([data.code]).size });
      setCode(data.code);
    } catch (err) {
      alert('Failed to load demo file: ' + err.message);
    } finally {
      setLoadingDemo(false);
    }
  }, []);

  const extension = file ? getExtension(file.name) : '';
  const language = LANG_LABELS[extension] || '';

  return (
    <div className="upload-screen" style={{ animation: 'fadeIn 0.6s ease-out' }}>
      <div className="upload-screen__hero">
        <h1 className="upload-screen__title">
          Scan Your Code for <span className="text-gradient">Security Vulnerabilities</span>
        </h1>
        <p className="upload-screen__desc">
          Upload a source file and let AI analyze it for security issues, explain risks in plain language, and suggest fixes.
        </p>
      </div>

      <div
        className={`upload-zone ${dragActive ? 'upload-zone--active' : ''} ${file ? 'upload-zone--has-file' : ''}`}
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept={ACCEPTED_EXTENSIONS.join(',')}
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
          style={{ display: 'none' }}
        />

        {!file ? (
          <>
            <div className="upload-zone__icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            <p className="upload-zone__text">Drop your code file here</p>
            <p className="upload-zone__subtext">or click to browse</p>
            <p className="upload-zone__formats">{ACCEPTED_EXTENSIONS.join('  •  ')}</p>
          </>
        ) : (
          <div className="upload-zone__file-info">
            <div className="upload-zone__file-icon">📄</div>
            <div>
              <p className="upload-zone__filename">{file.name}</p>
              <div className="upload-zone__meta">
                <span className="upload-zone__size">{(file.size / 1024).toFixed(1)} KB</span>
                {language && <span className="upload-zone__lang-badge">{language}</span>}
              </div>
            </div>
            <button
              className="upload-zone__clear"
              onClick={(e) => { e.stopPropagation(); setFile(null); setCode(''); }}
            >
              ✕
            </button>
          </div>
        )}
      </div>

      <div className="upload-screen__actions">
        <button
          className="btn btn-primary btn-lg"
          disabled={!file}
          onClick={() => onScan(file.name, code)}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 8 }}>
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          Scan Now
        </button>

        <button
          className="btn btn-ghost"
          onClick={handleDemoFile}
          disabled={loadingDemo}
        >
          {loadingDemo ? '⏳ Loading...' : '🧪 Try Demo File'}
        </button>
      </div>
    </div>
  );
}
