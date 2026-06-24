import os
import time
from .base import AgentInterface, EvalDataset
from .dataset import validate_dataset
from .groundedness import check_groundedness
from .routing import check_routing
from .report import summarize

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "agenteval"

try:
    from langsmith import RunTree, Client
    ls_client = Client()
except ImportError:
    RunTree = None
    ls_client = None

def run_eval(agent: AgentInterface, dataset: EvalDataset, name: str = "Evaluation", delay_seconds: float = 0.0) -> tuple[dict, list[dict]]:
    cases = dataset.load()
    validate_dataset(cases)
    
    results = []
    total_cases = len(cases)
    start_time_all = time.time()
    
    print(f"Running {name} on {total_cases} cases (throttle={delay_seconds}s)...")
    for i, case in enumerate(cases, 1):
        elapsed_so_far = time.time() - start_time_all
        if i > 1:
            avg_time = elapsed_so_far / (i - 1)
            eta_s = avg_time * (total_cases - i + 1)
            eta_str = f"ETA: {int(eta_s)}s"
        else:
            eta_str = "ETA: calc..."
            
        print(f"[{i}/{total_cases}] Evaluating {case['id']} | {eta_str}", flush=True)
        
        start = time.time()
        rt = None
        if RunTree:
            rt = RunTree(
                name=f"{name} Eval: {case['id']}",
                run_type="chain",
                project_name="agenteval",
                inputs={"input_text": case["input"]},
                tags=[name, case["category"]]
            )
            
        try:
            agent_res = agent.evaluate(case["input"])
            actual = agent_res.get("label", "ERROR")
            reasoning = agent_res.get("reasoning", "")
            routing_log = agent_res.get("routing_log", {})
            error = ""
        except Exception as e:
            actual = "ERROR"
            reasoning = ""
            routing_log = {}
            error = str(e)
            if "429" in str(e) or "rate limit" in str(e).lower():
                print("  [!] Rate limit hit. Sleeping for 60s gracefully...")
                time.sleep(60)
                agent_res = agent.evaluate(case["input"])
                actual = agent_res.get("label", "ERROR")
                reasoning = agent_res.get("reasoning", "")
                routing_log = agent_res.get("routing_log", {})
                error = ""
        elapsed = time.time() - start
        
        # Groundedness and routing eval
        time.sleep(delay_seconds) # Throttle for the judge
        judge_res = check_groundedness(case["input"], str(actual), reasoning)
        routing_res = check_routing(routing_log)
        
        correct = (str(actual).lower() == str(case["expected_label"]).lower())
        
        if rt:
            rt.end(outputs={
                "expected_label": case["expected_label"],
                "actual_label": actual,
                "reasoning": reasoning,
                "routing_log": routing_log,
                "correct": correct,
                "category": case["category"],
                "latency_seconds": elapsed,
                "error": error
            })
            rt.post()
            
            if ls_client:
                ls_client.create_feedback(
                    run_id=rt.id,
                    key="correctness",
                    score=1 if correct else 0,
                    comment=f"category:{case['category']} expected:{case['expected_label']} got:{actual}"
                )
            
        results.append({
            "id": case["id"],
            "category": case["category"],
            "input": case["input"],
            "expected": case["expected_label"],
            "actual": actual,
            "correct": correct,
            "reasoning": reasoning,
            "groundedness_verdict": judge_res.get("verdict", "error"),
            "routing": routing_res,
            "latency_seconds": elapsed,
            "error": error
        })
        
        if delay_seconds > 0 and i < total_cases:
            time.sleep(delay_seconds)
            
    summary = summarize(results, name=name)
    return summary, results
