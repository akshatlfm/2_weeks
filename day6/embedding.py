from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ── 1. Load PDF ───────────────────────────────────────────────
loader = PyPDFLoader("attentionpaper.pdf")
pages = loader.load()

# ── 2. Split into chunks ──────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)
chunks = splitter.split_documents(pages)
print(f"✅ Total chunks: {len(chunks)}")

# ── 3. Load embedding model ───────────────────────────────────
embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
print("✅ Embedding model loaded!")

# ── 4. Store chunks + embeddings in ChromaDB ──────────────────
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="./chroma_db"
)
print(f"✅ Stored {len(chunks)} chunks in ChromaDB!")
print("✅ Database saved to ./chroma_db folder")