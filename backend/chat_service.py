import os
from openai import OpenAI
from backend.config import config
from backend.retriever import retriever_config
from backend.prompt_builder import build_system_prompt, build_user_prompt

class ChatService:
    def __init__(self):
        # Initialize OpenAI client pointing to OpenRouter
        api_key = os.getenv("OPENROUTER_API_KEY", config.openrouter_api_key)
        
        if api_key != "placeholder_key_if_not_set":
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Gajanan Maharaj AI Guide"
                }
            )
        else:
            self.client = None
        
        self.system_prompt = build_system_prompt()

    def process_query(self, query: str) -> dict:
        """
        Main RAG pipeline execution.
        """
        # 1. Retrieve Phase
        
        # Check if the query is asking for a specific verse_id (e.g., "Show verse 1.5")
        # For simplicity, we also run semantic search which should handle exact text well,
        # but we can optionally parse for "verse X.Y" here. 
        # Using pure semantic search for robust flexibility as per requirements.
        
        retrieved_records = retriever_config.semantic_search(query, top_k=2)
        
        # 2. Generation Phase
        if not self.client:
            # Fallback for when no real API key is present
            return {
                "answer": "Error: OpenAI API key is not configured. Please add a valid key to .env so the Language Model can generate a response.",
                "verses": [r["metadata"] for r in retrieved_records]
            }

        user_prompt = build_user_prompt(query, retrieved_records)
        
        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-4o-mini", # Using a free capability model for openrouter placeholder
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2, # Low temperature to enforce strict grounding
                max_tokens=800
            )
            
            chat_response = response.choices[0].message.content
            
        except Exception as e:
            chat_response = f"An error occurred during response generation: {str(e)}"

        # Return answer along with the raw metadata of the verses used
        return {
            "answer": chat_response,
            "verses": [r["metadata"] for r in retrieved_records]
        }

chat_service = ChatService()
