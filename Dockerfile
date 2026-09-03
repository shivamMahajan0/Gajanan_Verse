# ---------- Stage 1: Build React frontend ----------
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend_react
COPY frontend_react/package.json frontend_react/package-lock.json ./
RUN npm ci
COPY frontend_react/ ./
RUN npm run build

# ---------- Stage 2: Python backend ----------
FROM python:3.11-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Build tools needed for chromadb's native deps (hnswlib, onnxruntime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python deps first so this layer is cached across code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend source
COPY backend/ ./backend/

# Pre-built ChromaDB vector store (already ingested — see README for re-ingesting)
COPY chroma_db/ ./chroma_db/

# Built frontend static assets from stage 1
COPY --from=frontend-builder /app/frontend_react/dist ./frontend_react/dist

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f "https://gajanan-verse-ptlh.onrender.com/" || exit 1

# Render (and most PaaS) inject $PORT at runtime; default to 8000 for local docker run
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
