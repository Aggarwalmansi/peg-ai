import logging
from memory.session_memory import add_message

logger = logging.getLogger(__name__)

# Graph is built lazily on first call to avoid import-time crashes
_graph = None

def _get_graph():
    global _graph
    if _graph is None:
        from agents.langgraph_flow import build_graph
        _graph = build_graph()
    return _graph


def run_supervisor(message: str, session_id: str = "default"):

    # Store user message first
    add_message(session_id, message, "user")

    input_state = {
        "message": message,
        "session_id": session_id,
        "context": [],
        "risk_score": 0,
        "decision": "",
        "action": "",
        "bait_reply": None,
        "signals": [],
        "trace": [],
    }

    graph = _get_graph()
    result = graph.invoke(input_state)

    return result