import os
import sys
import uuid
import random
import pandas as pd

# ------------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
RAW_CLAIMS_DIR = "data/raw/claims_tabular"
OUTPUT_DIR = "data/processed/synthetic_claims"

# ------------------------------------------------------------------
# Controlled reference data (DESIGN DECISIONS)
# ------------------------------------------------------------------

INSURER_CATEGORIES = {
    "Private": [
        "ICICI Lombard",
        "HDFC ERGO",
        "SBI General Insurance",
        "A Plus Health Insurance",
        "Alliance Health Insurance"
    ],
    "Government": [
        "Ayushman Mithra",
        "Pradhan Mantri Suraksha Bhima Yojana"
        "Saral Suraksha Bima Yojana"
    ]
}

POLICY_TYPES = [
    "Individual Health Policy",
    "Family Floater Policy",
    "Group Health Policy"
]

CLAIM_TYPES = [
    "Cashless",
    "Reimbursement"
]

HOSPITAL_CATEGORIES = [
    "Network Hospital",
    "Non-Network Hospital"
]

LENGTH_OF_STAY_OPTIONS = [
    "1–2 days",
    "3–5 days",
    "6–8 days"
]

DIAGNOSIS_OPTIONS = [
    "Knee Osteoarthritis",
    "Gallbladder Stones",
    "Cataract",
    "Hernia",
    "Fracture of Femur"
]

PROCEDURE_OPTIONS = [
    "Knee Replacement Surgery",
    "Laparoscopic Cholecystectomy",
    "Cataract Surgery",
    "Hernia Repair Surgery",
    "Orthopedic Surgical Fixation"
]

COST_BUCKETS = [
    "25,000 – 50,000",
    "50,000 – 1,00,000",
    "1,00,000 – 2,00,000",
    "2,00,000 – 5,00,000"
]

# ------------------------------------------------------------------
# Load structured datasets
# ------------------------------------------------------------------
def load_claim_datasets():
    datasets = []

    for file in os.listdir(RAW_CLAIMS_DIR):
        path = os.path.join(RAW_CLAIMS_DIR, file)

        if file.endswith(".csv"):
            datasets.append(pd.read_csv(path))
        elif file.endswith(".xlsx"):
            datasets.append(pd.read_excel(path))

    return datasets

# ------------------------------------------------------------------
# Generate a single synthetic claim document
# ------------------------------------------------------------------
def generate_claim_text(row) -> str:
    claim_id = str(uuid.uuid4())[:8]

    diagnosis = row.get("Diagnosis")
    procedure = row.get("Procedure")
    cost = row.get("Cost") or row.get("Amount")

    # Controlled fallbacks
    if not diagnosis or pd.isna(diagnosis):
        diagnosis = random.choice(DIAGNOSIS_OPTIONS)

    if not procedure or pd.isna(procedure):
        procedure = random.choice(PROCEDURE_OPTIONS)

    if not cost or pd.isna(cost):
        cost = random.choice(COST_BUCKETS)

    insurer_category = random.choice(list(INSURER_CATEGORIES.keys()))
    insurer_name = random.choice(INSURER_CATEGORIES[insurer_category])

    policy_type = random.choice(POLICY_TYPES)
    claim_type = random.choice(CLAIM_TYPES)
    hospital_category = random.choice(HOSPITAL_CATEGORIES)
    length_of_stay = random.choice(LENGTH_OF_STAY_OPTIONS)

    notes = (
        "All required documents are attached and coverage criteria appear to be met."
        if hospital_category == "Network Hospital"
        else "Claim may require additional review due to non-network hospital selection."
    )

    claim_text = f"""
Health Insurance Claim Summary

Claim ID: {claim_id}

Insurer Category: {insurer_category}
Insurer Name: {insurer_name}

Policy Type: {policy_type}
Claim Type: {claim_type}

Diagnosis:
{diagnosis}

Proposed Procedure:
{procedure}

Estimated Cost:
INR {cost}

Hospital Category:
{hospital_category}

Expected Length of Stay:
{length_of_stay}

Notes:
{notes}
""".strip()

    return claim_text

# ------------------------------------------------------------------
# Main execution
# ------------------------------------------------------------------
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Clean existing synthetic claims before regeneration
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".txt"):
            os.remove(os.path.join(OUTPUT_DIR, file))

    datasets = load_claim_datasets()
    claim_counter = 1

    for df in datasets:
        for _, row in df.iterrows():
            claim_text = generate_claim_text(row)

            filename = f"synthetic_claim_{claim_counter:04d}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(claim_text)

            claim_counter += 1

    print(f"Generated {claim_counter - 1} synthetic claim documents.")

# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
