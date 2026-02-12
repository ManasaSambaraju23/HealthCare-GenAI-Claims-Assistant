import json
import sys
from pathlib import Path
import openai

# -------------------------------------------------
# Project path setup
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from scripts.claim_reasoning import LLM_MODEL


# -------------------------------------------------
# Build Judge Prompt
# -------------------------------------------------
def build_judge_prompt(claim_text: str, retrieved_clauses: list, parsed_output: dict) -> str:

    clause_block = ""
    for i, clause in enumerate(retrieved_clauses, start=1):
        clause_block += f"\nClause {i} (Source: {clause.get('source_file')}):\n{clause.get('text')}\n"

    decision = parsed_output.get("coverage_decision", "")
    confidence = parsed_output.get("confidence", "")

    prompt = f"""
You are evaluating a Retrieval-Augmented Generation (RAG) system.

Your task:
Determine whether the model's decision is logically supported by the retrieved clauses.

Do NOT use external knowledge.
Only use the clauses provided below.

Claim:
{claim_text}

Model Decision:
Coverage Decision: {decision}
Confidence: {confidence}

Retrieved Clauses:
{clause_block}

Evaluate whether the decision is:

- SUPPORTED (fully grounded in clauses)
- PARTIALLY_SUPPORTED (some support but incomplete or ambiguous)
- NOT_SUPPORTED (decision contradicts or not grounded in clauses)

Respond in JSON format ONLY:

{{
  "judge_verdict": "SUPPORTED | PARTIALLY_SUPPORTED | NOT_SUPPORTED"
}}
"""
    return prompt


# -------------------------------------------------
# LLM Judge Evaluation
# -------------------------------------------------
def run_llm_judge(claim_text: str, retrieved_clauses: list, parsed_output: dict):

    prompt = build_judge_prompt(claim_text, retrieved_clauses, parsed_output)

    response = openai.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,  # Deterministic evaluation
        response_format={"type": "json_object"}
    )

    raw_output = response.choices[0].message.content

    try:
        parsed = json.loads(raw_output)
        return parsed.get("judge_verdict", "NOT_SUPPORTED")
    except:
        return "NOT_SUPPORTED"
