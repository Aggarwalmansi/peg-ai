from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
from sentence_transformers.losses import (
    MultipleNegativesRankingLoss,
)
from datasets import Dataset
import json

# Load triplets
with open("data/triplets_v2.jsonl") as f:
    triplets = [json.loads(l) for l in f]

dataset = Dataset.from_list(triplets)

# Load base model
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

# Loss function
loss = MultipleNegativesRankingLoss(model)

# Training args — modified for v2
args = SentenceTransformerTrainingArguments(
    output_dir="models/peg-ai-embeddings-v2",
    num_train_epochs=1,
    per_device_train_batch_size=16,
    warmup_ratio=0.1,
    learning_rate=1e-5,
    fp16=False,
    bf16=False,
    save_strategy="epoch",
    logging_steps=25,
)

trainer = SentenceTransformerTrainer(
    model=model,
    args=args,
    train_dataset=dataset,
    loss=loss,
)
trainer.train()

# Save fine-tuned model
model.save_pretrained(
    "models/peg-ai-embeddings-v2/final"
)
print("Fine-tuning v2 complete.")
