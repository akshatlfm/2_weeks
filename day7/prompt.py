from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# ── 1. Create a reusable prompt template ─────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {subject}. Answer clearly and concisely."),
    ("human", "{question}")
])
print("✅ Prompt template created!")

# ── 2. See what the template looks like ──────────────────────
print(f"\nInput variables: {prompt.input_variables}")

# ── 3. Fill in the template ───────────────────────────────────
filled = prompt.invoke({
    "subject": "transformer neural networks",
    "question": "What is multi-head attention?"
})
print(f"\nFilled prompt:\n{filled}")

# ── 4. Send filled prompt to model ───────────────────────────
model = ChatOllama(model="llama3.2")
response = model.invoke(filled)

print(f"\n✅ Model response:\n{response.content}")  