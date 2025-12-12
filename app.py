import os
import re
import gradio as gr
from dotenv import load_dotenv
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# LangChain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY missing in environment variables!")


# ------------------------------
# Load PDF documents
# ------------------------------
def load_pdf(data_path):
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"❌ Path '{data_path}' does not exist.")

    loader = PyPDFDirectoryLoader(data_path, glob="*.pdf")
    docs = loader.load()

    if not docs:
        raise ValueError("❌ No PDF files found in provided directory.")

    return docs


data_directory = "data/"
documents = load_pdf(data_directory)


# ------------------------------
# Clean extracted text
# ------------------------------
def clean_text(text):
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\d+/\d+/\d+\s+\d+:\d+:\d+\s+[AP]M", "", text)
    text = text.encode("ascii", "ignore").decode()
    return text.strip()


for document in documents:
    document.page_content = clean_text(document.page_content)


# ------------------------------
# Chunking
# ------------------------------
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
final_docs = text_splitter.split_documents(documents)

if not final_docs:
    raise ValueError("❌ No chunks were created from PDFs.")


# ------------------------------
# Embeddings + Vector store
# ------------------------------
embedding_model = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")
database = FAISS.from_documents(final_docs, embedding_model)


# ------------------------------
# Groq LLM
# ------------------------------
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama3-70b-8192"
)


# ------------------------------
# Prompt Template
# ------------------------------
prompt = ChatPromptTemplate.from_template("""
You are an expert Indian lawyer. Use the context to answer.

<context>
{context}
</context>

Question: {input}

Helpful Answer:
""")


document_chain = create_stuff_documents_chain(llm, prompt)
retriever = database.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)


# ------------------------------
# IPC Section Extractor
# ------------------------------
def extract_ipc_sections(text):
    matches = re.findall(r"\bSection\s+\d+\b", text, re.IGNORECASE)
    return sorted(list(set(matches))) if matches else ["IPC section not found"]


# ------------------------------
# Case Categorization
# ------------------------------
def categorize_case(text):
    categories = {
        "Criminal": ["murder", "assault", "robbery", "theft", "fraud", "kidnapping", "arson", "rape"],
        "Civil": ["property dispute", "contract", "divorce", "inheritance", "custody", "land dispute"],
        "Corporate": ["business", "tax fraud", "merger", "shareholder"],
        "Cyber": ["hacking", "cyber fraud", "phishing", "malware", "data breach"],
        "Labor": ["employment", "wages", "termination", "harassment"]
    }

    lower = text.lower()

    for category, keywords in categories.items():
        if any(keyword in lower for keyword in keywords):
            return category

    return "General Legal Issue"


def recommend_lawyer(category):
    mapping = {
        "Criminal": "Criminal Lawyer",
        "Civil": "Civil Lawyer",
        "Corporate": "Corporate Lawyer",
        "Cyber": "Cyber Crime Specialist",
        "Labor": "Labor Law Attorney",
        "General Legal Issue": "General Legal Consultant"
    }
    return mapping.get(category, "Legal Expert")


# ------------------------------
# Summarizer
# ------------------------------
def summarize_text(text):
    model_name = "sshleifer/distilbart-cnn-12-6"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    summary = summarizer(text, max_length=250, min_length=30, do_sample=False)
    return summary[0]["summary_text"]


# ------------------------------
# Main Chatbot response
# ------------------------------
def chatbot_response(name, query):
    result = retrieval_chain.invoke({"input": query})

    text = result["answer"]

    sections = extract_ipc_sections(text)
    category = categorize_case(query)
    lawyer_type = recommend_lawyer(category)
    summary = summarize_text(text)

    return f"""
### 👤 Dear {name},

### 📝 Case Category:
**{category}**

### ⚖ Relevant IPC Sections:
{", ".join(sections)}

### 📘 Summary:
{summary}

### 👨‍⚖ Recommended Lawyer:
**{lawyer_type}**
"""


# ------------------------------
# GRADIO UI
# ------------------------------
def main():
    with gr.Blocks(theme=gr.themes.Soft()) as ui:
        gr.Markdown("<h1 style='text-align:center;'>🏛 LawBot India — IPC Prediction & Legal Guidance</h1>")

        with gr.Column() as input_col:
            name = gr.Textbox(label="Your Name")
            case_desc = gr.Textbox(label="Case Description", lines=5)
            submit = gr.Button("Analyze Case", variant="primary")

        with gr.Column(visible=False) as output_col:
            result_md = gr.Markdown()
            clear_btn = gr.Button("Clear")

        def on_submit(n, c):
            answer = chatbot_response(n, c)
            return (
                gr.update(visible=False),     # hide input
                gr.update(visible=True),      # show output
                gr.update(value=answer)       # fill markdown
            )

        def on_clear():
            return (
                gr.update(visible=True),
                gr.update(visible=False),
                "",
                ""
            )

        submit.click(on_submit, inputs=[name, case_desc], outputs=[input_col, output_col, result_md])
        clear_btn.click(on_clear, outputs=[input_col, output_col, name, case_desc])

        ui.launch()


if __name__ == "__main__":
    main()
