# Learnify AI — Clean Project

This package contains the application source only. Generated dependencies and caches have been removed to keep the project small and reliable.

## Install

### Root / backend
```bash
npm install
```

### Frontend
```bash
cd frontend
npm install
cd ..
```

### Video service (optional)
```bash
cd video-service
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Local run

Backend:
```bash
npm start
```

Frontend (new terminal):
```bash
cd frontend
npm run dev
```

## Important

- Copy `.env.example` to `.env` and add your local values.
- Copy `frontend/.env.example` to `frontend/.env` if frontend environment variables are required.
- Do not commit `.env`, `node_modules`, `dist`, `__pycache__`, or video-service job output.
- The project still uses the existing frontend/backend/video-service architecture; only generated files and nonessential local artifacts were removed.
