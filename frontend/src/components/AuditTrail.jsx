import React, { useState } from 'react';

export default function AuditTrail({ auditData, verifyData, scanData }) {
  const [expanded, setExpanded] = useState(false);
  const [showJson, setShowJson] = useState(false);

  if (!auditData) return null;

  const formatTimestamp = (ts) => {
    try {
      return new Date(ts).toLocaleString();
    } catch {
      return ts;
    }
  };

  const handleExport = () => {
    const exportData = {
      ...auditData,
      verification_results: verifyData?.results || [],
    };
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `codesentry-audit-${auditData.session_id.slice(0, 8)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="audit-trail card" style={{ animation: 'slideUp 0.4s ease-out' }}>
      <div className="audit-trail__header" onClick={() => setExpanded(!expanded)}>
        <div className="audit-trail__header-left">
          <span className="audit-trail__icon">📋</span>
          <h3 className="audit-trail__title">Audit Trail</h3>
          <span className="audit-trail__badge">ArmorIQ</span>
        </div>
        <span className={`finding-card__chevron ${expanded ? 'finding-card__chevron--open' : ''}`}>
          ▾
        </span>
      </div>

      {expanded && (
        <div className="audit-trail__body">
          {/* Session Info */}
          <div className="audit-trail__meta">
            <div className="audit-trail__meta-item">
              <span className="audit-trail__meta-label">Session ID</span>
              <span className="audit-trail__meta-value">{auditData.session_id}</span>
            </div>
            <div className="audit-trail__meta-item">
              <span className="audit-trail__meta-label">Timestamp</span>
              <span className="audit-trail__meta-value">{formatTimestamp(auditData.timestamp)}</span>
            </div>
            <div className="audit-trail__meta-item">
              <span className="audit-trail__meta-label">File</span>
              <span className="audit-trail__meta-value">{auditData.filename}</span>
            </div>
          </div>

          {/* Summary Stats */}
          <div className="audit-trail__stats">
            <div className="audit-trail__stat">
              <span className="audit-trail__stat-number">{auditData.total_findings}</span>
              <span className="audit-trail__stat-label">Total Findings</span>
            </div>
            <div className="audit-trail__stat audit-trail__stat--resolved">
              <span className="audit-trail__stat-number">{auditData.resolved_count}</span>
              <span className="audit-trail__stat-label">Resolved</span>
            </div>
            <div className="audit-trail__stat audit-trail__stat--unresolved">
              <span className="audit-trail__stat-number">{auditData.unresolved_count}</span>
              <span className="audit-trail__stat-label">Unresolved</span>
            </div>
          </div>

          {/* Findings Table */}
          {auditData.findings && auditData.findings.length > 0 && (
            <div className="audit-trail__table-wrapper">
              <table className="audit-trail__table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Severity</th>
                    <th>Line</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {auditData.findings.map((f) => {
                    const verifyResult = verifyData?.results?.find(r => r.finding_id === f.id);
                    return (
                      <tr key={f.id}>
                        <td>{f.id}</td>
                        <td>{f.type}</td>
                        <td>
                          <span className={`audit-severity audit-severity--${f.severity?.toLowerCase()}`}>
                            {f.severity}
                          </span>
                        </td>
                        <td>{f.line}</td>
                        <td>
                          {verifyResult?.resolved
                            ? <span className="audit-status audit-status--resolved">✅ Resolved</span>
                            : <span className="audit-status audit-status--unresolved">⚠️ Unresolved</span>
                          }
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}

          {/* Actions */}
          <div className="audit-trail__actions">
            <button className="btn btn-ghost btn-sm" onClick={() => setShowJson(!showJson)}>
              {showJson ? '📊 Table View' : '{ } JSON View'}
            </button>
            <button className="btn btn-ghost btn-sm" onClick={handleExport}>
              ⬇️ Export JSON
            </button>
          </div>

          {/* JSON View */}
          {showJson && (
            <pre className="audit-trail__json code-block">
              {JSON.stringify({ ...auditData, verification_results: verifyData?.results }, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}
