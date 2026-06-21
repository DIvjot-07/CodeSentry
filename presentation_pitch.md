# CodeSentry — Hackathon Presentation Pitch Script

This pitch script is designed to align precisely with your 7-slide PowerPoint deck. It is structured for a 3-to-4 minute presentation, with time allocated for slide transitions, visual cues, and the live demo.

---

## Slide 1: Title Slide (0:00 - 0:20)
* **On Screen**: CodeSentry — AI-Powered Security Code Review Mentor. Team: **Ai-vengers** (Yashita Gaur & Divjot Bedi). Track 1 & 2 (ArmorClaw + ArmorIQ).
* **Speaker (Yashita or Divjot)**:
  > "Hello everyone! We are team **Ai-vengers**, representing the University School Of Automation And Robotics. Today, we are excited to introduce **CodeSentry**—your AI-Powered Security Code Review Mentor. Our project bridges the gap in modern software development by integrating automated security scanning with real-time AI mentoring, fully implementing both Track 1 (ArmorClaw) and Track 2 (ArmorIQ)."

---

## Slide 2: The Problem (0:20 - 0:50)
* **On Screen**: The Problem — Developers ship insecure code unknowingly. 74% breaches involve human error; 0 explanations given by typical scanners; 100% fixes left unverified.
* **Speaker**:
  > "Every day, junior developers, startups, and open-source maintainers push code containing critical vulnerabilities like SQL injections and hardcoded secrets. They don't do this out of carelessness, but because they simply don't recognize the risk. 
  > 
  > Current industry scanners like Snyk or Semgrep fail them. They dump raw, cryptic technical warnings with zero educational context, offer no verified proof that a developer's fix actually worked, and leave compliance teams without a secure audit trail. The gap is clear: **traditional scanners detect, but they do not teach, verify, or log.**"

---

## Slide 3: Proposed Solution (0:50 - 1:20)
* **On Screen**: Proposed Solution — CodeSentry: scan, explain, fix, verify, log all in one loop.
* **Speaker**:
  > "Our solution is **CodeSentry**—an all-in-one loop that turns security checks into interactive mentorship. 
  > 
  > Instead of just throwing a list of errors at developers, CodeSentry implements a 5-step loop:
  > 1. **Submit**: Developers upload code or link a PR.
  > 2. **Scan**: Our ArmorClaw engine identifies vulnerabilities.
  > 3. **Explain**: AI explains the risks in plain language with real-world analogies.
  > 4. **Fix & Re-scan**: The developer applies the fix, and the engine automatically re-scans.
  > 5. **Audit Log**: The entire interaction is verified and securely logged using ArmorIQ."

---

## Slide 4: Architecture & Tech Stack (1:20 - 1:45)
* **On Screen**: System Components showing Frontend (React), Backend (FastAPI), Security Scanner (ArmorClaw), AI Layer (Claude/Gemini API), Policy & Audit (ArmorIQ SDK), and Storage (PostgreSQL/SQLite).
* **Speaker**:
  > "Under the hood, CodeSentry is built on a highly modular and fast tech stack:
  > - **Frontend**: A sleek React app styled with custom dark-cyber CSS, rendering visual diffs and glassmorphism UI elements.
  > - **Backend**: A FastAPI server in Python orchestrating the entire review pipeline.
  > - **Security Scanner**: Our emulation of the **ArmorClaw** engine, checking rules across Python, JS, Java, and Go.
  > - **AI Layer**: Generative AI prompting (with a local fallback) to explain issues and provide targeted fixes.
  > - **Policy & Audit**: The **ArmorIQ SDK** emulator writing structured logs.
  > - **Storage**: An SQL database logging user sessions and review history."

---

## Slide 5: Key Features (1:45 - 2:10)
* **On Screen**: Key Features (Automated Scanning, Beginner-Friendly Explanations, Auto-Fix, Verification Loop, Compliance Audit, Team Skill Dashboard).
* **Speaker**:
  > "CodeSentry stands out through six key features:
  > 
  > - **Beginner-Friendly Explanations**: We use real-world analogies so developers understand *why* the code is vulnerable.
  > - **Auto-Fix Diff**: CodeSentry proposes a side-by-side git-style diff of the fix ready to apply with one click.
  > - **Verification Loop**: After a patch is applied, CodeSentry immediately triggers a re-scan. No more guessing if a fix worked—we verify it instantly.
  > - **Compliance Audit Trail**: Every action creates an immutable log entry, giving compliance teams audit-ready evidence."

---

## Slide 6: Impact & Feasibility (2:10 - 2:30)
* **On Screen**: Impact & Feasibility — Who benefits, Real-world impact, and Scalability.
* **Speaker**:
  > "The impact is immediate. Junior developers learn security on the job, turning every warning into a mini-lesson. Startups get enterprise-grade security review without hiring dedicated security staff. 
  > 
  > Architecturally, CodeSentry is highly scalable—it can plug directly into GitHub Actions or GitLab CI. Best of all, this entire end-to-end loop is fully functional and built within the hackathon timeframe."

---

## Slide 7: Demo & Conclusion (2:30 - End)
* **Action**: (Start the live demo on your screen)
* **Speaker**:
  > "Let's look at the live demo. We will click **Try Demo File** to load a vulnerable Python app. The **ArmorClaw Scan** flags 7 issues, including hardcoded secrets and SQL injections.
  > 
  > Look at line 10 for `API_KEY`. CodeSentry explains the billing and impersonation risks in plain language. If we look at line 11 for `DB_PASSWORD`, it dynamically adapts the warning, warning of database breaches and access risks.
  > 
  > When we click **Apply Fix**, the code is patched instantly. If we click **Verify All Fixes**, CodeSentry triggers a re-scan. Notice how `API_KEY` is now marked **Resolved** ✅. Everything is recorded in the **ArmorIQ Audit Trail** which we can export as JSON.
  > 
  > CodeSentry turns code review into a security lesson, proving fixes the way a senior mentor would. Thank you!"
