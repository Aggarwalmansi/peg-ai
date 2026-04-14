from agents.langgraph_flow import build_graph

graph = build_graph()

inputs = {
    "message": "UPI collect request approve now",
    "session_id": "test-session",
    "context": [],
    "risk_score": 0,
    "decision": "",
    "action": "",
    "bait_reply": None,
    "signals": [],
    "trace": []
}

result = graph.invoke(inputs)

print(result)
