import os
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = os.environ.get("LOCAL_LLM_MODEL", "qwen2.5:7b")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
TIMEOUT = int(os.environ.get("LOCAL_LLM_TIMEOUT_SECONDS", "300"))


def _offline_fallback_enabled():
    return os.environ.get("ENABLE_OFFLINE_FALLBACK", "true").lower() not in {
        "0",
        "false",
        "no",
        "off",
    }


def _generate_with_ollama(prompt):
    """Call Ollama's HTTP API so this also works in a container without CLI."""
    request = Request(
        f"{OLLAMA_HOST}/api/generate",
        data=json.dumps(
            {
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="ignore")[:500]
        if error.code == 404:
            raise RuntimeError(
                f'Ollama model "{MODEL}" is not available on {OLLAMA_HOST}. '
                f"Run `ollama pull {MODEL}` on that server first."
            ) from error
        raise RuntimeError(f"Ollama request failed ({error.code}): {body}") from error
    except (URLError, TimeoutError, OSError) as error:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_HOST}. Set OLLAMA_HOST to a "
            f"reachable Ollama server or install/start Ollama locally. {error}"
        ) from error
    except json.JSONDecodeError as error:
        raise RuntimeError("Ollama returned an invalid JSON response.") from error

    result = str(payload.get("response", "")).strip()
    if not result:
        raise RuntimeError("Local LLM returned an empty narration.")
    return result


def _offline_script(page_text, page_number):
    text = re.sub(r"\s+", " ", page_text).strip()
    if not text:
        return f"Page {page_number} does not contain enough readable text to narrate."

    # A deterministic narration keeps the video feature usable when the
    # optional Ollama service is not available. It never invents facts.
    parts = re.split(r"(?<=[.!?])\s+", text)
    selected = " ".join(parts[:8]).strip()
    return (
        f"Page {page_number}. Here is the material from this page, explained "
        f"directly from the uploaded notes: {selected}"
    )

def generate_script(page_text: str, page_number: int, options=None) -> str:
    options = options or {}
    language = options.get("language", "English")
    level = options.get("level", "College")
    style = options.get("style", "Teacher")
    duration = options.get("duration", "5")

    if not page_text.strip():
        return f"Page {page_number} does not contain enough readable text to narrate."

    prompt = f"""
You are a careful educational video teacher.
Create narration for page {page_number} of supplied study material.

Requirements:
- Explain ONLY the supplied material. Do not invent facts.
- Language: {language}
- Student level: {level}
- Teaching style: {style}
- Target video duration for the complete material: about {duration} minutes.
- Make the narration natural to speak aloud.
- Mention formulas exactly when present.
- If the page contains a diagram or figure but no extractable text, describe only what can be inferred from its text.
- Return ONLY narration, no title, no markdown.

STUDY MATERIAL:
{page_text[:12000]}
"""
    try:
        return _generate_with_ollama(prompt)
    except Exception:
        if not _offline_fallback_enabled():
            raise
        return _offline_script(page_text, page_number)
