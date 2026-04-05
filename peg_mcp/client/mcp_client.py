# mcp/client/mcp_client.py

import requests

MCP_SERVERS = {
    "pattern": "http://localhost:8001/check_pattern"
}


def call_pattern_server(message: str):
    try:
        response = requests.post(
            MCP_SERVERS["pattern"],
            json={"message": message},
            timeout=2
        )

        return response.json()

    except Exception:
        return {
            "pattern_match": False,
            "similar_cases": 0,
            "risk_boost": 0
        }