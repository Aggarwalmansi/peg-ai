import pandas as pd

df = pd.read_csv("data/raw/phishing_emails.csv")

print(df.head())
print(df.columns)
print(df['label'].value_counts())