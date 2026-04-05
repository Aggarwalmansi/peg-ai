from agents.supervisor_agent import supervisor_decision

test_cases = [
    "Boss send 5000 urgently",
    "UPI collect request approve now",
    "Maa I lost my phone send money urgently",
    "Bhai OTP bhej jaldi",
    "Let's meet tomorrow",
    "Dinner at home"
]

for msg in test_cases:
    result = supervisor_decision(msg)

    print("\n----------------------------")
    print("Message:", msg)
    print("Decision:", result["final_decision"])
    print("Action:", result["action"])
    print("Risk Score:", result["risk_score"])
    print("Explanation:", result["explanation"])

    if result["bait_reply"]:
        print("Bait:", result["bait_reply"])