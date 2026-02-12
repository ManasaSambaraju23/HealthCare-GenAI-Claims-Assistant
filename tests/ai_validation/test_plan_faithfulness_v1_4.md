# Phase V1.4 – Hallucination & Evidence Faithfulness Testing

## 1. Background

After stabilizing structured output in V1.3, the system reliably produces machine-readable decisions.

The next risk in RAG systems is hallucination — generating decisions not grounded in retrieved context.

## 2. Objective

Validate that coverage decisions are strictly supported by retrieved clauses.

Detect unsupported reasoning.

Measure grounding compliance rate.

## 3. Scope

### In Scope:

Compare model decision vs retrieved clauses

Validate evidence source alignment

Detect unsupported claims

### Out of Scope:

Model retraining

Prompt redesign

Policy correctness validation

## 4. Hallucination Detection Criteria

### A response is flagged if:

Decision contradicts retrieved clause

Evidence source not in retrieval set

Decision provided without supporting clause

Model references external knowledge

## 5. Execution Strategy

Select 50–100 claims

Store retrieved clauses for each claim

**Compare:** 

coverage_decision

evidence_sources

retrieved metadata

Manually inspect borderline cases

## 6. Metrics

| Metric |	Definition |
|--------|-------------|
| Faithfulness Rate	 |  % decisions fully supported |
| Unsupported Decision Rate	| %  unsupported outputs |
| Fabricated Evidence Rate	| % fake evidence references |

## 7. Exit Criteria

Faithfulness rate calculated

Hallucination types documented

Risk assessment recorded

