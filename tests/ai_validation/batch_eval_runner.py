import os
import sys
import json
import csv
import uuid
from datetime import datetime
from pathlib import Path
import re

REQUIRED_FIELDS = [
    "coverage_decision",
    "conditions_or_exclusions",
    "evidence_sources",
    "confidence"
]


def classify_json_error(raw_output: str):
    if raw_output is None:
        return "ERR-UNKNOWN"

    # Truncated JSON detection
    if raw_output.count("{") != raw_output.count("}"):
        return "ERR-JSON-02"

    # Markdown wrapper detection
    if "```" in raw_output:
        return "ERR-JSON-01"

    return "ERR-JSON-01"


def validate_schema(parsed_json: dict):
    for field in REQUIRED_FIELDS:
        if field not in parsed_json:
            return False
    return True


# -------------------------------------------------
# Project path setup
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

# -------------------------------------------------
# IMPORT EXISTING REASONING FUNCTION
# -------------------------------------------------
# This directly reuses your pipeline
from scripts.claim_reasoning import run_reasoning
# 
# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
BATCH_SIZE = 100
MAX_CLAIMS = 500 

# Optional targeted run (set to None for full V1.2 scope)
TARGET_START = 400   # e.g., 400 for claims 401–500
TARGET_END = 500     # exclusive


INPUT_CLAIMS_DIR = Path("data/processed/synthetic_claims")

OUTPUT_DIR = Path("tests/ai_validation/results")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / f"batch_eval_results_v1_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# -------------------------------------------------
# LOAD SYNTHETIC CLAIMS
# -------------------------------------------------
def load_claims_from_directory(dir_path: Path, limit: int):
    claim_files = sorted(dir_path.glob("synthetic_claim_*.txt"))
    claims = []

    for file_path in claim_files[:limit]:
        with open(file_path, "r", encoding="utf-8") as f:
            claim_text = f.read().strip()

        claims.append({
            "claim_id": file_path.stem,   # synthetic_claim_0001
            "claim_text": claim_text,
            "metadata": extract_metadata_from_text(claim_text)
        })

    return claims
# -------------------------------------------------
# METADATA EXTRACTOR
# -------------------------------------------------
def extract_metadata_from_text(text: str):
    metadata = {}

    lines = text.splitlines()
    for line in lines:
        if "Insurer:" in line:
            metadata["insurer"] = line.split(":", 1)[1].strip()
        elif "Insurer Name:" in line:
            metadata["insurer"] = line.split(":", 1)[1].strip()
        elif "Insurer Category:" in line:
            metadata["insurer_category"] = line.split(":", 1)[1].strip()

    return metadata

# -------------------------------------------------
# SAFE JSON PARSER FOR LLM OUTPUT
# -------------------------------------------------
def parse_llm_response(raw_response: str):
    try:
        return json.loads(raw_response)
    except Exception:
        return {
            "coverage_decision": "ERROR",
            "conditions_or_exclusions": [],
            "evidence_sources": [],
            "confidence": None
        }

# -------------------------------------------------
# BATCH EXECUTION
# -------------------------------------------------
def run_v1_1_batches():
    claim_files = sorted(INPUT_CLAIMS_DIR.glob("synthetic_claim_*.txt"))

    total_available = len(claim_files)
    total_to_run = min(MAX_CLAIMS, total_available)

    print(f"Total claims available: {total_available}")
    print(f"V1.1 evaluation scope: 0 to {total_to_run}")

    # Determine batch ranges
    if TARGET_START is not None and TARGET_END is not None:
        ranges = [(TARGET_START, TARGET_END)]
    else:
        ranges = [
            (start, min(start + BATCH_SIZE, total_to_run))
            for start in range(0, total_to_run, BATCH_SIZE)
        ]

    for start_idx, end_idx in ranges:
        batch_files = claim_files[start_idx:end_idx]

        print(f"\nRunning batch: claims {start_idx + 1} to {end_idx}")

        results = []

        for file_path in batch_files:
            with open(file_path, "r", encoding="utf-8") as f:
                claim_text = f.read().strip()

            claim_id = file_path.stem
            metadata = extract_metadata_from_text(claim_text)

            error_type = None
            raw_response = None
            parsed = None

            try:
                raw_response = run_reasoning(claim_text)

                try:
                    parsed = json.loads(raw_response)

                    if not validate_schema(parsed):
                        error_type = "ERR-SCHEMA-01"

                except json.JSONDecodeError:
                    error_type = classify_json_error(raw_response)

            except Exception as e:
                error_type = "ERR-RUNTIME-01"
                raw_response = str(e)

            if error_type:
                results.append({
                    "claim_id": claim_id,
                    "insurer": metadata.get("insurer"),
                    "coverage_decision": "ERROR",
                    "confidence": None,
                    "error_type": error_type,
                    "raw_llm_output": raw_response
                })
            else:
                results.append({
                    "claim_id": claim_id,
                    "insurer": metadata.get("insurer"),
                    "coverage_decision": parsed.get("coverage_decision"),
                    "confidence": parsed.get("confidence"),
                    "error_type": None,
                    "raw_llm_output": None
                })

        output_file = OUTPUT_DIR / f"batch_eval_results_v1_2_{start_idx + 1}_to_{end_idx}.csv"
        write_results_csv(results, output_file)

        print(f"Batch saved: {output_file}")


# -------------------------------------------------
# WRITE RESULTS
# -------------------------------------------------
def write_results_csv(results, output_path: Path):
    fieldnames = [
        "claim_id",
        "insurer",
        "coverage_decision",
        "confidence",
        "error_type",
        "raw_llm_output"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    print("Starting V1.1 batch evaluation (limited to 500 claims)...")
    run_v1_1_batches()
    print("\nV1.1 batch evaluation complete.")

