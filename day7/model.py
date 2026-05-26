from langchain_ollama import ChatOllama

# ── 1. Create the model ───────────────────────────────────────
model = ChatOllama(model="llama3.2")
print("✅ Model loaded!")

# ── 2. Invoke with a simple question ─────────────────────────
response = model.invoke("What is attention in transformers? Answer in one sentence.")

# ── 3. See the raw response object ───────────────────────────
print(f"\nFull response object:\n{response}")
print(f"\nJust the text:\n{response.content}")
print(f"\nType: {type(response)}")