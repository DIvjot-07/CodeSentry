from pydantic import BaseModel, Field
from typing import Optional


class ScanRequest(BaseModel):
    filename: str
    code: str


class Finding(BaseModel):
    id: str
    type: str
    severity: str  # Critical / High / Medium / Low
    line: int
    snippet: str
    scanner_message: str
    explanation: str = ""
    analogy: str = ""
    fix_snippet: str = ""


class ScanResponse(BaseModel):
    session_id: str
    filename: str
    language: str
    scan_timestamp: str
    findings: list[Finding]
    severity_summary: dict


class VerifyRequest(BaseModel):
    session_id: str
    fixed_code: str


class VerifyResult(BaseModel):
    finding_id: str
    original_type: str
    resolved: bool


class VerifyResponse(BaseModel):
    session_id: str
    results: list[VerifyResult]
    audit_log_id: str


class AuditLogEntry(BaseModel):
    audit_id: str
    session_id: str
    timestamp: str
    filename: str
    findings: list
    fixes_applied: int
    total_findings: int
    resolved_count: int
    unresolved_count: int
