import os
import json

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from src.ingestion.pdf_loader import load_all_policies
from src.utils.text_cleaning import clean_text
from src.ingestion.chunker import chunk_text

RAW_POLICY_DIR = "data/raw/policies"
OUTPUT_DIR = "data/processed/policy_chunks"
OUTPUT_FILE = "policy_chunks.json"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading policy PDFs...")
    policies = load_all_policies(RAW_POLICY_DIR)

    processed_documents = []

    for filename, text in policies.items():
        if not text or len(text.strip()) == 0:
            continue

        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text)

        for idx, chunk in enumerate(chunks):
            processed_documents.append({
                "source_file": filename,
                "chunk_id": idx,
                "text": chunk
            })

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_documents, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(processed_documents)} chunks to {output_path}")


if __name__ == "__main__":
    main()
