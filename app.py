import os
import gradio as gr
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from utils.retriever import load_and_process_documents, build_vector_store
from utils.summarizer import summarize_text
from utils.legal_utils import extract_ipc_sections, categorize_case, recommend_lawyer


# ---------------- ENV ----------------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY missing")


# ---------------- LOAD DATA ----------------
documents = load_and_process_documents("data/")
vector_store = build_vector_store(documents)

retriever = vector_store.as_retriever()


# ---------------- LLM ----------------
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)


prompt = ChatPromptTemplate.from_template("""
You are an expert Indian lawyer.

<context>
{context}
</context>

Question: {input}

Provide:
- Legal explanation
- Relevant IPC sections
- Clear reasoning
""")


document_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, document_chain)


# ---------------- MAIN LOGIC ----------------
def chatbot_response(name, query):
    result = chain.invoke({"input": query})
    text = result["answer"]

    sections = extract_ipc_sections(text)
    category = categorize_case(query)
    lawyer = recommend_lawyer(category)
    summary = summarize_text(text)

    return f"""
### 👤 Dear {name}

### 📝 Category:
**{category}**

### ⚖ IPC Sections:
{", ".join(sections)}

### 📘 Summary:
{summary}

### 👨‍⚖ Recommended Lawyer:
**{lawyer}**
"""


# ---------------- UI ----------------
def main():
    with gr.Blocks() as ui:
        gr.Markdown("# 🏛 AI Legal Case Predictor")

        name = gr.Textbox(label="Your Name")
        case = gr.Textbox(label="Case Description", lines=5)

        output = gr.Markdown()

        btn = gr.Button("Analyze Case")

        btn.click(chatbot_response, inputs=[name, case], outputs=output)

    ui.launch()


if __name__ == "__main__":
    main()
