import os
import uuid
import logging
from pathlib import Path
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    ScanRequest, ScanResponse, Finding,
    VerifyRequest, VerifyResponse, VerifyResult,
    AuditLogEntry,
)
from .scanner.engine import CodeScanner
from .ai.explainer import AIExplainer
from .audit.logger import AuditLogger

logger = logging.getLogger(__name__)

# ── Globals ──────────────────────────────────────────────────────────────────
scanner = CodeScanner()
explainer = AIExplainer(api_key=os.environ.get("GEMINI_API_KEY"))
audit_logger = AuditLogger()

# In-memory session store (hackathon scope — no persistence needed)
sessions: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    await audit_logger.init_db()
    logger.info("CodeSentry API started.")
    yield
    logger.info("CodeSentry API shutting down.")


app = FastAPI(
    title="CodeSentry API",
    description="AI-powered security code review backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── POST /api/scan ──────────────────────────────────────────────────────────

@app.post("/api/scan", response_model=ScanResponse)
async def scan_code(req: ScanRequest):
    """Upload code, run ArmorClaw scan, enrich with AI explanations."""
    session_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Run the scanner
    findings: list[Finding] = scanner.scan(req.code, req.filename)

    # 2. Enrich each finding with AI explanations
    language = scanner.get_language(req.filename)
    enriched: list[Finding] = []

    for f in findings:
        finding_dict = {
            "type": f.type,
            "severity": f.severity,
            "line": f.line,
            "snippet": f.snippet,
            "scanner_message": f.scanner_message,
        }
        ai_result = await explainer.explain_finding(finding_dict, language, req.code)
        enriched.append(Finding(
            id=f.id,
            type=f.type,
            severity=f.severity,
            line=f.line,
            snippet=f.snippet,
            scanner_message=f.scanner_message,
            explanation=ai_result.get("explanation", ""),
            analogy=ai_result.get("analogy", ""),
            fix_snippet=ai_result.get("fix_snippet", ""),
        ))

    # 3. Build severity summary
    severity_summary = {}
    for f in enriched:
        sev = f.severity
        severity_summary[sev] = severity_summary.get(sev, 0) + 1

    # 4. Store session for later verification
    sessions[session_id] = {
        "filename": req.filename,
        "code": req.code,
        "findings": enriched,
        "timestamp": timestamp,
    }

    return ScanResponse(
        session_id=session_id,
        filename=req.filename,
        language=language,
        scan_timestamp=timestamp,
        findings=enriched,
        severity_summary=severity_summary,
    )


# ── POST /api/verify ────────────────────────────────────────────────────────

@app.post("/api/verify", response_model=VerifyResponse)
async def verify_fixes(req: VerifyRequest):
    """Re-scan fixed code and report which findings are resolved."""
    session = sessions.get(req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Re-scan the patched code
    new_findings = scanner.scan(req.fixed_code, session["filename"])

    # Compare against original findings using type, line, and snippet content
    original_findings = session["findings"]
    results: list[VerifyResult] = []
    resolved_count = 0
    matched_new_indices = set()

    for orig in original_findings:
        is_still_present = False
        for idx, new_f in enumerate(new_findings):
            if idx in matched_new_indices:
                continue
            
            # Match by type and either line or snippet content
            type_match = (new_f.type == orig.type)
            line_match = (new_f.line == orig.line)
            snippet_match = (new_f.snippet.strip() == orig.snippet.strip())
            
            if type_match and (line_match or snippet_match):
                is_still_present = True
                matched_new_indices.add(idx)
                break
        
        is_resolved = not is_still_present
        if is_resolved:
            resolved_count += 1
        results.append(VerifyResult(
            finding_id=orig.id,
            original_type=orig.type,
            resolved=is_resolved,
        ))

    fixes_applied = len([r for r in results if r.resolved])
    unresolved_count = len(results) - resolved_count

    # Log to ArmorIQ audit
    findings_for_log = [
        {
            "id": f.id,
            "type": f.type,
            "severity": f.severity,
            "line": f.line,
        }
        for f in original_findings
    ]
    audit_id = await audit_logger.log_session(
        session_id=req.session_id,
        filename=session["filename"],
        findings=findings_for_log,
        fixes_applied=fixes_applied,
        resolved_count=resolved_count,
        unresolved_count=unresolved_count,
    )

    # Update session with fixed code
    sessions[req.session_id]["fixed_code"] = req.fixed_code

    return VerifyResponse(
        session_id=req.session_id,
        results=results,
        audit_log_id=audit_id,
    )


# ── GET /api/audit/{session_id} ────────────────────────────────────────────

@app.get("/api/audit/{session_id}")
async def get_audit_log(session_id: str):
    """Retrieve the audit log entry for a session."""
    log = await audit_logger.get_log(session_id)
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log


# ── GET /api/demo-file ─────────────────────────────────────────────────────

@app.get("/api/demo-file")
async def get_demo_file():
    """Return the pre-built vulnerable demo file for one-click demo."""
    demo_path = Path(__file__).parent / "demo" / "vulnerable_app.py"
    try:
        code = demo_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Demo file not found")

    return {"filename": "vulnerable_app.py", "code": code}
