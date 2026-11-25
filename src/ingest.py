"""Build the search index: chunk the docs, embed each chunk, save to index/."""
import json
import pathlib

import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lab import embed

DOCS = pathlib.Path("data/docs")
INDEX = pathlib.Path("index")
CHUNK_SIZE, CHUNK_OVERLAP = 800, 100


def main():
    INDEX.mkdir(exist_ok=True)
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    records, vectors = [], []

    for path in sorted(DOCS.glob("*.md")):
        chunks = splitter.split_text(path.read_text(encoding="utf-8"))
        if not chunks:
            print(f"skipped {path.name} (empty)")
            continue
        for i, (chunk, vec) in enumerate(zip(chunks, embed(chunks))):
            records.append({"id": f"{path.name}-{i}", "source": path.name, "text": chunk})
            vectors.append(vec)
        print(f"{path.name:<32} {len(chunks)} chunk(s)")

    matrix = np.array(vectors, dtype=np.float32)
    matrix /= np.linalg.norm(matrix, axis=1, keepdims=True)  # unit vectors: dot product = cosine
    np.save(INDEX / "vectors.npy", matrix)
    (INDEX / "chunks.json").write_text(json.dumps(records, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    print(f"\nindexed {len(records)} chunks into {INDEX}/")


if __name__ == "__main__":
    main()