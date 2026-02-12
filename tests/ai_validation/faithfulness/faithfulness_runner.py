import csv
from pathlib import Path
from datetime import datetime

# -------------------------------------------------
# Imports from faithfulness layer
# -------------------------------------------------
from reasoning_with_context import run_reasoning_with_context
from deterministic_validator import deterministic_faithfulness_check
from llm_judge import run_llm_judge


# -------------------------------------------------
# Configuration
# -------------------------------------------------
INPUT_DIR = Path("data/processed/synthetic_claims")
OUTPUT_DIR = Path("tests/ai_validation/results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE = 30  # Start small for V1.4


# -------------------------------------------------
# Extract insurer from claim text
# -------------------------------------------------
def extract_insurer_from_text(text: str):
    for line in text.splitlines():
        if "Insurer Name:" in line:
            return line.split(":", 1)[1].strip()
        elif "Insurer:" in line:
            return line.split(":", 1)[1].strip()
    return None


# -------------------------------------------------
# Load synthetic claims
# -------------------------------------------------
def load_claim_files(limit: int):
    claim_files = sorted(INPUT_DIR.glob("synthetic_claim_*.txt"))
    return claim_files[:limit]


# -------------------------------------------------
# Faithfulness Evaluation Runner
# -------------------------------------------------
def run_faithfulness_evaluation():

    claim_files = load_claim_files(BATCH_SIZE)
    results = []

    print(f"\nRunning V1.4 faithfulness evaluation on {len(claim_files)} claims...\n")

    for file_path in claim_files:

        with open(file_path, "r", encoding="utf-8") as f:
            claim_text = f.read().strip()

        claim_id = file_path.stem
        insurer = extract_insurer_from_text(claim_text)

        # -----------------------------
        # Step 1: Run RAG with context
        # -----------------------------
        rag_output = run_reasoning_with_context(claim_text)

        parsed_output = rag_output["parsed_output"]
        retrieved_clauses = rag_output["retrieved_clauses"]

        if not parsed_output:
            coverage_decision = None
            confidence = None
            deterministic_status = "UNSUPPORTED"
            judge_status = "NOT_SUPPORTED"
        else:
            coverage_decision = parsed_output.get("coverage_decision")
            confidence = parsed_output.get("confidence")

            # -----------------------------
            # Step 2: Deterministic check
            # -----------------------------
            deterministic_status = deterministic_faithfulness_check(
                parsed_output,
                retrieved_clauses
            )

            # -----------------------------
            # Step 3: LLM Judge check
            # -----------------------------
            judge_status = run_llm_judge(
                claim_text,
                retrieved_clauses,
                parsed_output
            )
            
            retrieved_sources = [c.get("source_file") for c in retrieved_clauses]
            retrieved_text_snippet = " ".join(
            [c.get("text", "") for c in retrieved_clauses]
           )[:300]  # limit to 300 chars
        results.append({
            "claim_id": claim_id,
            "insurer": insurer,
            "coverage_decision": coverage_decision,
            "confidence": confidence,
            "deterministic_status": deterministic_status,
            "judge_status": judge_status,
            "retrieved_sources": ", ".join(retrieved_sources),
            "retrieved_snippet": retrieved_text_snippet
        })

        print(f"{claim_id} → Deterministic: {deterministic_status} | Judge: {judge_status}")

    # -------------------------------------------------
    # Save Results
    # -------------------------------------------------
    output_file = OUTPUT_DIR / f"v1_4_faithfulness_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "claim_id",
                "insurer",
                "coverage_decision",
                "confidence",
                "deterministic_status",
                "judge_status",
                "retrieved_sources",
                "retrieved_snippet"
            ]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_file}")

    return results


# -------------------------------------------------
# Summary Metrics
# -------------------------------------------------
def print_summary_metrics(results):

    total = len(results)

    det_supported = sum(1 for r in results if r["deterministic_status"] == "SUPPORTED")
    det_partial = sum(1 for r in results if r["deterministic_status"] == "PARTIALLY_SUPPORTED")
    det_unsupported = sum(1 for r in results if r["deterministic_status"] == "UNSUPPORTED")

    judge_supported = sum(1 for r in results if r["judge_status"] == "SUPPORTED")
    judge_partial = sum(1 for r in results if r["judge_status"] == "PARTIALLY_SUPPORTED")
    judge_not_supported = sum(1 for r in results if r["judge_status"] == "NOT_SUPPORTED")

    print("\n===== V1.4 SUMMARY =====")
    print(f"Total Claims: {total}\n")

    print("Deterministic Results:")
    print(f"SUPPORTED: {det_supported} ({det_supported/total:.2%})")
    print(f"PARTIALLY_SUPPORTED: {det_partial} ({det_partial/total:.2%})")
    print(f"UNSUPPORTED: {det_unsupported} ({det_unsupported/total:.2%})\n")

    print("LLM Judge Results:")
    print(f"SUPPORTED: {judge_supported} ({judge_supported/total:.2%})")
    print(f"PARTIALLY_SUPPORTED: {judge_partial} ({judge_partial/total:.2%})")
    print(f"NOT_SUPPORTED: {judge_not_supported} ({judge_not_supported/total:.2%})")


# -------------------------------------------------
# Entry Point
# -------------------------------------------------
if __name__ == "__main__":
    results = run_faithfulness_evaluation()
    print_summary_metrics(results)
