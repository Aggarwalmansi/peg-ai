# PEG AI — Intelligent Scam Detection with Production-Grade Evaluation

PEG AI is an intelligent scam detection pipeline combining rule-based signals, machine learning classifiers, and Large Language Model (LLM) reasoning to identify social engineering attacks. This project implements both the robust multi-layer detection pipeline and a custom, decoupled evaluation harness (`agenteval`) designed to rigorously test accuracy, groundedness, and routing behavior against a diverse set of real-world scam vectors.

## The Problem

Scam detection is uniquely difficult for Indian users due to highly localized, rapidly evolving attack vectors. Attackers frequently use Hinglish (a fluid mix of Hindi and English) which evades standard English-only NLP models. Furthermore, scams rely heavily on manipulating legitimate operational flows—like UPI payment requests, OTP sharing, and local e-commerce delivery notifications. Distinguishing a malicious "Scan this QR to receive money" request from a legitimate "Scan my QR to pay for lunch" interaction requires deep contextual understanding rather than simple keyword matching.

## What This Project Builds

This project delivers two core components:
1. **The Detection Pipeline:** A hybrid decision engine that fuses traditional fallback rules (for fast, obvious matches) with an advanced LLM reasoning layer (using Groq/LLaMA) to classify ambiguous or complex social engineering attempts.
2. **The `agenteval` Harness:** A decoupled, generalized evaluation library. It runs three-layer evaluations (accuracy, LLM-as-judge groundedness, and tool-use routing logs) and pushes granular correctness feedback directly into LangSmith traces.

## Key Results

| Metric | Baseline | Final |
|---|---|---|
| **Overall Accuracy** | 53.7% | 96.3% |
| **Categories at 0%** | 3 | 0 |
| **Groundedness Rate** | not measured | 100% |
| **LangSmith Traces** | 0 | 82 |

*(Evaluated on an 82-case golden dataset spanning 19 categories).*

## Phase 4: Embedding Research (Findings)
We attempted to add RAG-based retrieval 
using fine-tuned embeddings. After three 
model iterations we determined:
- BGE-small-en-v1.5 has no Hinglish 
  representation (confirmed via L2 norms)
- Fine-tuning with 1,200 triplets on a 
  12-layer multilingual model is insufficient 
  for intent-based retrieval to outperform 
  direct LLM reasoning
- Estimated 15,000-25,000 cross-lingual 
  triplets needed for viability
- Decision: RAG not integrated; LLM pipeline 
  maintained at 96.3% accuracy

This is documented in research/phase4_findings.md

## The Critical Finding

During Phase 1, our baseline evaluation showed a severe 0% accuracy drop in the delivery, job, and reward categories, dragging overall accuracy down to 53.7%. Deep inspection of the pipeline revealed **a silent routing integration bug**. The fallback rule layer was erroneously triggering on safe keywords and silently overriding the LLM's correct output before the final decision layer. The LLM was correctly identifying scams, but the fusion logic was discarding its answers. Fixing this routing bug immediately boosted the pipeline's accuracy from 53.7% to 97.6%, proving that robust observability—not just better models—is the key to production AI reliability.

## What Still Fails and Why

Despite achieving 96.3% final accuracy, the pipeline struggles with three specific edge cases:
- `otp_safe_004`: A safe message sharing an OTP is flagged as a scam.
- `upi_safe_003`: A safe QR code scan for lunch payment is flagged as a scam.
- `delivery_safe_001`: An Amazon delivery OTP notification is incorrectly flagged as a scam.

We also discovered a critical blind spot in our evaluation architecture. Our LLM-as-judge (`llama-3.1-8b-instant`) inherited the exact same hallucination pattern as the primary classifier on the `delivery_safe_001` edge case. Both models lack the localized context that Amazon delivery agents in India legitimately require an OTP at the gate. 

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install langsmith python-dotenv
   ```
2. Configure your environment variables in `.env`:
   ```env
   GROQ_API_KEY=your_groq_api_key
   LANGCHAIN_API_KEY=your_langsmith_api_key
   ```
3. Execute the generalized evaluation:
   ```bash
   PYTHONPATH=. python run_peg_eval.py
   ```

## The `agenteval` Library

The evaluation logic is completely separated from the PEG AI business logic. You can plug any AI pipeline (e.g., LangGraph agents) into the harness by implementing the `AgentInterface` abstract base class found in `agenteval/base.py`. The runner automatically handles progress logging, API rate-limit throttling (e.g., Groq 429s), LLM-as-judge groundedness checks, and automated LangSmith trace logging with per-trace correctness feedback.
