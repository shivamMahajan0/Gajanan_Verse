from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings, loaded from environment variables."""
    # OpenRouter Settings
    openrouter_api_key: str = "placeholder_key_if_not_set"
    
    # ChromaDB Settings
    chroma_db_dir: str = "./chroma_db"
    chroma_collection_name: str = "gajanan_verses"
    
    # Server Settings
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"

config = Settings()
