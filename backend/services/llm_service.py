# backend/services/llm_service.py
# Fully local LLM using HuggingFace Transformers — NO API KEY NEEDED
import os
import requests
from typing import List, Dict, Any, Optional
from threading import Lock


class LLMService:
    def __init__(self):
        self._model = None
        self._tokenizer = None
        self._lock = Lock()
        self._model_name = "google/flan-t5-base"  # ~250MB, runs on CPU

        # --- SerpAPI Key (optional, for web search fallback) ---
        self.serp_api_key = os.getenv("SERP_API_KEY")
        if not self.serp_api_key:
            print("INFO: SERP_API_KEY not set. Web search fallback disabled.")

        print(f"INFO: LLM Service initialized. Model '{self._model_name}' will be loaded on first use.")


    def _load_model(self):
        """Lazy-load the model on first use (avoids blocking startup)."""
        if self._model is not None:
            return

        with self._lock:
            if self._model is not None:
                return  # Another thread loaded it while we waited

            print(f"Loading local LLM model: {self._model_name} (this may take a minute on first run)...")
            from transformers import T5ForConditionalGeneration, T5Tokenizer

            self._tokenizer = T5Tokenizer.from_pretrained(self._model_name)
            self._model = T5ForConditionalGeneration.from_pretrained(self._model_name)
            print(f"Model '{self._model_name}' loaded successfully!")


    def _generate_local(self, prompt: str, max_new_tokens: int = 512) -> str:
        """Generate a response using the local Flan-T5 model."""
        self._load_model()

        # Tokenize input — truncate to model's max input length (512 tokens for T5)
        inputs = self._tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        # Generate response
        outputs = self._model.generate(
            **inputs,
            max_new_tokens=min(max_new_tokens, 512),
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
            temperature=0.7,
            do_sample=True
        )

        response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response


    # ----------------------------------------------------------------
    # SerpAPI Web Search (optional)
    # ----------------------------------------------------------------
    async def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """Search the web using SerpAPI (requires SERP_API_KEY in .env)."""
        if not self.serp_api_key:
            return []

        try:
            params = {
                "api_key": self.serp_api_key,
                "q": query,
                "num": num_results,
                "engine": "google"
            }

            response = requests.get("https://serpapi.com/search", params=params)
            response.raise_for_status()
            data = response.json()

            results = []
            if "organic_results" in data:
                for result in data["organic_results"][:num_results]:
                    results.append({
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("snippet", ""),
                    })

            return results
        except Exception as e:
            print(f"SerpAPI web search error: {str(e)}")
            return []


    # ----------------------------------------------------------------
    # Simple LLM generate (for /api/llm/generate endpoint)
    # ----------------------------------------------------------------
    async def generate_response(
        self, prompt: str, model: str = "flan-t5",
        temperature: float = 0.7, max_tokens: int = 512
    ) -> str:
        """Generate a direct response using local LLM."""
        return await self.generate_workflow_response(
            query=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            context=None,
            custom_prompt=None,
            use_web_search=False,
        )


    # ----------------------------------------------------------------
    # Core Workflow Response (called during workflow execution)
    # ----------------------------------------------------------------
    async def generate_workflow_response(
        self,
        query: str,
        model: str = "flan-t5",
        temperature: float = 0.7,
        max_tokens: int = 512,
        context: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        use_web_search: bool = False
    ) -> str:
        """
        Generate a response using the LOCAL Flan-T5 model (no API key required).

        Behavior:
        - If context is provided (from PDF / Knowledge Base) → answer from document.
        - If use_web_search is True → also search web via SerpAPI and
          include web results as additional context for the LLM.
        - If use_web_search is False → answer ONLY from the document context.
        """
        import asyncio

        # ----- Build context sections -----
        context_parts = []

        # 1. Document / Knowledge Base context (RAG)
        if context and context.strip():
            context_parts.append(f"Document context:\n{context}")

        # 2. Web search context (only if toggle is ON)
        if use_web_search:
            web_results = await self.web_search(query, num_results=5)
            if web_results:
                web_text = "\n".join([
                    f"- {r['title']}: {r['snippet']}"
                    for r in web_results
                ])
                context_parts.append(f"Web search results:\n{web_text}")

        combined_context = "\n\n".join(context_parts) if context_parts else ""

        # ----- Build the prompt for Flan-T5 -----
        if custom_prompt and custom_prompt.strip():
            prompt = custom_prompt.replace("{context}", combined_context).replace("{query}", query)
        elif combined_context:
            # Flan-T5 works best with clear, concise instruction prompts
            prompt = (
                f"Answer the following question based on the given context. "
                f"If the context does not contain enough information, say so.\n\n"
                f"Context: {combined_context}\n\n"
                f"Question: {query}\n\n"
                f"Answer:"
            )
        else:
            prompt = f"Answer the following question:\n\nQuestion: {query}\n\nAnswer:"

        # ----- Run model in thread executor (model is synchronous) -----
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._generate_local(prompt, max_new_tokens=min(max_tokens, 512))
            )
            return response if response.strip() else "I could not generate a meaningful answer for this query."
        except Exception as e:
            return f"Error generating response: {str(e)}"
