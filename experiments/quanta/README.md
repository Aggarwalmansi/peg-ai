# PEG AI Quanta Experiments

This directory houses the experimentation harness for testing inference optimizations against the PEG AI pipeline. It operates by intercepting real API calls to capture accurate latency, token usage, and cost metrics without altering the core production evaluation logic.

## 1. Prerequisites & Environment Setup

To run the benchmarks, you must provide your own API keys via a `.env` file at the root of the repository (`peg-ai/.env`).

**Required Keys:**
- `GROQ_API_KEY`: Sourced from the Groq Cloud console. Required to power the underlying LLM models.
- `LANGCHAIN_API_KEY`: Sourced from LangSmith. Required by `agenteval` for tracing and uploading metrics.

*Note: Ensure LangSmith tracing is enabled via `LANGCHAIN_TRACING_V2=true` in your environment (already configured by default in `agenteval/runner.py`).*

## 2. Running the Baseline Benchmark

To run the baseline evaluation suite and capture performance metrics, execute:
```bash
PYTHONPATH=. python experiments/quanta/benchmarks/run_baseline.py
```
This runs a 20-case representative sample from the Golden Dataset. The harness will:
1. Wrap the `PegAiAdapter` in a `SafePegAiAdapter` (disabling persistent disk writes to prevent polluting `scam_memory.json`).
2. Monkeypatch the Groq client to capture live API metrics.
3. Automatically generate a JSON results file and a Markdown summary report.

## 3. Running the Stage 1 Prompt-Compression Variant

**Current State:** There is no distinct script for the variant. As per the current harness design, experiments are conducted by directly modifying the production pipeline (e.g., editing the system prompt in `tools/llm_guardian.py`) and re-running the baseline script:
```bash
PYTHONPATH=. python experiments/quanta/benchmarks/run_baseline.py
```
*(Note: The Stage 1 prompt compression changes were evaluated and subsequently reverted to maintain a clean working tree. To reproduce Stage 1 exactly, you must re-apply the prompt reductions to `llm_guardian.py` prior to running the benchmark).*

## 4. Configuration (`configs/baseline.yaml`)

The benchmark relies on `configs/baseline.yaml` to handle environmental specificities without hardcoding magic values in the runner:
- **Model Fallback:** Maps decommissioned models (e.g., `llama-3.1-8b-instant`) to available test equivalents (e.g., `openai/gpt-oss-20b`) to ensure the benchmark can run.
- **Judge Throttling:** Controls the `judge_throttle_seconds` pause between classification calls and the groundedness evaluator to prevent HTTP 429 Rate Limit errors from Groq.

## 5. Outputs & Metric Authenticity

- **`results/`**: Stores the raw JSON metrics for every run.
- **`reports/`**: Stores the human-readable Markdown summaries (`baseline_report.md`, `stage1_comparison.md`).

**Data Authenticity:** All metrics reported in this branch (Latency, Tokens, Cost) are strictly **REAL**. They are captured directly from live network HTTP requests to the Groq API endpoint. No LLM responses, processing times, or token counts are synthetic or mocked.

## 6. Statistical Sample Size Caveat

*(Note: The `p95` and `p99` latency metrics reported in the generated Markdown summaries are based on a sample size of n=20. At this scale, both metrics map mathematically to the single slowest outlier in the sample. They are indicative of real-world API spikes, but are not statistically precise).*
