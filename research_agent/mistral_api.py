import os
import time
from pathlib import Path
from typing import List, Dict

import requests

# API configuration

def _load_env() -> None:
    """Load variables from a .env file if present."""
    env_path = Path(".env")
    if env_path.exists():
        with env_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, val = line.split("=", 1)
                os.environ.setdefault(key, val)


_load_env()

MISTRAL_API_URL = os.getenv("MISTRAL_API_URL", "https://api.mistral.ai/v1/chat/completions")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "open-mistral-7b")
_RATE_LIMIT_SECONDS = float(os.getenv("MISTRAL_RATE_LIMIT", "1.0"))

_last_call = 0.0


def chat_completion(messages: List[Dict[str, str]], *, max_tokens: int = 300, temperature: float = 0.3, model: str = MISTRAL_MODEL) -> str:
    """Call the Mistral chat completion API with basic rate limiting."""
    if not MISTRAL_API_KEY:
        raise RuntimeError(
            "MISTRAL_API_KEY not set. Run ./setup_mistral.sh and load the .env file or set the variable manually."
        )
    global _last_call
    elapsed = time.monotonic() - _last_call
    if elapsed < _RATE_LIMIT_SECONDS:
        time.sleep(_RATE_LIMIT_SECONDS - elapsed)

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    try:
        resp = requests.post(MISTRAL_API_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        _last_call = time.monotonic()
        return data["choices"][0]["message"]["content"].strip()
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 401:
            print("Mistral API error: Unauthorized - check your API key")
        else:
            print(f"Mistral API HTTP error: {e}")
        return ""
    except Exception as e:
        print(f"Mistral API error: {e}")
        return ""
