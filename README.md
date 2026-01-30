# 🏥 Healthcare GenAI Claims Assistant (V1)

A **Generative AI–powered healthcare claims decision-support system** built using **Retrieval-Augmented Generation (RAG)** to analyze insurance policy documents and produce **evidence-grounded, auditable coverage decisions**.

🔍 Designed with a strong focus on **AI reliability, explainability, and quality validation** for **regulated healthcare & insurance domains**.

---

## 🎯 Business Problem

Healthcare insurance claims processing requires interpreting **complex policy language** across:
- Multiple insurers  
- Exclusions & waiting periods  
- Benefit limits & sub-limits  

📉 Manual review is **slow, inconsistent**, and prone to **interpretation errors**.

✅ This project demonstrates how **Generative AI + semantic retrieval** can assist claim analysis while maintaining **conservative, traceable, and auditable decision logic**.

---

## 🚀 Key Capabilities (V1)

### 📄 Policy Understanding
- Ingests **public healthcare insurance policy PDFs**
- Text preprocessing, normalization & **semantic chunking**

### 🧠 Semantic Retrieval
- **OpenAI embeddings** with batching for scalability
- **FAISS-based vector search**
- **Top-K retrieval** of relevant policy clauses per claim

### 🤖 Evidence-Grounded Reasoning
- LLM reasoning **strictly constrained to retrieved evidence**
- Prevents hallucinated policy interpretations

### 📊 Structured Outputs
Each claim produces:
- **Coverage decision**
- **Conditions / exclusions**
- **Evidence sources**
- **Confidence level**

### 🔁 Multi-Scenario Handling
- ✅ Covered  
- ⚠️ Covered with conditions  
- ❌ Not covered / exclusions  

---

## 🧾 Example Output

```json ```
{
  "coverage_decision": "Covered with conditions",
  "conditions_or_exclusions": [
    "Waiting period applies",
    "Sub-limits applicable as per policy terms"
  ],
  "evidence_sources": [
    "ICICI Lombard.pdf"
  ],
  "confidence": "High"
}

**🏗️ Architecture Overview**

Policy PDFs
   ↓
Text Extraction
   ↓
Chunking
   ↓
OpenAI Embeddings (Batched)
   ↓
FAISS Vector Index
   ↓
Semantic Retrieval (Top-K)
   ↓
LLM-based Claim Reasoning
   ↓
Structured Coverage Decision + Evidence


**🧪 Synthetic claims are used to simulate real-world usage — no sensitive data involved.**

**🛠️ Tech Stack**

🐍 Python

🔗 OpenAI Embeddings & Chat Completions

📚 FAISS (Vector Database)

🧮 Pandas

📄 PyPDF2

⚙️ Core RAG logic is implemented manually (no LangChain in V1) to ensure transparency, control, and debuggability.

**🔐 Data Governance & Compliance**

✅ Uses only publicly available policy documents

🧪 All claims are synthetically generated

🚫 No real patient, provider, or claim data

🎓 Built for learning, experimentation & portfolio demonstration

***📌 Project Status — Completed (V1)***

✔️ End-to-end RAG pipeline for healthcare claim analysis
✔️ Evidence-grounded & conservative LLM reasoning
✔️ Insurer-aware behavior via semantic retrieval
✔️ Robust handling of positive, conditional & negative scenarios

**🧪 QA / ML Testing Add-On (V1.1)**
**🧠 AI / ML Testing & Evaluation (Planned)**

The next iteration focuses on AI Quality Assurance and ML Testing, adapting traditional QA principles to probabilistic GenAI systems.

🔍 Planned Testing Areas
🔁 Prompt Regression Testing

Compare multiple prompt variants on the same claim set

Detect coverage decision drift due to prompt changes

Ensure backward compatibility of decision logic

📦 Batch Evaluation with Synthetic Claims

Run large batches of synthetic claims

Analyze outcome distribution:

✅ Covered

⚠️ Covered with conditions

❌ Not covered

❓ Insufficient evidence

Identify bias, over-approval, or over-rejection trends

⚠️ Negative & Edge Case Testing

Missing diagnosis or insurer

Ambiguous or conflicting inputs

Non-medical / out-of-scope queries

Validate safe fallback behavior & confidence degradation

🔄 Consistency & Robustness Testing

Re-run identical claims multiple times

Validate decision stability under low-temperature settings

Detect non-deterministic or unstable responses

🚨 Hallucination & Evidence Leakage Checks

Ensure responses rely only on retrieved policy clauses

Enforce:

❌ Not covered

❓ Insufficient evidence
when support is missing

**🧩 Why This Matters**

✨ This phase explicitly demonstrates:

ML testing

AI validation

GenAI quality engineering

Responsible AI practices for regulated domains
