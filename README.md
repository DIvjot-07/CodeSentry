# CodeSentry — AI-Powered Security Code Review

CodeSentry is a real-time, AI-driven security code review application designed for hackathons. It scans files in Python, JavaScript, Java, and Go, flags security issues, explains them in plain language with real-world analogies, and lets you verify corrected code side-by-side.

---

## Prerequisites
Before running, make sure you have the following installed:
1. **Python 3.x**
2. **Node.js** (including `npm`)

---

## How to Run

### 1. Run the Backend (FastAPI Server)

Open your terminal, navigate to the `backend/` directory, and run the following commands:

```bash
# Navigate to the backend directory
cd backend

# Install the required Python packages
pip install -r requirements.txt
```

Set your Gemini API key in the environment and start the uvicorn server:
```

#### Windows (Command Prompt)
```cmd
set GEMINI_API_KEY
python -m uvicorn main:app --reload --port 8000
```

```

The backend server will run at: **`http://localhost:8000`**

---

### 2. Run the Frontend (Vite + React)

Open a **separate** terminal window, navigate to the `frontend/` directory, and run:

```bash
# Navigate to the frontend directory
cd frontend

# Install the required frontend dependencies
npm install

# Start the Vite development server
npm run dev
```

The frontend development server will run at: **`http://localhost:5173`**

---

## Core Features
1. **Interactive File Upload**: Drag-and-drop a `.py`, `.js`, `.ts`, `.java`, or `.go` file, or click **Try Demo File** to load a pre-configured vulnerable script.
2. **Static Analysis & AI Enrichment**: Custom rules identify critical flaws, enriched with plain-language explanations, real-world analogies, and custom fixes from Gemini.
3. **Interactive Side-by-Side Diff**: Compare your vulnerable code directly with the AI-suggested fix, and apply the patch with a single click.
4. **Resilience & Verification**: Re-verify your code to check which vulnerabilities are successfully resolved.
5. **Session Audit Trail**: View structural log tables of past scanner activities and download them as JSON.
