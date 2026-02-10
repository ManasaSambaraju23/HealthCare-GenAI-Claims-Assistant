# AI Test Plan 
## Phase 1 – Batch Evaluation & Outcome Distribution Testing

System Under Test (SUT): Healthcare GenAI Claims Assistant – V1
Test Phase: V1.1 – AI / ML Validation
Test Type: Offline Batch Evaluation (Non-interactive)

## 1. Purpose & Test Objective
### 1.1 Purpose

The purpose of this test phase is to systematically validate decision behavior of the GenAI-based claims reasoning pipeline when executed at scale, using a controlled batch of synthetic claims.

Unlike deterministic software, GenAI systems exhibit probabilistic outputs. Therefore, correctness is evaluated at distribution and pattern level, not at single-response accuracy alone.

### 1.2 Primary Objectives

Detect systemic biases or skew in coverage decisions

Validate decision consistency across similar claims

Identify overconfidence risks in LLM-generated outputs

Establish a baseline behavior profile for future regression testing

### 1.3 Out of Scope (Explicit)

Prompt regression testing

Token-level output comparison

UI or API performance testing

Model fine-tuning or retraining

Human-in-the-loop adjudication

Ground-truth clinical or policy correctness validation

This phase evaluates behavioral patterns, not medical or legal correctness.

This phase focuses purely on observability and behavioral analysis, not optimization.

## 2. Test Scope
### 2.1 In Scope

Batch execution of 50–100 synthetic claims

End-to-end execution through:

Retrieval (FAISS)

Evidence-grounded reasoning

Structured output generation

Capture and analyze:

Coverage decisions

Confidence scores

Outcome distributions

### 2.2 Decision Classes Under Test

The system currently produces the following normalized outcomes:

Covered

Covered with conditions

Not covered

Insufficient evidence

These categories form the primary evaluation axis.

## 3. Test Strategy
### 3.1 Testing Approach

This is a black-box, outcome-driven evaluation, with internal signals used only for diagnostics (e.g., evidence sources).

The approach adapts traditional QA principles:

Equivalence partitioning → claim types (routine, exclusion-prone, ambiguous)

Boundary testing → low-evidence vs high-evidence claims

Trend analysis → outcome and confidence distributions

### 3.2 Why Batch Evaluation Is Required

Single-case testing hides systemic risk.

Batch testing enables:

Detection of decision imbalance

Identification of confidence inflation

Observation of retrieval + reasoning interaction effects

## 4. Test Data Strategy
### 4.1 Data Source

Synthetic claims generated in V1 (1000+ total)

No real patient or PHI data

Claims mapped (where possible) to:

Insurer / scheme

Procedure / condition

Cost / context

### 4.2 Batch Selection Criteria

For Phase 1:

Sample size: 50–100 claims

Mix of:

Clearly covered scenarios

Conditional scenarios

Likely exclusions

Ambiguous / low-evidence claims

Random sampling with light stratification is sufficient at this stage.

## 5. Test Execution Flow (High Level)

Load synthetic claims batch

Execute each claim through existing reasoning pipeline

Capture structured output per claim

Persist results into CSV / JSON

Perform offline analysis on distributions

## 6. Test Metrics & Observability
### 6.1 Primary Metrics (Must-Have)
Metric	Description

Outcome distribution	% Covered / Conditional / Not Covered / Insufficient

Confidence distribution	Spread of confidence scores

High-confidence rate	% outputs with confidence ≥ defined threshold

Insufficient evidence rate	Proxy for retrieval failure or ambiguity

Confidence is a normalized qualitative score (Low / Medium / High or numeric equivalent) derived from evidence consistency and policy support, not a calibrated probability.


### 6.2 Secondary Diagnostics (Optional, Not Blocking)

Insurer-wise outcome skew

Repeated evidence source patterns

Confidence vs decision correlation

## 7. Expected Outcomes & Acceptance Criteria
### 7.1 Expected “Healthy” Behavior

Aspect	Acceptable Characteristics

Outcome mix	No single class dominates (>70%)

Confidence	Majority in mid-range (0.6–0.85)

Insufficient evidence	Present but not excessive

Decision variability	Similar claims produce similar outcomes

### 7.2 Red Flags / Defects
Pattern	Risk

>80% Covered	Over-approval bias

>80% Not Covered	Over-rejection / conservative bias

Confidence >0.9 for most claims	Overconfidence / hallucination risk

Insufficient evidence near zero	Forced answers without grounding

Insurer-specific skew	Dataset or retrieval bias

These are test findings, not failures—documented as AI quality risks.

## 8. Defect Classification (AI-Specific)

Instead of classic “Pass/Fail”:

AI-BEH-01: Decision distribution skew

AI-CONF-02: Confidence inflation

AI-RET-03: Retrieval inadequacy

AI-BIAS-04: Insurer or scheme bias

Each defect is logged with:

Observed pattern

Impact

Reproducibility notes

Suggested next-phase mitigation

## 9. Test Deliverables
### 9.1 Artifacts Produced

batch_eval_results.csv

Summary statistics (computed offline)

README section documenting findings

Identified risks for Phase 2 testing

## 10. Risks & Limitations

Synthetic data may not capture real-world edge cases

LLM stochasticity introduces variance across runs

Results are directional, not statistically conclusive at this scale

Exact output reproducibility is not expected; stability of decision class and confidence band is the primary consistency criterion.


These are known and acceptable for Phase 1.


## 11. Exit Criteria

Phase 1 is considered complete when:

Batch execution runs successfully

Results are captured in structured format

Distribution patterns are analyzed and documented

### Clear risks and follow-ups are identified for Phase 2
