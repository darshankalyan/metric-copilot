"""Ask the same questions with and without the docs and save both answers side by side."""
import pathlib

import pandas as pd

from lab import ask
from rag import answer_question

QUESTIONS = [
    "Is a polite customer with an unresolved issue counted as dissatisfied?",
    "What is the minimum number of responses needed to report a journey's NPS?",
    "Which journey do card PIN issues belong to?",
    "What is Aurora Bank's NPS target for 2027?",
]

rows = []
for q in QUESTIONS:
    alone = ask(q, system="Answer in 1-3 sentences.")["text"].strip()
    answer, hits, _ = answer_question(q)
    rows.append({"question": q, "gemini_alone": alone, "rag": answer,
                 "retrieved": ", ".join(h["source"] for h in hits)})
    print(f"\nQ: {q}\n  alone: {alone}\n  rag:   {answer}")

pathlib.Path("results").mkdir(exist_ok=True)
pd.DataFrame(rows).to_csv("results/rag_vs_alone.csv", index=False)