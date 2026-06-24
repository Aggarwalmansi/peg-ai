import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from agenteval import run_eval
from adapters import PegAiAdapter, PegAiDataset

def main():
    print("\n" + "*" * 60)
    print("STARTING FULL PEG AI EVALUATION")
    print("*" * 60 + "\n")

    peg_agent = PegAiAdapter()
    peg_dataset = PegAiDataset()
    peg_summary, _ = run_eval(peg_agent, peg_dataset, name="PEG AI", delay_seconds=2.1)

    print("\nEvaluation successfully completed and logged!")

if __name__ == "__main__":
    main()
