# intelligence/indian_intelligence.py

def normalize(text: str) -> str:
    return text.lower().strip()


def indian_intelligence_score(message: str) -> dict:
    """
    Context-aware Indian scam detection layer.
    Not keyword-only → pattern + intent based.
    """

    msg = normalize(message)

    score = 0
    signals = []

    # ---------------------------
    # CRITICAL COMBINATIONS
    # ---------------------------

    # OTP + urgency → HIGH SCAM
    if "otp" in msg and ("bhej" in msg or "send" in msg or "share" in msg):
        score += 80
        signals.append("OTP Theft Attempt")

    # UPI + approve/request → CRITICAL
    if ("upi" in msg or "collect" in msg) and ("approve" in msg or "request" in msg):
        score += 85
        signals.append("UPI Collect Fraud")

    # Money + urgency → HIGH
    if ("send" in msg or "bhej" in msg or "transfer" in msg) and (
        "urgent" in msg or "jaldi" in msg or "abhi" in msg
    ):
        score += 70
        signals.append("Urgent Money Request")

    # Fake family emergency
    if ("maa" in msg or "bhai" in msg or "papa" in msg) and (
        "paise" in msg or "money" in msg or "send" in msg
    ):
        score += 75
        signals.append("Fake Family Emergency")

    # KYC scam
    if "kyc" in msg and ("update" in msg or "expire" in msg):
        score += 80
        signals.append("KYC Scam")

    # ---------------------------
    # MEDIUM SIGNALS
    # ---------------------------

    if "link" in msg or "click" in msg:
        score += 20
        signals.append("Suspicious Link")

    if "call" in msg and "urgent" in msg:
        score += 20
        signals.append("Pressure Tactic")

    # ---------------------------
    # SAFETY CHECK (VERY IMPORTANT)
    # ---------------------------

    # reduce score if message looks normal conversational
    if "let's" in msg or "kal milte" in msg or "dinner" in msg:
        score -= 30

    score = max(0, min(score, 100))

    return {
        "indian_score": score,
        "signals": signals,
    }