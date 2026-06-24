# From 53% to 96%: Finding and Fixing a Silent Routing Bug in a Production LLM Pipeline

## 1. Abstract
This report details the evaluation and remediation of PEG AI, an intelligent scam detection pipeline designed to identify complex social engineering attacks in localized contexts. We built a generalized evaluation harness (`agenteval`) to conduct a three-layer assessment across 82 golden dataset cases, discovering a critical, silent routing bug that suppressed the system's baseline accuracy to 53.7%. Fixing this structural integration flaw, combined with prompt tuning, improved the pipeline's overall classification accuracy to 96.3% while maintaining a 100% reasoning groundedness rate.

## 2. Problem Statement
Modern social engineering attacks heavily target highly localized user behaviors. In the Indian context, attackers blend languages (Hinglish) and exploit ubiquitous workflows, such as UPI payment requests and e-commerce delivery OTPs. Differentiating a malicious UPI request from a legitimate peer-to-peer transaction requires nuanced contextual understanding. To address this, PEG AI uses a hybrid architecture that fuses rule-based fallback signals with an LLM reasoning layer (Groq/LLaMA). However, deploying complex hybrid pipelines introduces structural vulnerabilities. We needed a rigorous, decoupled evaluation framework to isolate whether detection failures stemmed from poor LLM reasoning capabilities or systemic integration errors.

## 3. Methodology
We abandoned standard benchmarks in favor of a specialized 82-case golden dataset distributed across 19 categories, targeting localized scams, safe edge-cases, and Hinglish inputs. We generalized our testing code into an independent, reusable library called `agenteval`. The library implements an abstract `AgentInterface` capable of wrapping any pipeline, such as PEG AI or MeetingMind AI. 

We executed a three-layer evaluation strategy:
1. **Accuracy Testing:** We measured absolute pass/fail rates for binary classification (scam vs. safe).
2. **Groundedness Evaluation:** We forced the LLM to output a dedicated reasoning field, employing an independent LLM-as-judge pattern to verify that 100% of the reasoning explicitly referenced real input entities rather than boilerplate text.
3. **Routing Verification:** We injected structural observability into the fusion layer, logging `llm_called`, `fallback_called`, and `final_source` parameters. We tracked these metrics natively inside LangSmith traces, recording 82 individual runs with a P50 latency of 7.50s and a P99 latency of 37.90s at a 0% error rate.

## 4. Key Finding: The Routing Bug
The most critical insight from this project emerged during the baseline evaluation phase. The pipeline yielded a failing 53.7% overall accuracy (44/82). Specifically, we recorded a 0% accuracy rate across three major categories: delivery, job, and reward. 

Initial assumptions suggested the LLM lacked the contextual capability to understand these specific scam vectors. However, our evaluation harness's routing verification layer revealed a vastly different root cause. The system suffered from a silent routing integration bug at the decision fusion layer. The fallback system was over-triggering on innocuous keywords and silently overriding the LLM's correct output before the final decision could be rendered. The LLM was accurately classifying the scams, but the pipeline's deterministic layer discarded its conclusions. This finding demonstrates that in complex multi-agent systems, structural observability is as critical to performance as raw model intelligence. 

## 5. Results
Following the remediation of the routing bug and subsequent prompt tuning, pipeline performance increased dramatically. Overall accuracy jumped from 53.7% to 96.3% (79/82). All three categories that previously scored 0% were entirely resolved. 

Our groundedness evaluation confirmed that the LLM reasoning was structurally sound, achieving a 100% (82/82) groundedness rate where the model successfully based its conclusions on actual input tokens. Furthermore, the tool-use evaluation recorded a 100% success rate in capturing the `final_source` as "llm", mathematically verifying that the routing fix held securely in production.

## 6. Limitations and Open Problems
The current pipeline exhibits three remaining failures out of 82 cases:
- `otp_safe_004`: A safe message sharing a user's own OTP is flagged as a scam.
- `upi_safe_003`: A safe QR code scan for a peer-to-peer lunch payment is flagged as a scam.
- `delivery_safe_001`: An Amazon delivery agent requesting an OTP at the gate is incorrectly flagged as a scam.

During Phase 2, we uncovered a critical limitation in our evaluation architecture. The LLM-as-judge (`llama-3.1-8b-instant`) inherited the exact same contextual blind spot as the primary classification model on the `delivery_safe_001` edge case. Both models failed to recognize that sharing an OTP with an Amazon delivery driver is a legitimate, localized operational requirement in India. Independent evaluation requires an evaluator with superior context to the primary actor. 

## 7. Future Work
To resolve the evaluator blind spot, future iterations will employ a larger, more capable LLM as the judge model. Alternatively, we will inject few-shot examples detailing legitimate delivery contexts directly into the judge's system prompt. Finally, Phase 4 of this project will transition toward embedding fine-tuning, replacing static prompt tuning with a dynamic vector-search classification strategy to harden the pipeline against rapidly evolving, localized scam patterns.
