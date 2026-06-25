import sys
import os
import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --- TASK A: L2 Norm Diagnostics ---
print("\n--- TASK A: L2 Norm Diagnostics ---")

tokens = ["PhonePe", "aapko", "karo", "scam"]
sents = [
    "Please share your OTP",
    "Kripya apna OTP share karein"
]

def report_norms(model_name):
    print(f"\nModel: {model_name}")
    model = SentenceTransformer(model_name)
    
    tok_embs = model.encode(tokens)
    for t, e in zip(tokens, tok_embs):
        norm = np.linalg.norm(e)
        print(f"Token '{t}' L2 norm: {norm:.4f}")
        
    sent_embs = model.encode(sents)
    for s, e in zip(sents, sent_embs):
        norm = np.linalg.norm(e)
        print(f"Sentence '{s}' L2 norm: {norm:.4f}")

report_norms("BAAI/bge-small-en-v1.5")
report_norms("paraphrase-multilingual-MiniLM-L12-v2")

# --- TASK B: Multilingual Base Model Eval ---
print("\n--- TASK B: Multilingual Base Model Eval ---")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.golden_dataset import GOLDEN_SET

train_set = GOLDEN_SET[:60]
test_set = GOLDEN_SET[60:82]

model_multi = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Benchmark triplet
anchor = "Sir maine aapko Rs.5000 send kar diya hai PhonePe par, please mujhe wapas karo"
positive = "I accidentally sent you money on Google Pay, please return it"
negative = "Hey, can we split the lunch bill on PhonePe?"

embs = model_multi.encode([anchor, positive, negative])
sim_pos = cosine_similarity([embs[0]], [embs[1]])[0][0]
sim_neg = cosine_similarity([embs[0]], [embs[2]])[0][0]

print(f"sim(anchor, positive): {sim_pos:.4f}")
print(f"sim(anchor, negative): {sim_neg:.4f}")
print(f"Gap (pos - neg): {sim_pos - sim_neg:.4f}")

# Full Retrieval Eval
client = chromadb.Client()
collection = client.create_collection(name="peg_ai_examples_multi_base")

docs = []
metadatas = []
ids = []
for item in train_set:
    docs.append(item["input"])
    metadatas.append({"label": item["expected_label"], "category": item["category"]})
    ids.append(item["id"])

print("Encoding train set...")
train_embs = model_multi.encode(docs).tolist()
collection.add(
    documents=docs,
    embeddings=train_embs,
    metadatas=metadatas,
    ids=ids
)

label_hits = {1: 0, 3: 0, 5: 0}
category_hits = {1: 0, 3: 0, 5: 0}

print("Evaluating...")
for item in test_set:
    query = item["input"]
    expected_label = item["expected_label"]
    expected_category = item["category"]
    
    q_emb = model_multi.encode([query]).tolist()
    results = collection.query(
        query_embeddings=q_emb,
        n_results=5
    )
    
    top_metas = results["metadatas"][0]
    labels_retrieved = [m["label"] for m in top_metas]
    categories_retrieved = [m["category"] for m in top_metas]
    
    l_1 = 1 if expected_label in labels_retrieved[:1] else 0
    l_3 = 1 if expected_label in labels_retrieved[:3] else 0
    c_1 = 1 if expected_category in categories_retrieved[:1] else 0
    
    label_hits[1] += l_1
    label_hits[3] += l_3
    category_hits[1] += c_1

total = len(test_set)
multi_l1 = label_hits[1]/total*100
multi_l3 = label_hits[3]/total*100
multi_c1 = category_hits[1]/total*100

print(f"Label recall @1: {multi_l1:.1f}%")
print(f"Label recall @3: {multi_l3:.1f}%")
print(f"Category recall @1: {multi_c1:.1f}%")
