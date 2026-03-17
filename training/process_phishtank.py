import pandas as pd

df = pd.read_csv("data/raw/phishtank_urls.csv")

df = df[["url","target"]]

df["label"] = "scam"

df.to_csv("data/processed/phishtank_processed.csv", index=False)

print("PhishTank dataset processed")