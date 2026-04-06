from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your supervisor (LangGraph or normal)
from agents.supervisor_graph import run_supervisor

app = FastAPI(title="PEG AI Backend")

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev, allow all. In prod, use: ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Schema
# -------------------------
class MessageRequest(BaseModel):
    message: str


# -------------------------
# API Route
# -------------------------
@app.post("/analyze")
def analyze(req: MessageRequest):
    logger.info(f"Analyzing message: {req.message}")
    
    try:
        result = run_supervisor(req.message)
        logger.info(f"Analysis result: {result}")
        
        return {
            "message": result.get("message", req.message),
            "decision": result.get("decision", "unknown"),
            "risk_score": result.get("risk_score", 0),
            "action": result.get("action", "none"),
            "bait_reply": result.get("bait_reply"),
            "signals": result.get("signals", []),
            "recommendation": result.get("recommendation", "No specific recommendation."),
            "trace": result.get("trace", [])
        }
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return {
            "error": str(e),
            "decision": "error",
            "risk_score": 0,
            "action": "none",
            "signals": ["Processing Error"],
            "recommendation": "Backend error occurred. Please try again later."
        }


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"status": "PEG AI running"}