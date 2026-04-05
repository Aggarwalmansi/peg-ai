from agents.langgraph_flow import build_graph

graph = build_graph()

inputs = {
    "message": "UPI collect request approve now",
    "risk_score": 0,
    "decision": "",
    "action": "",
    "bait_reply": None
}

result = graph.invoke(inputs)

print(result)