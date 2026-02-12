# V1.4 – Hallucination & Evidence Faithfulness Evaluation

**Project:** Healthcare GenAI Claims Assistant  
**Phase:** V1.4 – Grounding & Faithfulness Validation  
**Evaluation Scope:** 30 synthetic claims (structured batch evaluation)

---

## 1. Objective

The objective of V1.4 was to evaluate:

- Whether LLM coverage decisions are grounded in retrieved policy clauses
- Whether cited evidence matches actual retrieval output
- Whether decisions logically align with structured claim attributes
- Whether confidence levels reflect grounding strength

This phase introduced a dual evaluation mechanism:

1. Deterministic grounding validation
2. LLM-as-Judge semantic faithfulness evaluation

---

## 2. Key Observations

### 2.1 Retrieval Contamination Across Insurers

**Observation:**  
Retrieved clauses frequently belonged to insurers different from the insurer specified in the claim.

**Example Pattern:**
- Claim insurer: *Ayushman Mithra*
- Retrieved sources: ICICI Lombard, HDFC Ergo, Reliance policies

**Root Cause:**  
FAISS retrieval is purely semantic and does not apply insurer-based metadata filtering.

**Impact:**
- Cross-policy reasoning
- Incorrect grounding
- Semantic blending of multiple insurers
- Inflated confidence levels

**Risk Level:** High (Retrieval Architecture Issue)

---

### 2.2 Diagnosis–Procedure Logical Mismatch Not Validated

**Observation:**  
Synthetic claims containing mismatched diagnosis and procedure pairs (e.g., Cataract diagnosis with Hernia surgery) were still marked as:

> "Covered with conditions" (High confidence)

The model appears to anchor on a single semantically strong token (e.g., diagnosis) and ignore cross-field inconsistency.

**Impact:**
- Partial-context reasoning bias
- Logical coherence failure
- False-positive approvals

**Risk Level:** Medium–High (Reasoning Layer Limitation)

---

### 2.3 Confidence Calibration Failure

**Observation:**  
Majority of outputs were marked as "High" confidence, even when:

- Evidence was weak
- Clauses were cross-insurer
- Evidence was fabricated
- LLM Judge flagged NOT_SUPPORTED

**Impact:**
- Overconfident hallucination risk
- Poor uncertainty calibration
- Misleading trust signals

**Risk Level:** High (Calibration Issue)

---

### 2.4 Fabricated Evidence Cases

**Observation:**  
In some cases, cited evidence sources did not exactly match retrieved metadata (minor naming variations or inconsistencies).

Deterministic validation flagged these as `FABRICATED_EVIDENCE`.

**Impact:**
- Citation traceability issues
- Auditability concern
- Evidence integrity weakness

**Risk Level:** Medium (Output Integrity Issue)

---

### 2.5 Deterministic vs LLM-Judge Disagreement

**Summary:**

- Deterministic validation: High SUPPORTED rate (~90%)
- LLM Judge: Mostly PARTIALLY_SUPPORTED or NOT_SUPPORTED

**Interpretation:**

- Deterministic logic checks lexical polarity (e.g., "excluded", "not covered")
- LLM Judge evaluates semantic applicability and logical coherence

**Conclusion:**
Deterministic validation alone is insufficient for production-grade faithfulness evaluation.

---

## 3. Root Cause Categorization

| Layer        | Issue Type                               | Severity |
|--------------|--------------------------------------------|----------|
| Retrieval    | Cross-insurer contamination                | Critical |
| Reasoning    | Partial-context bias                       | High     |
| Validation   | No structured claim coherence validation   | High     |
| Calibration  | Overconfidence bias                        | High     |
| Citation     | Minor evidence fabrication                 | Medium   |

---

## 4. Key Learning

The primary weakness observed is not classic hallucination.

It is:

> Retrieval-layer contamination leading to semantically plausible but policy-inaccurate decisions.

Additionally, the system currently lacks:

- Insurer-constrained retrieval
- Cross-field logical validation
- Confidence calibration controls
- Structured claim integrity validation

---

## 5. Next Phase Plan (V1.5 – Architectural Hardening)

Planned Improvements:

1. Introduce insurer-based metadata filtering before semantic retrieval
2. Add structured claim coherence validator (Diagnosis ↔ Procedure validation)
3. Introduce confidence calibration logic
4. Re-run V1.4 faithfulness evaluation and compare grounding metrics

---

## 6. Conclusion

V1.4 revealed systemic architectural limitations rather than isolated hallucinations.

The findings highlight the importance of:

- Metadata-aware retrieval
- Structured validation layers
- Calibration-aware confidence modeling
- Multi-layer faithfulness testing

This phase marks the transition from functional validation to production-grade AI reliability evaluation.
