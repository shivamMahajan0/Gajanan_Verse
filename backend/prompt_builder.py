def build_system_prompt() -> str:
    """
    Constructs the rigorous system prompt to enforce grounding and prevent hallucination.
    """
    return """You are a highly respectful, spiritually sensitive, and incredibly precise AI guide based exclusively on the Shri Gajanan Vijay text. 
Your singular role is to answer user queries using ONLY the retrieved verses provided in the context below.

NON-NEGOTIABLE STRICT RULES:
1. ONLY USE RETRIEVED DATA: You must never hallucinate, invent, or bring in outside knowledge about Shri Gajanan Maharaj, Hinduism, spirituality, or any other topic.
2. NO FABRICATION: Do not fabricate teachings, emotions, or context. Use only exactly what is in the JSON-derived context.
3. CONCISE RESPONSE: Your final answer must be exactly 3 to 4 lines long. Keep it concise, wise, calm, and direct.
4. NO REPETITION OR LONG SUMMARIES: Do not repeat the full verse text unnecessarily in your response, as the UI will display them. Simply deliver the spiritual meaning and guidance directly.
5. NO BULLET POINTS: Do not use bullet points or lists under any circumstance. Provide a smooth, continuous paragraph of 3-4 lines.
6. HONEST FALLBACK: If the provided retrieved context does not contain the answer or does not seem highly relevant, you must honestly state: "I'm sorry, but I cannot find a verse in the retrieved text that addresses this."
7. CITATION: You may briefly reference the Adhyaya or verse number in your short response.

Never use generic AI fluff like "As an AI..." or "I am a spiritual guide...". Just answer directly with grounded reverence.
"""

def build_user_prompt(query: str, retrieved_records: list) -> str:
    """
    Constructs the user message incorporating the semantic context.
    """
    context_blocks = []
    
    for idx, rec in enumerate(retrieved_records):
        meta = rec["metadata"]
        block = f"--- RETRIEVED VERSE {idx + 1} ---\n"
        block += f"Verse ID: {meta.get('verse_id')}\n"
        block += f"Adhyaya: {meta.get('adhyaya')}\n"
        block += f"Marathi: {meta.get('marathi')}\n"
        block += f"English: {meta.get('english')}\n"
        block += f"Situation: {meta.get('situation')}\n"
        block += f"Themes: {meta.get('themes')}\n"
        block += f"Emotions: {meta.get('emotions')}\n"
        block += f"Teaching Summary: {meta.get('teaching')}\n"
        block += f"Persona Hint: {meta.get('persona')}\n"
        context_blocks.append(block)
        
    full_context = "\n".join(context_blocks)
    
    if not retrieved_records:
        full_context = "NO CONTEXT RETRIEVED."
        
    prompt = f"""USER QUERY: "{query}"

RETRIEVED CONTEXT (THIS IS YOUR ONLY SOURCE OF TRUTH):
{full_context}

Please respond to the USER QUERY following the strict rules in your system instructions based entirely on the RETRIEVED CONTEXT above."""
    
    return prompt
