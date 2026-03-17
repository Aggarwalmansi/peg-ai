import pandas as pd

df = pd.read_csv("data/processed/guardian_dataset.csv")

print("Original dataset:", len(df))

# keep only required columns
df = df[["message","label"]]

# remove null messages
df = df.dropna(subset=["message"])

# remove empty messages
df = df[df["message"].str.strip() != ""]

# remove duplicates
df = df.drop_duplicates()

print("After cleaning:", len(df))

print("\nLabel distribution:")
print(df["label"].value_counts())

df.to_csv("data/processed/guardian_dataset_clean.csv", index=False)

print("\nClean dataset saved")