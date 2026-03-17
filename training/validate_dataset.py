import pandas as pd

df = pd.read_csv("data/processed/guardian_dataset_clean.csv")

print("Dataset size:", len(df))

print("\nLabel distribution:")

print(df["label"].value_counts())

print("\nExample rows:")

print(df.sample(5))