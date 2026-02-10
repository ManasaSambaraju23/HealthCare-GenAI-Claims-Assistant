# V1.1 Batch Evaluation – Outcome & Robustness Analysis

## 1. Overview
This document summarizes the results of V1.1 batch evaluation testing for the
Healthcare GenAI Claims Assistant. The objective of this phase was to evaluate
system behavior at scale using synthetic claims and identify distribution-level
patterns, risks, and robustness gaps.

---

## 2. Test Scope & Setup
- Total synthetic claims available: 1,066
- Claims evaluated in V1.1: 500 (~47%)
- Batch size: 100 claims per run
- Execution mode: Chunked offline inference
- Data type: Fully synthetic claims (no real patient or policyholder data)

---

## 3. Outcome Distribution (500 Claims)

| Decision Category | Count | Percentage |
|------------------|-------|------------|
| Covered | 0 | 0% |
| Covered with conditions | 221 | 44.2% |
| Not covered | 24 | 4.8% |
| ERROR | 255 | 51% |

### Observation
- No unconditional "Covered" decisions were observed.
- A significant proportion of claims resulted in ERROR outcomes.

---

## 4. Confidence Distribution (Non-ERROR Cases)

| Confidence Level | Count |
|-----------------|-------|
| High | 207 |
| Medium | 40 |
| Low | 0 |

### Notes
- ERROR cases do not have confidence values, as structured output was not produced.
- Confidence is primarily distributed between High and Medium levels.

---

## 5. Insurer-Level Observations
- ERROR cases are evenly distributed between private insurers and government schemes.
- No strong insurer-specific bias was observed in ERROR frequency.
- Private insurers show a higher proportion of High-confidence decisions.
- Government schemes predominantly result in Medium-confidence decisions.

---

## 6. ERROR Analysis (High-Level)

### What ERROR Represents
- Failure to produce valid structured JSON output.
- Absence of confidence and evidence fields.
- Indicates robustness or formatting issues rather than explicit coverage decisions.

### What ERROR Does NOT Represent
- It does not indicate incorrect coverage logic.
- It does not indicate missing or malformed input data.
- It does not imply insurer bias.

### Key Limitation
Current batch outputs do not capture raw LLM responses for ERROR cases, limiting
the ability to classify root causes (e.g., JSON non-compliance vs reasoning ambiguity).

---

## 7. Key AI Quality Findings (V1.1)
- **AI-BEH-01:** Absence of unconditional "Covered" outcomes (potential over-conservatism).
- **AI-ROBUST-01:** High ERROR rate indicating robustness issues under batch execution.
- **AI-CONF-02:** Confidence skew favoring private insurers.
- **OBS-GAP-01:** Insufficient observability for ERROR diagnosis.

---

## 8. Limitations of V1.1
- No visibility into raw LLM outputs for ERROR cases.
- Root cause of ERROR outcomes cannot be conclusively determined.
- No prompt or output enforcement applied in this phase by design.

---

## 9. Next Steps (V1.2)
V1.2 will focus on improving observability for ERROR cases by:
- Capturing raw LLM responses for failed outputs
- Classifying ERROR types (e.g., JSON parse failure, partial output)
- Enabling targeted robustness and prompt regression testing

