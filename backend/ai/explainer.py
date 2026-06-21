import json
import asyncio
import logging

logger = logging.getLogger(__name__)

# ── Fallback explanations for when no API key is available ──────────────────

FALLBACK_EXPLANATIONS = {
    "SQL Injection": {
        "explanation": (
            "This code inserts user input directly into an SQL query string. An attacker can "
            "craft input like `' OR 1=1 --` to bypass authentication, dump entire tables, or "
            "even delete data. This is consistently ranked the #1 web application vulnerability."
        ),
        "analogy": (
            "It's like a bank teller who reads your deposit slip aloud as a command — if you "
            "write 'and also empty vault 7', they'd do it without question."
        ),
        "fix_snippet": (
            "# Use parameterized queries:\n"
            "cursor.execute(\"SELECT * FROM users WHERE username = ? AND password = ?\", (username, password))"
        ),
    },
    "Hardcoded Secret": {
        "explanation": (
            "Secrets like API keys and passwords are embedded directly in source code. Anyone "
            "with access to the repository — including public GitHub — can see and use these "
            "credentials to impersonate your application or access your services."
        ),
        "analogy": (
            "It's like writing your house key combination on a sticky note taped to the front door."
        ),
        "fix_snippet": (
            "import os\n"
            "API_KEY = os.environ.get('API_KEY')\n"
            "DB_PASSWORD = os.environ.get('DB_PASSWORD')"
        ),
    },
    "Command Injection": {
        "explanation": (
            "User input is passed directly into a system shell command. An attacker can append "
            "shell metacharacters like `; rm -rf /` or `| cat /etc/passwd` to execute any command "
            "on your server with the application's privileges."
        ),
        "analogy": (
            "It's like letting a stranger dictate commands to your personal assistant, who will "
            "execute anything they hear without questioning it."
        ),
        "fix_snippet": (
            "import subprocess\n"
            "# Use a list of arguments — no shell interpretation:\n"
            "result = subprocess.run(['ping', '-c', '1', host], capture_output=True, text=True)"
        ),
    },
    "Insecure Deserialization": {
        "explanation": (
            "Pickle can execute arbitrary Python code during deserialization. An attacker can "
            "craft a malicious payload that runs system commands, installs backdoors, or steals "
            "data the moment it's unpickled — before your code even inspects the result."
        ),
        "analogy": (
            "It's like opening a package from an unknown sender that contains a spring-loaded "
            "mechanism — it triggers the moment you open it, not after you inspect its contents."
        ),
        "fix_snippet": (
            "import json\n"
            "# Use a safe serialization format:\n"
            "obj = json.loads(data)"
        ),
    },
    "Weak Cryptography": {
        "explanation": (
            "MD5 and SHA1 are broken hash algorithms — known collision attacks exist and brute-force "
            "attacks are trivially fast on modern hardware. Passwords hashed with MD5 can be cracked "
            "in seconds using rainbow tables or GPU-powered tools like hashcat."
        ),
        "analogy": (
            "It's like using a lock from the 1800s on your front door — it looks like security, "
            "but any modern lockpick can open it in seconds."
        ),
        "fix_snippet": (
            "import bcrypt\n"
            "# Use a proper password hashing algorithm:\n"
            "hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())"
        ),
    },
    "Debug Mode Enabled": {
        "explanation": (
            "Debug mode exposes detailed error pages with stack traces, source code, environment "
            "variables, and even an interactive debugger in some frameworks. This gives attackers "
            "a complete map of your application internals to plan further attacks."
        ),
        "analogy": (
            "It's like leaving the building blueprints, alarm codes, and security camera feeds "
            "on the reception desk for anyone to browse."
        ),
        "fix_snippet": (
            "import os\n"
            "# Use environment-based configuration:\n"
            "app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')"
        ),
    },
    "Code Injection (eval/exec)": {
        "explanation": (
            "eval() and exec() execute arbitrary Python code at runtime. If any portion of the "
            "input string comes from a user, they can run any code with your application's full "
            "privileges — reading files, accessing databases, or pivoting to other systems."
        ),
        "analogy": (
            "It's like giving a stranger the master key to your building and saying 'do whatever "
            "you want' — you have zero control over what they'll access."
        ),
        "fix_snippet": (
            "import ast\n"
            "# For safe literal evaluation:\n"
            "result = ast.literal_eval(user_input)\n"
            "# Or use a proper parser for your specific use case"
        ),
    },
    "Cross-Site Scripting (XSS)": {
        "explanation": (
            "Setting innerHTML with user-controlled data allows attackers to inject malicious "
            "scripts that run in other users' browsers. These scripts can steal session cookies, "
            "redirect to phishing sites, or perform actions on behalf of the victim."
        ),
        "analogy": (
            "It's like letting a stranger write whatever they want on a bulletin board in your "
            "lobby — including fake fire evacuation instructions."
        ),
        "fix_snippet": (
            "// Use textContent for plain text (safe):\n"
            "element.textContent = userInput;\n"
            "// Or use DOMPurify for HTML:\n"
            "element.innerHTML = DOMPurify.sanitize(userInput);"
        ),
    },
    "Code Injection (eval)": {
        "explanation": (
            "eval() parses and executes a string as JavaScript code. If user input flows into "
            "eval(), an attacker can execute arbitrary code in your application's context, "
            "potentially stealing data, hijacking sessions, or compromising the server."
        ),
        "analogy": (
            "It's like a genie that grants wishes to anyone — including malicious strangers — "
            "with no restrictions or safety checks."
        ),
        "fix_snippet": (
            "// Use JSON.parse() for data parsing:\n"
            "const data = JSON.parse(userInput);\n"
            "// Or use a safe expression evaluator library"
        ),
    },
}


class AIExplainer:
    """
    Generates human-friendly explanations for security findings using
    Google Gemini AI, with graceful fallback to pre-written explanations.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        self.model = None

        if api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash")
                logger.info("Gemini AI initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini AI: {e}. Using fallback mode.")
                self.model = None

    def _build_prompt(self, finding: dict, language: str, full_code: str) -> str:
        return f"""System: You are a senior security engineer and mentor. When given a code vulnerability finding from a static analysis scanner, you will:
1. Explain in 2-3 sentences WHY this is dangerous, using plain language a junior developer can understand.
2. Provide a real-world analogy in one sentence.
3. Provide a corrected code snippet that fixes the exact issue. Only output the fixed lines, not the whole file.

Respond in this exact JSON format:
{{"explanation": "...", "analogy": "...", "fix_snippet": "..."}}

Language: {language}
Vulnerability type: {finding['type']}
Severity: {finding['severity']}
Vulnerable code snippet (line {finding['line']}): {finding['snippet']}
Scanner message: {finding['scanner_message']}

Full file context:
{full_code}"""

    def _parse_ai_response(self, response_text: str) -> dict:
        """Parse JSON from Gemini response, handling markdown code block wrapping."""
        text = response_text.strip()

        # Remove markdown code blocks if present
        if text.startswith("```"):
            # Remove opening ```json or ```
            first_newline = text.index("\n")
            text = text[first_newline + 1:]
            # Remove closing ```
            if text.endswith("```"):
                text = text[:-3].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON from the text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            return {}

    def _call_gemini_sync(self, prompt: str) -> str:
        """Synchronous call to Gemini API."""
        response = self.model.generate_content(prompt)
        return response.text

    def _get_fallback(self, finding_type: str) -> dict:
        """Get pre-written fallback explanation for a vulnerability type."""
        # Try exact match first
        if finding_type in FALLBACK_EXPLANATIONS:
            return FALLBACK_EXPLANATIONS[finding_type].copy()

        # Try partial match
        for key, value in FALLBACK_EXPLANATIONS.items():
            if key.lower() in finding_type.lower() or finding_type.lower() in key.lower():
                return value.copy()

        # Generic fallback
        return {
            "explanation": (
                f"This code contains a {finding_type} vulnerability that could allow an attacker "
                f"to compromise the security of your application. Review the flagged code and apply "
                f"security best practices for this type of issue."
            ),
            "analogy": (
                "It's like leaving a window open in a secure building — it may seem harmless, "
                "but it provides an entry point for anyone looking."
            ),
            "fix_snippet": "// Review and fix the flagged code following security best practices.",
        }

    async def explain_finding(self, finding: dict, language: str, full_code: str) -> dict:
        """
        Generate an AI-powered explanation for a security finding.

        Falls back to pre-written explanations if the API key is unavailable
        or the API call fails.
        """
        if self.model is not None:
            try:
                prompt = self._build_prompt(finding, language, full_code)
                # Run synchronous Gemini call in a thread to avoid blocking
                response_text = await asyncio.to_thread(self._call_gemini_sync, prompt)
                parsed = self._parse_ai_response(response_text)

                if parsed and "explanation" in parsed:
                    return {
                        "explanation": parsed.get("explanation", ""),
                        "analogy": parsed.get("analogy", ""),
                        "fix_snippet": parsed.get("fix_snippet", ""),
                    }
            except Exception as e:
                logger.warning(f"Gemini API call failed for finding {finding.get('type')}: {e}")

        # Fallback to pre-written explanations
        fallback = self._get_fallback(finding.get("type", "Unknown"))

        if finding.get("type") == "Hardcoded Secret":
            import re
            snippet = finding.get("snippet", "").strip()
            var_name = "SECRET_VAR"
            # Match assignments like: var = '...' or const var = '...' or var := '...'
            match = re.search(r'(?:const|let|var)?\s*([a-zA-Z0-9_.-]+)\s*(?::=|=)\s*', snippet, re.IGNORECASE)
            if match:
                var_name = match.group(1).strip()
            
            # Specific explanations and analogies based on variable type
            if any(p in var_name.lower() for p in ["password", "passwd", "pw"]):
                fallback["explanation"] = (
                    f"A database or service password ({var_name}) is hardcoded directly in the source code. "
                    f"If this code is committed to version control, attackers can access your database, "
                    f"leading to data breaches, unauthorized modifications, or data deletion."
                )
                fallback["analogy"] = (
                    "It's like leaving the key to your safe deposit box in an envelope labeled 'Safe Key' on your desk."
                )
            else:
                fallback["explanation"] = (
                    f"An API key or secret token ({var_name}) is hardcoded in the source code. "
                    f"If this code is leaked or committed to version control, third parties can abuse your credentials, "
                    f"impersonate your application, and run up massive usage bills."
                )
                fallback["analogy"] = (
                    "It's like printing your company's credit card number on the back of every employee's business card."
                )
                
            # Build custom fix snippet based on language and variable name
            lang = language.lower() if language else "python"
            if "go" in lang:
                fallback["fix_snippet"] = (
                    f"import \"os\"\n"
                    f"// Use os.Getenv to retrieve the secret from environment variables\n"
                    f"{var_name} := os.Getenv(\"{var_name}\")"
                )
            elif any(js in lang for js in ["javascript", "typescript", "js", "ts"]):
                fallback["fix_snippet"] = (
                    f"// Use process.env to retrieve the secret from environment variables\n"
                    f"const {var_name} = process.env.{var_name};"
                )
            elif "java" in lang:
                fallback["fix_snippet"] = (
                    f"// Use System.getenv to retrieve the secret from environment variables\n"
                    f"String {var_name} = System.getenv(\"{var_name}\");"
                )
            else:  # Python default
                fallback["fix_snippet"] = (
                    f"import os\n"
                    f"// Use os.environ.get to retrieve the secret from environment variables\n"
                    f"{var_name} = os.environ.get('{var_name}')"
                )
        return fallback
