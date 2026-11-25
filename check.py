# check.py: test each piece separately. The last number printed shows where it stops.
import sys
sys.path.insert(0, "src")                     # so Python can find src/lab.py

print("1. starting")
from lab import embed, EMBED_MODEL
print("2. key loaded, embedding model:", EMBED_MODEL)

vec = embed(["NPS measures customer loyalty."])[0]
print("3. Gemini embedding works, vector length:", len(vec))

import numpy as np
print("4. numpy works:", np.__version__)
print("\nALL GOOD: run python src/ingest.py next")