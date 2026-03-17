import os
import pandas as pd

dataset = []

base_dir = "data/raw/nazario"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".txt"):
            path = os.path.join(root, file)

            with open(path, "r", encoding="latin1") as f:
                text = f.read()

            dataset.append({
                "message": text,
                "label": "scam"
            })

df = pd.DataFrame(dataset)

df.to_csv("data/processed/nazario_phishing.csv", index=False)

print("Parsed", len(df), "emails")