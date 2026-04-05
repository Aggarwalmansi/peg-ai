def execute_action(state: dict) -> dict:

    action = state.get("action")

    if action == "block_and_bait":
        return {
            "action_taken": [
                "blocked_sender",
                "bait_engaged",
                "flagged_as_scam"
            ],
            "status": "success"
        }

    elif action == "warn_and_monitor":
        return {
            "action_taken": "user_warned",
            "status": "success"
        }

    elif action == "log_only":
        return {
            "action_taken": "logged",
            "status": "success"
        }

    return {
        "action_taken": "none",
        "status": "safe"
    }