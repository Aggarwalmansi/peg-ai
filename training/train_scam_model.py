import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

data = pd.read_csv("data/scam_dataset.csv")

X = data["message"]
y = data["label"]

vectorizer = TfidfVectorizer(stop_words="english")

X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

pickle.dump(model, open("models/scam_model.pkl","wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl","wb"))

print("Model trained and saved")