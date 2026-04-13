# agents/langgraph_flow.py

from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict

from agents.guardian_engine_v2 import analyze_message
from intelligence.indian_intelligence import indian_intelligence_score
from tools.bait_generator import generate_bait_reply
from tools.action_engine import execute_action

from memory.session_memory import get_context, add_message
from memory.long_term_memory import store_event
from memory.vector_memory import store_vector_event, search_similar
from tools.url_intelligence import analyze_urls
from agents.tool_executor import run_tool

# -----------------------------
# STATE DEFINITION
# -----------------------------
class AgentState(TypedDict):
    message: str
    session_id: str
    context: List[Dict]

    risk_score: int
    decision: str
    action: str
    bait_reply: str

    signals: List[str]
    trace: list
    confidence: float

    tool_call: dict
    action_result: dict
    recommendation: str
    llm_decision: str


# -----------------------------
# CONSTANTS
# -----------------------------
CRITICAL_SIGNALS = [
    "OTP Theft Attempt",
    "UPI Collect Fraud",
    "Fake Family Emergency"
]


# -----------------------------
# NODE 1: GUARDIAN
# -----------------------------
def guardian_node(state: AgentState):

    context = get_context(state["session_id"])
    result = analyze_message(state["message"])

    state["trace"] = state.get("trace", [])
    state["trace"].append(f"[Guardian] risk={result['risk_score']}")

    state["context"] = context
    state["risk_score"] = result["risk_score"]
    state["decision"] = result["final_decision"]
    state["llm_decision"] = result.get("llm_prediction", "safe")

    return state


# -----------------------------
# NODE 2: INDIAN INTELLIGENCE
# -----------------------------
def intelligence_node(state: AgentState):

    result = indian_intelligence_score(state["message"])

    state["risk_score"] = max(state["risk_score"], result["indian_score"])
    state["signals"] = result["signals"]

    state["trace"].append(f"[Indian] signals={result['signals']}")
    tool_result = state.get("tool_result", {})

    # Example: pattern boost
    if state.get("tool_used") == "pattern_check":
        if tool_result.get("documents"):
            state["risk_score"] += 15
            state["trace"].append("Pattern tool boosted risk")

    # URL boost
    if state.get("tool_used") == "url_check":
        if tool_result.get("malicious"):
            state["risk_score"] += 40
            state["signals"].append("Malicious URL")

    return state


# -----------------------------
# NODE 3: SEMANTIC INTELLIGENCE
# -----------------------------
def semantic_node(state: AgentState):

    try:
        results = search_similar(state["message"])
        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
    except Exception:
        # Collection may be empty on fresh deployment — skip semantic boost
        docs = []
        distances = []

    # CRITICAL OVERRIDE
    if any(sig in state.get("signals", []) for sig in CRITICAL_SIGNALS):
        state["risk_score"] = max(state["risk_score"], 90)
        state["trace"].append("[Override] Critical scam detected")

    # SEMANTIC BOOST
    if docs:
        similarity_score = 1 - distances[0] if distances else 0.5
        similarity_score = max(0, min(similarity_score, 1))

        boost = int(similarity_score * 20)
        state["risk_score"] += boost

        state["trace"].append(
            f"[Semantic] similarity={round(similarity_score,2)} boost={boost}"
        )

    return state


# -----------------------------
# NODE 4: DECISION ENGINE (🔥 MCP + RECOMMENDATION)
# -----------------------------
def decision_node(state: AgentState):

    # Clamp risk
    state["risk_score"] = max(0, min(state["risk_score"], 100))

    # Decision logic
    if state["risk_score"] >= 80:
        state["action"] = "block_and_bait"
        state["decision"] = "scam"

    elif state["risk_score"] >= 50:
        state["action"] = "warn_and_monitor"
        state["decision"] = "scam"

    elif state["risk_score"] >= 30:
        state["action"] = "log_only"
        state["decision"] = "scam"

    else:
        state["action"] = "allow"
        state["decision"] = "safe"

    # Minimum scam floor
    if state["decision"] == "scam":
        state["risk_score"] = max(state["risk_score"], 40)

    # Confidence
    state["confidence"] = round(state["risk_score"] / 100, 2)

    # -----------------------------
    # MCP TOOL CALL (🔥 IMPORTANT)
    # -----------------------------
    state["tool_call"] = {
        "tool": state["action"],
        "input": {
            "message": state["message"],
            "risk": state["risk_score"],
            "signals": state.get("signals", [])
        }
    }

    # -----------------------------
    # USER RECOMMENDATION
    # -----------------------------
    if state["decision"] == "scam":
        state["recommendation"] = (
            "Do not send money. Report this to cybercrime.gov.in or call 1930."
        )
    else:
        state["recommendation"] = "No action needed."

    state["trace"].append(
        f"[Decision] risk={state['risk_score']} → {state['action']}"
    )

    return state


# -----------------------------
# NODE 5: BAIT NODE
# -----------------------------
def bait_node(state: AgentState):

    if state["action"] == "block_and_bait":

        bait = generate_bait_reply(
            message=state["message"],
            context=state.get("context"),
            signals=state.get("signals")
        )

        state["bait_reply"] = bait

        if bait:
            add_message(state["session_id"], bait, "agent")

        state["trace"].append("[Bait] generated")

    else:
        state["bait_reply"] = None

    return state


# -----------------------------
# NODE 6: ACTION NODE (🔥 REAL WORLD EXECUTION)
# -----------------------------
def action_node(state: AgentState):

    action_result = execute_action(state)

    state["action_result"] = action_result

    state["trace"].append(f"[Action] {action_result}")

    return state


# -----------------------------
# NODE 7: MEMORY NODE
# -----------------------------
def memory_node(state: AgentState):

    store_event({
        "user_message": state["message"],
        "agent_reply": state.get("bait_reply"),
        "decision": state["decision"],
        "action": state["action"],
        "risk_score": state["risk_score"],
        "confidence": state.get("confidence"),
        "signals": state.get("signals", []),
        "trace": state.get("trace", [])
    })

    if state["decision"] == "scam":
        store_vector_event(
            text=state["message"],
            metadata={
                "risk": state["risk_score"],
                "signals": ", ".join(state.get("signals", []))
            }
        )

    return state


def url_node(state: AgentState):

    result = analyze_urls(state["message"], state.get("llm_decision", "safe"))

    if result["malicious"]:
        state["risk_score"] += result["risk_boost"]

        state["trace"].append(
            f"Malicious URL detected: {result['url']}"
        )

    return state

def tool_node(state: AgentState):

    result = run_tool(state["message"])

    state["tool_used"] = result["tool_used"]
    state["tool_result"] = result["tool_result"]

    state["trace"].append(f"Tool used: {result['tool_used']}")

    return state
def mcp_tool_node(state: AgentState):

    try:
        from peg_mcp.client.peg_client import run_mcp
        result = run_mcp(state["message"])

        raw = result.content[0].text

        import json
        parsed = json.loads(raw)

        state["trace"].append(f"[MCP] {parsed}")

        if parsed.get("pattern_match"):
            state["risk_score"] += parsed.get("score", 1) * 5
            state["signals"].append("MCP Pattern Match")

    except ImportError:
        state["trace"].append("[MCP] Skipped (mcp package not installed)")
    except Exception as e:
        state["trace"].append(f"[MCP ERROR] {str(e)}")

    return state
# -----------------------------
# BUILD GRAPH
# -----------------------------
def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("guardian", guardian_node)
    builder.add_node("intelligence", intelligence_node)
    builder.add_node("semantic", semantic_node)
    builder.add_node("decision", decision_node)
    builder.add_node("bait", bait_node)
    builder.add_node("action", action_node)
    builder.add_node("memory", memory_node)
    builder.add_node("mcp_tool", mcp_tool_node)
    builder.add_node("url_check", url_node)
    builder.add_node("tool", tool_node)
    builder.set_entry_point("guardian")

    builder.add_edge("guardian", "tool")
    builder.add_edge("tool", "intelligence")
    builder.add_edge("intelligence", "semantic")
    builder.add_edge("semantic", "mcp_tool")
    builder.add_edge("mcp_tool", "decision")
    builder.add_edge("decision", "bait")
    builder.add_edge("bait", "action")
    builder.add_edge("action", "memory")

    return builder.compile()