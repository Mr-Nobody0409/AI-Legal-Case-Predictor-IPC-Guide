import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from utils.retriever import load_and_process_documents, build_vector_store
from utils.legal_utils import extract_ipc_sections, categorize_case, recommend_lawyer
from utils.summarizer import summarize_text

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# ─── Load env ────────────────────────────────────────────────────────────────
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Set it in backend/.env")

# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="AI Legal Case Predictor API",
    description="RAG-based IPC section prediction using LangChain + Groq",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Bootstrap RAG pipeline on startup ───────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    global chain
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    documents = load_and_process_documents(data_dir)
    vector_store = build_vector_store(documents)
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama3-70b-8192",
        temperature=0.2,
    )

    prompt = ChatPromptTemplate.from_template("""
You are an expert Indian criminal lawyer with deep knowledge of the Indian Penal Code (IPC).

<context>
{context}
</context>

Case Description: {input}

Provide a thorough legal analysis covering:
1. The applicable IPC sections and their exact numbers (format: IPC 302, IPC 420, etc.)
2. A plain-language explanation of each section
3. The legal reasoning connecting the facts to the sections
4. Potential defenses or mitigating factors
5. Likely legal outcomes or penalties

Be precise, structured, and professional.
""")

    document_chain = create_stuff_documents_chain(llm, prompt)
    chain = create_retrieval_chain(retriever, document_chain)


# ─── Schemas ─────────────────────────────────────────────────────────────────
class AnalyzeRequest(BaseModel):
    name: str
    case_description: str


class IPCSection(BaseModel):
    section: str
    description: str


class AnalyzeResponse(BaseModel):
    name: str
    category: str
    ipc_sections: list[str]
    summary: str
    full_analysis: str
    recommended_lawyer: str


# ─── Routes ──────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"message": "AI Legal Case Predictor API is running", "version": "2.0.0"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_case(request: AnalyzeRequest):
    if not request.case_description.strip():
        raise HTTPException(status_code=400, detail="Case description cannot be empty.")
    if len(request.case_description) < 20:
        raise HTTPException(status_code=400, detail="Please provide a more detailed case description.")

    try:
        result = chain.invoke({"input": request.case_description})
        full_text = result["answer"]

        sections = extract_ipc_sections(full_text)
        category = categorize_case(request.case_description)
        lawyer = recommend_lawyer(category)
        summary = summarize_text(full_text)

        return AnalyzeResponse(
            name=request.name,
            category=category,
            ipc_sections=sections,
            summary=summary,
            full_analysis=full_text,
            recommended_lawyer=lawyer,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/api/ipc-categories")
async def get_ipc_categories():
    """Returns the list of supported legal case categories."""
    return {
        "categories": [
            {"key": "theft", "label": "Theft & Property Crimes", "icon": "🏠"},
            {"key": "assault", "label": "Assault & Violence", "icon": "⚠️"},
            {"key": "fraud", "label": "Fraud & Cheating", "icon": "📄"},
            {"key": "murder", "label": "Murder & Culpable Homicide", "icon": "⚖️"},
            {"key": "cybercrime", "label": "Cybercrime", "icon": "💻"},
            {"key": "sexual_offence", "label": "Sexual Offences", "icon": "🔒"},
            {"key": "defamation", "label": "Defamation", "icon": "📢"},
            {"key": "kidnapping", "label": "Kidnapping & Abduction", "icon": "🚨"},
            {"key": "other", "label": "Other", "icon": "📋"},
        ]
    }
