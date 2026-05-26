from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3.2")
parser = StrOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer in 2-3 sentences."),
    ("human", "{question}")
])

# ── 1. Build chain with LCEL ──────────────────────────────────
chain = prompt | model | parser
print("✅ Chain built!")
print(f"Chain type: {type(chain)}")

# ── 2. Regular invoke ─────────────────────────────────────────
print("\n--- Regular invoke ---")
response = chain.invoke({"question": "What is multi-head attention?"})
print(response)

# ── 3. Streaming ──────────────────────────────────────────────
print("\n--- Streaming ---")
for chunk in chain.stream({"question": "What is positional encoding?"}):
    print(chunk, end="", flush=True)
print()

# ── 4. Batching ───────────────────────────────────────────────
print("\n--- Batching ---")
responses = chain.batch([
    {"question": "What is a transformer?"},
    {"question": "What is self-attention?"},
])
for i, r in enumerate(responses):
    print(f"Q{i+1}: {r[:100]}...")