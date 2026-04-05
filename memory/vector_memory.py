import chromadb
from sentence_transformers import SentenceTransformer

# -----------------------------
# INIT
# -----------------------------
client = chromadb.Client()

collection = client.get_or_create_collection(name="peg_memory")

model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# STORE EVENT
# -----------------------------
def store_vector_event(text: str, metadata: dict):

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

    embedding = model.encode(text).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    return results