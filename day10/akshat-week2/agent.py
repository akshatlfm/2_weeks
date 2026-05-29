import math
from typing import Annotated, TypedDict

from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

load_dotenv()
CHROMA_DIR = "chroma_db"
COLLECTION = "pdf_rag"

LLM = ChatGroq(model="llama-3.1-8b-instant")

SYSTEM = """You are an assistant that answers questions from a personal PDF.

To use a tool, reply with EXACTLY one of:
  RETRIEVE: <search query>
  CALCULATE: <math expression>

Rules:
- If the question is about document content, use RETRIEVE first.
- If math is needed, use CALCULATE.
- After retrieving, write your answer and cite: **Sources:** filename | page N
- Once you have everything, just write the final answer."""


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def agent_node(state: State) -> State:
    response = LLM.invoke([SystemMessage(content=SYSTEM)] + state["messages"])
    return {"messages": [response]}


def retrieve_node(state: State) -> State:
    query = state["messages"][-1].content.split("RETRIEVE:", 1)[-1].strip()

    vs = Chroma(
        collection_name=COLLECTION,
        persist_directory=CHROMA_DIR,
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    )
    results = vs.similarity_search_with_score(query, k=4)

    if not results:
        context = "No relevant content found."
    else:
        context = "\n\n---\n\n".join(
            f"[{doc.metadata.get('source','?')} | page {doc.metadata.get('page', 0)}]\n{doc.page_content}"
            for doc, _ in results
        )

    return {"messages": [ToolMessage(content=context, tool_call_id="retrieve")]}


def calculator_node(state: State) -> State:
    expr = state["messages"][-1].content.split("CALCULATE:", 1)[-1].strip()

    allowed = {
        "sqrt": math.sqrt, "log": math.log, "sin": math.sin,
        "cos": math.cos,   "pi": math.pi,   "e": math.e,
        "abs": abs,        "round": round,
    }
    try:
        result = eval(expr, {"__builtins__": {}}, allowed)
        content = f"{expr} = {result}"
    except Exception as exc:
        content = f"Error: {exc}"

    return {"messages": [ToolMessage(content=content, tool_call_id="calc")]}


def route(state: State) -> str:
    last = state["messages"][-1]
    if not isinstance(last, AIMessage):
        return END
    if "RETRIEVE:" in last.content:
        return "retrieve"
    if "CALCULATE:" in last.content:
        return "calc"
    return END


graph = StateGraph(State)
graph.add_node("agent",    agent_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("calc",     calculator_node)

graph.set_entry_point("agent")
graph.add_conditional_edges(
    "agent", route,
    {"retrieve": "retrieve", "calc": "calc", END: END}
)
graph.add_edge("retrieve", "agent")
graph.add_edge("calc",     "agent")

graph = graph.compile()


def chat(question: str) -> str:
    result = graph.invoke({"messages": [HumanMessage(content=question)]})
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Type 'quit' to exit\n")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"quit", "exit"}: break
        if q: print(f"\nAgent: {chat(q)}\n")