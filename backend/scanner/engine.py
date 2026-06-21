import os
from ..models import Finding
from .rules.python_rules import scan_python
from .rules.javascript_rules import scan_javascript
from .rules.java_rules import scan_java
from .rules.go_rules import scan_go


# Map file extensions to language names and scanner functions
LANGUAGE_MAP = {
    ".py": ("Python", scan_python),
    ".js": ("JavaScript", scan_javascript),
    ".ts": ("TypeScript", scan_javascript),  # Use JS rules for TS
    ".jsx": ("JavaScript (JSX)", scan_javascript),
    ".tsx": ("TypeScript (TSX)", scan_javascript),
    ".java": ("Java", scan_java),
    ".go": ("Go", scan_go),
}


class CodeScanner:
    """Main static analysis engine that dispatches to language-specific rules."""

    def detect_language(self, filename: str) -> tuple[str, callable | None]:
        """Detect language from file extension and return (language_name, scanner_fn)."""
        _, ext = os.path.splitext(filename.lower())
        if ext in LANGUAGE_MAP:
            return LANGUAGE_MAP[ext]
        return ("Unknown", None)

    def scan(self, code: str, filename: str) -> list[Finding]:
        """
        Scan the given code for security vulnerabilities.

        Returns a list of Finding objects with unique IDs.
        """
        language, scanner_fn = self.detect_language(filename)

        if scanner_fn is None:
            return []

        # Run the language-specific scanner — returns list[dict]
        raw_findings = scanner_fn(code)

        # Convert to Finding models with unique IDs
        findings: list[Finding] = []
        for idx, raw in enumerate(raw_findings, start=1):
            finding = Finding(
                id=f"f{idx}",
                type=raw["type"],
                severity=raw["severity"],
                line=raw["line"],
                snippet=raw["snippet"],
                scanner_message=raw["scanner_message"],
            )
            findings.append(finding)

        return findings

    def get_language(self, filename: str) -> str:
        """Return the detected language name for a filename."""
        language, _ = self.detect_language(filename)
        return language
