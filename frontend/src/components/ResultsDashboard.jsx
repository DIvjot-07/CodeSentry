import React from 'react';
import FindingCard from './FindingCard';
import SeverityChip from './SeverityChip';

export default function ResultsDashboard({
  scanData,
  currentCode,
  fixedFindings,
  verifyData,
  onApplyFix,
  onVerify,
  isVerifying,
  isVerified,
}) {
  const { filename, scan_timestamp, findings, severity_summary, language } = scanData;
  const fixCount = fixedFindings.size;
  const totalFindings = findings.length;

  // Build verification result map
  const verifyMap = {};
  if (verifyData?.results) {
    verifyData.results.forEach(r => {
      verifyMap[r.finding_id] = r.resolved;
    });
  }

  const formatTimestamp = (ts) => {
    try {
      return new Date(ts).toLocaleString();
    } catch {
      return ts;
    }
  };

  return (
    <div className="results-dashboard" style={{ animation: 'fadeIn 0.5s ease-out' }}>
      {/* Results Header */}
      <div className="results-header card">
        <div className="results-header__info">
          <div className="results-header__file">
            <span className="results-header__file-icon">📄</span>
            <div>
              <h2 className="results-header__filename">{filename}</h2>
              <span className="results-header__timestamp">{formatTimestamp(scan_timestamp)}</span>
            </div>
          </div>
          <div className="results-header__language-badge">{language}</div>
        </div>

        <div className="results-header__summary">
          {Object.entries(severity_summary)
            .sort(([a], [b]) => {
              const order = { Critical: 0, High: 1, Medium: 2, Low: 3 };
              return (order[a] ?? 9) - (order[b] ?? 9);
            })
            .map(([severity, count]) => (
              <div key={severity} className="results-header__stat">
                <SeverityChip severity={severity} />
                <span className="results-header__count">{count}</span>
              </div>
            ))
          }
          <div className="results-header__total">
            {totalFindings} {totalFindings === 1 ? 'issue' : 'issues'} found
          </div>
        </div>
      </div>

      {/* Findings List */}
      <div className="findings-list">
        {findings.map((finding, index) => (
          <FindingCard
            key={finding.id}
            finding={finding}
            index={index}
            isFixed={fixedFindings.has(finding.id)}
            isResolved={verifyMap[finding.id]}
            isVerified={isVerified}
            onApplyFix={onApplyFix}
          />
        ))}
      </div>

      {/* Verify CTA */}
      {!isVerified && (
        <div className="verify-cta">
          <button
            className="btn btn-primary btn-lg verify-btn"
            onClick={onVerify}
            disabled={fixCount === 0 || isVerifying}
          >
            {isVerifying ? (
              <>
                <span className="verify-btn__spinner" />
                Verifying...
              </>
            ) : (
              <>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 8 }}>
                  <polyline points="20 6 9 17 4 12" />
                </svg>
                Verify All Fixes ({fixCount}/{totalFindings})
              </>
            )}
          </button>
          {fixCount === 0 && (
            <p className="verify-cta__hint">Apply at least one fix to enable verification</p>
          )}
        </div>
      )}

      {/* Verification Summary */}
      {isVerified && verifyData && (
        <div className="verify-summary card" style={{ animation: 'slideUp 0.4s ease-out' }}>
          <h3 className="verify-summary__title">✅ Verification Complete</h3>
          <div className="verify-summary__stats">
            <div className="verify-summary__stat verify-summary__stat--resolved">
              <span className="verify-summary__stat-number">
                {verifyData.results.filter(r => r.resolved).length}
              </span>
              <span>Resolved</span>
            </div>
            <div className="verify-summary__stat verify-summary__stat--unresolved">
              <span className="verify-summary__stat-number">
                {verifyData.results.filter(r => !r.resolved).length}
              </span>
              <span>Unresolved</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
