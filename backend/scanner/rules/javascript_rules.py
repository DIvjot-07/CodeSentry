import re


def scan_javascript(code: str) -> list[dict]:
    """Scan JavaScript/TypeScript code for security vulnerabilities."""
    findings = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("//") or stripped.startswith("/*"):
            continue

        # --- eval() Usage ---
        if re.search(r'\beval\s*\(', line):
            findings.append({
                "type": "Code Injection (eval)",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "eval() executes arbitrary JavaScript code at runtime. If user input reaches "
                    "eval(), an attacker can run any code in the application context, steal data, "
                    "or hijack sessions. Use JSON.parse() for data or safer alternatives."
                ),
            })

        # --- innerHTML Assignment (XSS) ---
        if re.search(r'\.innerHTML\s*=', line) or re.search(r'\.innerHTML\s*\+=', line):
            findings.append({
                "type": "Cross-Site Scripting (XSS)",
                "severity": "Medium",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "Setting innerHTML with dynamic content can inject malicious scripts into the page. "
                    "An attacker can steal cookies, redirect users, or deface the website. "
                    "Use textContent for plain text or a sanitization library like DOMPurify."
                ),
            })

        # --- Hardcoded Secrets ---
        if re.search(
            r'(?:const|let|var)\s+\w*(?:api_key|apiKey|password|secret|token|API_KEY|PASSWORD|SECRET|TOKEN)\w*'
            r'\s*=\s*["\'][^"\']{3,}["\']',
            line,
            re.IGNORECASE,
        ):
            findings.append({
                "type": "Hardcoded Secret",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "A secret value is hardcoded in JavaScript source code. Client-side JavaScript "
                    "is fully visible to users in the browser. Even in server-side Node.js, hardcoded "
                    "secrets in code will leak via version control. Use environment variables."
                ),
            })

        # --- SQL Injection in template literals ---
        if re.search(r'(?:query|execute|run)\s*\(\s*`[^`]*\$\{', line):
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "User input is interpolated into an SQL query via template literals. "
                    "This allows SQL injection attacks. Use parameterized queries with "
                    "placeholders (e.g., db.query('SELECT * FROM users WHERE id = $1', [id]))."
                ),
            })

        # --- SQL Injection with string concatenation ---
        if re.search(r'(?:query|execute|run)\s*\(\s*["\'].*\+', line):
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "User input is concatenated into an SQL query string. "
                    "Use parameterized queries to prevent SQL injection."
                ),
            })

        # --- child_process.exec with template literals ---
        if re.search(r'(?:child_process\.)?exec\s*\(\s*`[^`]*\$\{', line):
            # Make sure it's not eval (already caught above)
            if 'eval' not in line:
                findings.append({
                    "type": "Command Injection",
                    "severity": "High",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "User input is interpolated into a shell command via child_process.exec(). "
                        "An attacker can inject shell metacharacters to execute arbitrary commands. "
                        "Use child_process.execFile() with an argument array instead."
                    ),
                })

        # --- child_process.exec with string concatenation ---
        if re.search(r'(?:child_process\.)?exec\s*\(\s*["\'].*\+', line):
            if 'eval' not in line:
                findings.append({
                    "type": "Command Injection",
                    "severity": "High",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "User input is concatenated into a shell command string. "
                        "Use child_process.execFile() with an argument array instead."
                    ),
                })

    return findings
