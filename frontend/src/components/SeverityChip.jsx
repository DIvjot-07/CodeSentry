import React from 'react';

const severityConfig = {
  critical: { className: 'severity-chip--critical', label: 'Critical' },
  high:     { className: 'severity-chip--high',     label: 'High' },
  medium:   { className: 'severity-chip--medium',   label: 'Medium' },
  low:      { className: 'severity-chip--low',      label: 'Low' },
  info:     { className: 'severity-chip--info',     label: 'Info' },
};

export default function SeverityChip({ severity }) {
  const key = (severity || 'info').toLowerCase();
  const config = severityConfig[key] || severityConfig.info;

  const dotStyle = {
    width: 6,
    height: 6,
    borderRadius: '50%',
    background: 'currentColor',
  };

  return (
    <span className={`severity-chip ${config.className}`}>
      <span style={dotStyle} />
      {config.label}
    </span>
  );
}
