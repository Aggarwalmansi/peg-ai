import pickle
import functools
import os
import logging
from tools.behavior_engine import behavioral_score
from tools.llm_guardian import llm_classify
from agents.honeypot_agent import generate_bait_reply

logger = logging.getLogger(__name__)

# -----------------------------
# LAZY LOADERS (True Singleton)
# -----------------------------
_guardian_model = None
_guardian_vectorizer = None

def get_model():
    """Lazy-load the guardian classification model safely."""
    global _guardian_model
    if _guardian_model == "FAILED":
        raise FileNotFoundError("Model file previously failed to load.")
    if _guardian_model is None:
        model_path = "models/guardian_model_v1.pkl"
        if not os.path.exists(model_path):
            _guardian_model = "FAILED"
            raise FileNotFoundError(f"Model file not found at {model_path}")
        try:
            _guardian_model = pickle.load(open(model_path, "rb"))
        except Exception as e:
            _guardian_model = "FAILED"
            raise e
    return _guardian_model


def get_vectorizer():
    """Lazy-load the text vectorizer safely."""
    global _guardian_vectorizer
    if _guardian_vectorizer == "FAILED":
        raise FileNotFoundError("Vectorizer file previously failed to load.")
    if _guardian_vectorizer is None:
        vec_path = "models/vectorizer_v1.pkl"
        if not os.path.exists(vec_path):
            _guardian_vectorizer = "FAILED"
            raise FileNotFoundError(f"Vectorizer file not found at {vec_path}")
        try:
            _guardian_vectorizer = pickle.load(open(vec_path, "rb"))
        except Exception as e:
            _guardian_vectorizer = "FAILED"
            raise e
    return _guardian_vectorizer

def analyze_message(message):
    """
    Main engine that orchestrates ML, Behavioral Analysis,
    LLM reasoning, and the Honeypot bait generation.
    Falls back gracefully if model files are unavailable.
    """
    # 1. ML Prediction (with safe fallback when models not deployed)
    try:
        vectorizer = get_vectorizer()
        model = get_model()
        vec = vectorizer.transform([message])
        ml_res = model.predict(vec)[0]
        ml_pred = "scam" if ml_res == 1 else "safe"
    except (FileNotFoundError, Exception) as e:
        logger.warning(f"ML model unavailable, using rule-based fallback: {e}")
        ml_pred = "safe"

    # 2. Behavioral Risk Scoring (0-100)
    risk = behavioral_score(message)

    # 3. LLM Reasoning (Deep Context Analysis)
    llm_pred = llm_classify(message)

    # --- FINAL DECISION LOGIC ---
    if llm_pred == "scam":
        final = "scam"
    elif ml_pred == "scam" and risk > 30:
        final = "scam"
    elif risk > 60:
        final = "scam"
    else:
        final = "safe"

    # --- ACTIVE DEFENSE (HONEYPOT) ---
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