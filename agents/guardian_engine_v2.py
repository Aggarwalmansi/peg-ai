import pickle
from tools.behavior_engine import behavioral_score
from tools.llm_guardian import llm_classify
from agents.honeypot_agent import generate_bait_reply

# Load models once at the start
model = pickle.load(open("models/guardian_model_v1.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer_v1.pkl", "rb"))

def analyze_message(message):
    """
    Main engine that orchestrates ML, Behavioral Analysis, 
    LLM reasoning, and the Honeypot bait generation.
    """
    # 1. ML Prediction (Handling 0/1 to string conversion)
    vec = vectorizer.transform([message])
    ml_res = model.predict(vec)[0]
    # Convert numeric ML output to string for consistent logic
    ml_pred = "scam" if ml_res == 1 else "safe"

    # 2. Behavioral Risk Scoring (0-100)
    risk = behavioral_score(message)

    # 3. LLM Reasoning (Deep Context Analysis)
    llm_pred = llm_classify(message)

    # --- FINAL DECISION LOGIC ---
    # We prioritize the LLM and High Risk scores
    if llm_pred == "scam":
        final = "scam"
    elif ml_pred == "scam" and risk > 30:
        final = "scam"
    elif risk > 60:
        final = "scam"
    else:
        final = "safe"

    # --- ACTIVE DEFENSE (HONEYPOT) ---
    # Only generate a bait reply if it's actually a scam
    bait = None
    if final == "scam":
        bait = generate_bait_reply(message)

    return {
        "message": message,
        "ml_prediction": ml_pred,
        "llm_prediction": llm_pred,
        "risk_score": risk,
        "final_decision": final,
        "bait_reply": bait
    }