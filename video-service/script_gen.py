import os
import subprocess
import json
import re

MODEL = os.environ.get("LOCAL_LLM_MODEL", "qwen2.5:7b")
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
        result = subprocess.run(
            ["ollama", "run", MODEL, prompt],
            capture_output=True, text=True, timeout=TIMEOUT,
            encoding="utf-8", errors="ignore"
        )
    except FileNotFoundError:
        raise RuntimeError(
            f"Ollama is not installed or not in PATH. Install Ollama and run: ollama pull {MODEL}"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Local LLM timed out after {TIMEOUT} seconds.")

    if result.returncode != 0:
        raise RuntimeError(f"Ollama failed: {result.stderr.strip()[:500]}")

    text = result.stdout.strip()
    if not text:
        raise RuntimeError("Local LLM returned an empty narration.")
    return text
