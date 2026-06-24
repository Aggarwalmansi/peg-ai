def check_routing(routing_log: dict) -> dict:
    # Generalized log extraction for tool-use/routing overrides
    return {
        "final_source": routing_log.get("final_source", "unknown"),
        "llm_called": routing_log.get("llm_called", False),
        "fallback_called": routing_log.get("fallback_called", False)
    }
