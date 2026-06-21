import re


def scan_go(code: str) -> list[dict]:
    """Scan Go code for security vulnerabilities."""
    findings = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("//"):
            continue

        # --- SQL Injection via fmt.Sprintf in db.Query / db.Exec ---
        if re.search(r'(?:db|tx)\.\s*(?:Query|Exec|QueryRow)\s*\(\s*fmt\.Sprintf\s*\(', line):
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "SQL query is constructed with fmt.Sprintf and passed to db.Query/Exec. "
                    "This allows SQL injection. Use parameterized queries with $1, $2 "
                    "placeholders: db.Query(\"SELECT * FROM users WHERE id = $1\", id)."
                ),
            })

        # SQL string concatenation
        if re.search(
            r'(?:db|tx)\.\s*(?:Query|Exec|QueryRow)\s*\(\s*["\'].*\+', line
        ) or re.search(
            r'(?:db|tx)\.\s*(?:Query|Exec|QueryRow)\s*\(.*\+\s*["\']', line
        ):
            findings.append({
                "type": "SQL Injection",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "SQL query is built with string concatenation and passed to a database method. "
                    "Use parameterized queries to prevent SQL injection."
                ),
            })

        # --- Command Injection via exec.Command ---
        if re.search(r'exec\.Command\s*\(', line):
            # Check if a variable (not a string literal) is the command argument
            if re.search(r'exec\.Command\s*\(\s*[a-zA-Z_]', line):
                findings.append({
                    "type": "Command Injection",
                    "severity": "High",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "exec.Command() is called with a variable as the command or arguments. "
                        "If user input reaches this call, an attacker can execute arbitrary OS commands. "
                        "Validate and whitelist allowed commands and arguments."
                    ),
                })

        # exec.Command with fmt.Sprintf
        if re.search(r'exec\.Command\s*\(\s*fmt\.Sprintf', line):
            findings.append({
                "type": "Command Injection",
                "severity": "High",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "exec.Command() with fmt.Sprintf allows injection of shell arguments. "
                    "Pass arguments as separate parameters to exec.Command instead of "
                    "formatting them into a single string."
                ),
            })

        # --- Hardcoded Secrets ---
        if re.search(
            r'(?:apiKey|password|secret|token|dbPassword|APIKey|Password|Secret|Token)\s*'
            r'(?::=|=)\s*"[^"]{3,}"',
            line,
            re.IGNORECASE,
        ):
            # Exclude os.Getenv and config lookups
            if not re.search(r'os\.Getenv|viper\.|config\.|\.Get', line):
                findings.append({
                    "type": "Hardcoded Secret",
                    "severity": "Critical",
                    "line": i,
                    "snippet": line.rstrip(),
                    "scanner_message": (
                        "A secret value is hardcoded in Go source code. Compiled Go binaries "
                        "contain readable string literals that can be extracted. "
                        "Use environment variables (os.Getenv) or a secrets manager."
                    ),
                })

        # Also catch const declarations with secrets
        if re.search(
            r'(?:const|var)\s+\w*(?:Key|Secret|Password|Token)\w*\s*(?:string\s*)?=\s*"[^"]{3,}"',
            line,
            re.IGNORECASE,
        ):
            findings.append({
                "type": "Hardcoded Secret",
                "severity": "Critical",
                "line": i,
                "snippet": line.rstrip(),
                "scanner_message": (
                    "A secret is declared as a const/var with a literal string value. "
                    "Use runtime configuration or environment variables."
                ),
            })

    return findings
