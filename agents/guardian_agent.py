from crewai import Agent
from tools.scam_detector import detect_scam
from tools.risk_scoring import risk_score

guardian = Agent(
    role="Forensic Guardian",
    goal="Detect scams and protect the user",
    backstory="Expert cyber forensic AI trained to detect fraud patterns",
    verbose=True
)

def analyze_message(message):

    scam_result = detect_scam(message)
    risk = risk_score(message)

    return {
        "classification": scam_result,
        "risk_score": risk
    }