# src/ingest.py
# EXTRACT docs -> TRANSFORM (chunk + embed with Gemini) -> LOAD into a simple numpy index
# Run from the project root:  python src/ingest.py

import json
import pathlib
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lab import embed

DOCS_DIR = pathlib.Path("data/docs")
INDEX_DIR = pathlib.Path("index")
INDEX_DIR.mkdir(exist_ok=True)

splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)

records = []        # one entry per chunk: id, source file, chunk number, text
all_vectors = []    # one vector per chunk, in the same order as records

for f in sorted(DOCS_DIR.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    chunks = splitter.split_text(text)

    if not chunks:                                        # data-quality check
        print(f"SKIPPED {f.name}: empty")
        continue

    vectors = embed(chunks)                               # Gemini: one vector per chunk

    for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
        records.append({"id": f"{f.name}-{i}", "source": f.name, "chunk": i, "text": chunk})
        all_vectors.append(vec)

    print(f"{f.name:<32} {len(text):>5} chars -> {len(chunks)} chunk(s)")

# Turn the list of vectors into a matrix: one row per chunk, one column per number
matrix = np.array(all_vectors, dtype=np.float32)

# Normalise each row to length 1, so cosine similarity becomes a simple dot product
matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)

# Save: the numbers (vectors.npy) and the matching text + sources (chunks.json)
np.save(INDEX_DIR / "vectors.npy", matrix)
(INDEX_DIR / "chunks.json").write_text(
    json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
)

print(f"\nDone. Indexed {len(records)} chunks. Matrix shape: {matrix.shape} (chunks x numbers)")