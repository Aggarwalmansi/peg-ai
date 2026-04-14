from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("peg-server")


# 🔧 TOOL 1: Pattern Detection
@mcp.tool()
def check_scam_pattern(message: str) -> dict:
    """
    Detect common scam patterns
    """

    patterns = ["upi", "otp", "urgent", "send money"]

    score = sum(1 for p in patterns if p in message.lower())

    return {
        "pattern_match": score > 0,
        "score": score
    }


# 🔧 TOOL 2: URL Detection
@mcp.tool()
def check_url(message: str) -> dict:
    """
    Detect if message contains URL
    """

    if "http" in message:
        return {"has_url": True}

    return {"has_url": False}


# 🔧 RESOURCE (VERY IMPORTANT)
@mcp.resource("peg://history")
def get_history():
    return "User interaction history placeholder"


if __name__ == "__main__":
    print("PEG MCP Server Starting...", file=sys.stderr)
    mcp.run()
