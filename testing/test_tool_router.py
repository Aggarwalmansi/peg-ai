from agents.tool_executor import run_tool

tests = [
    "UPI collect request approve now",
    "Click here https://fake-kyc-update.com",
    "Let's meet tomorrow",
]

for msg in tests:
    result = run_tool(msg)

    print("\nMessage:", msg)
    print("Tool:", result["tool_used"])
    print("Result:", result["tool_result"])