import json
import os
import chromadb
from chromadb.utils import embedding_functions
from backend.config import config

def load_json_data(filepath: str):
    """Loads and returns the JSON dataset."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_searchable_text(record: dict) -> str:
    """Combines all relevant fields into a single rich text block for embedding."""
    parts = []
    
    # Core verse identifiers
    parts.append(f"Adhyaya: {record.get('adhyaya', 'Unknown')}")
    parts.append(f"Verse {record.get('verse_id', 'Unknown')}")
    
    # Text
    if record.get('verse_text_marathi'):
        parts.append(f"Marathi: {record['verse_text_marathi']}")
    if record.get('verse_text_english'):
        parts.append(f"English: {record['verse_text_english']}")
        
    # Contextual metadata
    if record.get('situation'):
        parts.append(f"Situation Context: {record['situation']}")
        
    emotions = record.get('emotions', [])
    if emotions:
        parts.append(f"Emotions/State: {', '.join(emotions)}")
        
    themes = record.get('themes', [])
    if themes:
        parts.append(f"Themes: {', '.join(themes)}")
        
    # Teaching
    if record.get('teaching_summary'):
        parts.append(f"Teaching Summary: {record['teaching_summary']}")
        
    if record.get('persona_hint'):
        parts.append(f"Tone/Persona: {record['persona_hint']}")
        
    return "\n".join(parts)

def build_metadata(record: dict) -> dict:
    """Extracts raw fields for ChromaDB metadata filtering."""
    # Chroma metadata values must be str, int, float, or bool
    return {
        "adhyaya": int(record.get('adhyaya', 0)),
        "verse_id": str(record.get('verse_id', '')),
        "marathi": str(record.get('verse_text_marathi', '')),
        "english": str(record.get('verse_text_english', '')),
        "situation": str(record.get('situation', '')),
        # Join lists into strings for metadata storage
        "emotions": ",".join(record.get('emotions', [])),
        "themes": ",".join(record.get('themes', [])),
        "teaching": str(record.get('teaching_summary', '')),
        "persona": str(record.get('persona_hint', '')),
        "source": str(record.get('source', 'Shri Gajanan Vijay'))
    }

def run_ingestion(data_path: str):
    """Main ingestion pipeline."""
    print(f"Loading data from {data_path}...")
    records = load_json_data(data_path)
    
    print("Setting up ChromaDB client...")
    chroma_client = chromadb.PersistentClient(path=config.chroma_db_dir)
    
    # Use Local Embeddings to avoid OpenAI cost
    print("Using Local Default Embedding Function (all-MiniLM-L6-v2)...")
    embedding_function = embedding_functions.DefaultEmbeddingFunction()
    
    # Create or get collection. We use get_or_create to allow clean re-indexing if needed.
    # To force a pure re-index, one could delete the collection first.
    print(f"Accessing collection '{config.chroma_collection_name}'...")
    try:
        chroma_client.delete_collection(name=config.chroma_collection_name)
        print("Deleted existing collection for clean re-index.")
    except Exception:
        pass # It's fine if it doesn't exist yet
        
    collection = chroma_client.create_collection(
        name=config.chroma_collection_name,
        embedding_function=embedding_function
    )
    
    documents = []
    metadata = []
    ids = []
    
    print("Processing records...")
    for idx, record in enumerate(records):
        vid = record.get('verse_id')
        if not vid:
            print(f"Skipping record at index {idx} due to missing verse_id.")
            continue
            
        doc_text = build_searchable_text(record)
        meta = build_metadata(record)
        
        documents.append(doc_text)
        metadata.append(meta)
        ids.append(vid)

    print(f"Prepared {len(documents)} documents for indexing.")
    print("Adding to ChromaDB (this may take a while depending on dataset size and embedding service)...")
    
    # Batch add to avoid memory/network payload issues
    batch_size = 500
    for i in range(0, len(documents), batch_size):
        end = min(i + batch_size, len(documents))
        print(f"  Indexing batch {i} to {end}...")
        collection.add(
            documents=documents[i:end],
            metadatas=metadata[i:end],
            ids=ids[i:end]
        )
        
    print("Ingestion complete! All records successfully vectorized and stored.")

if __name__ == "__main__":
    # Assumes the script is run from the project root or backend folder
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gajanan_vijay_master.json')
    run_ingestion(data_file)
