from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── 1. Load the PDF ───────────────────────────────────────────
loader = PyPDFLoader("attentionpaper.pdf")  # 👈 make sure PDF is in same folder
pages = loader.load()

print(f"✅ Total pages loaded: {len(pages)}")
print(f"\n--- Sample of page 1 ---\n{pages[0].page_content[:300]}")

# ── 2. Split into chunks ──────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
)

chunks = splitter.split_documents(pages)

print(f"\n✅ Total chunks created: {len(chunks)}")
print(f"\n--- Chunk 1 ---\n{chunks[0].page_content}")
print(f"\n--- Chunk 2 ---\n{chunks[1].page_content}")
print(f"\n--- Chunk 1 metadata ---\n{chunks[0].metadata}")