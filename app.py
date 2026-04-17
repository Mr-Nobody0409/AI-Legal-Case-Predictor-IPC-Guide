from fastapi import FastAPI
from pydantic import BaseModel

from rag_pipeline import run_query
from utils import extract_ipc_sections, categorize_case, recommend_lawyer, summarize_text

app = FastAPI(title="AI Legal Case Predictor")

class CaseInput(BaseModel):
    name: str
    case_description: str

@app.post("/predict")
def predict_case(data: CaseInput):
    answer = run_query(data.case_description)

    sections = extract_ipc_sections(answer)
    category = categorize_case(data.case_description)
    lawyer = recommend_lawyer(category)
    summary = summarize_text(answer)

    return {
        "user": data.name,
        "category": category,
        "ipc_sections": sections,
        "summary": summary,
        "recommended_lawyer": lawyer
    }

@app.get("/")
def home():
    return {"message": "API running"}
