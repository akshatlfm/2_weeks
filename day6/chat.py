from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import ollama

# ── 1. Load embedding model + ChromaDB ───────────────────────
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)
print("✅ RAG System Ready! Type 'quit' to exit.\n")

# ── 2. Conversation memory ────────────────────────────────────
conversation_history = []

# ── 3. Chat loop ──────────────────────────────────────────────
while True:

    # Get user question
    question = input("You: ").strip()
    if question.lower() == "quit":
        print("Goodbye!")
        break

    # ── 4. Retrieve relevant chunks ───────────────────────────
    retrieved_chunks = vectorstore.similarity_search(
        query=question,
        k=3
    )

    # ── 5. Build context + citations ──────────────────────────
    context = ""
    citations = []
    for i, chunk in enumerate(retrieved_chunks):
        context += f"\n[{i+1}] {chunk.page_content}\n"
        citations.append({
            "index": i+1,
            "page": chunk.metadata['page'],
            "preview": chunk.page_content[:80]
        })

    # ── 6. Build system prompt with context ───────────────────
    system_prompt = f"""You are a helpful assistant. Answer ONLY 
using the provided context. If the answer is not in the context, 
say 'I cannot find this in the document.' Do NOT use outside 
knowledge. Only cite source numbers [1], [2], or [3].

Context from document:
{context}"""

    # ── 7. Add user question to history ───────────────────────
    conversation_history.append({
        "role": "user",
        "content": question
    })

    # ── 8. Build full messages = system + history ─────────────
    messages = [{"role": "system", "content": system_prompt}] + conversation_history

    # ── 9. Send to Ollama ─────────────────────────────────────
    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    answer = response['message']['content']

    # ── 10. Add assistant reply to history ────────────────────
    conversation_history.append({
        "role": "assistant",
        "content": answer
    })

    # ── 11. Print answer + citations ──────────────────────────
    print(f"\n🤖 Assistant: {answer}")
    print("\n📌 Sources:")
    for c in citations:
        print(f"  [{c['index']}] Page {c['page']} → {c['preview']}...")
    print()