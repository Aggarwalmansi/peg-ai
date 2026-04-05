from agents.langgraph_flow import build_graph
from memory.session_memory import add_message


graph = build_graph()


def run_supervisor(message: str, session_id: str = "default"):

    # store user message first
    add_message(session_id, message, "user")

    input_state = {
        "message": message,
        "session_id": session_id,
        "context": [],

        "risk_score": 0,
        "decision": "",
        "action": "",
        "bait_reply": None,
        "signals": []
    }

    result = graph.invoke(input_state)

    return result