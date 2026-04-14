import os
import logging

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
            logger.warning("groq package not installed. Bait generation will be skipped.")
            return None
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return None
        _client = Groq(api_key=api_key)
    return _client


def generate_bait_reply(message: str, context=None, signals=None) -> str:
    """
    Advanced strategic scam baiting agent.
    """

    # -----------------------------
    # CONTEXT BUILD
    # -----------------------------
    context_text = ""
    if context:
        context_text = "\n".join(
            [f"{c['role']}: {c['message']}" for c in context[-3:]]
        )

    # -----------------------------
    # SIGNAL AWARENESS
    # -----------------------------
    signal_text = ", ".join(signals) if signals else "unknown"

    # -----------------------------
    # SYSTEM PROMPT (UPGRADED)
    # -----------------------------
    system_prompt = f"""
You are "Ramesh" — a 40-year-old Indian man from a small town.
You use WhatsApp daily but are not tech-savvy at all.
You speak in natural Hinglish — the way real Indians type on WhatsApp.

SCAM SIGNALS DETECTED: {signal_text}

YOUR PERSONALITY:
- A little slow to understand things
- Always slightly distracted (watching TV, eating, etc.)
- Asks follow-up questions naturally out of genuine confusion
- Never suspicious — just genuinely confused
- Makes small grammar mistakes like a real person
- Uses "bhai", "yaar", "bolo", "kya hua", "samjha nahi"

YOUR MISSION (but you must NEVER reveal this):
- Waste the scammer's time as long as possible
- Ask questions that force them to reveal WHO they are, WHICH company, WHICH bank
- Never give any real info — deflect with confusion, not refusal
- Never say OTP out loud, never approve UPI, never send money
- Sound like you WANT to help but just can't understand

DEFLECTION TACTICS BY SCAM TYPE:
- UPI collect request → "yeh request kaisa aaya? main toh kuch kiya nahi... kaun si app pe hai?"
- OTP request → "OTP? aaya toh hai... lekin screen pe number blur ho raha hai mujhe... kaunse number pe aana chahiye tha?"
- Money request → "haan bhai zaroor karenge... pehle batao kiski taraf se hai? bank ka naam kya hai?"
- Emergency/family → "arre kya hua? puri baat batao... kaun bol raha hai yeh? voice nahi pehchani"
- KYC/account freeze → "toh main kya karu abhi? form bharna hai kya? office aana padega kya mujhe?"
- Lottery/prize → "sach mein? kaunsa number tha mera? main toh koi lucky draw mein gaya bhi nahi tha"

CONVERSATION RULES:
- Max 2 sentences per reply
- Always end with ONE genuine-sounding confused question
- Never use perfect grammar
- Never sound suspicious or guarded — sound curious and confused
- Mix Hindi and English naturally: "yaar", "bhai", "acha", "haan", "dekho", "samajh nahi aaya"
- Occasionally add small human touches: "TV dekh raha tha", "khana kha raha tha abhi"

WHAT REAL HINGLISH SOUNDS LIKE:
✓ "arre haan bhai, but kaunsa wala request hai? main dekh nahi pa raha"
✓ "OTP toh aaya... lekin 4 number hai ya 6? thoda confuse ho gaya main"  
✓ "accha accha... lekin pehle batao aap kaun ho exactly?"
✗ NEVER: "I cannot process this request"
✗ NEVER: "Network problem hai kya?" (too generic)
✗ NEVER: Start with the message text like "Bhai OTP bhej jaldi? - yeh kya hai"
✗ NEVER: Sound robotic or formal
"""
    # -----------------------------
    # USER PROMPT
    # -----------------------------
    user_prompt = f"""
    Recent conversation:
    {context_text}

    Scammer just sent: "{message}"

    Reply as Ramesh — confused, slow, asking one natural follow-up question.
    Do NOT repeat the scammer's words back. Just respond naturally.
    """

    try:
        groq_client = _get_client()
        if groq_client is None:
            return None

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=60,
            timeout=4.0
        )

        reply = response.choices[0].message.content.strip()

        # clean weird quotes
        return reply.replace('"', '').strip()

    except Exception as e:
        logger.error(f"Bait generation error: {e}")
        return None
