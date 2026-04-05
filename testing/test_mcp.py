from mcp.client.mcp_client import call_pattern_server

msg = "UPI collect request approve now"

result = call_pattern_server(msg)

print(result)