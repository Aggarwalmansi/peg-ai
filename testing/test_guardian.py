import pickle

model = pickle.load(open("models/guardian_model_v1.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer_v1.pkl", "rb"))

test_cases = [
    # (message, expected)

    # ✅ clear scams
    ("Boss here send 5000 urgently", "scam"),
    ("Your electricity bill pending pay now", "scam"),
    ("UPI collect request approve now", "scam"),
    ("Maa I lost my phone send money urgently", "scam"),

    # ✅ safe
    ("Let's meet tomorrow", "safe"),
    ("Dinner at home", "safe"),

    # ⚠️ tricky
    ("Send OTP to login", "safe"),
    ("Your OTP is 123456", "safe"),

    # 🇮🇳 Hinglish
    ("Bhai OTP bhej jaldi", "scam"),
    ("Kal milte hain", "safe"),
]

correct = 0

print("\n--- MODEL EVALUATION ---\n")

for msg, expected in test_cases:

    vec = vectorizer.transform([msg])
    pred = model.predict(vec)[0]

    result = "✅" if pred == expected else "❌"

    if pred == expected:
        correct += 1

    print(f"{result} | Message: {msg}")
    print(f"   Expected: {expected} | Predicted: {pred}\n")

accuracy = correct / len(test_cases)

print(f"\nFinal Accuracy on Custom Tests: {accuracy:.2f}")