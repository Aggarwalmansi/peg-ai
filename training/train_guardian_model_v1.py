import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.metrics import classification_report, confusion_matrix

import pickle

# -----------------------------
# STEP 1: Load Dataset
# -----------------------------

df = pd.read_csv("data/processed/guardian_dataset_clean.csv")

X = df["message"]
y = df["label"]

# -----------------------------
# STEP 2: Train-Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# -----------------------------
# STEP 3: Vectorization
# -----------------------------

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1,2),   # important for fraud phrases
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# STEP 4: Train Models
# -----------------------------

models = {
    "Logistic Regression": LogisticRegression(max_iter=200),
    "Naive Bayes": MultinomialNB(),
    "Linear SVM": LinearSVC()
}

best_model = None
best_recall = 0

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train_vec, y_train)

    preds = model.predict(X_test_vec)

    print("\nClassification Report:")
    print(classification_report(y_test, preds))

    cm = confusion_matrix(y_test, preds)

    print("Confusion Matrix:")
    print(cm)

    # Extract recall for scam class
    report = classification_report(y_test, preds, output_dict=True)

    scam_recall = report["scam"]["recall"]

    print("Scam Recall:", scam_recall)

    if scam_recall > best_recall:
        best_recall = scam_recall
        best_model = model

# -----------------------------
# STEP 5: Save Best Model
# -----------------------------

pickle.dump(best_model, open("models/guardian_model_v1.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer_v1.pkl", "wb"))

print("\nBest model saved with scam recall:", best_recall)