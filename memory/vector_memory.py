import chromadb
from sentence_transformers import SentenceTransformer
import functools

# -----------------------------
# LAZY LOADERS
# -----------------------------

@functools.lru_cache(maxsize=1)
def get_chroma_client():
    """Lazy-load ChromaDB client."""
    return chromadb.Client()

@functools.lru_cache(maxsize=1)
def get_collection():
    """Lazy-load ChromaDB collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(name="peg_memory")

@functools.lru_cache(maxsize=1)
def get_model():
    """Lazy-load SentenceTransformer model."""
    # Using a small, efficient model for Render Free Tier
    return SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# STORE EVENT
# -----------------------------
def store_vector_event(text: str, metadata: dict):
    model = get_model()
    collection = get_collection()
    
    embedding = model.encode(text).tolist()

    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[str(hash(text))]
    )


# -----------------------------
# SEARCH SIMILAR
# -----------------------------
def search_similar(text: str, top_k=3):
    model = get_model()
    collection = get_collection()

    embedding = model.encode(text).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results