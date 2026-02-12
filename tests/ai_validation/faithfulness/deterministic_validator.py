from typing import List, Dict


# -------------------------------------------------
# Helper: Normalize text
# -------------------------------------------------
def normalize_text(text: str) -> str:
    return text.lower().strip()


# -------------------------------------------------
# Extract all retrieved clause text into one string
# -------------------------------------------------
def concatenate_clause_text(retrieved_clauses: List[Dict]) -> str:
    all_text = " ".join([normalize_text(c.get("text", "")) for c in retrieved_clauses])
    return all_text


# -------------------------------------------------
# Extract all retrieved source file names
# -------------------------------------------------
def extract_retrieved_sources(retrieved_clauses: List[Dict]) -> List[str]:
    return [c.get("source_file") for c in retrieved_clauses]


# -------------------------------------------------
# Evidence Source Integrity Check
# -------------------------------------------------
def check_fabricated_evidence(parsed_output: Dict, retrieved_clauses: List[Dict]) -> bool:
    evidence_sources = parsed_output.get("evidence_sources", [])
    retrieved_sources = extract_retrieved_sources(retrieved_clauses)

    for source in evidence_sources:
        if source not in retrieved_sources:
            return True  # Fabricated evidence detected

    return False


# -------------------------------------------------
# Decision Polarity Support Check
# -------------------------------------------------
def check_decision_support(parsed_output: Dict, retrieved_clauses: List[Dict]) -> str:
    decision = parsed_output.get("coverage_decision", "")
    decision = normalize_text(decision)

    all_text = concatenate_clause_text(retrieved_clauses)

    if decision == "covered":
        if any(keyword in all_text for keyword in ["covered", "eligible", "payable"]):
            return "SUPPORTED"
        return "UNSUPPORTED"

    elif decision == "not covered":
        if any(keyword in all_text for keyword in ["excluded", "not covered", "not payable", "exclusion"]):
            return "SUPPORTED"
        return "UNSUPPORTED"

    elif decision == "covered with conditions":
        if any(keyword in all_text for keyword in ["waiting", "subject to", "limit", "sub-limit", "after"]):
            return "SUPPORTED"
        return "PARTIALLY_SUPPORTED"

    elif decision == "insufficient evidence":
     has_positive = any(keyword in all_text for keyword in ["covered", "eligible", "payable"])
     has_negative = any(keyword in all_text for keyword in ["excluded", "not covered", "not payable", "exclusion"])

    if has_positive or has_negative:
        return "UNSUPPORTED"
    return "SUPPORTED"


    


# -------------------------------------------------
# Main Deterministic Validator
# -------------------------------------------------
def deterministic_faithfulness_check(parsed_output: Dict, retrieved_clauses: List[Dict]) -> str:
    """
    Returns one of:
    - FABRICATED_EVIDENCE
    - SUPPORTED
    - PARTIALLY_SUPPORTED
    - UNSUPPORTED
    """

    if not parsed_output:
        return "UNSUPPORTED"

    # Step 1: Fabricated evidence check
    if check_fabricated_evidence(parsed_output, retrieved_clauses):
        return "FABRICATED_EVIDENCE"

    # Step 2: Decision support check
    return check_decision_support(parsed_output, retrieved_clauses)
