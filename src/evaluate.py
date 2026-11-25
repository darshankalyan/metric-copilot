# src/evaluate.py
# Run every question in a test file through the RAG app and score it.
# Run from the project root:
#   python src/evaluate.py                       -> uses eval/eval.csv
#   python src/evaluate.py eval/eval_hard.csv    -> uses the hard test set

import sys                                                        # NEW: reads the file name you type
import pathlib
import pandas as pd
from rag import answer_question

pathlib.Path("results").mkdir(exist_ok=True)

# NEW: which test file to use (default = eval/eval.csv)
path = sys.argv[1] if len(sys.argv) > 1 else "eval/eval.csv"
tests = pd.read_csv(path, encoding="utf-8")

# NEW: a separate results file per test set, e.g. results/eval_hard_results.csv
out_file = f"results/{pathlib.Path(path).stem}_results.csv"

print(f"Evaluating: {path}  ({len(tests)} questions)\n")

rows = []
for _, t in tests.iterrows():
    question, expected = t["question"], t["expected_source"]
    answerable = expected != "NONE"

    answer, hits, _ = answer_question(question)
    sources = [h["source"] for h in hits]
    scores = [h["score"] for h in hits]
    said_idk = "i don't know" in answer.lower().replace("’", "'")    # handle curly apostrophes

    row = {
        "question": question,
        "expected": expected,
        "top1": sources[0],
        "top3": ", ".join(sources),
        "margin_1v2": round(scores[0] - scores[1], 3),                # retrieval confidence
        "hit@1": answerable and sources[0] == expected,               # right doc ranked first
        "hit@3": answerable and expected in sources,                  # right doc in top 3
        "cited_correct": answerable and expected in answer,           # answer cites the right file
        "said_idk": said_idk,
        "answer": answer,
    }
    rows.append(row)

    if not answerable:
        status = "REFUSED ✓" if said_idk else "ANSWERED ✗"
    elif row["hit@1"]:
        status = "HIT@1"
    elif row["hit@3"]:
        status = "HIT@3"
    else:
        status = "MISS"
    print(f"{status:<11} margin={row['margin_1v2']:.3f}  top1={sources[0]:<30} {question[:50]}")

res = pd.DataFrame(rows)
res.to_csv(out_file, index=False)                                  # NEW: saves to out_file

ans = res[res["expected"] != "NONE"]
non = res[res["expected"] == "NONE"]
print("\n===== SUMMARY =====")
print(f"Retrieval hit@1:        {ans['hit@1'].sum()}/{len(ans)}")
print(f"Retrieval hit@3:        {ans['hit@3'].sum()}/{len(ans)}")
print(f"Correct citation:       {ans['cited_correct'].sum()}/{len(ans)}")
print(f"False 'I don't know':   {ans['said_idk'].sum()}/{len(ans)}   (should be 0)")
print(f"Refused unanswerable:   {non['said_idk'].sum()}/{len(non)}   (should be all)")
print(f"Smallest margin:        {ans['margin_1v2'].min():.3f}  (most fragile question)")
print(f"\nSaved to {out_file}")                                     # NEW: shows the real file name