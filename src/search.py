# src/search.py
# The core of a vector database: find the stored chunks closest in meaning to a question.

import json
import pathlib
import numpy as np
from lab import embed

INDEX_DIR = pathlib.Path("index")
if not (INDEX_DIR / "vectors.npy").exists():
    raise SystemExit("No index found. Run: python src/ingest.py")

MATRIX = np.load(INDEX_DIR / "vectors.npy")                                   # chunks x numbers
RECORDS = json.loads((INDEX_DIR / "chunks.json").read_text(encoding="utf-8"))  # text + source


def search(question, k=3):
    """Return the k chunks most similar to the question, best first."""
    q = np.array(embed([question])[0], dtype=np.float32)   # embed with the SAME model
    q = q / np.linalg.norm(q)                              # normalise like the documents
    scores = MATRIX @ q                                    # cosine similarity with EVERY chunk at once
    top = np.argsort(scores)[::-1][:k]                     # positions of the k highest scores
    return [{**RECORDS[i], "score": float(scores[i])} for i in top]