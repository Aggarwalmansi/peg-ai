import pickle

model = pickle.load(open("models/scam_model.pkl","rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl","rb"))

def detect_scam(message):

    vec = vectorizer.transform([message])
    prediction = model.predict(vec)[0]

    if prediction == 1:
        return "SCAM"
    else:
        return "SAFE"