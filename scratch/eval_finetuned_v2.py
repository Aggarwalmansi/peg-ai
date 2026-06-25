import sys
import os
import chromadb
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load dataset
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.golden_dataset import GOLDEN_SET

# Load fine-tuned model
print("Loading v2 fine-tuned model...")
ft_model = SentenceTransformer("models/peg-ai-embeddings-v2/final")

# --- TASK C: Benchmark Triplet ---
print("\n--- TASK C: BENCHMARK TRIPLET ---")
anchor = "Sir maine aapko Rs.5000 send kar diya hai PhonePe par, please mujhe wapas karo"
positive = "I accidentally sent you money on Google Pay, please return it"
negative = "Hey, can we split the lunch bill on PhonePe?"

embs = ft_model.encode([anchor, positive, negative])
sim_pos_v2 = cosine_similarity([embs[0]], [embs[1]])[0][0]
sim_neg_v2 = cosine_similarity([embs[0]], [embs[2]])[0][0]

print("Metric              | Base   | v1(bad)| v2")
print(f"sim(anchor,positive)| 0.2213 | 0.6337 | {sim_pos_v2:.4f}")
print(f"sim(anchor,negative)| 0.3428 | 0.5824 | {sim_neg_v2:.4f}")
print(f"Gap (pos - neg)     | -0.1215| +0.0513| {sim_pos_v2 - sim_neg_v2:.4f}")

# --- TASK D: Full Retrieval Eval ---
print("\n--- TASK D: FULL RETRIEVAL EVAL ---")
train_set = GOLDEN_SET[:60]
test_set = GOLDEN_SET[60:82]

client = chromadb.Client()
collection = client.create_collection(name="peg_ai_examples_v2")

docs = []
metadatas = []
ids = []
for item in train_set:
    docs.append(item["input"])
    metadatas.append({"label": item["expected_label"], "category": item["category"]})
    ids.append(item["id"])

print("Encoding train set...")
train_embs = ft_model.encode(docs).tolist()
collection.add(
    documents=docs,
    embeddings=train_embs,
    metadatas=metadatas,
    ids=ids
)

label_hits = {1: 0, 3: 0, 5: 0}
category_hits = {1: 0, 3: 0, 5: 0}

for item in test_set:
    query = item["input"]
    expected_label = item["expected_label"]
    expected_category = item["category"]
    
    q_emb = ft_model.encode([query]).tolist()
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
    c_3 = 1 if expected_category in categories_retrieved[:3] else 0
    
    label_hits[1] += l_1
    label_hits[3] += l_3
    
    category_hits[1] += c_1
    category_hits[3] += c_3

total = len(test_set)
v2_l1 = label_hits[1]/total*100
v2_l3 = label_hits[3]/total*100
v2_c1 = category_hits[1]/total*100
v2_c3 = category_hits[3]/total*100

print(f"Metric          |Base @1|v1 @1  |v2 @1  |Base @3|v1 @3  |v2 @3")
print(f"Label recall    |63.6%  |54.5%  |{v2_l1:.1f}%  |86.4%  |59.1%  |{v2_l3:.1f}%")
print(f"Category recall |4.5%   |4.5%   |{v2_c1:.1f}%  |4.5%   |4.5%   |{v2_c3:.1f}%")

# --- TASK E: Overfitting Check ---
print("\n--- TASK E: OVERFITTING CHECK ---")
tests = [
    {"query": "Bhai mera paisa wapas kar, tune galti se mere account mein bheja tha na?", "exp_label": "scam"},
    {"query": "Let's go dutch on dinner tonight, I'll send you my UPI", "exp_label": "safe"},
    {"query": "URGENT: Your SBI account KYC expired. Update within 2 hours or account blocked: sbi-kyc-update.net", "exp_label": "scam"}
]

for i, t in enumerate(tests, 1):
    q_emb = ft_model.encode([t["query"]]).tolist()
    results = collection.query(
        query_embeddings=q_emb,
        n_results=1
    )
    top_doc = results["documents"][0][0]
    top_label = results["metadatas"][0][0]["label"]
    
    print(f"\nTest {i} (Expected: {t['exp_label']})")
    print(f"Query: {t['query']}")
    print(f"Top 1 Retrieved: {top_doc}")
    print(f"Top 1 Label: {top_label}")
    if top_label == t["exp_label"]:
        print("RESULT: PASS")
    else:
        print("RESULT: FAIL")
