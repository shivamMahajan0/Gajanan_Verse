# Gajanan Maharaj AI Guide

A production-grade Conversational AI application providing spiritually sensitive guidance based exclusively on the structured JSON dataset from Shri Gajanan Vijay. 

Built with **FastAPI**, **ChromaDB**, **OpenAI**, and a premium **Vanilla UI**.

## 🚀 Architecture Overview

1. **Ingestion Pipeline (`ingest.py`)**: Safely loads JSON data, constructs rich conversational text documents, and stores embeddings using ChromaDB's local `all-MiniLM-L6-v2` embedding function.
2. **Retrieval Layer (`retriever.py`)**: Handles Semantic Similarity Search & exact lookups via `ChromaDB`.
3. **Generation Engine (`chat_service.py` & `prompt_builder.py`)**: Interacts with the LLM via **OpenRouter** using a strictly engineered system prompt that explicitly denies hallucinations.
4. **API Endpoints (`main.py`)**: Fast, asynchronous FastAPI routes to serve the static generated React frontend and manage chat interactions.
5. **Frontend UI**: A powerful React.js single page application (SPA) built with Vite, utilizing modern React hooks and Lucide icons for a premium experience.

## 📂 Folder Structure

```
.
├── backend/
│   ├── config.py             # Centralized settings via pydantic
│   ├── ingest.py             # Data indexing script using local embeddings
│   ├── retriever.py          # ChromaDB interface
│   ├── prompt_builder.py     # Rigorous prompt engineering rules
│   ├── chat_service.py       # Main interaction logic (OpenRouter Calls)
│   └── main.py               # FastAPI entry point
├── frontend_react/           # Vite React Application directory
│   ├── src/                  # React source (App.jsx, index.css)
│   └── dist/                 # Compiled static assets served by FastAPI
├── .env.example              # Template Environment file
├── requirements.txt          # Python dependencies
├── README.md                 # This documentation
└── gajanan_vijay_master.json # Source Data
```

## 🛠️ Local Setup & Run Steps

### 1. Prerequisites
- Python 3.10+
- The `gajanan_vijay_master.json` file in the root directory.

### 2. Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and **ADD YOUR REAL OPENAI API KEY**. Without it, the retriever will fall back to default models, and chat generation will log an error.

### 4. Indexing the Dataset
Run the ingestion pipeline to embed and store data in ChromaDB:
```bash
python -m backend.ingest
```

### 5. Running the Application
Start the FastAPI backend (this also serves the frontend):
```bash
uvicorn backend.main:app --reload
```

Open your browser and navigate to: [http://localhost:8000](http://localhost:8000)

## ☁️ Deployment Guidance

This stack is architected to be highly deployable:

1. **Render / Railway / Heroku**: 
   - Define a `Procfile` -> `web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Set environment variables (`OPENAI_API_KEY`, etc.) in the dashboard.
   - For persisting ChromaDB between restarts, attach a persistent Volume mapped to `./chroma_db`.
2. **Docker**:
   - Create a `Dockerfile` executing `python -m uvicorn backend.main:app`. Ensure port mapping is correctly configured.
3. **Frontend decoupling**:
   - Because the frontend is static HTML/CSS/JS, you can optionally deploy the `frontend/` folder to Vercel/Netlify for global edge delivery, while pointing the JS `fetch` calls to a hosted version of the FastAPI backend.

for BAckend blash the following request
## use python version 3.10
0.In cmd blash cd dir
1.On Windows: venv\Scripts\activate
2.pip install -r requirements.txt
3.In .env paste your OpenRouter api key
4.python -m backend.ingest
5.uvicorn backend.main:app --reload ## download uvicorn or use python backend.main:app 

for frontend 
1.in cmd blash cd dir of frontend-react
2.npm run dev
