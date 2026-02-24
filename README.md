# Newpage.io Assignment — Option 1: Chat With Your Docs (RAG)

## What this project does (in simple words)
This project lets you upload documents (like PDFs or text files) and ask questions about them.
It finds the most relevant parts of the documents and uses an AI model to answer based on those parts.

## Why it exists
This is a simple, well-engineered demo of a common AI pattern called RAG (Retrieval-Augmented Generation).

## Quickstart (will expand as we add modules)
1. Create a virtual environment
2. Install dependencies
3. Start the API
4. Test `GET /health`

## Architecture (high level)
- API layer (FastAPI)
- Ingestion layer (load files + break into chunks)
- Retrieval layer (search relevant chunks)
- Generation layer (LLM answers with citations)

## Design decisions (will grow)
- Start small and reliable (health endpoint, then upload, then indexing, then chat)
- Prefer correctness over “always answering”
- Add Docker + tests + observability after core works

## What I would add next
- Hybrid retrieval (BM25 + vector)
- Reranking for better relevance
- Evaluation harness with golden Q/A set
- Auth + rate limiting for production
