# ⚖️ AI Legal Case Predictor – IPC Guide  
### 🧠 Retrieval-Augmented Generation (RAG) System for Legal Intelligence

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Inter&size=26&pause=1200&color=F39C12&center=true&vCenter=true&width=700&lines=AI+for+Legal+Intelligence;RAG+%2B+LLM+%2B+Vector+Search;Predicting+IPC+Sections+with+Context" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/LangChain-RAG-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/FAISS-Vector%20DB-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Groq-LLM-purple?style=for-the-badge">
  <img src="https://img.shields.io/badge/FastAPI-Backend-teal?style=for-the-badge&logo=fastapi">
</p>

---

## 📌 Problem Statement  

Identifying relevant **Indian Penal Code (IPC) sections** from legal case descriptions is:

- ⏳ Time-consuming  
- ⚖️ Requires legal expertise  
- ❌ Prone to human error  

---

## 🚀 Solution  

This project builds an **AI-powered legal analysis system** using a **Retrieval-Augmented Generation (RAG)** pipeline:

- 🔍 Extracts semantic meaning from case descriptions  
- 📚 Retrieves relevant IPC sections using vector similarity  
- 🧠 Generates structured legal reasoning using LLMs  

---

## 🧠 System Architecture  

User Input → Text Processing → Chunking → Embeddings → FAISS → LLM → IPC Prediction

---

## 📄 Research Foundation  

Based on IEEE research:

> **“AI-Based Legal Case Predictor for IPC Sections Using NLP and Machine Learning”**

### 🔬 Key Contributions

- NLP-based legal classification system  
- Semantic retrieval using FAISS  
- RAG integration for contextual reasoning  
- 📊 Achieved **92% F1-score**  
- ⚡ Reduced retrieval time by ~40%  

---

## 🔄 Research → Implementation Mapping  

| Research Concept | Implementation |
|-----------------|--------------|
| NLP Classification | `utils/legal_utils.py` |
| RAG Pipeline | `utils/retriever.py` |
| Vector Database | FAISS |
| LLM Reasoning | Groq (LLaMA3) |
| UI Layer | Gradio |

---

## ✨ Key Features  

- 🔍 **RAG-based Legal Retrieval (LangChain + FAISS)**  
- ⚡ **40% faster retrieval vs keyword search**  
- 🎯 **92% F1-score (IPC classification)**  
- 📄 Structured legal explanation output  
- 🧩 Modular & scalable backend design  

---

## 📊 Dataset & Evaluation  

- 📂 Source: IPC legal documents (PDFs)  
- 🧹 Preprocessing: Cleaning + Chunking (1000 tokens, overlap 200)  
- 🧠 Embeddings: MiniLM (Sentence Transformers)  

### 📈 Evaluation Method
- Manual validation on curated test cases  
- F1-score based on predicted vs actual IPC sections  

> ⚠️ Note: Evaluation performed on controlled test samples

---

## 🛠️ Tech Stack  

**Backend:** FastAPI  
**AI/ML:** LangChain, FAISS, HuggingFace  
**LLM:** Groq (LLaMA3), Gemini  
**Processing:** NumPy, Pandas  
**UI:** Gradio  

---

## 📈 Results  

- 🎯 **92% F1-score** in IPC classification  
- ⚡ **~40% faster retrieval latency**  
- 🧠 Improved contextual accuracy via semantic search  

---

## 🔌 API Example  

### 📥 Request
{
  "case_description": "Person committed theft under..."
}

## 📤 Response
{
  "ipc_sections": ["IPC 378", "IPC 379"],
  "confidence": 0.92,
  "explanation": "Based on semantic similarity..."
}

---

## ⚙️ Installation
- git clone https://github.com/Mr-Nobody0409/AI-Legal-Case-Predictor-IPC-Guide
- cd AI-Legal-Case-Predictor-IPC-Guide
- pip install -r requirements.txt

---

## ▶️ How to Run
- Run Backend
  uvicorn app:app --reload
- Run UI
  python ui.py

---

## ⚠️ Challenges
- Handling long and complex legal text
- Context-sensitive interpretation of IPC sections
- Semantic similarity vs keyword mismatch
- Multi-label classification (multiple IPC sections per case)

---

## 🚧 Future Improvements
- 🌐 React-based frontend dashboard
- 🌍 Multi-language legal support
- 📚 Case law retrieval integration
- ☁️ Cloud deployment (OCI / AWS)

---

📚 References
- Indian Penal Code dataset
- RAG-based legal AI research papers

---

👤 Author

Lohith Reddy B

<p align="center"> <a href="mailto:lohithreddyb@gmail.com"> <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white"> </a> <a href="https://linkedin.com/in/lohith-reddy-mrnobody"> <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"> </a> <a href="https://github.com/Mr-Nobody0409"> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"> </a> </p>
