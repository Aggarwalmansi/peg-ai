import json
import os
from agenteval import AgentInterface, EvalDataset

try:
    from groq import Groq
except ImportError:
    Groq = None

MEETING_MIND_DATASET = [
    {
        "id": "mm_action_001",
        "input": "Alice: Let's follow up on the design doc. Bob: I'll draft it by Friday.",
        "expected_label": "true",
        "category": "action_item",
        "notes": "Clear action item"
    },
    {
        "id": "mm_action_002",
        "input": "Charlie: The weather is really nice today. Dave: Yeah, I love spring.",
        "expected_label": "false",
        "category": "chit_chat",
        "notes": "No action item"
    },
    {
        "id": "mm_action_003",
        "input": "Eve: Make sure to schedule the deployment window. Frank: Will do, let me coordinate with infra team tomorrow.",
        "expected_label": "true",
        "category": "action_item",
        "notes": "Clear action item"
    },
    {
        "id": "mm_action_004",
        "input": "Grace: Did you see the new UI update? Heidi: Yes, it looks great.",
        "expected_label": "false",
        "category": "chit_chat",
        "notes": "No action item"
    },
    {
        "id": "mm_action_005",
        "input": "Ivan: I need you to review the PR before we merge it today. Judy: I am on it.",
        "expected_label": "true",
        "category": "action_item",
        "notes": "Clear action item"
    }
]

class MeetingMindDataset(EvalDataset):
    def load(self) -> list[dict]:
        return MEETING_MIND_DATASET

class MeetingMindAdapter(AgentInterface):
    def __init__(self):
        self.client = None
        if Groq is not None:
            api_key = os.getenv("GROQ_API_KEY")
            if api_key:
                self.client = Groq(api_key=api_key)

    def evaluate(self, input_text: str) -> dict:
        if not self.client:
            return {"label": "error", "reasoning": "No Groq client available.", "routing_log": {}}
            
        prompt = f"""
You are MeetingMind, an AI that extracts action items from meeting transcripts.
Analyze the transcript. Does it contain a concrete action item assigned to a person?

Transcript: {input_text}

Reply in strict JSON:
{{"label": "true"|"false", "reasoning": "One sentence quoting the specific commitment or stating there is none."}}
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                response_format={"type": "json_object"},
                timeout=5.0
            )
            content = json.loads(response.choices[0].message.content.strip())
            return {
                "label": str(content.get("label", "false")).lower(),
                "reasoning": content.get("reasoning", ""),
                "routing_log": {
                    "final_source": "llm",
                    "llm_called": True,
                    "fallback_called": False
                }
            }
        except Exception as e:
            return {"label": "error", "reasoning": str(e), "routing_log": {}}
