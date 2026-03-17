def behavioral_score(message):

    msg = message.lower()

    score = 0

    # money intent
    if any(x in msg for x in ["send", "bhej", "transfer", "upi"]):
        score += 30

    # urgency
    if any(x in msg for x in ["urgent", "jaldi", "immediately"]):
        score += 25

    # authority
    if any(x in msg for x in ["bank", "kyc", "account"]):
        score += 20

    # emotional
    if any(x in msg for x in ["maa", "brother", "friend"]):
        score += 30

    return score