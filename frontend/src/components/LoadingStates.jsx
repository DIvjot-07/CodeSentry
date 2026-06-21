import React from 'react';

export function ScanningAnimation() {
  return (
    <div className="scanning-overlay">
      <div className="scanning-overlay__radar">
        <div className="scanning-overlay__radar-ring" />
        <div className="scanning-overlay__radar-ring" />
        <div className="scanning-overlay__radar-ring" />
        <div className="scanning-overlay__radar-sweep" />
        <div className="scanning-overlay__radar-dot" />
      </div>
      <div className="scanning-overlay__text">
        Scanning for vulnerabilities
        <span className="scanning-overlay__dots">
          <span className="scanning-overlay__dot" />
          <span className="scanning-overlay__dot" />
          <span className="scanning-overlay__dot" />
        </span>
      </div>
      <div className="scanning-overlay__subtext">
        AI is analyzing your code for security issues
      </div>
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="skeleton-card" style={{ animationDelay: `${Math.random() * 0.3}s` }}>
      <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
        <div className="skeleton skeleton-chip" />
        <div className="skeleton skeleton-text" style={{ width: '30%', height: 20 }} />
        <div className="skeleton skeleton-chip" style={{ width: 60 }} />
      </div>
      <div className="skeleton skeleton-text" />
      <div className="skeleton skeleton-text" />
      <div className="skeleton skeleton-text--short" />
      <div style={{ marginTop: 16 }}>
        <div className="skeleton" style={{ height: 80, borderRadius: 8 }} />
      </div>
    </div>
  );
}
