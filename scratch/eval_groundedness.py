import sys
import os
import json
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluation.golden_dataset import GOLDEN_SET
from agents.supervisor_agent import supervisor_decision

def check_groundedness(input_text, reasoning):
    words = [w.strip(".,!?\"'") for w in reasoning.split()]
    significant_words = [w.lower() for w in words if len(w) > 3]
    if not significant_words:
        return False
    
    input_lower = input_text.lower()
    matches = [w for w in significant_words if w in input_lower]
    # Grounded if at least 2 significant words match, or ratio is decent
    return len(matches) >= 2 or len(matches) == len(significant_words)

def run():
    target_ids = ["delivery_hinglish_scam_001", "delivery_safe_001"]
    
    passing_cases = [c for c in GOLDEN_SET if c["id"] not in target_ids]
    # Sample 10 cases
    random.seed(42)
    sample_passing = random.sample(passing_cases, 10)
    sample = [c for c in GOLDEN_SET if c["id"] in target_ids] + sample_passing
    
    results = []
    for c in sample:
        res = supervisor_decision(c["input"])
        reasoning = res.get("reasoning", "")
        grounded = check_groundedness(c["input"], reasoning)
        
        results.append({
            "id": c["id"],
            "input": c["input"],
            "label": res["final_decision"],
            "reasoning": reasoning,
            "grounded": grounded
        })
    
    with open("artifacts/groundedness_report.md", "w") as f:
        f.write("# Phase 2 Groundedness Eval\n\n")
        for r in results:
            f.write(f"### `{r['id']}`\n")
            f.write(f"- **Input:** {r['input']}\n")
            f.write(f"- **Label:** {r['label']}\n")
            f.write(f"- **Reasoning:** {r['reasoning']}\n")
            f.write(f"- **Grounded:** {r['grounded']}\n\n")

if __name__ == "__main__":
    run()
