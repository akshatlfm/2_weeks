import glob
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "chroma_db"
COLLECTION = "pdf_rag"

def ingest():
    pdf_paths = glob.glob("*.pdf")
    if not pdf_paths:
        raise FileNotFoundError("No PDFs found in current directory")

    docs = []
    for path in pdf_paths:
        pages = PyPDFLoader(path).load()
        docs.extend(pages)
        print(f"Loaded {Path(path).name} — {len(pages)} pages")

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=100
    ).split_documents(docs)
    print(f"Split into {len(chunks)} chunks")

    Chroma.from_documents(
        documents=chunks,
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
    )
    print("Stored in ChromaDB")

if __name__ == "__main__":
    ingest()