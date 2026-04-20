# ⚖️ AI Legal Case Predictor – IPC Guide (RAG System)

## 📌 Problem Statement  

Identifying relevant **Indian Penal Code (IPC) sections** from legal case descriptions is:
- Time-consuming  
- Requires domain expertise  
- Prone to human error  

---

## 🚀 Solution  

This project implements an **AI-powered legal analysis system** using a **Retrieval-Augmented Generation (RAG)** pipeline to:

- Extract legal meaning from case descriptions  
- Retrieve relevant IPC sections using vector similarity  
- Predict applicable laws with high accuracy

---

## 📄 Research Foundation  

This project is based on an IEEE research paper:

**“AI-Based Legal Case Predictor for IPC Sections Using NLP and Machine Learning”**

### Key Contributions from Research:
- Designed an NLP-based legal classification system for IPC prediction  
- Implemented semantic retrieval using vector embeddings (FAISS)  
- Integrated Retrieval-Augmented Generation (RAG) for improved contextual accuracy  
- Achieved **92% F1-score** on classification tasks  
- Reduced legal information retrieval time by ~40%  

### Research → Implementation Mapping:

| Research Component | Implementation |
|------------------|--------------|
| NLP Classification | `utils.py` (categorization + extraction) |
| RAG Architecture | `rag_pipeline.py` |
| Vector Database | FAISS |
| LLM Reasoning | Groq (LLaMA3) |
| System Interface | FastAPI + Gradio |

---

## 🧠 Key Features  

- 🔍 **RAG Pipeline (LangChain + FAISS)** for semantic retrieval  
- ⚡ **40% faster retrieval latency** vs keyword-based search  
- 🎯 **92% F1-score** for IPC classification  
- 📄 Structured legal reasoning output  
- 🔗 Modular backend design (API-ready)

---

## Dataset
- Source: IPC legal documents (PDF)
- Preprocessing: cleaning + chunking
- Evaluation: manual validation + classification metrics

---

## 🏗️ Architecture  
User Input
->
Text Processing (Cleaning + NLP)
->
Embedding Model (MiniLM)
->
FAISS Vector Search
->
LangChain Retrieval
->
LLM (LLaMA3 via Groq)
->
IPC Prediction + Explanation + Summary

---

## 🛠️ Tech Stack  

**Backend:** Python, FastAPI  
**AI/ML:** LangChain, FAISS, HuggingFace Transformers  
**LLM:** Gemini / Groq API  
**Data Processing:** Pandas, NumPy  

---

## 📊 Results  

- Achieved **92% F1-score** on IPC classification  
- Reduced retrieval latency by **~40%**  
- Improved contextual accuracy using semantic search  

---

## Request 
{
  "case_description": "Person committed theft under..."
}

## Responce
{
  "ipc_sections": ["IPC 378", "IPC 379"],
  "confidence": 0.92,
  "explanation": "Based on semantic similarity..."
}

---

## ⚙️ Installation
git clone https://github.com/Mr-Nobody0409/AI-Legal-Case-Predictor-IPC-Guide
cd AI-Legal-Case-Predictor-IPC-Guide
pip install -r requirements.txt
uvicorn main:app --reload

---

## ⚡ HOW TO RUN
uvicorn app:app --reload
python ui.py

---

## 🧪 Future Improvements
Add frontend (React dashboard)
Multi-language legal support
Case law retrieval integration
Deployment on cloud (OCI / AWS)

---

## 📚 References
Indian Penal Code dataset
RAG-based legal AI research



