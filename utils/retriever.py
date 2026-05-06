import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document


EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Fallback IPC knowledge base if no PDFs exist in data/
FALLBACK_IPC_DOCS = [
    Document(page_content="""
IPC Section 302 – Murder
Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.
Murder is defined under Section 300: culpable homicide is murder if done with intention to cause death, or with knowledge that the act is likely to cause death.
"""),
    Document(page_content="""
IPC Section 378 & 379 – Theft
Section 378: Whoever, intending to take dishonestly any moveable property out of the possession of any person without that person's consent, moves that property, commits theft.
Section 379: Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.
"""),
    Document(page_content="""
IPC Section 420 – Cheating and dishonestly inducing delivery of property
Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, and which is capable of being converted into a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.
"""),
    Document(page_content="""
IPC Section 354 – Assault or criminal force to woman with intent to outrage her modesty
Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage her modesty, shall be punished with imprisonment of either description for a term which shall not be less than one year but which may extend to five years, and shall also be liable to fine.
"""),
    Document(page_content="""
IPC Section 376 – Punishment for rape
(1) Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, but which may extend to imprisonment for life, and shall also be liable to fine.
Rape is defined in Section 375 of the IPC.
"""),
    Document(page_content="""
IPC Section 406 – Punishment for criminal breach of trust
Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.
Criminal breach of trust (Section 405): Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, or dishonestly uses or disposes of that property in violation of any direction of law prescribing the mode in which such trust is to be discharged, commits criminal breach of trust.
"""),
    Document(page_content="""
IPC Section 498A – Husband or relative of husband of a woman subjecting her to cruelty
Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine.
Cruelty: (a) any wilful conduct which is of such a nature as is likely to drive the woman to commit suicide or to cause grave injury or danger to life, limb or health; (b) harassment with a view to coercing her or any person related to her to meet any unlawful demand for any property or valuable security.
"""),
    Document(page_content="""
IPC Section 363 & 364 – Kidnapping
Section 363: Whoever kidnaps any person from India or from lawful guardianship, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.
Section 364: Whoever kidnaps or abducts any person in order that such person may be murdered or may be so disposed of as to be put in danger of being murdered, shall be punished with imprisonment for life or rigorous imprisonment for a term which may extend to ten years, and shall also be liable to fine.
"""),
    Document(page_content="""
IPC Section 120B – Criminal Conspiracy
(1) Whoever is a party to a criminal conspiracy to commit an offence punishable with death, imprisonment for life or rigorous imprisonment for a term of two years or upwards, shall, where no express provision is made in this Code for the punishment of such a conspiracy, be punished in the same manner as if he had abetted such offence.
"""),
    Document(page_content="""
IPC Section 323 & 325 – Voluntarily causing hurt / grievous hurt
Section 323: Whoever, except in the case provided for by section 334, voluntarily causes hurt, shall be punished with imprisonment of either description for a term which may extend to one year, or with fine which may extend to one thousand rupees, or with both.
Section 325: Whoever, except in the case provided for by section 335, voluntarily causes grievous hurt, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.
"""),
    Document(page_content="""
IPC Section 390 & 392 – Robbery
Section 390: In all robbery there is either theft or extortion. Robbery is theft when the offender puts the person in fear or causes hurt.
Section 392: Whoever commits robbery shall be punished with rigorous imprisonment for a term which may extend to ten years, and shall also be liable to fine; and, if the robbery be committed on the highway between sunset and sunrise, the imprisonment may be extended to fourteen years.
"""),
    Document(page_content="""
IPC Section 463 & 465 – Forgery
Section 463: Whoever makes any false document or false electronic record or part of a document or electronic record, with intent to cause damage or injury, commits forgery.
Section 465: Punishment for forgery: Whoever commits forgery shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both.
"""),
    Document(page_content="""
IPC Section 499 & 500 – Defamation
Section 499: Whoever, by words either spoken or intended to be read, or by signs or by visible representations, makes or publishes any imputation concerning any person intending to harm, or knowing or having reason to believe that such imputation will harm, the reputation of such person, commits defamation.
Section 500: Whoever defames another shall be punished with simple imprisonment for a term which may extend to two years, or with fine, or with both.
"""),
    Document(page_content="""
IPC Section 503 & 506 – Criminal Intimidation
Section 503: Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, commits criminal intimidation.
Section 506: Punishment for criminal intimidation: Imprisonment of either description for a term which may extend to two years, or with fine, or with both; and if the threat be to cause death or grievous hurt — up to seven years.
"""),
]


def load_and_process_documents(data_dir: str) -> list[Document]:
    """
    Loads PDFs/text files from the data directory.
    Falls back to the built-in IPC knowledge base if no files are found.
    """
    documents = []

    if os.path.exists(data_dir):
        try:
            pdf_loader = DirectoryLoader(
                data_dir, glob="**/*.pdf", loader_cls=PyPDFLoader, silent_errors=True
            )
            documents.extend(pdf_loader.load())
        except Exception:
            pass

        try:
            txt_loader = DirectoryLoader(
                data_dir, glob="**/*.txt", loader_cls=TextLoader, silent_errors=True
            )
            documents.extend(txt_loader.load())
        except Exception:
            pass

    if not documents:
        print("⚠️  No documents found in data/ — using built-in IPC knowledge base.")
        documents = FALLBACK_IPC_DOCS

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)


def build_vector_store(documents: list[Document]) -> FAISS:
    """Creates a FAISS vector store from documents using MiniLM embeddings."""
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.from_documents(documents, embeddings)
