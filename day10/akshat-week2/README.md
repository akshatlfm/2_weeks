# PDF RAG Agent — LangGraph + Groq

## Setup
    pip install -r requirements.txt
    add GROQ_API_KEY in .env
    python ingest.py
    python agent.py

## Example Questions
1. "What is the education background of Akshat Agarwal?"
2. "What are the skills mentioned in the document?"
3. "What is sqrt(225) + 50?"

## MCP Trade-off
The calculator was planned as a real MCP server (separate process, stdio transport).
Due to time constraints it is implemented as a LangGraph node instead.
Trade-off: simpler setup, but the tool is not reusable by other MCP clients.