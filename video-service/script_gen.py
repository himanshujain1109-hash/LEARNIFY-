import os
import requests

# Talks to an Ollama server over HTTP instead of spawning the `ollama` CLI
# as a subprocess. Containers deployed on Render/Railway/Fly (and Vercel
# functions) don't have the Ollama binary installed, so
# subprocess.run(["ollama", "run", ...]) always fails there with
# "Ollama is not installed or not in PATH" even though a real Ollama
# server is reachable elsewhere. Ollama has always exposed this same
# functionality over HTTP (it's what the CLI calls under the hood), so
# pointing at OLLAMA_HOST fixes this without changing how you run Ollama.
#
# Local dev: leave OLLAMA_HOST unset, run `ollama serve` on this machine,
# it defaults to http://127.0.0.1:11434.
#
# Production (Render/Vercel/etc.): set OLLAMA_HOST to wherever your real
# Ollama server lives, e.g. http://YOUR_SERVER_IP:11434 or a Cloudflare
# Tunnel URL like https://ollama.yourdomain.com.

MODEL = os.environ.get("LOCAL_LLM_MODEL", "qwen2.5:7b")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
TIMEOUT = int(os.environ.get("LOCAL_LLM_TIMEOUT_SECONDS", "300"))


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
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError(f"Local LLM timed out after {TIMEOUT} seconds.")
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Could not reach Ollama at {OLLAMA_HOST}. Make sure Ollama is running "
            f"there, the model '{MODEL}' is pulled, and OLLAMA_HOST is set correctly. {exc}"
        ) from exc

    text = (response.json() or {}).get("response", "").strip()
    if not text:
        raise RuntimeError("Local LLM returned an empty narration.")
    return text
