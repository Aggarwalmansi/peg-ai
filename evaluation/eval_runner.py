"""
Eval runner for PEG AI.

This script:
1. Loads the golden dataset
2. Sends each input through your actual pipeline (same code path your
   API uses — not a reimplementation, the real thing)
3. Compares the actual output to the expected_label
4. Produces a scored report broken down by category

Run with: python3 eval_runner.py

IMPORTANT: Update the `run_pipeline` function below to call YOUR actual
PEG AI pipeline function/endpoint. This is a placeholder showing the
shape — it will not give real results until you wire it to your code.
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime

from golden_dataset import GOLDEN_SET


# ---------------------------------------------------------------------
# STEP 1: Wire this to your real pipeline.
#
# Option A — import your pipeline function directly (fastest, no network
# hop, good for local iteration):

import sys
import os

# Add the project root to sys.path so we can import from agents/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.supervisor_agent import supervisor_decision

def run_pipeline(text: str) -> str:
    result = supervisor_decision(text)
    return result.get("final_decision", "safe")

#
# Option B — call your live/local API endpoint (closer to real-world
# behavior, also measures network latency):
#
#   import requests
#   def run_pipeline(text: str) -> str:
#       resp = requests.post("http://localhost:8000/analyze",
#                             json={"message": text}, timeout=15)
#       return resp.json()["label"]
#
# Use Option A first — it isolates pipeline logic from network issues.
# Switch to Option B later to test the full deployed system end-to-end.
# ---------------------------------------------------------------------


@dataclass
class EvalResult:
    id: str
    category: str
    input: str
    expected: str
    actual: str
    correct: bool
    latency_seconds: float
    error: str = ""


def run_eval(dataset, delay_seconds: float = 0.0) -> list[EvalResult]:
    results = []
    total_cases = len(dataset)
    start_time_all = time.time()
    
    for i, case in enumerate(dataset, 1):
        elapsed_so_far = time.time() - start_time_all
        if i > 1:
            avg_time = elapsed_so_far / (i - 1)
            eta_s = avg_time * (total_cases - i + 1)
            eta_str = f"ETA: {int(eta_s)}s"
        else:
            eta_str = "ETA: calc..."
            
        print(f"[{i}/{total_cases}] Evaluating {case['id']} | {eta_str}", flush=True)
        start = time.time()
        try:
            actual = run_pipeline(case["input"])
            error = ""
        except Exception as e:
            actual = "ERROR"
            error = str(e)
            if "429" in str(e) or "rate limit" in str(e).lower():
                print("  [!] Rate limit hit. Sleeping for 60s gracefully...")
                time.sleep(60)
                actual = run_pipeline(case["input"])
                error = ""
        elapsed = time.time() - start

        results.append(EvalResult(
            id=case["id"],
            category=case["category"],
            input=case["input"],
            expected=case["expected_label"],
            actual=actual,
            correct=(actual == case["expected_label"]),
            latency_seconds=elapsed,
            error=error,
        ))
        
        if delay_seconds > 0 and i < total_cases:
            time.sleep(delay_seconds)
            
    return results


def summarize(results: list[EvalResult]):
    total = len(results)
    correct = sum(r.correct for r in results)
    overall_acc = correct / total if total else 0.0

    print(f"\n{'='*60}")
    print(f"OVERALL ACCURACY: {correct}/{total} = {overall_acc:.1%}")
    print(f"{'='*60}\n")

    # Breakdown by category — this is the part that actually teaches you
    # something. A flat accuracy number hides WHERE the system is weak.
    by_category = {}
    for r in results:
        by_category.setdefault(r.category, []).append(r)

    print("BY CATEGORY:")
    for cat, items in sorted(by_category.items()):
        cat_correct = sum(r.correct for r in items)
        cat_total = len(items)
        avg_latency = sum(r.latency_seconds for r in items) / cat_total
        print(f"  {cat:20s} {cat_correct}/{cat_total} ({cat_correct/cat_total:.0%})  "
              f"avg latency: {avg_latency:.2f}s")

    # Show every FAILURE in detail — this is where real learning happens.
    # Don't just look at the score, read WHY each one failed.
    failures = [r for r in results if not r.correct]
    if failures:
        print(f"\nFAILURES ({len(failures)}):")
        for r in failures:
            print(f"  [{r.id}] expected={r.expected} got={r.actual}")
            print(f"    input: {r.input[:80]}")
            if r.error:
                print(f"    error: {r.error}")
    else:
        print("\nNo failures.")

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "overall_accuracy": overall_acc,
        "total": total,
        "correct": correct,
        "by_category": {
            cat: {
                "correct": sum(r.correct for r in items),
                "total": len(items),
                "avg_latency": sum(r.latency_seconds for r in items) / len(items),
            }
            for cat, items in by_category.items()
        },
        "failures": [
            {"id": r.id, "expected": r.expected, "actual": r.actual, "input": r.input}
            for r in failures
        ],
    }


def save_run(summary: dict, path: str = "eval_runs.jsonl"):
    """
    Append this run's summary to a log file. Over time, this becomes your
    track record — you can plot accuracy over commits/days and PROVE
    whether changes you made actually helped or hurt.
    """
    with open(path, "a") as f:
        f.write(json.dumps(summary) + "\n")
    print(f"\nRun saved to {path}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run PEG AI evaluation suite.")
    parser.add_argument("--dataset", choices=["dev", "full"], default="dev", help="Dataset to run.")
    parser.add_argument("--delay-seconds", type=float, default=2.1, help="Delay between requests to avoid rate limits.")
    args = parser.parse_args()

    if args.dataset == "dev":
        dataset_to_run = GOLDEN_SET[:10]
    else:
        dataset_to_run = GOLDEN_SET

    print(f"Running eval on {len(dataset_to_run)} cases (throttle={args.delay_seconds}s)...")
    results = run_eval(dataset_to_run, delay_seconds=args.delay_seconds)
    summary = summarize(results)
    save_run(summary)