# agents/tool_executor.py

from tools.tool_registry import TOOLS
from agents.tool_router import decide_tool


def run_tool(message: str):
    """
    Decide + execute tool safely
    """

    tool_name = decide_tool(message)

    tool = TOOLS.get(tool_name)

    if not tool:
        return {
            "tool_used": "none",
            "tool_result": {}
        }

    try:
        result = tool({"message": message})

    except Exception as e:
        return {
            "tool_used": tool_name,
            "tool_result": {"error": str(e)}
        }

    return {
        "tool_used": tool_name,
        "tool_result": result
    }