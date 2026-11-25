# CX Metric Copilot

A small RAG app that answers questions about customer-experience metrics (NPS, CSAT,
dissatisfaction, attrition) from a set of metric definitions. It cites the document it used
and says "I don't know" when the docs don't cover the question.

I built it because in CX analytics the same questions keep coming up, like "does a polite
customer with an unresolved complaint count as dissatisfied?", and the answer depends on
the company's own definitions, not general knowledge. All data is made up (a fictional bank).

## How it works
- `ingest.py` splits the 9 docs into chunks, embeds them with Gemini (`gemini-embedding-001`)
  and saves the vectors to `index/`.
- `search.py` embeds the question and ranks chunks by cosine similarity, in plain numpy.
- `rag.py` gives the top 3 chunks to Gemini with instructions to answer only from them
  and cite the file.
- `evaluate.py` scores the whole thing against a question set.

## Results
| Test set | Right doc ranked 1st | Right doc in top 3 | Correct citation | Refused unanswerable |
|---|---|---|---|---|
| Original (10 + 2 unanswerable) | 10/10 | 10/10 | 10/10 | 2/2 |
| Paraphrased + Hindi (9 + 1) | 8/9 | 9/9 | 9/9 | 1/1 |

Without the docs, Gemini answered "yes" to the polite-customer question. It mixed up
sentiment with resolution, which is exactly what the dissatisfaction definition rules out.
It also invented a "Card Management" journey. With the docs it got both right.

## What I learned
- Paraphrased questions halved the gap between the best and second-best match
  (average 0.096 to 0.049). Retrieval was right, but only just. The one miss, "can we
  average CSAT and NPS?", pulled the NPS doc because it names NPS, while the rule sits in
  the CSAT doc.
- Task-specific embeddings (`RETRIEVAL_DOCUMENT` / `RETRIEVAL_QUERY`) are often
  recommended. Here they dropped hit@1 to 7/9, so I left them out.
- I started with Chroma, but its local embedding runtime crashed on my machine
  (Python 3.14). With nine documents a numpy matrix is enough; for a real corpus I'd use
  a vector database.

## Run it
```
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
copy .env.example .env        # add a free Gemini API key
python src/ingest.py
python src/rag.py "Are dormant accounts counted as attrition?"
python src/evaluate.py eval/eval_hard.csv
```

## Next
Hybrid (keyword + vector) search for the near-ties, a FastAPI endpoint, and a CI check
that fails if the hit rate drops.