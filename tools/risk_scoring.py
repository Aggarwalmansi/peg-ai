import re

def risk_score(message):

    score = 0

    if "urgent" in message.lower():
        score += 20

    if "otp" in message.lower():
        score += 30

    if re.search(r"http", message):
        score += 25

    return score