# CodeSentry — Product Requirements Document (Hackathon MVP)

**Team:** Ai-vengers (Yashita Gaur, Divjot Bedi)  
**College:** University School of Automation and Robotics  
**Tracks:** ArmorClaw + ArmorIQ  
**Document Type:** MVP PRD — Hackathon Scope Only

---

## 1. Overview

CodeSentry is an AI-powered security code review mentor that goes beyond detecting vulnerabilities — it explains them in plain language, suggests fixes, verifies those fixes, and logs the entire review for compliance. The MVP demonstrates a complete scan → explain → fix → verify → log loop, end-to-end, within a hackathon timeframe.

---

## 2. Problem Statement

Developers — especially juniors and small teams — routinely ship insecure code not out of carelessness but because they don't recognize the risk. Existing scanners like Snyk and Semgrep surface findings with no explanation, no verification, and no audit trail. The result: vulnerabilities slip through, security knowledge never grows within the team, and compliance is an afterthought.

**The gap:** scanners detect, but don't teach, verify, or log.

---

## 3. Goals & Success Criteria

### Goals
- Demonstrate a working scan → explain → fix → verify → audit loop.
- Show that AI (Claude) can translate raw scanner output into beginner-friendly, actionable guidance.
- Produce a logged, auditable review record per scan session.

### MVP Success Criteria
| Criteria | Target |
|---|---|
| Code upload triggers a real ArmorClaw scan | ✅ Must have |
| Claude explains each finding in plain language | ✅ Must have |
| Auto-fix suggestion rendered as a diff | ✅ Must have |
| Re-scan after fix confirms resolution | ✅ Must have |
| ArmorIQ audit log entry created per session | ✅ Must have |
| UI is usable by a non-security-expert | ✅ Must have |
| Team skill dashboard | ❌ Out of scope (post-hackathon) |

---

## 4. User Personas

### Primary: Junior Developer
- Little to no formal security training.
- Understands code but not vulnerability patterns.
- Needs: clear explanations, copy-paste fixes, confirmation that the fix worked.

### Secondary: Startup Tech Lead
- No dedicated security staff.
- Needs: fast, trustworthy security gates on PRs without hiring a specialist.

### Tertiary: Open-Source Maintainer
- Receives PRs from unknown contributors.
- Needs: consistent, explainable security checks before merge.

---

## 5. Scope — MVP Features

### 5.1 Code Upload
- User uploads a code file (`.py`, `.js`, `.ts`, `.java`, `.go`) via drag-and-drop or file picker.
- File is sent to the backend for processing.
- **Out of scope for MVP:** GitHub PR linking, direct repo integration.

### 5.2 ArmorClaw Scan
- Backend passes the uploaded file to the ArmorClaw scanner.
- Returns a list of findings, each with:
  - Vulnerability type (e.g. SQL Injection, Hardcoded Secret)
  - Severity level (Critical / High / Medium / Low)
  - Line number(s) affected
  - Raw scanner message

### 5.3 AI Explanation (Claude)
- For each ArmorClaw finding, the backend calls the Claude API with the vulnerable code snippet + scanner finding as context.
- Claude returns:
  - A plain-language explanation of why the issue is dangerous.
  - A real-world analogy (e.g. "A hardcoded API key is like writing your house key number on the front door").
  - A suggested fixed code snippet.
- Displayed inline under each finding in the UI.

### 5.4 Auto-Fix & Diff View
- The Claude-suggested fix is rendered as a unified diff (original vs. fixed).
- A "Apply Fix" button replaces the original snippet in the editor/preview.
- Fixed code is passed back for re-scan.

### 5.5 Verification Re-scan
- After a fix is applied, the updated code is re-submitted to ArmorClaw automatically.
- If the finding is gone: badge shows **Resolved ✅**.
- If still present: badge shows **Still Vulnerable ⚠️** with the original explanation retained.

### 5.6 ArmorIQ Audit Log
- At the end of each session, one audit log entry is written via the ArmorIQ SDK containing:
  - Timestamp
  - File name
  - List of findings (type, severity, line)
  - Fix applied (yes/no)
  - Re-scan result (resolved/unresolved)
- Log is displayed in a simple "Audit Trail" panel in the UI.

---

## 6. Out of Scope (MVP)

- GitHub / GitLab CI integration
- Multi-file / full-repo scanning
- User authentication & persistent accounts
- Team skill dashboard & trend analytics
- Custom vulnerability rule configuration
- SaaS billing or self-hosted deployment packaging

---

## 7. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Vite), Tailwind CSS |
| Backend | Python 3.11 + FastAPI |
| Security Scanner | ArmorClaw |
| AI Layer | Claude API (`claude-sonnet-4-6`) |
| Audit & Policy | ArmorIQ SDK |
| Storage (session) | In-memory / SQLite (MVP) |
| Diff Rendering | `react-diff-viewer` or similar |

---

## 8. System Architecture

```
User (Browser)
     │
     ▼
React Frontend
     │  (1) Upload file
     ▼
FastAPI Backend
     │  (2) Run scan
     ▼
ArmorClaw Scanner ──► findings JSON
     │  (3) For each finding
     ▼
Claude API ──────────► explanation + fix suggestion
     │  (4) Apply fix & re-scan
     ▼
ArmorClaw Scanner ──► resolved / unresolved
     │  (5) Log session
     ▼
ArmorIQ SDK ─────────► audit log entry
     │
     ▼
React Frontend ◄─── Full results rendered
```

---

## 9. API Contracts (Internal)

### POST `/api/scan`
**Request:**
```json
{ "filename": "app.py", "code": "<raw source code string>" }
```
**Response:**
```json
{
  "session_id": "uuid",
  "findings": [
    {
      "id": "f1",
      "type": "SQL Injection",
      "severity": "Critical",
      "line": 42,
      "snippet": "...",
      "scanner_message": "...",
      "explanation": "...",    // from Claude
      "analogy": "...",        // from Claude
      "fix_snippet": "..."     // from Claude
    }
  ]
}
```

### POST `/api/verify`
**Request:**
```json
{ "session_id": "uuid", "fixed_code": "<patched source code string>" }
```
**Response:**
```json
{
  "session_id": "uuid",
  "results": [
    { "finding_id": "f1", "resolved": true }
  ],
  "audit_log_id": "armoriq-log-uuid"
}
```

---

## 10. UI Screens (MVP)

### Screen 1: Upload
- Drag-and-drop zone or file picker.
- Language auto-detected from extension.
- "Scan Now" button.

### Screen 2: Results Dashboard
- Header: file name, scan timestamp, overall severity badge.
- Per finding card:
  - Severity chip (color-coded)
  - Vulnerability type + line number
  - Plain-language explanation (Claude)
  - Real-world analogy (Claude)
  - Diff view (original vs. fix)
  - "Apply Fix" button
- "Verify All Fixes" CTA at bottom.

### Screen 3: Verification Results
- Per finding: Resolved ✅ or Still Vulnerable ⚠️ badge.
- Audit Trail panel: collapsible JSON log of the full session.

---

## 11. Claude Prompt Design

```
System:
You are a senior security engineer and mentor. When given a code vulnerability 
finding from a static analysis scanner, you will:
1. Explain in 2-3 sentences WHY this is dangerous, using plain language a 
   junior developer can understand.
2. Provide a real-world analogy in one sentence.
3. Provide a corrected code snippet that fixes the exact issue.

Keep explanations concise. Avoid excessive jargon. Format the fixed code 
as a code block in the same language as the input.

User:
Language: {language}
Vulnerability type: {type}
Severity: {severity}
Vulnerable code snippet (line {line}):
{snippet}

Scanner message: {scanner_message}
```

---

## 12. Build Plan (Hackathon Timeline)

| Phase | Tasks | Time Estimate |
|---|---|---|
| **Setup** | Scaffold FastAPI + React, install ArmorClaw + ArmorIQ SDKs | 2 hrs |
| **Scan Pipeline** | `/api/scan` endpoint, ArmorClaw integration, parse findings | 3 hrs |
| **AI Layer** | Claude API call per finding, prompt tuning, parse response | 3 hrs |
| **Frontend — Results** | Findings cards, diff view, severity chips | 4 hrs |
| **Verify Loop** | Re-scan on fixed code, resolved/unresolved badge | 2 hrs |
| **ArmorIQ Logging** | SDK integration, audit trail UI panel | 2 hrs |
| **Polish & Demo Prep** | Error handling, loading states, demo script | 2 hrs |
| **Total** | | **~18 hrs** |

---

## 13. Demo Script

1. Open CodeSentry in browser.
2. Upload `vulnerable_app.py` (pre-prepared file with a hardcoded API key + SQL injection).
3. Click **Scan Now** → ArmorClaw findings appear with severity badges.
4. Show Claude's plain-language explanation and analogy for the SQL injection finding.
5. Click **Apply Fix** → diff view shows the parameterized query replacement.
6. Click **Verify** → both findings show **Resolved ✅**.
7. Scroll to Audit Trail panel → show the ArmorIQ log entry with timestamps and resolution status.

---

## 14. Risks & Mitigations

| Risk | Mitigation |
|---|---|
| ArmorClaw SDK setup time | Prepare integration code in advance; have mock scanner JSON as fallback |
| Claude API latency per finding | Show streaming or skeleton loaders; batch calls where possible |
| ArmorIQ SDK unfamiliarity | Read docs early; stub the log call with a local JSON file as fallback |
| Demo file too simple to impress | Use a realistic multi-vulnerability Python file as demo input |

---

*PRD Version 1.0 — Hackathon MVP Scope*
