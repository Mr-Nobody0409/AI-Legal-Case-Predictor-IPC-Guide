import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS

from utils.preprocessing import clean_text


def load_and_process_documents(data_path="data/"):
    if not os.path.exists(data_path):
        raise FileNotFoundError("Data folder not found")

    loader = PyPDFDirectoryLoader(data_path, glob="*.pdf")
    docs = loader.load()

    for doc in docs:
        doc.page_content = clean_text(doc.page_content)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(docs)


def build_vector_store(documents):
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="sentence-transformers/all-MiniLM-l6-v2"
    )

    return FAISS.from_documents(documents, embeddings)
