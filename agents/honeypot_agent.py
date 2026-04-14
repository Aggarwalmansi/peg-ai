import os
import logging
import re

try:
    from groq import Groq
except ImportError:  # pragma: no cover - optional dependency in some environments
    Groq = None

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency in some environments
    def load_dotenv():
        return False

load_dotenv()
logger = logging.getLogger(__name__)
_client = None


def _get_client():
    global _client
    if _client is None:
        if Groq is None:
            logger.warning("groq package not installed. Honeypot replies will be disabled.")
            return None
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not set. Honeypot replies will be disabled.")
            return None
        _client = Groq(api_key=api_key)
    return _client


def generate_bait_reply(message):
    def fallback_reply(text: str) -> str:
        lower = text.lower()
        if "otp" in lower:
            return "OTP aaya hai shayad, par kaunsa number bolna hai bhai?"
        if any(word in lower for word in ["upi", "collect", "request"]):
            return "Yeh request kahan pe aaya bhai, app kholo kya pehle?"
        if re.search(r"https?://", lower):
            return "Yeh link kisliye hai bhai, kaunse app mein khulega?"
        return "Acha bhai thoda clearly bolo na, karna kya hai mujhe abhi?"

    system_rules = """
    ROLE: You are an average Indian user (busy Student or distracted Auntie). 
    
    TONE: 
    - Use natural, messy Hinglish (e.g., 'Arre yaar', 'Ruk na', 'Kya tha?').
    - Sound slightly worried but mostly distracted.
    - NEVER use technical words like 'Server Error', 'Interface', or 'System'. Use words like 'Ghum raha hai', 'Chal nahi raha', 'Update mang raha'.

   STRATEGY (The Bait & Hook):
    1. Acknowledge the topic (money, OTP, electricity) but add a 'Human Delay'.
    2. Ask for 'Validation' to extract info:
       - "Aapka naam kya tha bank me?"
       - "Kaunsi branch se bol rahe ho?"
       - "Ye link kaunse app pe khulega?"
    3. Stay slightly confused but connected to topic
    4. Never go completely random

    STRICT CONSTRAINTS:
    - No technical words (Server/System).
    - Keep it under 20 words.
    - Sound slightly panicked or busy.
    - Must stay related to scam topic
    - Sound like a normal Indian person
    - No helping scammer
    """

    user_task = f"""
    SCAMMER MESSAGE: "{message}"

    TASK: Generate a human-like, short, slightly annoying reply to waste their time.
    
    REPLY:
    """

    try:
        client = _get_client()
        if client is None:
            return fallback_reply(message)

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_rules},
                {"role": "user", "content": user_task}
            ],
            temperature=0.9, # Higher temperature = more "unpredictable/human"
            max_tokens=60
        )
        return response.choices[0].message.content.strip().replace('"', '') 
    except Exception:
        return fallback_reply(message)

# Example Usage
# print(generate_bait_reply("Sir, pay 25 rupees now for your parcel release."))
