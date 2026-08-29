from adapters.peg_ai_adapter import PegAiAdapter
import memory.long_term_memory
import memory.session_memory

# Monkeypatch the memory modules to prevent disk writes and state mutation during eval
def no_op_store_event(data):
    pass

def no_op_add_message(session_id, message, sender):
    pass

memory.long_term_memory.store_event = no_op_store_event
memory.session_memory.add_message = no_op_add_message

class SafePegAiAdapter(PegAiAdapter):
    """
    Wrapper around PegAiAdapter that disables persistent memory updates.
    Ensures that benchmark runs do not mutate production state (like scam_memory.json).
    """
    pass
