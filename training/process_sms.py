import pandas as pd

df = pd.read_csv("data/raw/spam.csv", encoding="latin-1")
df = df.rename(columns={
    "v1": "label",
    "v2": "message"
})

df["label"] = df["label"].map({
    "ham": "safe",
    "spam": "scam"
})

df = df[["message","label"]]

df.to_csv("data/interim/sms_processed.csv", index=False)

print("SMS dataset processed:", len(df))