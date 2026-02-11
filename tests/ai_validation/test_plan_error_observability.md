# Test Plan
## Phase V1.2 – Error Observability & Structured Output Robustness

System Under Test (SUT): Healthcare GenAI Claims Assistant (RAG-based)
Test Phase: V1.2 – Error Observability Validation
Test Type: Offline Instrumented Batch Evaluation

## 1. Background

During V1.1 batch evaluation of 500 synthetic claims (~47% dataset coverage), a high ERROR rate (~51%) was observed.

However, ERROR outcomes lacked diagnostic granularity, as raw LLM responses were not captured.

This phase addresses the observability gap identified in V1.1.

## 2. Purpose & Objective

The objective of V1.2 is to:

Classify ERROR outcomes into meaningful root-cause categories

Distinguish formatting failures from reasoning failures

Capture raw LLM outputs for failed cases

Improve robustness visibility without modifying prompts or model configuration

This phase does not attempt to fix failures.

## 3. Scope

### In Scope

Instrument batch evaluation pipeline

Capture raw LLM output

Categorize error types

Run evaluation on a controlled subset (100–200 claims)

Generate structured error analysis report

### Out of Scope

Prompt redesign

JSON enforcement tools

Retry mechanisms

Model changes

Confidence recalibration

## 4. Error Classification Framework

ERROR outcomes will be categorized as follows:

### ERR-JSON-01 – Invalid JSON Format

Non-parseable output

Markdown wrapping

Extra explanation text

Missing quotes

### ERR-JSON-02 – Partial / Truncated Output

JSON cut mid-field

Missing closing braces

### ERR-SCHEMA-01 – Schema Violation

**Missing required fields:**

coverage_decision

confidence

evidence_sources

### ERR-RUNTIME-01 – Runtime Exception

Retrieval failure

API error

Timeout

Unexpected pipeline exception

### ERR-UNKNOWN

Any error not matching defined categories

## 5. Test Data Strategy

**Use:**

Previously identified ERROR claims from V1.1
OR

Controlled batch of 100–200 claims

**This ensures:**

Faster execution

Targeted error classification

## 6. Instrumentation Enhancements

The batch runner will be enhanced to log:

Field	Description

error_type	Classified root cause

raw_llm_output	Full unparsed model output

parsing_stage	Stage at which failure occurred

## 7. Execution Steps

Update batch runner with instrumentation

Execute selected batch

Generate instrumented CSV

Analyze error distribution

Document findings

## 8. Expected Outcomes

After V1.2, ERROR outcomes should be:

Quantified by category

Measurable and explainable

Separated into formatting vs logic vs runtime causes

## 9. Exit Criteria

### V1.2 is considered complete when:

All ERROR cases are classified

Root-cause percentages are computed

Observability gap from V1.1 is resolved

Findings are documented in v1_2_error_analysis.md
