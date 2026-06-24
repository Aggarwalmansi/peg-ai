import os
import json
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
            logger.warning("groq package not installed. LLM classification will be skipped.")
            return None
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not set. LLM classification will be skipped.")
            return None
        _client = Groq(api_key=api_key)
    return _client

def llm_classify(message):
    # The 'system' role sets the persona, the 'user' role provides the data
    prompt = f"""
    You are 'Bharat Guardiun', a specialized Indian Cyber-Crime Investigator expert in localized fraud patterns.
    
    ### TASK:
    Analyze the incoming message. Classify it as SCAM or SAFE.
    
    CRITICAL INSTRUCTION: Avoid false positives. 
    - Just because a message mentions "OTP", "UPI", "Bank", "KYC", or "account blocked" does NOT make it a scam if it's a normal discussion, a user complaint, or a standard automated message.
    - True scams have urgency, pressure, malicious links, or strangers asking for money/OTP/downloads.
    - Friends asking for small money/UPI transfers, testing UPI, or legitimate delivery agents asking for OTPs are SAFE.
    - Normal conversational Hinglish is SAFE.

    ### EXAMPLES FOR CONTEXT:
    - "Your electricity will be cut at 9:30 PM. Call 828... immediately" -> scam
    - "OTP share mat karna, par verification ke liye batao" -> scam
    - "My OTP is 123456. Don't share it." -> safe
    - "I didn't receive the OTP yet, can you resend?" -> safe
    - "Bhai OTP bhej de jaldi se, payment karni hai." -> safe
    - "I'm going to the bank today to update my KYC documents." -> safe
    - "Can you track my order? AW1234" -> safe
    - "Maine tujhe 500 UPI kar diye hai, check kar lena." -> safe

    ### MESSAGE TO ANALYZE:
    "{message}"

    ### OUTPUT INSTRUCTIONS:
    - Return a JSON object with exactly two fields.
    - "label": strictly "scam" or "safe".
    - "reasoning": one sentence explaining what specific evidence in the message triggered this classification. You MUST quote actual words/entities from the input message, rather than generic boilerplate.
    """

    try:
        groq_client = _get_client()
        if groq_client is None:
            return "safe"  # graceful degradation when no API key

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"},
            timeout=4.0
        )

        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)
        return {
            "label": parsed.get("label", "safe").lower(),
            "reasoning": parsed.get("reasoning", "")
        }

    except Exception as e:
        logger.error(f"LLM Error: {e}")
        return {"label": "safe", "reasoning": f"Error: {e}", "error": True}
