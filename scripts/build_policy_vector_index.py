import os
import sys
import json
import openai
import faiss
import numpy as np

# Add project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# -----------------------------
# CONFIG
# -----------------------------
CHUNKS_PATH = "data/processed/policy_chunks/policy_chunks.json"
INDEX_DIR = "data/processed/vector_index"
INDEX_FILE = "policy_faiss.index"
META_FILE = "policy_metadata.json"

EMBEDDING_MODEL = "text-embedding-3-small"

openai.api_key = os.getenv("OPENAI_API_KEY")

# -----------------------------
def load_chunks():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
def embed_texts(texts, batch_size=100):
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"Embedding batch {i // batch_size + 1} / {(len(texts) // batch_size) + 1}")

        response = openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch
        )

        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)

    return all_embeddings


# -----------------------------
def main():
    os.makedirs(INDEX_DIR, exist_ok=True)

    print("Loading policy chunks...")
    chunks = load_chunks()

    texts = [c["text"] for c in chunks]

    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = embed_texts(texts)

    vectors = np.array(embeddings).astype("float32")
    dim = vectors.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    faiss.write_index(index, os.path.join(INDEX_DIR, INDEX_FILE))

    with open(os.path.join(INDEX_DIR, META_FILE), "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print("FAISS index and metadata saved successfully.")

# -----------------------------
if __name__ == "__main__":
    main()
