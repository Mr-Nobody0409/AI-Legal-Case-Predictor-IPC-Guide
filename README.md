# ⚖️ AI Legal Case Predictor – IPC Guide v2.0

> Migrated from Gradio → **React + FastAPI** full-stack architecture.
> RAG pipeline: LangChain · FAISS · MiniLM · Groq LLaMA3-70B

---

## 📁 Project Structure

```
ai-legal-predictor/
├── backend/
│   ├── app.py                  # FastAPI application (main entry point)
│   ├── requirements.txt
│   ├── .env.example            # Copy to .env and add GROQ_API_KEY
│   ├── data/                   # Place IPC PDF/TXT documents here (optional)
│   └── utils/
│       ├── __init__.py
│       ├── retriever.py        # Document loading + FAISS vector store
│       ├── legal_utils.py      # IPC extraction, categorization, lawyer rec.
│       └── summarizer.py       # Lightweight text summarizer
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── App.module.css
        ├── index.css
        ├── api/
        │   └── legalApi.js     # Axios API client
        └── components/
            ├── Header.jsx / .module.css
            ├── CaseForm.jsx / .module.css
            ├── ResultCard.jsx / .module.css
            └── LoadingOverlay.jsx / .module.css
```

---

## ⚙️ Setup & Run

### 1 — Prerequisites
- Python 3.10+
- Node.js 18+
- A free [Groq API key](https://console.groq.com)

### 2 — Backend

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# → Open .env and set GROQ_API_KEY=your_key_here

# Start FastAPI server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at **http://localhost:8000**
Swagger docs at **http://localhost:8000/docs**

### 3 — Frontend

```bash
# In a new terminal, from the project root
cd frontend

npm install
npm run dev
```

The app will be live at **http://localhost:5173**

---

## 🔌 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/api/analyze` | Analyze a legal case |
| GET | `/api/ipc-categories` | List case categories |

### POST `/api/analyze`
```json
// Request
{ "name": "Arjun Sharma", "case_description": "The accused broke into..." }

// Response
{
  "name": "Arjun Sharma",
  "category": "Theft & Property Crimes",
  "ipc_sections": ["IPC 378", "IPC 379", "IPC 323"],
  "summary": "...",
  "full_analysis": "...",
  "recommended_lawyer": "Criminal Lawyer (Specialization: Property & Theft Law)"
}
```

---

## 📚 Adding Your Own IPC Documents

Place any PDF or TXT files in `backend/data/`. On next server restart, they will be loaded, chunked (1000 tokens, 200 overlap), and indexed into FAISS.

If no files are present, the system uses a built-in fallback IPC knowledge base covering the most common sections.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + CSS Modules |
| Backend | FastAPI + Uvicorn |
| AI/ML | LangChain, FAISS, HuggingFace MiniLM |
| LLM | Groq (LLaMA3-70B-8192) |
| HTTP | Axios (frontend) |
