import asyncio
import json
import logging
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SERVER_PATH = BASE_DIR / "mcp_servers" / "peg_mcp_server.py"


def _normalize_tool_result(result):
    if isinstance(result, dict):
        return result

    content = getattr(result, "content", None) or []
    if not content:
        return {}

    first = content[0]
    text = getattr(first, "text", None)
    if isinstance(text, str):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("MCP tool returned non-JSON text: %s", text)
            return {"raw_text": text}

    structured = getattr(first, "structuredContent", None)
    if isinstance(structured, dict):
        return structured

    return {}


async def call_mcp_tool(message: str):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            await session.list_tools()

            result = await session.call_tool(
                "check_scam_pattern",
                {"message": message}
            )

            return _normalize_tool_result(result)


def run_mcp(message):
    return asyncio.run(call_mcp_tool(message))
