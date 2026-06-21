import React, { useState } from 'react';
import SeverityChip from './SeverityChip';
import DiffViewer from './DiffViewer';

export default function FindingCard({ finding, index, isFixed, isResolved, isVerified, onApplyFix }) {
  const [expanded, setExpanded] = useState(true);

  const getResolvedBadge = () => {
    if (!isVerified) return null;
    if (isResolved === true) {
      return <span className="badge-resolved">✅ Resolved</span>;
    }
    if (isResolved === false) {
      return <span className="badge-vulnerable">⚠️ Still Vulnerable</span>;
    }
    return null;
  };

  return (
    <div
      className={`finding-card card ${isFixed ? 'finding-card--fixed' : ''} ${isResolved === true ? 'finding-card--resolved' : ''}`}
      style={{ animation: `slideUp 0.4s ease-out ${index * 0.1}s both` }}
    >
      {/* Header Row */}
      <div className="finding-card__header" onClick={() => setExpanded(!expanded)}>
        <div className="finding-card__header-left">
          <SeverityChip severity={finding.severity} />
          <span className="finding-card__type">{finding.type}</span>
          <span className="finding-card__line">Line {finding.line}</span>
        </div>
        <div className="finding-card__header-right">
          {getResolvedBadge()}
          <span className={`finding-card__chevron ${expanded ? 'finding-card__chevron--open' : ''}`}>
            ▾
          </span>
        </div>
      </div>

      {/* Expandable Content */}
      {expanded && (
        <div className="finding-card__body">
          {/* Vulnerable Code Snippet */}
          <div className="finding-card__section">
            <div className="finding-card__section-label">🔍 Scanner Finding</div>
            <div className="code-block">
              <span className="code-block__line-num">{finding.line}</span>
              <code>{finding.snippet}</code>
            </div>
            <p className="finding-card__scanner-msg">{finding.scanner_message}</p>
          </div>

          {/* AI Explanation */}
          {finding.explanation && (
            <div className="finding-card__section">
              <div className="finding-card__section-label">💡 Why This Is Dangerous</div>
              <p className="finding-card__explanation">{finding.explanation}</p>
            </div>
          )}

          {/* Analogy */}
          {finding.analogy && (
            <div className="finding-card__analogy">
              <div className="finding-card__analogy-icon">🔗</div>
              <p>{finding.analogy}</p>
            </div>
          )}

          {/* Diff View */}
          {finding.fix_snippet && (
            <div className="finding-card__section">
              <div className="finding-card__section-label">📝 Suggested Fix</div>
              <DiffViewer
                oldCode={finding.snippet}
                newCode={finding.fix_snippet}
              />
            </div>
          )}

          {/* Apply Fix Button */}
          {finding.fix_snippet && !isVerified && (
            <div className="finding-card__actions">
              <button
                className={`btn ${isFixed ? 'btn-success' : 'btn-primary'}`}
                disabled={isFixed}
                onClick={() => onApplyFix(finding.id, finding.fix_snippet, finding.snippet)}
              >
                {isFixed ? '✓ Fix Applied' : '🔧 Apply Fix'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
