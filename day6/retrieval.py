from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_model
)
print("✅ ChromaDB loaded from disk!")

question = "What are the problems with recurrent neural networks?"

results = vectorstore.similarity_search(
    query=question,
    k=3
)

print(f"\n🔍 Question: {question}")
print(f"📄 Retrieved {len(results)} chunks:\n")

for i, chunk in enumerate(results):
    print(f"--- Chunk {i+1} ---")
    print(f"Content: {chunk.page_content}")
    print(f"Page: {chunk.metadata['page']}")
    print()