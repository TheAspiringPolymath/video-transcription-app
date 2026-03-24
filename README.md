# Video Transcription & Analysis App

Personal-use web app for transcribing videos (YouTube, local files, Google Drive) and generating structured analysis using local Whisper + LLMs (OpenAI or Ollama).

## Prerequisites

- Docker Desktop 4.x+
- 16 GB RAM minimum (Whisper medium requires ~5 GB VRAM or ~8 GB RAM)
- ffmpeg (bundled inside Docker — no host install needed)
- OpenAI API key **or** Ollama running locally

### Hardware Requirements

| Whisper Model | RAM (CPU) | VRAM (GPU) | Speed (1 min audio) |
|---------------|-----------|------------|---------------------|
| tiny          | ~1 GB     | ~1 GB      | ~10 s               |
| base          | ~2 GB     | ~1 GB      | ~15 s               |
| small         | ~3 GB     | ~2 GB      | ~30 s               |
| medium        | ~8 GB     | ~5 GB      | ~2 min              |
| large-v3      | ~16 GB    | ~10 GB     | ~5 min              |

> **Warning:** Running Whisper large-v3 on CPU only can take 10–30× real time. For best performance, use a GPU or choose a smaller model.

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd video-transcription-app

# 2. Set up environment variables
cp .env.example .env
# Edit .env — at minimum set OPENAI_API_KEY (or configure Ollama)

# 3. (Optional) Add Google Drive credentials
# Copy google-credentials.json to credentials/

# 4. Build and start
docker compose up --build
```

### Service URLs

| Service    | URL                        |
|------------|----------------------------|
| Frontend   | http://localhost:3000      |
| API        | http://localhost:8000      |
| API Docs   | http://localhost:8000/docs |
| Redis      | localhost:6379 (internal)  |

## Environment Variables

| Variable                   | Required | Default                | Description                           |
|----------------------------|----------|------------------------|---------------------------------------|
| `OPENAI_API_KEY`           | Yes*     | —                      | OpenAI API key (*if using OpenAI)     |
| `LLM_PROVIDER`             | No       | `openai`               | `openai` or `ollama`                  |
| `OPENAI_MODEL`             | No       | `gpt-4o`               | OpenAI model name                     |
| `OLLAMA_BASE_URL`          | No       | `http://ollama:11434`  | Ollama service URL                    |
| `OLLAMA_MODEL`             | No       | `llama3.1:8b`          | Ollama model name                     |
| `WHISPER_MODEL`            | No       | `medium`               | Whisper model size (see table above)  |
| `WHISPER_LANGUAGE`         | No       | `pt`                   | Source audio language code            |
| `GOOGLE_CREDENTIALS_PATH`  | No       | —                      | Path to Google OAuth credentials file |
| `FRONTEND_URL`             | No       | `http://localhost:3000`| CORS allowed origin                   |
| `OUTPUTS_DIR`              | No       | `/app/outputs`         | Job output directory (inside Docker)  |
| `REDIS_URL`                | No       | `redis://redis:6379/0` | Redis connection URL                  |

## Development Commands

```bash
# Start all services
docker compose up

# With local Ollama LLM
docker compose -f docker-compose.yml -f docker-compose.ollama.yml up

# Watch worker logs (pipeline progress)
docker compose logs -f worker

# Backend only (API + worker)
docker compose up backend worker redis

# Rebuild after dependency changes
docker compose up --build

# Run backend tests
docker compose run --rm backend pytest

# Stop all services
docker compose down

# Stop and remove volumes (full reset)
docker compose down -v
```

## Project Structure

```
.
├── frontend/          # React 18 + Vite + TypeScript
├── backend/           # FastAPI + Celery workers
│   ├── core/          # Celery app configuration
│   ├── routers/       # API route handlers
│   ├── services/      # Business logic & pipeline
│   ├── models/        # Pydantic schemas
│   ├── repositories/  # File-system persistence
│   └── workers/       # Celery task definitions
├── outputs/           # Job artifacts (gitignored)
├── credentials/       # Google OAuth files (gitignored)
├── docker-compose.yml
└── docker-compose.ollama.yml
```
