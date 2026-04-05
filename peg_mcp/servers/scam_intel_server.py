# mcp/servers/scam_intel_server.py
from fastapi import FastAPI
from memory.vector_memory import search_similar

app = FastAPI()

@app.post("/check_pattern")
def check_pattern(data: dict):
    message = data.get("message")
    results = search_similar(message)
    similar_cases = len(results.get("documents", [[]])[0])

    if similar_cases > 0:                          # ← indent inside function
        return {
            "pattern_match": True,
            "similar_cases": similar_cases,
            "risk_boost": min(similar_cases * 2, 20)
        }

    # 🔥 FALLBACK
    if "upi" in message.lower() or "otp" in message.lower():   # ← indent
        return {
            "pattern_match": True,
            "similar_cases": 1,
            "risk_boost": 10
        }

    return {                                        # ← indent inside function
        "pattern_match": False,
        "similar_cases": 0,
        "risk_boost": 0
    }