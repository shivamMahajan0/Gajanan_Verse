import os
import chromadb
from chromadb.utils import embedding_functions
from backend.config import config

class GajananRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=config.chroma_db_dir)
        
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
        try:
            self.collection = self.client.get_collection(
                name=config.chroma_collection_name, 
                embedding_function=self.embedding_fn
            )
        except Exception as e:
            print(f"Warning: Could not load collection. Has 'ingest.py' been run? Error: {e}")
            self.collection = None

    def exact_verse_lookup(self, verse_id: str) -> dict:
        """Looks up a specific verse by its exact ID."""
        if not self.collection:
            return {"error": "Database not initialized"}
            
        results = self.collection.get(
            ids=[verse_id],
            include=["metadatas"]
        )
        
        if results and results["metadatas"] and len(results["metadatas"]) > 0:
            return results["metadatas"][0]
        return None

    def semantic_search(self, query: str, top_k: int = 5) -> list:
        """Performs semantic search to find relevant verses."""
        if not self.collection:
            return []
            
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["metadatas", "distances", "documents"]
        )
        
        structured_results = []
        if results and results["metadatas"] and len(results["metadatas"]) > 0:
            metas = results["metadatas"][0]
            dists = results["distances"][0] if "distances" in results else [0]*len(metas)
            docs = results["documents"][0] if "documents" in results else [""]*len(metas)
            
            for m, d, doc in zip(metas, dists, docs):
                # distance close to 0 is better (cosine distance typically)
                structured_results.append({
                    "metadata": m,
                    "document": doc,
                    "distance": d
                })
                
        return structured_results

retriever_config = GajananRetriever()
