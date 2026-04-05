# agents/supervisor_agent.py

from agents.guardian_engine_v2 import analyze_message
from tools.bait_generator import generate_bait_reply
from intelligence.indian_intelligence import indian_intelligence_score
from memory.session_memory import add_message, get_context
from memory.long_term_memory import store_event


def supervisor_decision(message: str, session_id: str = "default") -> dict:
    """
    Central brain of PEG.
    Combines:
    - ML + LLM (guardian)
    - Indian intelligence layer
    - Context memory
    - Decision engine
    """

    result = {
        "message": message,
        "final_decision": None,
        "risk_score": 0,
        "action": None,
        "bait_reply": None,
        "signals": [],
        "explanation": None
    }

    # -----------------------------
    # STEP 0: STORE USER MESSAGE
    # -----------------------------
    add_message(session_id, message, "user")

    # -----------------------------
    # STEP 1: CONTEXT
    # -----------------------------
    context = get_context(session_id)

    # -----------------------------
    # STEP 2: CORE ANALYSIS
    # -----------------------------
    guardian_analysis = analyze_message(message)
    indian_analysis = indian_intelligence_score(message)

    guardian_score = guardian_analysis["risk_score"]
    indian_score = indian_analysis["indian_score"]

    # -----------------------------
    # STEP 3: SCORE FUSION
    # -----------------------------
    final_score = max(guardian_score, indian_score)

    result["risk_score"] = final_score
    result["signals"] = indian_analysis["signals"]

    # -----------------------------
    # STEP 4: FINAL DECISION
    # -----------------------------
    if final_score >= 40:
        result["final_decision"] = "scam"
    else:
        result["final_decision"] = "safe"

    # -----------------------------
    # STEP 5: ACTION ENGINE
    # -----------------------------
    if result["final_decision"] == "scam":

        # HIGH RISK
        if final_score >= 75:
            result["action"] = "block_and_bait"

            bait = generate_bait_reply(message, context)
            result["bait_reply"] = bait

            # store agent response in memory
            if bait:
                add_message(session_id, bait, "agent")

            if indian_analysis["signals"]:
                result["explanation"] = (
                    f"High-risk Indian scam detected: {', '.join(indian_analysis['signals'])}. "
                    "User should not respond. Bait deployed."
                )
            else:
                result["explanation"] = (
                    "High-risk scam detected via behavioral and ML signals. Bait deployed."
                )

        # MEDIUM RISK
        elif final_score >= 40:
            result["action"] = "warn_and_monitor"

            if indian_analysis["signals"]:
                result["explanation"] = (
                    f"Suspicious pattern detected: {', '.join(indian_analysis['signals'])}. "
                    "User should be cautious."
                )
            else:
                result["explanation"] = (
                    "Moderate-risk suspicious message. User should be cautious."
                )

        # LOW RISK
        else:
            result["action"] = "log_only"
            result["explanation"] = "Low confidence anomaly. Logged for learning."

    else:
        result["action"] = "allow"
        result["explanation"] = "Message appears safe."

    # -----------------------------
    # STEP 6: LONG-TERM MEMORY
    # -----------------------------
    store_event({
        "user_message": message,
        "agent_reply": result.get("bait_reply"),
        "decision": result["final_decision"],
        "action": result["action"],
        "risk_score": result["risk_score"],
        "signals": result.get("signals", [])
    })

    return result