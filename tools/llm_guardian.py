import os
from groq import Groq
from dotenv import load_dotenv

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

client = Groq(api_key=api_key)

def llm_classify(message):
    # The 'system' role sets the persona, the 'user' role provides the data
    prompt = f"""
    You are 'Bharat Guardiun', a specialized Indian Cyber-Crime Investigator expert in localized fraud patterns.
    
    ### TASK:
    Analyze the incoming message for signs of 'Desi Scams' including:
    1. Digital Arrest/CBI Impersonation (FedEx/Narcotics/Police).
    2. UPI 'Collect' Request fraud (Refund/Cashback tricks).
    3. Electricity/Utility disconnection threats (Pressure tactics).
    4. Personal Distress Impersonation (Accident/Bail/Hospital scams using Hinglish).
    5. Fake Job/WFH (YouTube likes/Telegram tasks).

    ### EXAMPLES FOR CONTEXT:
    - "Bhai 500 bhej urgent, petrol khatam ho gaya" -> scam
    - "Your electricity will be cut at 9:30 PM. Call 828... immediately" -> scam
    - "Dinner kab hai? Ghar jaldi aana" -> safe
    - "OTP share mat karna, par verification ke liye batao" -> scam

    ### MESSAGE TO ANALYZE:
    "{message}"

    ### OUTPUT INSTRUCTIONS:
    - Classify as exactly 'scam' or 'safe'.
    - Output ONLY the word. No explanations. No punctuation.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )

        return response.choices[0].message.content.strip().lower()

    except Exception as e:
        print("LLM Error:", e)
        return "safe"