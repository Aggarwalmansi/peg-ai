# agents/tool_router.py
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
            logger.warning("groq package not installed. Falling back to rule-based tool routing.")
            return None
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not set. Falling back to rule-based tool routing.")
            return None
        _client = Groq(api_key=api_key)
    return _client


def decide_tool(message: str) -> str:
    """
    Intelligent tool selection with hard constraints
    """

    # HARD RULE (no LLM needed)
    if "http://" in message or "https://" in message:
        return "url_check"

    prompt = f"""
You are PEG AI.

Decide which tool to use.

TOOLS:
- scam_detect → general scam detection
- pattern_check → repeated fraud / known scam patterns

RULES:
- UPI / OTP / money / urgent → pattern_check
- normal conversation → scam_detect

MESSAGE:
"{message}"

    Return ONLY one word:
scam_detect OR pattern_check
"""

    try:
        client = _get_client()
        if client is None:
            return "scam_detect"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        tool = response.choices[0].message.content.strip().lower()

        if tool not in ["scam_detect", "pattern_check"]:
            return "scam_detect"

        return tool

    except Exception:
        return "scam_detect"
