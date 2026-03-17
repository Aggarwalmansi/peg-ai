from fastapi import FastAPI
from agents.guardian_agent import analyze_message

app = FastAPI()

@app.post("/analyze")

def analyze(data: dict):

    message = data["message"]

    result = analyze_message(message)

    return result