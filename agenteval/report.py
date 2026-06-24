import os
import json
from datetime import datetime

def summarize(results: list[dict], name: str = "Evaluation"):
    total = len(results)
    correct = sum(1 for r in results if r.get("correct"))
    overall_acc = correct / total if total else 0.0

    grounded = sum(1 for r in results if r.get("groundedness_verdict") in ("grounded", "partially_grounded"))
    grounded_rate = grounded / total if total else 0.0

    print(f"\n{'='*60}")
    print(f"[{name}] OVERALL ACCURACY: {correct}/{total} = {overall_acc:.1%}")
    print(f"[{name}] GROUNDEDNESS RATE: {grounded}/{total} = {grounded_rate:.1%}")
    print(f"{'='*60}\n")
    
    # Calculate by_category
    by_category = {}
    for r in results:
        cat = r.get("category", "unknown")
        if cat not in by_category:
            by_category[cat] = {"correct": 0, "total": 0, "avg_latency": 0.0}
        by_category[cat]["total"] += 1
        if r.get("correct"):
            by_category[cat]["correct"] += 1
        by_category[cat]["avg_latency"] += r.get("latency_seconds", 0.0)
        
    for cat in by_category:
        if by_category[cat]["total"] > 0:
            by_category[cat]["avg_latency"] /= by_category[cat]["total"]
            
    # Collect failures
    failures = []
    for r in results:
        if not r.get("correct"):
            failures.append({
                "id": r.get("id"),
                "category": r.get("category"),
                "expected": r.get("expected"),
                "actual": r.get("actual"),
                "reasoning": r.get("reasoning"),
                "input": r.get("input")
            })

    summary_dict = {
        "timestamp": datetime.utcnow().isoformat(),
        "overall_accuracy": overall_acc,
        "groundedness_rate": grounded_rate,
        "total": total,
        "correct": correct,
        "by_category": by_category,
        "failures": failures
    }
    
    if name == "PEG AI":
        # Log to eval_runs.jsonl
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "eval_runs.jsonl"))
        with open(log_path, "a") as f:
            f.write(json.dumps(summary_dict) + "\n")

    return summary_dict
