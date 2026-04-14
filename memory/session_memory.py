# memory/session_memory.py

from collections import defaultdict

# In-memory store (later Redis)
session_store = defaultdict(list)
MAX_MESSAGES_PER_SESSION = 20


def add_message(session_id: str, message: str, role: str):
    """
    role: 'user' or 'agent'
    """
    session_store[session_id].append({
        "role": role,
        "message": message
    })
    session_store[session_id] = session_store[session_id][-MAX_MESSAGES_PER_SESSION:]


def get_context(session_id: str, limit: int = 3):
    """
    Get last N messages
    """
    return session_store[session_id][-limit:]


def clear_session(session_id: str):
    session_store[session_id] = []
