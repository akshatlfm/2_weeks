from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import ollama

# ── 1. Load embedding model ───────────────────────────────────
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ── 2. Load ChromaDB from disk ────────────────────────────────
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)
print("✅ ChromaDB loaded!")

# ── 3. Define your question ───────────────────────────────────
question = "What are the problems with recurrent neural networks?"

# ── 4. Retrieve relevant chunks ───────────────────────────────
retrieved_chunks = vectorstore.similarity_search(
    query=question,
    k=3
)
print(f"✅ Retrieved {len(retrieved_chunks)} chunks!")

# ── 5. Build context from chunks ──────────────────────────────
context = ""
citations = []

for i, chunk in enumerate(retrieved_chunks):
    context += f"\n[{i+1}] {chunk.page_content}\n"
    citations.append({
        "index": i+1,
        "page": chunk.metadata['page'],
        "preview": chunk.page_content[:80]
    })

# ── 6. Build the prompt ───────────────────────────────────────
prompt = f"""You are a helpful assistant. Answer ONLY using the 
provided context. If the answer is not in the context, say 
'I cannot find this in the document.' Do NOT use outside knowledge.
Only cite source numbers [1], [2], or [3] that are provided below.

Context:
{context}

Question: {question}

Answer:"""

# ── 7. Send to Ollama LLM ─────────────────────────────────────
print("\n🤖 Asking LLM...\n")
response = ollama.chat(
    model="llama3.2",
    messages=[{"role": "user", "content": prompt}]
)

answer = response['message']['content']

# ── 8. Print answer + citations ───────────────────────────────
print("=" * 60)
print(f"Question: {question}")
print("=" * 60)
print(f"\n💬 Answer:\n{answer}")
print("\n📌 Sources:")
for c in citations:
    print(f"  [{c['index']}] Page {c['page']} → {c['preview']}...")
print("=" * 60)