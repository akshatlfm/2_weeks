from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

# ── 1. Load embedding model ───────────────────────────────────
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("✅ Embedding model loaded!")

# ── 2. Load ChromaDB ──────────────────────────────────────────
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)
print("✅ ChromaDB loaded!")

# ── 3. Create retriever ───────────────────────────────────────
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
print("✅ Retriever created!")

# ── 4. Conversation memory ────────────────────────────────────
conversation_history = []

# ── 5. Format retrieved docs ──────────────────────────────────
def format_docs(docs):
    formatted = ""
    for i, doc in enumerate(docs):
        formatted += f"\n[{i+1}] {doc.page_content}\n"
    return formatted

# ── 6. Format conversation history ───────────────────────────
def format_history(history):
    if not history:
        return "No previous conversation."
    formatted = ""
    for turn in history:
        formatted += f"Human: {turn['human']}\nAssistant: {turn['assistant']}\n\n"
    return formatted

# ── 7. Prompt template with memory ───────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not in the context say 'I cannot find this in the document.'
Do NOT use outside knowledge.

Previous conversation:
{history}

Context from document:
{context}"""),
    ("human", "{question}")
])

# ── 8. Model + parser ─────────────────────────────────────────
model = ChatOllama(model="llama3.2")
parser = StrOutputParser()

# ── 9. RAG chain ──────────────────────────────────────────────
rag_chain = (
    {
        "context":  retriever | format_docs,
        "question": RunnablePassthrough(),
        "history":  lambda _: format_history(conversation_history)
    }
    | prompt
    | model
    | parser
)
print("✅ RAG chain with memory built!")
print("Type 'quit' to exit\n")

# ── 10. Chat loop ─────────────────────────────────────────────
while True:
    question = input("You: ").strip()
    if question.lower() == "quit":
        print("Goodbye!")
        break

    # Get answer from chain
    answer = rag_chain.invoke(question)

    # Add to conversation history
    conversation_history.append({
        "human": question,
        "assistant": answer
    })

    print(f"\n🤖 Assistant: {answer}")
    print(f"💬 History length: {len(conversation_history)} turns\n")