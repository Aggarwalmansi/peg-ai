from abc import ABC, abstractmethod
from typing import List, Dict

class AgentInterface(ABC):
    @abstractmethod
    def evaluate(self, input_text: str) -> dict:
        """
        Must return a dict with keys:
        - label: str
        - reasoning: str
        - routing_log: dict
        """
        pass

class EvalDataset(ABC):
    @abstractmethod
    def load(self) -> List[Dict]:
        """
        Must return a list of dicts with keys:
        - id: str
        - input: str
        - expected_label: str
        - category: str
        - notes: str
        """
        pass
