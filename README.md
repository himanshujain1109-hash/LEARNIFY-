# Learnify AI — Vercel-ready frontend

Deploy this folder to Vercel.

## Vercel Environment Variables

```env
VITE_API_URL=https://YOUR-BACKEND-DOMAIN/api
VITE_VIDEO_API_URL=https://YOUR-VIDEO-DOMAIN
```

For local testing:

```env
VITE_API_URL=http://localhost:5000/api
VITE_VIDEO_API_URL=http://localhost:8000
```

Build command: `npm run build`
Output directory: `dist`

The Vercel package is intentionally frontend-only. Ollama, MongoDB, FFmpeg and the video worker belong on the Local AI Server package.
