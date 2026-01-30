Healthcare GenAI Claims Assistant (V1)

A GenAI-powered healthcare claims decision-support system built using Retrieval-Augmented Generation (RAG) to analyze insurance policy documents and produce evidence-grounded coverage decisions.

Designed with a focus on AI reliability, explainability, and quality validation in regulated healthcare and insurance domains.

Business Problem

Healthcare insurance claims processing involves interpreting complex policy wording across insurers, exclusions, waiting periods, and benefit limits. Manual review is slow, inconsistent, and prone to interpretation errors.

This project demonstrates how Generative AI + semantic retrieval can support claim analysis while maintaining conservative, auditable decision logic.

Key Capabilities (V1)

Policy document ingestion from public healthcare insurance PDFs

Text preprocessing, normalization, and semantic chunking

OpenAI embedding generation with batching for scalability

FAISS-based vector search for semantic policy retrieval

Top-K retrieval of relevant policy clauses per claim

LLM-based claim reasoning constrained strictly to retrieved evidence

Structured output generation:

Coverage decision

Conditions / exclusions

Evidence sources

Confidence level

Multi-scenario validation:

Covered

Covered with conditions

Not covered / exclusions

Example Output
{
  "coverage_decision": "Covered with conditions",
  "conditions_or_exclusions": [
    "Waiting period applies",
    "Sub-limits applicable as per policy terms"
  ],
  "evidence_sources": [
    "ICICI Lombard.pdf"
  ],
  "confidence": "High"
}

Architecture Overview

Policy PDFs
→ Text Extraction
→ Chunking
→ OpenAI Embeddings (batched)
→ FAISS Vector Index
→ Semantic Retrieval (Top-K)
→ LLM-based Claim Reasoning
→ Structured Coverage Decision + Evidence

Synthetic claims are used to simulate real-world usage without any sensitive data.

Tech Stack

Python

OpenAI Embeddings & Chat Completions

FAISS (Vector Database)

Pandas

PyPDF2

Core RAG logic implemented manually (no LangChain in V1) for transparency and control.

Data Governance & Compliance

Uses only publicly available policy documents

All claims are synthetically generated

No real patient, provider, or claim data is used

Designed for learning, experimentation, and portfolio demonstration

Project Status
Completed (V1)

End-to-end RAG pipeline for healthcare claim analysis

Evidence-grounded and conservative LLM reasoning

Insurer-aware behavior via semantic retrieval

Robust handling of positive, conditional, and negative scenarios

2️⃣ QA / ML TESTING ADD-ON SECTION (V1.1)



AI / ML Testing & Evaluation (Planned – V1.1)

The next iteration of this project will focus on AI quality assurance and ML testing, leveraging traditional QA principles adapted for probabilistic GenAI systems.

Planned Testing Areas
1. Prompt Regression Testing

Evaluate multiple prompt variants against the same claim set

Detect changes in coverage decisions due to prompt modifications

Ensure backward compatibility of decision logic

2. Batch Evaluation Using Synthetic Claims

Run large batches of synthetic claims through the pipeline

Analyze distribution of outcomes:

Covered

Covered with conditions

Not covered

Insufficient evidence

Identify bias, over-rejection, or over-approval patterns

3. Negative & Edge Case Testing

Claims with missing diagnosis or insurer

Ambiguous or conflicting claim inputs

Non-medical and out-of-scope queries

Validate safe fallback behavior and confidence degradation

4. Consistency & Robustness Testing

Re-run identical claims multiple times

Validate decision stability under low-temperature settings

Detect non-deterministic or unstable responses

5. Hallucination & Evidence Leakage Checks

Ensure responses rely only on retrieved policy clauses

Validate that unsupported claims return “Not covered” or “Insufficient evidence”

This phase explicitly demonstrates ML testing, AI validation, and GenAI quality engineering skills.

