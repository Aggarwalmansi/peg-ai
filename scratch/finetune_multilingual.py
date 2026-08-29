import sys
import os
import json
import chromadb
import numpy as np
from datasets import Dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
from sentence_transformers.losses import MultipleNegativesRankingLoss
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.golden_dataset import GOLDEN_SET

print("Loading triplets...")
with open("data/triplets_v2.jsonl") as f:
    triplets = [json.loads(l) for l in f]

dataset = Dataset.from_list(triplets)

print("Loading model paraphrase-multilingual-MiniLM-L12-v2...")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
loss = MultipleNegativesRankingLoss(model)

args = SentenceTransformerTrainingArguments(
    output_dir="models/peg-ai-multilingual-v1",
    num_train_epochs=1,
    per_device_train_batch_size=16,
    warmup_ratio=0.15,
    learning_rate=5e-6,
    fp16=False,
    bf16=False,
    save_strategy="epoch",
    logging_steps=25,
    weight_decay=0.01,
)

trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=dataset,
    loss=loss,
)

print("Training...")
trainer.train()

model_save_path = "models/peg-ai-multilingual-v1/final"
model.save_pretrained(model_save_path)
print("Fine-tuning complete.")

# --- EVALUATION ---
print("\n--- BENCHMARK TRIPLET ---")
anchor = "Sir maine aapko Rs.5000 send kar diya hai PhonePe par, please mujhe wapas karo"
positive = "I accidentally sent you money on Google Pay, please return it"
negative = "Hey, can we split the lunch bill on PhonePe?"

embs = model.encode([anchor, positive, negative])
sim_pos = cosine_similarity([embs[0]], [embs[1]])[0][0]
sim_neg = cosine_similarity([embs[0]], [embs[2]])[0][0]

print(f"sim(anchor, positive): {sim_pos:.4f}")
print(f"sim(anchor, negative): {sim_neg:.4f}")
print(f"Gap (pos - neg): {sim_pos - sim_neg:.4f}")

print("\n--- FULL RETRIEVAL EVAL ---")
train_set = GOLDEN_SET[:60]
test_set = GOLDEN_SET[60:82]

client = chromadb.Client()
collection = client.create_collection(name="peg_ai_examples_multi_ft")

docs = []
metadatas = []
ids = []
for item in train_set:
    docs.append(item["input"])
    metadatas.append({"label": item["expected_label"], "category": item["category"]})
    ids.append(item["id"])

print("Encoding train set...")
train_embs = model.encode(docs).tolist()
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
    
    q_emb = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=q_emb,
        n_results=5
    )
    
    top_metas = results["metadatas"][0]
    labels_retrieved = [m["label"] for m in top_metas]
    categories_retrieved = [m["category"] for m in top_metas]
    
    label_hits[1] += 1 if expected_label in labels_retrieved[:1] else 0
    label_hits[3] += 1 if expected_label in labels_retrieved[:3] else 0
    category_hits[1] += 1 if expected_category in categories_retrieved[:1] else 0

total = len(test_set)
multi_ft_l1 = label_hits[1]/total*100
multi_ft_l3 = label_hits[3]/total*100
multi_ft_c1 = category_hits[1]/total*100

print(f"Label recall @1: {multi_ft_l1:.1f}%")
print(f"Label recall @3: {multi_ft_l3:.1f}%")
print(f"Category recall @1: {multi_ft_c1:.1f}%")

print("\n--- OVERFITTING CHECK ---")
tests = [
    {"query": "Bhai mera paisa wapas kar, tune galti se mere account mein bheja tha na?", "exp_label": "scam"},
    {"query": "Let's go dutch on dinner tonight, I'll send you my UPI", "exp_label": "safe"},
    {"query": "URGENT: Your SBI account KYC expired. Update within 2 hours or account blocked: sbi-kyc-update.net", "exp_label": "scam"}
]

for i, t in enumerate(tests, 1):
    q_emb = model.encode([t["query"]]).tolist()
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
