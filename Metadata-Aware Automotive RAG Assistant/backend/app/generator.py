"""
Drive Wise - Generator Module
LLM-powered answer generation with source attribution and evaluation.
Uses Google Gemini API for grounded response generation.
"""

from typing import List, Dict, Optional
from app.config import GEMINI_API_KEY, GEMINI_MODEL

# Try to import Google GenAI (new SDK)
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None


# ──────────────────────────────────────────────
# System Prompt for Grounded Responses
# ──────────────────────────────────────────────
SYSTEM_PROMPT = """You are Drive Wise, an expert automotive AI assistant that helps users understand car brochures. 
You provide accurate, helpful, and well-structured answers based ONLY on the provided brochure content.

CRITICAL RULES:
1. ONLY use information from the provided brochure context to answer questions.
2. If the context does not contain information to answer the question, clearly state: "I don't have this specific information in the brochure. The brochure context provided does not cover this topic."
3. NEVER make up or infer specifications, prices, or features that are not explicitly mentioned in the context.
4. When citing information, mention the source section naturally in your response (e.g., "According to the Safety Features section...").
5. Format your response in a clear, readable manner using bullet points for lists and specifications.
6. Be conversational and helpful, as if you're a knowledgeable car dealer explaining features to a customer.
7. If multiple sources provide related information, synthesize them into a coherent answer.
8. For numerical specifications (dimensions, mileage, power), be precise and include units."""


class Generator:
    """
    LLM-powered response generator with grounded prompts and evaluation.
    Falls back to context-based formatting when Gemini API is unavailable.
    """

    def __init__(self):
        """Initialize the Gemini model if API key is available."""
        self.client = None
        self.is_available = False

        if GEMINI_AVAILABLE and GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            try:
                self.client = genai.Client(api_key=GEMINI_API_KEY)
                self.is_available = True
                print(f"Gemini model ({GEMINI_MODEL}) initialized successfully.")
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}. Using fallback mode.")
        else:
            print("Gemini API key not configured. Using fallback response mode.")
            print("Set GEMINI_API_KEY in your .env file for AI-powered responses.")

    def generate(
        self,
        query: str,
        context: str,
        brand: str,
        model: str,
        sources: List[Dict]
    ) -> Dict:
        """
        Generate a grounded answer using the LLM or fallback formatter.
        
        Args:
            query: User's natural language question
            context: Formatted context string from retriever
            brand: Selected car brand
            model: Selected car model
            sources: List of source metadata dicts
            
        Returns:
            Dict with 'answer' and 'evaluation' keys
        """
        if self.is_available:
            return self._generate_with_gemini(query, context, brand, model, sources)
        else:
            return self._generate_fallback(query, context, brand, model, sources)

    def _generate_with_gemini(
        self,
        query: str,
        context: str,
        brand: str,
        model_name: str,
        sources: List[Dict]
    ) -> Dict:
        """Generate response using Google Gemini API."""
        # Build the grounded prompt
        prompt = self._build_prompt(query, context, brand, model_name)

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                )
            )
            answer = response.text

            # Compute evaluation metrics
            evaluation = self._evaluate_response(query, answer, context, sources)

            return {
                "answer": answer,
                "evaluation": evaluation
            }
        except Exception as e:
            print(f"Gemini generation failed: {e}")
            return self._generate_fallback(query, context, brand, model_name, sources)

    def _generate_fallback(
        self,
        query: str,
        context: str,
        brand: str,
        model_name: str,
        sources: List[Dict]
    ) -> Dict:
        """
        Fallback response when Gemini API is unavailable.
        Formats the retrieved context into a structured answer.
        """
        if not context or context == "No relevant brochure content found.":
            answer = (
                f"I couldn't find specific information about your query in the "
                f"{brand} {model_name} brochure. Please try rephrasing your question "
                f"or ask about a specific feature like engine, mileage, safety, "
                f"dimensions, interior, or infotainment."
            )
            return {
                "answer": answer,
                "evaluation": {
                    "context_relevance": 0.0,
                    "answer_groundedness": 0.0,
                    "answer_completeness": 0.0
                }
            }

        # Format a structured response from the context
        sections_used = set()
        for source in sources:
            meta = source.get("metadata", {})
            if "section" in meta:
                sections_used.add(meta["section"])

        sections_str = ", ".join(sections_used) if sections_used else "the brochure"

        answer = (
            f"Based on the **{brand} {model_name}** brochure "
            f"(from {sections_str}):\n\n"
            f"{context}\n\n"
            f"---\n"
            f"*Note: This is a direct excerpt from the brochure. "
            f"For AI-powered conversational answers, please configure your "
            f"Gemini API key in the .env file.*"
        )

        return {
            "answer": answer,
            "evaluation": {
                "context_relevance": 0.7,
                "answer_groundedness": 1.0,
                "answer_completeness": 0.6
            }
        }

    def _build_prompt(
        self,
        query: str,
        context: str,
        brand: str,
        model_name: str
    ) -> str:
        """Build the grounded prompt for the LLM."""
        return f"""The user is asking about the **{brand} {model_name}**.

Here is the relevant brochure content retrieved for their question:

---
{context}
---

User's Question: {query}

Please provide a comprehensive, accurate answer based ONLY on the brochure content above. 
If the brochure content doesn't contain the answer, say so clearly.
Structure your response with bullet points for specifications and features."""

    def _evaluate_response(
        self,
        query: str,
        answer: str,
        context: str,
        sources: List[Dict]
    ) -> Dict[str, float]:
        """
        Compute quality evaluation metrics for the response.
        
        Metrics:
        - context_relevance: How relevant the retrieved chunks are to the query
        - answer_groundedness: How grounded the answer is in the context
        - answer_completeness: How completely the answer addresses the query
        """
        # Simple heuristic-based evaluation
        # In production, these would use a separate LLM evaluation step

        # Context relevance: check keyword overlap between query and context
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())
        common_words = query_words.intersection(context_words)
        # Filter out common stop words
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "of", "in",
                      "to", "for", "on", "with", "what", "how", "does", "do",
                      "this", "that", "it", "and", "or", "but", "not", "its"}
        meaningful_common = common_words - stop_words
        meaningful_query = query_words - stop_words
        context_relevance = (
            len(meaningful_common) / max(len(meaningful_query), 1)
        )
        context_relevance = min(1.0, context_relevance)

        # Answer groundedness: check if answer terms appear in context
        answer_words = set(answer.lower().split())
        meaningful_answer = answer_words - stop_words
        grounded_words = meaningful_answer.intersection(context_words)
        answer_groundedness = (
            len(grounded_words) / max(len(meaningful_answer), 1)
        )
        answer_groundedness = min(1.0, answer_groundedness)

        # Answer completeness: based on answer length relative to context
        answer_length = len(answer.split())
        completeness = min(1.0, answer_length / 50)  # Expect at least ~50 words

        return {
            "context_relevance": round(context_relevance, 3),
            "answer_groundedness": round(answer_groundedness, 3),
            "answer_completeness": round(completeness, 3)
        }
