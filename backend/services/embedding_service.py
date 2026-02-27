# # backend/services/embedding_service.py
# import openai
# import os
# from typing import List, Dict, Any
# from google import genai
# from google.genai.errors import APIError as GeminiAPIError
# import numpy as np

# class EmbeddingService:
#     def __init__(self):
#         # --- OpenAI Client Initialization ---
#         openai_key = os.getenv("OPENAI_API_KEY")
#         self.openai_client = openai.OpenAI(api_key=openai_key) if openai_key else None
        
#         # --- Gemini Client Initialization ---
#         gemini_key = os.getenv("GEMINI_API_KEY")
#         self.gemini_client = genai.Client(api_key=gemini_key) if gemini_key else None

#         if not (self.openai_client or self.gemini_client):
#             print("WARNING: Neither OpenAI nor Gemini API keys are available for EmbeddingService.")

#     async def create_embeddings(
#         self, 
#         texts: List[str], 
#         model: str = "text-embedding-3-small"
#     ) -> List[List[float]]:
#         """
#         Creates embeddings for a list of texts using either OpenAI or Gemini.
#         Default model: OpenAI.
#         """
#         if not texts:
#             return []

#         if model.startswith("text-embedding") and self.openai_client:
#             # --- OpenAI Embeddings ---
#             try:
#                 response = self.openai_client.embeddings.create(
#                     model=model,
#                     input=texts
#                 )
#                 return [embedding.embedding for embedding in response.data]
#             except Exception as e:
#                 raise Exception(f"OpenAI Embedding Error: {str(e)}")

#         elif model.startswith("text-002") or model.startswith("gemini") and self.gemini_client:
#             # --- Gemini Embeddings (using the supported model name) ---
#             # NOTE: gemini embedding is currently synchronous in the SDK, but we keep the async wrapper
#             try:
#                 # Use a specific Gemini model supported for embedding, if the base model name is passed
#                 if "gemini" in model.lower():
#                      gemini_model = "text-embedding-004" # Current high-quality embedding model
#                 else:
#                      gemini_model = model

#                 response = self.gemini_client.models.embed_content(
#                     model=gemini_model,
#                     content=texts,
#                     task_type="RETRIEVAL_DOCUMENT" # Specify task type for better performance
#                 )
#                 # The response.embedding property is a list of embeddings
#                 return response.embedding

#             except GeminiAPIError as e:
#                 raise Exception(f"Gemini Embedding API Error: {str(e)}")
#             except Exception as e:
#                 raise Exception(f"Gemini Embedding Error: {str(e)}")
        
#         else:
#             raise ValueError(f"Unsupported model '{model}' or missing required API client.")

#     # --- RAG UTILITIES (REMOVED) ---
#     # The following methods are moved to DocumentService, which is responsible for ChromaDB interaction:
#     # - get_or_create_collection
#     # - store_document_embeddings
#     # - search_similar_documents
#     # - chunk_text
#     pass
# backend/services/embedding_service.py
# SerpAPI-only mode: use local ChromaDB embeddings (no OpenAI/Gemini)
import os
from typing import List

class EmbeddingService:
    def __init__(self):
        self._local_ef = None  # Lazy-load to avoid import at init

    def _get_local_embedding_function(self):
        """Lazy-load ChromaDB's default local embedding (no API key needed)."""
        if self._local_ef is None:
            try:
                from chromadb.utils import embedding_functions
                self._local_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            except Exception as e:
                raise Exception(
                    f"Local embedding failed. Install: pip install sentence-transformers. Error: {e}"
                )
        return self._local_ef

    async def create_embeddings(
        self, 
        texts: List[str], 
        model: str = "text-embedding-3-small"
    ) -> List[List[float]]:
        """
        Creates embeddings using local SentenceTransformer model (no OpenAI/Gemini).
        """
        if not texts:
            return []
        ef = self._get_local_embedding_function()
        # SentenceTransformer is sync; run in executor for async compatibility
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: ef(texts))