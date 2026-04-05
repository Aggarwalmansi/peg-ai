# tools/tool_registry.py

from agents.guardian_engine_v2 import analyze_message
from memory.vector_memory import search_similar
from tools.url_intelligence import analyze_urls


def scam_tool(input_data):
    return analyze_message(input_data["message"])


def pattern_tool(input_data):
    return search_similar(input_data["message"])


def url_tool(input_data):
    return analyze_urls(input_data["message"])


TOOLS = {
    "scam_detect": scam_tool,
    "pattern_check": pattern_tool,
    "url_check": url_tool
}