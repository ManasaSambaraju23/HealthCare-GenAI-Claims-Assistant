import json
import sys
from pathlib import Path
import openai

# -------------------------------------------------
# Project path setup
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

# -------------------------------------------------
# Import existing pipeline components
# -------------------------------------------------
from scripts.claim_reasoning import (
    load_index_and_metadata,
    retrieve_clauses,
    build_prompt,
    LLM_MODEL
)

# -------------------------------------------------
# Run reasoning with retrieval context
# -------------------------------------------------
def run_reasoning_with_context(query: str):
    """
    Executes full RAG pipeline and returns:
    - Parsed decision output
    - Retrieved clauses
    """

    index, metadata = load_index_and_metadata()

    # Step 1: Retrieve clauses
    retrieved_clauses = retrieve_clauses(query, index, metadata)

    # Step 2: Build prompt
    prompt = build_prompt(query, retrieved_clauses)

    # Step 3: Call LLM (structured output mode)
    response = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    raw_output = response.choices[0].message.content

    try:
        parsed_output = json.loads(raw_output)
    except json.JSONDecodeError:
        parsed_output = None

    return {
        "parsed_output": parsed_output,
        "raw_output": raw_output,
        "retrieved_clauses": retrieved_clauses
    }
