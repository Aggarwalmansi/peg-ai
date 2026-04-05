# agents/tool_router.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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