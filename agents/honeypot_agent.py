from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def generate_bait_reply(message):
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
    except Exception as e:
        return None

# Example Usage
# print(generate_bait_reply("Sir, pay 25 rupees now for your parcel release."))