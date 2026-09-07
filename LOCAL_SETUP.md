# Learnify AI — Fully Local AI Mode

This version removes Gemini/Anthropic/Edge-TTS dependencies from the generation workflow.

## Local stack

- Node/Express: app backend
- MongoDB: local database
- Ollama: local LLM
- PyMuPDF: PDF extraction
- pyttsx3: offline system TTS
- Pillow + MoviePy + FFmpeg: video rendering

No Gemini/OpenAI/Anthropic API key is required.

## 1. Install prerequisites

### Node.js
Install Node.js 20+.

### MongoDB
Install MongoDB Community Server and run it locally.

### Ollama
Install Ollama, then download a model:

```bash
ollama pull qwen2.5:7b
```

If your PC has limited RAM, use:

```bash
ollama pull qwen2.5:3b
```

Then change `LOCAL_LLM_MODEL=qwen2.5:3b`.

Verify:

```bash
ollama run qwen2.5:7b
```

### Python
Install Python 3.10+.

### FFmpeg
Install FFmpeg and make sure `ffmpeg` is available in PATH.

## 2. Backend

From the project root:

```bash
npm install
copy .env.example .env
npm start
```

Linux/macOS:

```bash
cp .env.example .env
npm start
```

The backend runs on:

`http://localhost:5000`

## 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal, normally:

`http://localhost:5173`

## 4. Video service

Open another terminal:

```bash
cd video-service
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Install:

```bash
pip install -r requirements.txt
```

Start:

```bash
uvicorn server:app --host 127.0.0.1 --port 8000
```

The video service runs on:

`http://localhost:8000`

## 5. What changed

### Removed

- `@google/genai`
- Gemini lesson generation
- Gemini tutor generation
- Gemini notes-to-video generation
- `edge-tts` cloud TTS

### Added

- `backend/lib/local-ai.js`
- Ollama CLI integration
- Offline `pyttsx3` narration
- Video customization controls
- Local-only environment configuration

## Important limitation

"Fully local" means the AI model itself runs on your machine. You still need to install/download the open-source model once.

For example:

```bash
ollama pull qwen2.5:7b
```

After the model is downloaded, generation does not require Gemini, OpenAI, Anthropic, or another cloud AI API.

## Recommended hardware

- 8 GB RAM: use 3B model; expect slow generation
- 16 GB RAM: 7B/8B quantized models are practical
- NVIDIA GPU: much faster
- 32 GB RAM + GPU: recommended for longer videos

## PDF → Video workflow

```text
PDF
 ↓
Local PDF extraction
 ↓
Ollama local LLM
 ↓
Teaching narration
 ↓
Offline TTS
 ↓
Generated educational slide
 ↓
MoviePy + FFmpeg
 ↓
MP4
```
