import sys
import os
import json
import random
from collections import defaultdict

# Load dataset
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from evaluation.golden_dataset import GOLDEN_SET

os.makedirs("data", exist_ok=True)

# Organize dataset
scams_by_category = defaultdict(list)
safe_hard_by_category = defaultdict(list)
all_safes_by_category = defaultdict(list)
hinglish_scams = []
hinglish_safes = []
all_scams = []
all_safes = []

for item in GOLDEN_SET:
    cat = item["category"]
    label = item["expected_label"]
    if label == "scam":
        all_scams.append(item)
        if cat == "hinglish_scam":
            hinglish_scams.append(item)
        else:
            scams_by_category[cat].append(item)
    else:
        all_safes.append(item)
        
        # Base category for safes
        base_cat = cat.replace("_hard_negative", "").replace("_safe", "")
        all_safes_by_category[base_cat].append(item)

        if "hinglish" in cat:
            hinglish_safes.append(item)
        if cat.endswith("_hard_negative"):
            safe_hard_by_category[base_cat].append(item)

triplets = []

# Rules 1 and 2: For each scam (in standard categories)
# For each scam in a category, pair it with every other scam in that category, and every hard negative.
for cat, scams in scams_by_category.items():
    hard_negatives = safe_hard_by_category.get(cat, [])
    
    for anchor in scams:
        # Positives: all other scams in the same category
        positives = [s for s in scams if s["id"] != anchor["id"]]
        if not positives:
            positives = [s for s in all_scams if s["id"] != anchor["id"]]
            
        for positive in positives:
            if hard_negatives:
                for negative in hard_negatives:
                    triplets.append({
                        "anchor": anchor["input"],
                        "positive": positive["input"],
                        "negative": negative["input"],
                        "anchor_category": cat,
                        "hardness": "hard",
                        "teaching_signal": f"Differentiates malicious {cat} intent from legitimate {cat} topic."
                    })

# Rule 3: Cross-language pairs
for anchor in hinglish_scams:
    base_cat = anchor["id"].split("_")[0] 
    
    positives = scams_by_category.get(base_cat, [])
    if not positives:
        positives = all_scams
        
    for positive in positives:
        for negative in hinglish_safes:
            triplets.append({
                "anchor": anchor["input"],
                "positive": positive["input"],
                "negative": negative["input"],
                "anchor_category": "hinglish_scam",
                "hardness": "hard",
                "teaching_signal": f"Teaches that Hinglish language surface doesn't imply scam intent, while matching intent across languages."
            })

# Rule 4 (NEW for v2): Easy negatives
# For each scam anchor, pick a random safe message from a COMPLETELY DIFFERENT category as the negative.
# We want to add ~360 easy negatives. Let's add 1 easy negative for every scam anchor, per positive pair? No, just add easy negatives.
# Let's say for every anchor and positive pair, we add 1 easy negative. That would add 832 easy negatives.
# The user said "target ratio 70% hard, 30% easy... With 832 existing, add approx 360".
# 832 existing hard. Let's shuffle the pairs and add exactly 360 easy negatives.

hard_triplets = list(triplets) # 832
easy_triplets = []
random.seed(42)

# Generate pairs of (anchor, positive) to add easy negatives to.
# Let's just create 360 of them.
pairs = [(t["anchor"], t["positive"], t["anchor_category"]) for t in hard_triplets]
random.shuffle(pairs)
pairs = pairs[:360]

for anchor_text, positive_text, anchor_category in pairs:
    # Pick a random safe message from a different category
    different_safes = [s for s in all_safes if anchor_category not in s["category"] and "hinglish" not in s["category"]]
    if different_safes:
        negative = random.choice(different_safes)
        easy_triplets.append({
            "anchor": anchor_text,
            "positive": positive_text,
            "negative": negative["input"],
            "anchor_category": anchor_category,
            "hardness": "easy",
            "teaching_signal": f"Teaches broad semantic distance between {anchor_category} scam and different topic safe."
        })

triplets.extend(easy_triplets)

# Save JSONL
with open("data/triplets_v2.jsonl", "w") as f:
    for t in triplets:
        json.dump({"anchor": t["anchor"], "positive": t["positive"], "negative": t["negative"]}, f)
        f.write("\n")

print(f"Total triplets generated: {len(triplets)}")

hard_count = sum(1 for t in triplets if t["hardness"] == "hard")
easy_count = sum(1 for t in triplets if t["hardness"] == "easy")
total = len(triplets)

print(f"Hard negatives: {hard_count} ({hard_count/total*100:.1f}%)")
print(f"Easy negatives: {easy_count} ({easy_count/total*100:.1f}%)")
