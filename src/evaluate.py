"""Score the RAG app on a test set: retrieval hit@1/@3, citations, refusals, margins.

Usage: python src/evaluate.py [eval/eval.csv | eval/eval_hard.csv]
"""
import pathlib
import sys

import pandas as pd

from rag import answer_question

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "eval/eval.csv")
tests = pd.read_csv(path, encoding="utf-8")

rows = []
for q, expected in zip(tests["question"], tests["expected_source"]):
    answer, hits, _ = answer_question(q)
    sources = [h["source"] for h in hits]
    row = {
        "question": q,
        "expected": expected,
        "top1": sources[0],
        "margin": round(hits[0]["score"] - hits[1]["score"], 3),
        "hit@1": sources[0] == expected,
        "hit@3": expected in sources,
        "cited": expected in answer,
        "refused": "i don't know" in answer.lower().replace("’", "'"),
        "answer": answer,
    }
    rows.append(row)

    if expected == "NONE":
        status = "refused" if row["refused"] else "ANSWERED"
    else:
        status = "hit@1" if row["hit@1"] else "hit@3" if row["hit@3"] else "MISS"
    print(f"{status:<9} {row['margin']:.3f}  {q[:60]}")

res = pd.DataFrame(rows)
pathlib.Path("results").mkdir(exist_ok=True)
res.to_csv(f"results/{path.stem}_results.csv", index=False)

ans, unans = res[res["expected"] != "NONE"], res[res["expected"] == "NONE"]
n = len(ans)
print(f"\nhit@1 {ans['hit@1'].sum()}/{n} | hit@3 {ans['hit@3'].sum()}/{n} | "
      f"cited {ans['cited'].sum()}/{n} | false refusals {ans['refused'].sum()}/{n} | "
      f"refused unanswerable {unans['refused'].sum()}/{len(unans)}")
print(f"margin: avg {ans['margin'].mean():.3f}, min {ans['margin'].min():.3f}")