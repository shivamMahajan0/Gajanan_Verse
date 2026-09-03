from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from backend.chat_service import chat_service
from backend.retriever import retriever_config
from backend.config import config

app = FastAPI(title="Gajanan Maharaj AI Guide", version="1.0.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    verses: list

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint performing RAG-based question answering.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
        
    try:
        result = chat_service.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/verse/{verse_id}")
async def get_verse(verse_id: str):
    """
    Endpoint for exact verse lookups.
    """
    record = retriever_config.exact_verse_lookup(verse_id)
    if not record:
        raise HTTPException(status_code=404, detail="Verse not found.")
    return {"verse": record}

# Mount static frontend files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend_react", "dist")
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=config.host, port=config.port, reload=config.debug)
