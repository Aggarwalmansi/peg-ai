from agents.supervisor_graph import run_supervisor

tests = [
    "UPI collect request approve now",
    "Bhai OTP bhej jaldi",
    "Let's meet tomorrow",
    "Click here https://testsafebrowsing.appspot.com/s/phishing.html"

]

for msg in tests:
    result = run_supervisor(msg)

    print("\n------------------")
    print("Message:", msg)
    print("Decision:", result["decision"])
    print("Action:", result["action"])
    print("Risk:", result["risk_score"])
    print("Bait:", result["bait_reply"])
