from agents.guardian_engine_v2 import analyze_message

tests = [
    "Boss here send 5000 urgently",
    "UPI collect request approve now",
    "Maa I lost my phone send money urgently",
    "Bhai OTP bhej jaldi",
    "Let's meet tomorrow",
]

for msg in tests:
    result = analyze_message(msg)

    print("\nMessage:", msg)
    print(result)

    if result["bait_reply"]:
        print("Bait Reply:", result["bait_reply"])