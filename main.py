from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import os
import traceback

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PEG AI Backend")

# -----------------------------
# CORS Middleware (Proper Production Config)
# -----------------------------
# Allow local dev and any Vercel deployment
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

# Get origins from environment if provided (comma-separated string)
env_origins = os.environ.get("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([o.strip() for o in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https://.*\.vercel\.app$", # Strictly allow all vercel domains safely
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# -----------------------------
# Global Error Handler
# Ensures CORS headers are SENT even on 500 errors
# -----------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"GLOBAL ERROR: {str(exc)}")
    logger.error(traceback.format_exc())
    
    # Safely get origin from request for the CORS header fallback
    origin = request.headers.get("origin", "*")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error", 
            "detail": str(exc),
            "status": "error"
        },
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }
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
    try:
        # DEFERRED IMPORT to prevent startup lag
        from agents.supervisor_graph import run_supervisor

        logger.info(f"Analyzing message: {req.message}")
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
