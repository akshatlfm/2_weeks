from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# ── 1. Basic StrOutputParser ──────────────────────────────────
print("=" * 50)
print("PART 1: StrOutputParser")
print("=" * 50)

model = ChatOllama(model="llama3.2")
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

# Connect with pipe operator
chain = prompt | model | parser

response = chain.invoke({"question": "What is attention in one sentence?"})

print(f"Type: {type(response)}")
print(f"Answer: {response}")

# Test it behaves like a normal string
print(type(response))
print(f"Upper: {response.upper()}")
print(f"Length: {len(response)}")
print(f"Is string-like: {isinstance(response, str)}")






# ── 2. Structured output with Pydantic ────────────────────────
print("\n" + "=" * 50)
print("PART 2: Structured Output")
print("=" * 50)

# Define the structure you want
class ConceptExplanation(BaseModel):
    concept: str = Field(description="the concept being explained")
    simple_explanation: str = Field(description="explanation in simple terms")
    example: str = Field(description="a concrete example")
    difficulty: str = Field(description="MUST be exactly one word: beginner, intermediate, or advanced")

# Tell LangChain to use this structure
structured_model = model.with_structured_output(ConceptExplanation)

structured_prompt = ChatPromptTemplate.from_messages([
    ("system", "Explain the given concept in a structured way."),
    ("human", "Explain: {concept}")
])

structured_chain = structured_prompt | structured_model

result = structured_chain.invoke({"concept": "multi-head attention"})

print(f"Type: {type(result)}")
print(f"Result Object: {result}")
print(f"\nConcept: {result.concept}")
print(f"Simple explanation: {result.simple_explanation}")
print(f"Example: {result.example}")
print(f"Difficulty: {result.difficulty}")