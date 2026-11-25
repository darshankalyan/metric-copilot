"""Thin wrappers around the Gemini API: text generation and embeddings."""
import os
import time

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv(usecwd=True))
if not os.getenv("GEMINI_API_KEY"):
    raise SystemExit("GEMINI_API_KEY not found. Copy .env.example to .env and add your key.")

client = genai.Client()
MODEL = "gemini-3.5-flash-lite"
EMBED_MODEL = "gemini-embedding-001"


def _retry(call, retries=4):
    """Retry on rate limits (429) and overloads (503), backing off 5s, 10s, 20s."""
    for attempt in range(retries):
        try:
            return call()
        except Exception as e:
            transient = "429" in str(e) or "503" in str(e)
            if not transient or attempt == retries - 1:
                raise
            wait = 5 * 2 ** attempt
            print(f"  rate-limited, retrying in {wait}s")
            time.sleep(wait)


def ask(prompt, system=None, temperature=0.0, max_tokens=400, schema=None):
    settings = dict(temperature=temperature, max_output_tokens=max_tokens,
                    system_instruction=system)
    if schema is not None:
        settings.update(response_mime_type="application/json", response_schema=schema)
    config = types.GenerateContentConfig(**settings)

    start = time.time()
    response = _retry(lambda: client.models.generate_content(
        model=MODEL, contents=prompt, config=config))
    latency = round(time.time() - start, 2)
    time.sleep(4)  # stay under the free-tier per-minute limit

    usage = response.usage_metadata
    return {
        "text": response.text or "",
        "latency_s": latency,
        "in_tokens": getattr(usage, "prompt_token_count", None),
        "out_tokens": getattr(usage, "candidates_token_count", None),
    }


def embed(texts, task_type=None):
    """Return one embedding vector per input text."""
    config = types.EmbedContentConfig(task_type=task_type) if task_type else None
    result = _retry(lambda: client.models.embed_content(
        model=EMBED_MODEL, contents=texts, config=config))
    time.sleep(1)
    return [e.values for e in result.embeddings]