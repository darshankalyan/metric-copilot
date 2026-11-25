"""Cosine-similarity search over the index built by ingest.py."""
import json
import pathlib

import numpy as np

from lab import embed

INDEX = pathlib.Path("index")
if not (INDEX / "vectors.npy").exists():
    raise SystemExit("No index found. Run: python src/ingest.py")

MATRIX = np.load(INDEX / "vectors.npy")
RECORDS = json.loads((INDEX / "chunks.json").read_text(encoding="utf-8"))


def search(question, k=3):
    """Return the k most similar chunks, best first, each with a similarity score."""
    q = np.array(embed([question])[0], dtype=np.float32)
    q /= np.linalg.norm(q)
    scores = MATRIX @ q
    top = np.argsort(scores)[::-1][:k]
    return [{**RECORDS[i], "score": float(scores[i])} for i in top]


if __name__ == "__main__":
    import sys
    question = " ".join(sys.argv[1:]) or "Is a polite customer with an unresolved issue counted as dissatisfied?"
    for hit in search(question):
        print(f"{hit['score']:.3f}  {hit['source']:<32} {hit['text'][:60]!r}")