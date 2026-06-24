import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluation.golden_dataset import GOLDEN_SET
from agents.supervisor_agent import supervisor_decision

def run():
    sample = GOLDEN_SET[:10]
    results = []
    
    for c in sample:
        res = supervisor_decision(c["input"])
        routing = res.get("routing", {})
        
        results.append({
            "id": c["id"],
            "input": c["input"],
            "final_source": routing.get("final_source", "unknown"),
            "llm_called": routing.get("llm_called", False),
            "fallback_called": routing.get("fallback_called", False)
        })
    
    with open("artifacts/routing_report.md", "w") as f:
        f.write("# Phase 2 Routing Eval\n\n")
        f.write("| ID | Final Source | LLM Called | Fallback Called |\n")
        f.write("|---|---|---|---|\n")
        for r in results:
            f.write(f"| `{r['id']}` | {r['final_source']} | {r['llm_called']} | {r['fallback_called']} |\n")

if __name__ == "__main__":
    run()
