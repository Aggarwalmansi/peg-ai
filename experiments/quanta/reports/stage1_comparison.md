# Experiment 1: Prompt Compression Comparison

## Overview
- **Variant Name:** Prompt Compression (removing few-shot examples and shortening system instructions)
- **Target:** System prompt size reduction.
- **Reason:** Baseline report showed high input tokens (519.8 avg) contributing to higher cost and processing times. This experiment tested whether the LLM could maintain classification accuracy with a minimal set of instructions.

## Side-by-Side Comparison

| Metric | Baseline (Original Prompt) | Variant (Compressed Prompt) | Delta / Change |
| :--- | :--- | :--- | :--- |
| **Input Tokens (Avg)** | 519.75 | 217.75 | ⬇️ **-58.1%** |
| **Output Tokens (Avg)** | 203.1 | 138.1 | ⬇️ **-32.0%** |
| **Warm E2E Latency (p50)** | 1.95s | 0.92s | ⚡ **-1.03s** (-52.8%) |
| **Warm E2E Latency (p95)** | 15.12s | 9.93s | ⚡ **-5.19s** (-34.3%) |
| **Warm E2E Latency (Avg)** | 4.84s | 1.94s | ⚡ **-2.90s** (-59.9%) |
| **Average TPS** | 180.2 tokens/s | 259.5 tokens/s | 🚀 **+44.0%** |
| **Cost per 20 cases** | $0.000845 | $0.000439 | 💰 **-48.0%** |
| **Overall Accuracy** | 100.0% | 100.0% | 🟢 **No change** |
| **Groundedness Rate** | 100.0% | 100.0% | 🟢 **No change** |

*(Note: At n=20 sample size, p95 and p99 both reflect the single slowest sample. These are indicative, not statistically precise at this sample size.)*

## Conclusion
The prompt compression variant successfully halved the p50 latency (from 1.95s to 0.92s) and almost halved the operational cost without degrading classification accuracy or groundedness. The model generated shorter reasoning outputs when provided a shorter system prompt, which contributed significantly to the latency reduction.

This variant is highly recommended for merging into production.
