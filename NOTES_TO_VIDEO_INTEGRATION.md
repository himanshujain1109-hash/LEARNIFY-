# Local Notes-to-Video

The Notes-to-Video service is now designed for local/offline AI generation.

## Services

React frontend -> FastAPI video service -> Ollama local LLM -> pyttsx3 -> MoviePy/FFmpeg.

No Gemini, Anthropic, OpenAI or Edge-TTS API key is required.

See `LOCAL_SETUP.md` for installation.
