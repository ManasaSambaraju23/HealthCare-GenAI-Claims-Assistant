# HealthCare-GenAI-Claims-Assistant
GenAI-powered decision-support system for analyzing healthcare insurance claims and prior authorization requests using Retrieval-Augmented Generation (RAG) on public policy and guideline documents.

## Project Status
🚧 This project is actively being built in public.

### Completed so far:
- Ingested and processed healthcare insurance policy PDFs
- Cleaned and chunked policy text for retrieval
- Generated structured synthetic insurance claim documents
- Created OpenAI embeddings with batching for scalability
- Built a FAISS vector index for efficient semantic retrieval

### In progress:
- Claim-aware policy retrieval (RAG)
- Evidence-backed answer generation
- Responsible AI & explainability layers.

## High-Level Architecture

Policy PDFs
→ Text Extraction
→ Chunking
→ OpenAI Embeddings (batched)
→ FAISS Vector Index
→ Retrieval-Augmented Generation (in progress)

Synthetic claims are used as query inputs to validate policy coverage
without using any real or sensitive patient data.

## Data & Compliance

- All policy documents used are publicly available
- All insurance claims are synthetically generated
- No real patient, provider, or claim data is used
- This project is intended for learning and demonstration purposes only

## Tech Stack

- Python
- OpenAI Embeddings
- FAISS (vector search)
- Pandas
- PyPDF2

(LLM-based retrieval and QA in progress)

