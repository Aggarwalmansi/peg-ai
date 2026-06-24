import sys
import os
import json
import random
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from evaluation.golden_dataset import GOLDEN_SET
from agents.supervisor_agent import supervisor_decision
from tools.llm_guardian import _get_client

def run_llm_judge(input_text, label, reasoning):
    client = _get_client()
    if not client:
        return {"verdict": "error", "explanation": "No Groq client available."}
        
    prompt = f"""
You are evaluating whether an AI's reasoning correctly interprets the INTENT of the input, not just the surface words.

Input: {input_text}
Label: {label}
Reasoning: {reasoning}

Does the reasoning correctly understand the CONTEXT and INTENT — or does it misinterpret a legitimate action as malicious? Reply only in JSON:
{{"verdict": "grounded"|"partially_grounded"|"hallucinated", "explanation": "one sentence"}}
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"},
            timeout=10.0
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except Exception as e:
        return {"verdict": "error", "explanation": str(e)}

def run():
    target_ids = ["delivery_hinglish_scam_001", "delivery_safe_001"]
    
    passing_cases = [c for c in GOLDEN_SET if c["id"] not in target_ids]
    random.seed(42)
    sample_passing = random.sample(passing_cases, 5)
    sample = [c for c in GOLDEN_SET if c["id"] in target_ids] + sample_passing
    
    results = []
    print("Running LLM judge...")
    for i, c in enumerate(sample):
        print(f"[{i+1}/{len(sample)}] Evaluating {c['id']}")
        
        # 1. Get original decision and reasoning
        res = supervisor_decision(c["input"])
        reasoning = res.get("reasoning", "")
        label = res.get("final_decision", "")
        
        time.sleep(2.1) # Throttle to avoid rate limits
        
        # 2. Run LLM judge
        judge_res = run_llm_judge(c["input"], label, reasoning)
        
        time.sleep(2.1) # Throttle again
        
        results.append({
            "id": c["id"],
            "input": c["input"],
            "label": label,
            "reasoning": reasoning,
            "judge_verdict": judge_res.get("verdict"),
            "judge_explanation": judge_res.get("explanation")
        })
        
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts", "llm_judge_report.md"))
    with open(report_path, "w") as f:
        f.write("# LLM-as-Judge Evaluation\n\n")
        for r in results:
            f.write(f"### `{r['id']}`\n")
            f.write(f"- **Input:** {r['input']}\n")
            f.write(f"- **Label:** {r['label']}\n")
            f.write(f"- **Reasoning:** {r['reasoning']}\n")
            f.write(f"- **Judge Verdict:** {r['judge_verdict']}\n")
            f.write(f"- **Judge Explanation:** {r['judge_explanation']}\n\n")
            
    print(f"Done! Report saved to {report_path}")

if __name__ == "__main__":
    run()
