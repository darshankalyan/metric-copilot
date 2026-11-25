# src/peek.py
# Ask questions -> see which chunks come back. Retrieval only, no answer generation.
# Run from the project root:  python src/peek.py

from search import search

questions = [
    "Is a polite customer with an unresolved issue counted as dissatisfied?",
    "What is the minimum number of responses needed to report a journey's NPS?",
    "Which journey do card PIN issues belong to?",
]

for q in questions:
    print(f"\nQ: {q}")
    for r in search(q, k=3):
        print(f"  score={r['score']:.3f}  {r['source']:<32} | {r['text'][:60]!r}")