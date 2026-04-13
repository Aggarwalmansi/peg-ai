from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PEG AI Backend")

# -----------------------------
# CORS Middleware
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Health Check (Fastest Path)
# -------------------------
@app.get("/")
def root():
    return {"status": "PEG AI running", "version": "1.0.1"}

# -------------------------
# Request Schema
# -------------------------
class MessageRequest(BaseModel):
    message: str

# -------------------------
# API Route (Lazy-loads Agents on first call)
# -------------------------
@app.post("/analyze")
def analyze(req: MessageRequest):
    # DEFERRED IMPORT to prevent startup lag
    from agents.supervisor_graph import run_supervisor
    
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)