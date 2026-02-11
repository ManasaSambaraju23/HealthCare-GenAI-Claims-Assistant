import os
import sys
import json
import faiss
import numpy as np
import openai

# -------------------------------------------------
# Project setup
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

INDEX_DIR = "data/processed/vector_index"
INDEX_FILE = "policy_faiss.index"
META_FILE = "policy_metadata.json"

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"   # cost-efficient, reasoning-capable
TOP_K = 5

openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------------------------
def load_index_and_metadata():
    index = faiss.read_index(os.path.join(INDEX_DIR, INDEX_FILE))
    with open(os.path.join(INDEX_DIR, META_FILE), "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata

# -------------------------------------------------
def embed_query(query):
    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    return np.array(response.data[0].embedding).astype("float32")

# -------------------------------------------------
def retrieve_clauses(query, index, metadata):
    query_vector = embed_query(query)
    distances, indices = index.search(np.array([query_vector]), TOP_K)

    retrieved = []
    for idx in indices[0]:
        retrieved.append(metadata[idx])

    return retrieved

# -------------------------------------------------
def build_prompt(query, clauses):
    context = ""
    for i, c in enumerate(clauses, start=1):
        context += f"\nClause {i} (Source: {c['source_file']}):\n{c['text']}\n"

    prompt = f"""
You are a healthcare insurance policy expert.

Answer the claim question strictly using ONLY the policy clauses provided below.
If coverage is subject to waiting periods, sub-limits, exclusions, or policy conditions,
respond as "Covered with conditions" and explicitly list them.

Only respond as "Covered" if the policy clauses clearly indicate unconditional coverage.

If the claim mentions a specific insurer or scheme, prioritize clauses from that insurer or scheme.
If evidence comes from mixed insurers, lower confidence or state "Insufficient evidence".

Claim question:
{query}

Policy clauses:
{context}

Respond in the following JSON format ONLY:

{{
  "coverage_decision": "Covered | Covered with conditions | Not covered | Insufficient evidence",
  "conditions_or_exclusions": [
    "condition or exclusion 1",
    "condition or exclusion 2"
  ],
  "evidence_sources": [
    "policy file name(s)"
  ],
  "confidence": "High | Medium | Low"
}}
"""
    return prompt

# -------------------------------------------------
def run_reasoning(query):
    index, metadata = load_index_and_metadata()
    clauses = retrieve_clauses(query, index, metadata)
    prompt = build_prompt(query, clauses)

    response = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    return response.choices[0].message.content

# -------------------------------------------------
if __name__ == "__main__":

    test_queries = [
        {
            "label": "Cataract – conditional coverage",
            "query": """
            Is cataract surgery covered in the first year of a health insurance policy?
            """
        },
        {
            "label": "Cosmetic surgery – exclusion",
            "query": """
            Is cosmetic hair transplant surgery covered under health insurance?
            """
        },
        {
            "label": "Synthetic claim – ICICI Lombard",
            "query": """
            Claim Summary:
            Insurer: ICICI Lombard
            Policy Type: Individual Health Insurance
            Diagnosis: Cataract
            Proposed Procedure: Cataract surgery
            Estimated Cost: INR 45,000
            Policy Duration: 3 years

            Is this claim covered under the policy?
            """
        },
        {
            "label": "Synthetic claim – Ayushman Bharat",
            "query": """
            Claim Summary:
            Insurer: Ayushman Bharat (Government Scheme)
            Diagnosis: Knee replacement due to osteoarthritis
            Proposed Procedure: Knee replacement surgery
            Hospital Category: Government empanelled hospital

            Is this claim covered under the scheme?
            """
        }
    ]

    for item in test_queries:
        print("\n" + "=" * 120)
        print(f"TEST CASE: {item['label']}")
        print("=" * 120)

        result = run_reasoning(item["query"])
        print("\nLLM RESPONSE:\n")
        print(result)
