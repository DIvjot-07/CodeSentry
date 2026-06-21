import React, { useState, useCallback } from 'react';
import Header from './components/Header';
import UploadScreen from './components/UploadScreen';
import ResultsDashboard from './components/ResultsDashboard';
import AuditTrail from './components/AuditTrail';
import { ScanningAnimation } from './components/LoadingStates';
import { scanCode, verifyFixes, getAuditLog } from './utils/api';

export default function App() {
  const [screen, setScreen] = useState('upload');
  const [scanData, setScanData] = useState(null);
  const [verifyData, setVerifyData] = useState(null);
  const [auditData, setAuditData] = useState(null);
  const [currentCode, setCurrentCode] = useState('');
  const [filename, setFilename] = useState('');
  const [fixedFindings, setFixedFindings] = useState(new Set());
  const [error, setError] = useState(null);

  const handleScan = useCallback(async (file, code) => {
    setError(null);
    setFilename(file);
    setCurrentCode(code);
    setScreen('scanning');
    setFixedFindings(new Set());
    setVerifyData(null);
    setAuditData(null);

    try {
      const data = await scanCode(file, code);
      setScanData(data);
      setScreen('results');
    } catch (err) {
      setError(err.message || 'Scan failed');
      setScreen('upload');
    }
  }, []);

  const handleApplyFix = useCallback((findingId, fixSnippet, originalSnippet) => {
    setCurrentCode(prev => {
      // Replace the vulnerable snippet with the fix
      const lines = prev.split('\n');
      const finding = scanData?.findings?.find(f => f.id === findingId);
      if (!finding) return prev;

      const snippetTrimmed = finding.snippet.trim();
      let lineIdx = finding.line - 1;

      // If the line number doesn't match the snippet (due to shifts), search the entire file
      if (
        lineIdx < 0 || 
        lineIdx >= lines.length || 
        (!lines[lineIdx].includes(snippetTrimmed) && lines[lineIdx].trim() !== snippetTrimmed)
      ) {
        lineIdx = lines.findIndex(l => l.includes(snippetTrimmed) || l.trim() === snippetTrimmed);
      }

      if (lineIdx >= 0 && lineIdx < lines.length) {
        // Get indentation of original line
        const indent = lines[lineIdx].match(/^(\s*)/)[1];
        const fixLines = fixSnippet.split('\n')
          .filter(l => !l.trim().startsWith('#') && !l.trim().startsWith('//') && l.trim() !== '')
          .map(l => indent + l.trimStart());

        if (fixLines.length > 0) {
          lines.splice(lineIdx, 1, ...fixLines);
        }
      }

      return lines.join('\n');
    });

    setFixedFindings(prev => new Set([...prev, findingId]));
  }, [scanData]);

  const handleVerify = useCallback(async () => {
    if (!scanData?.session_id) return;
    setError(null);
    setScreen('verifying');

    try {
      const data = await verifyFixes(scanData.session_id, currentCode);
      setVerifyData(data);

      // Fetch audit log
      try {
        const audit = await getAuditLog(scanData.session_id);
        setAuditData(audit);
      } catch (e) {
        console.warn('Could not fetch audit log:', e);
      }

      setScreen('verified');
    } catch (err) {
      setError(err.message || 'Verification failed');
      setScreen('results');
    }
  }, [scanData, currentCode]);

  const handleReset = useCallback(() => {
    setScreen('upload');
    setScanData(null);
    setVerifyData(null);
    setAuditData(null);
    setCurrentCode('');
    setFilename('');
    setFixedFindings(new Set());
    setError(null);
  }, []);

  return (
    <div className="app">
      <Header screen={screen} onReset={handleReset} />

      <main className="main-content">
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)} className="error-banner__close">✕</button>
          </div>
        )}

        {screen === 'upload' && (
          <UploadScreen onScan={handleScan} />
        )}

        {screen === 'scanning' && (
          <ScanningAnimation />
        )}

        {(screen === 'results' || screen === 'verifying' || screen === 'verified') && scanData && (
          <>
            <ResultsDashboard
              scanData={scanData}
              currentCode={currentCode}
              fixedFindings={fixedFindings}
              verifyData={verifyData}
              onApplyFix={handleApplyFix}
              onVerify={handleVerify}
              isVerifying={screen === 'verifying'}
              isVerified={screen === 'verified'}
            />
            {screen === 'verified' && auditData && (
              <AuditTrail auditData={auditData} verifyData={verifyData} scanData={scanData} />
            )}
          </>
        )}

        {screen === 'verifying' && (
          <div className="verifying-overlay">
            <div className="verifying-spinner" />
            <p>Re-scanning to verify fixes...</p>
          </div>
        )}
      </main>
    </div>
  );
}
