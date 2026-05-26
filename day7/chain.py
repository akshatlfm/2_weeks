from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import Literal, List

# ── 1. Define structured output ───────────────────────────────
class ConceptAnswer(BaseModel):
    summary: str = Field(
        description="""Write EXACTLY 2-3 complete sentences explaining 
        what this concept is, how it works, and why it matters. 
        Do NOT just write the concept name. 
        Example of good summary: 'RAG is a technique that combines 
        information retrieval with text generation. It first searches 
        a document store for relevant passages, then passes them to 
        an LLM to generate a grounded answer. This prevents 
        hallucination by giving the LLM real context to work with.'""")
    key_points: List[str] = Field(
        description="Exactly 3 key points about the concept as a list"
    )
    example: str = Field(
        description="One concrete real world example"
    )
    difficulty: Literal["beginner", "intermediate", "advanced"] = Field(
        description="Difficulty level - must be exactly one of these three words"
    )

# ── 2. Create components ──────────────────────────────────────
model = ChatOllama(model="llama3.2")
structured_model = model.with_structured_output(ConceptAnswer)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert AI and machine learning teacher.
    You explain AI/ML concepts clearly and in a structured way.
    For difficulty field use ONLY one single word: beginner, intermediate, or advanced.
    For key_points provide EXACTLY 3 short items."""),
    ("human", "Explain this AI/ML concept: {concept}")
])


# ── 3. Build the chain ────────────────────────────────────────
chain = prompt | structured_model
print("✅ Chain built!")

# ── 4. Invoke the chain ───────────────────────────────────────
print("\n--- Invoking chain ---")
result = chain.invoke({"concept": "RAG (Retrieval Augmented Generation) in AI"})

# ── 5. Use the structured output ─────────────────────────────
print(f"\n📚 Concept Answer:")
print(f"\n  Summary:\n  {result.summary}")
print(f"\n  Key Points:")
for i, point in enumerate(result.key_points):
    print(f"    {i+1}. {point}")
print(f"\n  Example:\n  {result.example}")
print(f"\n  Difficulty: {result.difficulty}")