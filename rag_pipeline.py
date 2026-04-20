import os
import re
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# ------------------------------
# Text Cleaning
# ------------------------------
def clean_text(text):
    text = re.sub(r"\n", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.encode("ascii", "ignore").decode()
    return text.strip()

# ------------------------------
# Load & Process Documents
# ------------------------------
def load_documents(path="data/"):
    loader = PyPDFDirectoryLoader(path, glob="*.pdf")
    docs = loader.load()

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)

# ------------------------------
# Build RAG Pipeline
# ------------------------------
def build_rag():
    docs = load_documents()

    embeddings = HuggingFaceBgeEmbeddings(
        model_name="sentence-transformers/all-MiniLM-l6-v2"
    )

    db = FAISS.from_documents(docs, embeddings)

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
Helpful Answer:
""")

    doc_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever()

    return create_retrieval_chain(retriever, doc_chain)

# Initialize once
rag_chain = build_rag()

# ------------------------------
# Run Query
# ------------------------------
def run_query(query: str):
    result = rag_chain.invoke({"input": query})
    return result["answer"]
