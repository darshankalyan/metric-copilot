# src/lab.py
# Toolbox for every model call in this project:
#   ask()   -> Gemini GENERATES text (used later in rag.py)
#   embed() -> Gemini turns texts into EMBEDDINGS (used in ingest.py and peek.py)

import os
import time
from dotenv import load_dotenv, find_dotenv
from google import genai
from google.genai import types

# --- Load the API key from .env (searched from the folder you run from) ---
load_dotenv(find_dotenv(usecwd=True))
if not os.getenv("GEMINI_API_KEY"):
    raise SystemExit(
        "GEMINI_API_KEY not found.\n"
        "Check: (1) .env is in the project root (metric-copilot), "
        "(2) it contains exactly GEMINI_API_KEY=your_key (no quotes, no spaces)."
    )

client = genai.Client()                 # reads GEMINI_API_KEY automatically
MODEL = "gemini-3.5-flash-lite"         # text generation model (free tier)
EMBED_MODEL = "gemini-embedding-001"    # embedding model (free tier, 100+ languages)


def ask(prompt, system=None, temperature=0.0, max_tokens=400, schema=None, retries=4):
    """Send one prompt to the model. Returns text + latency + token counts."""
    settings = dict(
        temperature=temperature,
        max_output_tokens=max_tokens,
        system_instruction=system,
    )
    if schema is not None:
        settings.update(response_mime_type="application/json", response_schema=schema)
    config = types.GenerateContentConfig(**settings)

    for attempt in range(retries):
        try:
            start = time.time()
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
            latency = round(time.time() - start, 2)
            usage = response.usage_metadata
            time.sleep(4)                                   # stay under free per-minute limit
            return {
                "text": response.text or "",
                "latency_s": latency,
                "in_tokens": getattr(usage, "prompt_token_count", None),
                "out_tokens": getattr(usage, "candidates_token_count", None),
            }
        except Exception as e:
            error = str(e)
            if ("429" in error or "503" in error) and attempt < retries - 1:
                wait = 5 * 2 ** attempt                     # 5s, 10s, 20s
                print(f"  Busy or rate-limited, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise


def embed(texts, retries=4):
    """Turn a LIST of texts into a LIST of vectors (one list of numbers per text)."""
    for attempt in range(retries):
        try:
            result = client.models.embed_content(model=EMBED_MODEL, contents=texts)
            time.sleep(1)                                   # gentle on the free tier
            return [e.values for e in result.embeddings]    # same order as the input
        except Exception as e:
            error = str(e)
            if ("429" in error or "503" in error) and attempt < retries - 1:
                wait = 5 * 2 ** attempt
                print(f"  Embedding busy, retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise