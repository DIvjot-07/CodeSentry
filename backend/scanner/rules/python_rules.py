import re


def scan_python(code: str) -> list[dict]:
    """Scan Python code for security vulnerabilities."""
    findings = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # --- SQL Injection ---
        # Detect cursor.execute / .execute with f-strings or string concatenation,
        # or variable assignments building SQL queries dynamically.
        is_sqli = False
        if re.search(r'\.execute\s*\(\s*f["\']', line) or \
           re.search(r'\.execute\s*\(\s*["\'].*\+', line) or \
           re.search(r'\.execute\s*\(.*%\s', line) or \
           re.search(r'\.execute\s*\(.*\.format\s*\(', line):
            is_sqli = True
        elif re.search(r'\b(?:sql|query|stmt|sql_query|sql_stmt)\b\s*(?:\+?=|=)\s*', line, re.IGNORECASE):
            if re.search(r'=\s*f["\']', line) or \
               re.search(r'["\'].*\+\s*', line) or \
               re.search(r'\.format\s*\(', line) or \
               re.search(r'["\'].*%\s*', line) or \
               re.search(r'\+\s*["\']', line):
                is_sqli = True

        if is_sqli:
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "User input is concatenated directly into an SQL query string. "
                    "This allows an attacker to inject arbitrary SQL commands, "
                    "potentially reading, modifying, or deleting all data in the database. "
                    "Use parameterized queries instead."
                ),
            })

        # --- Hardcoded Secrets ---
        if re.search(
            r'(?:api_key|password|secret|token|db_password|api_secret|private_key)\s*='
            r'\s*["\'][^"\'{}]{3,}["\']',
            line,
            re.IGNORECASE,
        ):
            # Exclude comparison operators (==) and env var lookups
            if not re.search(r'==', line) and not re.search(r'os\.environ|os\.getenv|config\[', line, re.IGNORECASE):
                findings.append({
                    "type": "Hardcoded Secret",
                    "severity": "Critical",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "A secret value (API key, password, or token) is hardcoded in source code. "
                        "If this code is committed to version control, the secret is exposed to anyone "
                        "with repository access. Use environment variables or a secrets manager."
                    ),
                })

        # --- Command Injection ---
        if re.search(
            r'os\.system\s*\(\s*f["\']', line
        ) or re.search(
            r'os\.system\s*\(\s*["\'].*\+', line
        ) or re.search(
            r'os\.system\s*\(.*%\s', line
        ) or re.search(
            r'subprocess\.(?:call|run|Popen|check_output|check_call)\s*\(\s*f["\']', line
        ) or re.search(
            r'subprocess\.(?:call|run|Popen|check_output|check_call)\s*\(\s*["\'].*\+', line
        ) or re.search(
            r'os\.popen\s*\(\s*f["\']', line
        ):
            findings.append({
                "type": "Command Injection",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "User-controlled input is passed to a system command via string interpolation. "
                    "An attacker can inject shell metacharacters (;, |, &&) to execute arbitrary "
                    "commands on the server. Use subprocess with a list of arguments instead."
                ),
            })

        # --- Insecure Deserialization ---
        if re.search(r'pickle\.loads?\s*\(', line):
            findings.append({
                "type": "Insecure Deserialization",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "Untrusted data is deserialized with pickle, which can execute arbitrary code "
                    "during deserialization. An attacker can craft a malicious pickle payload to "
                    "gain remote code execution. Use safe formats like JSON."
                ),
            })

        if re.search(r'yaml\.load\s*\(', line) and not re.search(r'Loader\s*=\s*(?:Safe|Base)Loader', line):
            if 'safe_load' not in line:
                findings.append({
                    "type": "Insecure Deserialization",
                    "severity": "High",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "yaml.load() without a safe Loader can execute arbitrary Python code "
                        "embedded in the YAML input. Use yaml.safe_load() instead."
                    ),
                })

        # --- Weak Cryptography ---
        if re.search(r'hashlib\.(?:md5|sha1)\s*\(', line):
            findings.append({
                "type": "Weak Cryptography",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "MD5/SHA1 are cryptographically broken hash algorithms. They are vulnerable to "
                    "collision attacks and should not be used for password hashing or security-sensitive "
                    "operations. Use bcrypt, scrypt, or argon2 for passwords; SHA-256+ for integrity."
                ),
            })

        # --- Debug Mode ---
        if re.search(r'debug\s*=\s*True', line):
            findings.append({
                "type": "Debug Mode Enabled",
                "severity": "Medium",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "Debug mode is enabled, which can expose stack traces, environment variables, "
                    "and internal application details to end users. This gives attackers a detailed "
                    "map of the application internals. Disable debug mode in production."
                ),
            })

        # --- Eval / Exec Usage ---
        if re.search(r'\beval\s*\(', line) or re.search(r'\bexec\s*\(', line):
            # Ignore comments
            if not stripped.startswith("#"):
                findings.append({
                    "type": "Code Injection (eval/exec)",
                    "severity": "High",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "eval()/exec() execute arbitrary Python code at runtime. If any part of the "
                        "input is user-controlled, an attacker can execute any code with the privileges "
                        "of the application. Use safer alternatives like ast.literal_eval() for data parsing."
                    ),
                })

    return findings
