import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from agenteval import run_eval
from adapters import PegAiAdapter, PegAiDataset, MeetingMindAdapter, MeetingMindDataset

def main():
    print("\n" + "*" * 60)
    print("STARTING GENERALIZED EVALUATION HARNESS")
    print("*" * 60 + "\n")

    # 1. Evaluate PEG AI (Sample of 5)
    peg_agent = PegAiAdapter()
    peg_dataset = PegAiDataset()
    peg_summary, _ = run_eval(peg_agent, peg_dataset, name="PEG AI", delay_seconds=2.1)

    # 2. Evaluate MeetingMind (5 cases)
    mm_agent = MeetingMindAdapter()
    mm_dataset = MeetingMindDataset()
    mm_summary, _ = run_eval(mm_agent, mm_dataset, name="MeetingMind", delay_seconds=2.1)

    # 3. Side-by-Side Report
    print("\n\n" + "#" * 60)
    print("SIDE-BY-SIDE EVALUATION RESULTS")
    print("#" * 60)
    
    print(f"\n{'Metric':<25} | {'PEG AI':<15} | {'MeetingMind':<15}")
    print("-" * 61)
    
    peg_acc = f"{peg_summary['overall_accuracy']:.1%}"
    peg_gr = f"{peg_summary['groundedness_rate']:.1%}"
    
    mm_acc = f"{mm_summary['overall_accuracy']:.1%}"
    mm_gr = f"{mm_summary['groundedness_rate']:.1%}"
    
    print(f"{'Overall Accuracy':<25} | {peg_acc:<15} | {mm_acc:<15}")
    print(f"{'Groundedness Rate':<25} | {peg_gr:<15} | {mm_gr:<15}")
    print("\nEvaluation harness successfully verified across domains!")

if __name__ == "__main__":
    main()
