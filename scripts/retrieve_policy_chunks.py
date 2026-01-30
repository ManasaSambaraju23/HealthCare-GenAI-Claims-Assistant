import os
import sys
import json
import faiss
import numpy as np
import openai

# -------------------------------------------------
# Add project root
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# -------------------------------------------------
# Paths & config
# -------------------------------------------------
INDEX_DIR = "data/processed/vector_index"
INDEX_FILE = "policy_faiss.index"
META_FILE = "policy_metadata.json"

EMBEDDING_MODEL = "text-embedding-3-small"
TOP_K = 5

openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------------------------
def load_index_and_metadata():
    index = faiss.read_index(os.path.join(INDEX_DIR, INDEX_FILE))

    with open(os.path.join(INDEX_DIR, META_FILE), "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata

# -------------------------------------------------
def embed_query(query: str):
    response = openai.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    )
    return np.array(response.data[0].embedding).astype("float32")

# -------------------------------------------------
def main():
    index, metadata = load_index_and_metadata()

    queries = [
        {
            "label": "Positive scenario – likely covered",
            "text": """
            Is knee replacement surgery covered under a private health insurance
            policy for osteoarthritis, and what conditions apply?
            """
        },
        {
            "label": "Conditional scenario – depends on policy terms",
            "text": """
            Is cataract surgery covered in the first year of a health insurance
            policy, and are there any waiting periods?
            """
        },
        {
            "label": "Negative scenario – likely not covered / irrelevant",
            "text": """
            Is cosmetic hair transplant surgery covered under health insurance?
            """
        }
    ]

    for query_item in queries:
        print("\n" + "=" * 100)
        print(f"QUERY TYPE: {query_item['label']}")
        print("QUERY:")
        print(query_item["text"].strip())
        print("=" * 100)

        query_vector = embed_query(query_item["text"])
        distances, indices = index.search(
            np.array([query_vector]), TOP_K
        )

        print("\nTop retrieved policy clauses:\n")

        for rank, idx in enumerate(indices[0], start=1):
            chunk = metadata[idx]
            distance = distances[0][rank - 1]

            print(f"Result {rank}")
            print(f"Source file: {chunk['source_file']}")
            print(f"L2 distance: {distance:.4f}")
            print("Text:")
            print(chunk["text"][:700])
            print("-" * 80)

# -------------------------------------------------
if __name__ == "__main__":
    main()