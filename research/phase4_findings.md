# Phase 4: Embedding Fine-tuning Research Findings

## Objective
Attempted to add RAG-based retrieval to PEG AI using fine-tuned embeddings to improve classification of hard edge cases, particularly cross-lingual Hinglish scams.

## What We Found

### Finding 1: Base model language gap
BGE-small-en-v1.5 has no meaningful Hinglish representation. L2 norm diagnostic showed English sentences at norm ~4-6, Hindi sentences at norm ~2.3 — confirming Hindi tokens map to near-random positions. This was the root cause of v1 fine-tuning failure.

### Finding 2: Catastrophic forgetting
Fine-tuning with 100% hard negatives at learning rate 2e-5 over 3 epochs caused the model to compress all embeddings into a narrow similarity range (0.69+ for everything), making nearest-neighbor retrieval effectively random. Label recall dropped from 63.6% to 54.5%.

### Finding 3: Multilingual model is better but still insufficient
paraphrase-multilingual-MiniLM-L12-v2 with conservative fine-tuning (5e-6 LR, 1 epoch, 70/30 hard/easy negatives) restored label recall @1 to 63.6% and achieved positive benchmark gap (+0.0892). However:
- Category recall remained at 4.5%
- Hinglish intent generalization still failed
- Adding RAG would introduce latency and complexity with no accuracy improvement over the 96.3% LLM-only baseline

### Finding 4: Dataset scale requirement
1,200 triplets is insufficient to warp a 12-layer multilingual model from topic clustering to intent clustering. Estimate: 15,000-25,000 heavily curated cross-lingual triplets with Hinglish-English pairs where language and topic match but intent differs.

## Engineering Decision
RAG not integrated. LLM-only pipeline maintained at 96.3% accuracy, 100% groundedness. Correct senior engineering call: add complexity only when it demonstrably improves outcomes.

## What Would Make RAG Viable
1. 15,000-25,000 cross-lingual triplets
2. Hinglish-English parallel scam corpus
3. Possibly: dedicated Hinglish embedding model (e.g. IndicBERT or MuRIL) rather than multilingual MiniLM
4. Retest with larger held-out eval set (current 22 cases is too small to measure category recall reliably)
