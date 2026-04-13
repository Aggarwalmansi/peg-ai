import functools
import logging

logger = logging.getLogger(__name__)

# -----------------------------
# LAZY LOADERS (DISABLED FOR RENDER FREE TIER OOM)
# -----------------------------

def get_chroma_client():
    return None

def get_collection():
    return None

def get_model():
    return None

# -----------------------------
# STORE EVENT (MOCK)
# -----------------------------
def store_vector_event(text: str, metadata: dict):
    # Disabled to prevent memory crashes on Render
    pass


# -----------------------------
# SEARCH SIMILAR (MOCK)
# -----------------------------
def search_similar(text: str, top_k=3):
    # Disabled to prevent memory crashes on Render
    # Returning empty results prevents graph from crashing
    return {"documents": [[]], "distances": [[]]}