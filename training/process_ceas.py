import pandas as pd

df = pd.read_csv("data/raw/CEAS_08.csv")

df = df.rename(columns={
    "body": "message"
})

df["label"] = df["label"].map({
    0: "safe",
    1: "scam"
})

df = df[["message","label"]]

df.to_csv("data/interim/ceas_processed.csv", index=False)

print("CEAS processed:", len(df))