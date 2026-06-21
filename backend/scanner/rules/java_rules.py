import re


def scan_java(code: str) -> list[dict]:
    """Scan Java code for security vulnerabilities."""
    findings = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
            continue

        # --- SQL Injection via Statement concatenation ---
        if re.search(
            r'(?:executeQuery|executeUpdate|execute)\s*\(\s*["\'].*\+', line
        ) or re.search(
            r'(?:executeQuery|executeUpdate|execute)\s*\(\s*.*\+\s*["\']', line
        ) or re.search(
            r'Statement.*\.execute\w*\s*\(\s*["\'].*\+', line
        ) or re.search(
            r'createStatement\s*\(\s*\).*execute', line
        ):
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "SQL query is built via string concatenation with a Statement object. "
                    "This allows attackers to inject arbitrary SQL. "
                    "Use PreparedStatement with parameterized queries instead."
                ),
            })

        # Also detect string concat building a query variable
        if re.search(
            r'(?:String\s+)?(?:sql|query|stmt)\s*=\s*["\'](?:SELECT|INSERT|UPDATE|DELETE).*\+',
            line,
            re.IGNORECASE,
        ):
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "An SQL query string is built using concatenation, which is likely passed "
                    "to a Statement for execution. Use PreparedStatement with ? placeholders."
                ),
            })

        # --- Runtime.exec() ---
        if re.search(r'Runtime\.getRuntime\s*\(\s*\)\.exec\s*\(', line):
            findings.append({
                "type": "Command Injection",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "Runtime.exec() executes system commands. If user input is included in the "
                    "command string, an attacker can inject arbitrary OS commands. "
                    "Use ProcessBuilder with an explicit argument list and validate all inputs."
                ),
            })

        # --- ProcessBuilder with string concat ---
        if re.search(r'ProcessBuilder\s*\(.*\+', line):
            findings.append({
                "type": "Command Injection",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "User input may be concatenated into a ProcessBuilder command. "
                    "Validate and sanitize all inputs before passing to process execution."
                ),
            })

        # --- Hardcoded Passwords/Secrets ---
        if re.search(
            r'(?:String\s+)?(?:password|passwd|secret|apiKey|api_key|token|API_KEY|SECRET_KEY)\s*='
            r'\s*"[^"]{3,}"',
            line,
            re.IGNORECASE,
        ):
            # Exclude empty strings, comparisons, and config lookups
            if not re.search(r'\.get|\.getProperty|System\.getenv|==|\.equals', line):
                findings.append({
                    "type": "Hardcoded Secret",
                    "severity": "Critical",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "A password or secret key is hardcoded in Java source code. "
                        "Compiled .class files can be decompiled to reveal these values. "
                        "Use environment variables, config files, or a vault service."
                    ),
                })

    return findings
