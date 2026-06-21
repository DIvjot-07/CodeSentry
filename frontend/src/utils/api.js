const API_BASE = '/api';

export async function scanCode(filename, code) {
  const res = await fetch(`${API_BASE}/scan`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ filename, code })
  });
  if (!res.ok) throw new Error('Scan failed');
  return res.json();
}

export async function verifyFixes(sessionId, fixedCode) {
  const res = await fetch(`${API_BASE}/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, fixed_code: fixedCode })
  });
  if (!res.ok) throw new Error('Verification failed');
  return res.json();
}

export async function getAuditLog(sessionId) {
  const res = await fetch(`${API_BASE}/audit/${sessionId}`);
  if (!res.ok) throw new Error('Audit log fetch failed');
  return res.json();
}

export async function getDemoFile() {
  const res = await fetch(`${API_BASE}/demo-file`);
  if (!res.ok) throw new Error('Demo file fetch failed');
  return res.json();
}
