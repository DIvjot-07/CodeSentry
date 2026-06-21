import json
import uuid
import aiosqlite
from datetime import datetime, timezone


class AuditLogger:
    """ArmorIQ-equivalent audit logging system backed by SQLite."""

    def __init__(self, db_path: str = "audit.db"):
        self.db_path = db_path

    async def init_db(self):
        """Create the audit_logs table if it doesn't exist."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    audit_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    findings TEXT NOT NULL,
                    fixes_applied INTEGER DEFAULT 0,
                    total_findings INTEGER DEFAULT 0,
                    resolved_count INTEGER DEFAULT 0,
                    unresolved_count INTEGER DEFAULT 0
                )
            """)
            await db.commit()

    async def log_session(
        self,
        session_id: str,
        filename: str,
        findings: list,
        fixes_applied: int,
        resolved_count: int,
        unresolved_count: int,
    ) -> str:
        """Insert an audit log entry and return the audit_id."""
        audit_id = f"armoriq-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()
        total_findings = resolved_count + unresolved_count

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO audit_logs
                    (audit_id, session_id, timestamp, filename, findings,
                     fixes_applied, total_findings, resolved_count, unresolved_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    audit_id,
                    session_id,
                    timestamp,
                    filename,
                    json.dumps(findings),
                    fixes_applied,
                    total_findings,
                    resolved_count,
                    unresolved_count,
                ),
            )
            await db.commit()

        return audit_id

    async def get_log(self, session_id: str) -> dict | None:
        """Retrieve the audit log entry for a given session_id."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM audit_logs WHERE session_id = ? ORDER BY timestamp DESC LIMIT 1",
                (session_id,),
            ) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                return {
                    "audit_id": row["audit_id"],
                    "session_id": row["session_id"],
                    "timestamp": row["timestamp"],
                    "filename": row["filename"],
                    "findings": json.loads(row["findings"]),
                    "fixes_applied": row["fixes_applied"],
                    "total_findings": row["total_findings"],
                    "resolved_count": row["resolved_count"],
                    "unresolved_count": row["unresolved_count"],
                }
