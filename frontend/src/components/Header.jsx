import React from 'react';

export default function Header({ screen, onReset }) {
  const getStatusText = () => {
    switch (screen) {
      case 'upload': return 'Ready to Scan';
      case 'scanning': return 'Scanning...';
      case 'results': return 'Review Findings';
      case 'verifying': return 'Verifying...';
      case 'verified': return 'Verified';
      default: return 'Ready';
    }
  };

  return (
    <header className="header">
      <div className="header__inner">
        <div className="header__logo" onClick={onReset} style={{ cursor: 'pointer' }}>
          <span className="header__shield">🛡️</span>
          <div>
            <div className="header__title">CodeSentry</div>
            <div className="header__subtitle">AI-Powered Security Code Review</div>
          </div>
        </div>
        <div className="header__right">
          {screen !== 'upload' && (
            <button className="btn btn-ghost btn-sm" onClick={onReset}>
              ← New Scan
            </button>
          )}
          <div className="header__status">
            <span className={`header__status-dot ${screen === 'scanning' || screen === 'verifying' ? 'header__status-dot--active' : ''}`} />
            <span>{getStatusText()}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
