import re
import requests
import os

SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_API_KEY")


def extract_urls(text):
    return re.findall(r'https?://\S+', text)


def basic_heuristic_check(url):
    """
    Lightweight intelligence (VERY IMPORTANT)
    """

    suspicious_keywords = [
        "kyc", "verify", "update", "bank", "login",
        "secure", "account", "urgent", "suspend"
    ]

    score = 0

    for word in suspicious_keywords:
        if word in url.lower():
            score += 1

    if "@" in url:
        score += 2  # phishing trick

    if url.count("-") >= 3:
        score += 1  # suspicious domain

    return score


def check_url_safety_google(url):
    """
    Google Safe Browsing (optional layer)
    """

    if not SAFE_BROWSING_API_KEY:
        return False

    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={SAFE_BROWSING_API_KEY}"

    body = {
        "client": {
            "clientId": "peg-ai",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        res = requests.post(endpoint, json=body)
        data = res.json()

        if "matches" in data:
            return True

    except Exception:
        pass

    return False


def analyze_urls(message):
    from tools.llm_guardian import llm_classify
    urls = extract_urls(message)
    llm_decision = llm_classify(message)
    if not urls:
        return {
            "malicious": False,
            "risk_boost": 0
        }

    for url in urls:

        print("🔍 Checking URL:", url)

        # 1. Heuristic detection (always works)
        heuristic_score = basic_heuristic_check(url)

        # 2. Google API (if available)
        google_flag = check_url_safety_google(url)
        
        # FINAL DECISION
        if heuristic_score >= 2 or google_flag or llm_decision == "scam":
            return {
                "malicious": True,
                "url": url,
                "risk_boost": 40,
                "reason": "Suspicious URL pattern"
            }

    return {
        "malicious": False,
        "risk_boost": 0
    }