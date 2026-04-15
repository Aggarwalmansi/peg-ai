# PEG AI

PEG AI, short for Personal Economic Guardian, is an agentic scam-detection and response system built to identify suspicious digital messages, explain the risk, and optionally generate bait replies that waste scammer time without exposing real user information.

The project combines rule-based detection, lightweight ML classification, LLM-assisted judgment, Indian scam-pattern intelligence, and a modern frontend for interactive analysis. It is designed as a deployable full-stack application with a FastAPI backend and a Vite/React frontend.

## What PEG AI Does

- Analyzes incoming text messages for fraud patterns
- Scores message risk using behavioral, heuristic, ML, and LLM signals
- Applies India-specific scam intelligence for localized fraud patterns
- Generates bait replies for high-risk scam conversations
- Records lightweight memory for audit and traceability
- Supports MCP-based pattern checking as part of the decision flow
- Exposes a simple API and UI for real-time interaction

## Core Use Cases

- Detecting UPI scam attempts
- Identifying OTP theft and urgent money-request fraud
- Flagging suspicious links and fake KYC/account freeze messages
- Generating safe bait replies for active scam engagement
- Demonstrating an agentic fraud-defense pipeline for demos, research, or product prototyping

## Project Structure

```text
peg-ai/
├── agents/              # Orchestration, graph flow, routing, bait and guardian logic
├── api/                 # API compatibility entrypoint
├── data/                # Datasets used for training and validation
├── frontend/            # Vite + React frontend
├── intelligence/        # Region-specific scam intelligence logic
├── mcp_servers/         # Local MCP server used for pattern tools
├── memory/              # Session and long-term storage helpers
├── models/              # Serialized ML artifacts
├── peg_mcp/             # MCP client/server integration code
├── testing/             # Manual and lightweight test scripts
├── tools/               # Detection, baiting, URL intelligence, actions
├── training/            # Dataset preparation and model training utilities
├── main.py              # Primary FastAPI backend entrypoint
├── render.yaml          # Render deployment configuration
└── requirements.txt     # Python dependencies
```

## Architecture

PEG AI uses a staged decision pipeline:

1. Message intake through the FastAPI backend
2. Guardian analysis using behavioral logic, ML artifacts, and optional LLM classification
3. Tool routing and intelligence scoring
4. MCP-based scam-pattern enrichment
5. Decision engine for `allow`, `log_only`, `warn_and_monitor`, or `block_and_bait`
6. Bait reply generation for high-risk scam scenarios
7. Action logging and lightweight memory storage

### Main Backend Flow

The deployed backend route is:

- [`main.py`](main.py)

The request flows through:

- [`agents/supervisor_graph.py`](agents/supervisor_graph.py)
- [`agents/langgraph_flow.py`](agents/langgraph_flow.py)
- [`agents/guardian_engine_v2.py`](agents/guardian_engine_v2.py)
- [`tools/bait_generator.py`](tools/bait_generator.py)
- [`peg_mcp/client/peg_client.py`](peg_mcp/client/peg_client.py)

## Tech Stack

### Backend

- Python 3.10
- FastAPI
- Uvicorn
- LangGraph
- Groq SDK
- scikit-learn
- NumPy
- MCP Python SDK

### Frontend

- React
- Vite
- Plain CSS

### Deployment

- Render for backend
- Vercel or any static hosting platform for frontend

## Features

### 1. Hybrid Scam Detection

PEG AI does not rely on a single model. It combines:

- Rule-based behavioral scoring
- Serialized ML model inference from `models/`
- LLM classification using Groq
- Indian scam-pattern enrichment
- MCP-based pattern validation

### 2. Active Scam Defense

For high-risk scam messages, the system can generate bait replies that:

- sound human and natural
- avoid sharing real user data
- keep the scammer engaged
- force the scammer to reveal more information

When Groq is unavailable, the system now falls back to deterministic bait replies so the high-risk flow still returns a useful response.

### 3. Explainable Output

Each analysis response can include:

- decision
- action
- risk score
- scam signals
- recommendation
- trace of reasoning steps

### 4. Lightweight Memory

PEG AI stores:

- short session context in memory
- long-term event history in a local JSON file

The current implementation intentionally keeps this lightweight for deployment simplicity.

## API

### Health Check

```http
GET /
```

Example response:

```json
{
  "status": "PEG AI running",
  "version": "1.0.1"
}
```

### Analyze Message

```http
POST /analyze
Content-Type: application/json
```

Request body:

```json
{
  "message": "UPI collect request approve now"
}
```

Example response:

```json
{
  "message": "UPI collect request approve now",
  "decision": "scam",
  "risk_score": 90,
  "action": "block_and_bait",
  "bait_reply": "Accha yeh UPI request kis app pe dikh raha hai bhai, main thoda confuse ho gaya?",
  "signals": [
    "UPI Collect Fraud",
    "MCP Pattern Match"
  ],
  "recommendation": "Do not send money. Report this to cybercrime.gov.in or call 1930.",
  "trace": [
    "[Guardian] risk=30",
    "Tool used: pattern_check",
    "[Indian] signals=['UPI Collect Fraud']",
    "[Override] Critical scam detected",
    "[MCP] {'pattern_match': true, 'score': 2}",
    "[Decision] risk=100 → block_and_bait",
    "[Bait] generated"
  ]
}
```

## Local Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd peg-ai
```

### 2. Create a Python Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Configure Backend Environment

```bash
cp .env.example .env
```

Then set your real values in `.env`.

### 5. Start the Backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. Set Up the Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

By default, the frontend expects:

```env
VITE_API_URL=http://localhost:8000
```

## Models

PEG AI expects these model artifacts:

- `models/guardian_model_v1.pkl`
- `models/vectorizer_v1.pkl`

These are used by the guardian engine and scam detector. If the artifacts are missing, the backend now falls back more gracefully, but production deployments should still include them for best results.

## MCP Integration

PEG AI includes local MCP support for pattern checking.

Relevant files:

- [`mcp_servers/peg_mcp_server.py`](mcp_servers/peg_mcp_server.py)
- [`peg_mcp/client/peg_client.py`](peg_mcp/client/peg_client.py)

Current MCP behavior:

- starts a local stdio MCP server
- lists tools
- calls `check_scam_pattern`
- uses the returned score to increase risk and add MCP trace data

## Testing

The `testing/` directory contains lightweight scripts for manual validation.

Examples:

- [`testing/test_guardian_v2.py`](testing/test_guardian_v2.py)
- [`testing/test_supervisor_graph.py`](testing/test_supervisor_graph.py)
- [`testing/test_langgraph.py`](testing/test_langgraph.py)
- [`testing/test_mcp_real.py`](testing/test_mcp_real.py)

Suggested manual validation scenarios:

- normal personal message
- OTP scam
- UPI collect request
- fake KYC freeze message
- malicious URL message
- family emergency money scam


## Status

PEG AI is currently in an MVP-plus stage with a working end-to-end scam-defense flow, active bait support, MCP integration, deployable frontend/backend structure, and a clearer path toward production hardening.
