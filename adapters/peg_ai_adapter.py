from agenteval import AgentInterface, EvalDataset
from agents.supervisor_agent import supervisor_decision
from evaluation.golden_dataset import GOLDEN_SET

class PegAiAdapter(AgentInterface):
    def evaluate(self, input_text: str) -> dict:
        # Calls the legacy PEG AI pipeline
        res = supervisor_decision(input_text)
        return {
            "label": res.get("final_decision", "error"),
            "reasoning": res.get("reasoning", ""),
            "routing_log": res.get("routing", {})
        }

class PegAiDataset(EvalDataset):
    def load(self) -> list[dict]:
        return GOLDEN_SET
