import asyncio
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def call_mcp_tool(message: str):

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_servers/peg_mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()
            print("🔧 Available tools:", tools)

            result = await session.call_tool(
                "check_scam_pattern",
                {"message": message}
            )

            return result


def run_mcp(message):
    return asyncio.run(call_mcp_tool(message))