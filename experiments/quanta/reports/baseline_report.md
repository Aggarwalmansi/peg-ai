# Baseline Benchmark Report

## Overview
- **Timestamp:** 2026-08-29T08:26:09.445791
- **Sample Size:** 20 cases

## Latency Metrics
- **Cold Start Latency:** 3.50s
- **Warm E2E Latency (p50):** 1.95s
- **Warm E2E Latency (p95):** 15.12s
- **Warm E2E Latency (p99):** 15.12s
*(Note: At n=20 sample size, p95 and p99 both reflect the single slowest sample. These are indicative, not statistically precise at this sample size.)*
- **Warm E2E Latency (Avg):** 4.84s
- **TTFT (Time to First Token):** *Equivalent to API latency as calls are non-streaming.*

## Token & Generation Metrics
- **Average Input Tokens:** 217.8
- **Average Output Tokens:** 138.1
- **Average TPS (Tokens Per Second):** 259.5 tokens/sec
- **TPOT (Time Per Output Token - p50):** 0.0040s
- **TPOT (Time Per Output Token - p95):** 0.0107s
- **TPOT (Time Per Output Token - p99):** 0.0107s

## Quality Metrics
- **Overall Accuracy:** 100.0%
- **Groundedness Rate:** 100.0%

## Cost Estimates
- **Total Cost for Sample:** $0.000439
- **Average Cost per Case:** $0.000022
*(Based on LLaMA-3.1-8b-instant Groq pricing: $0.05/1M input, $0.08/1M output)*

## Methodology
- 1 warmup iteration executed prior to benchmark to exclude cold-start initialization times.
- Evaluated a random, seeded sample of 20 cases from the Golden Dataset.
- LLM metrics were monkeypatched securely around Groq API calls specifically targeting the PEG AI pipeline to avoid capturing groundedness evaluation metrics.
- Did not alter production code paths.
