"""
Drive Wise - Retriever Module
Implements metadata-filtered retrieval with cross-encoder re-ranking.
"""

from typing import List, Dict, Optional
from sentence_transformers import CrossEncoder

from app.config import RERANKER_MODEL, TOP_K_RETRIEVAL, TOP_N_RERANK
from app.vectorstore import VectorStore


class Retriever:
    """
    Enhanced retriever with:
    1. Metadata filtering (brand/model)
    2. Vector similarity search
    3. Cross-encoder re-ranking
    4. Context window control
    """

    def __init__(self, vectorstore: VectorStore):
        """
        Initialize the retriever with a vector store and re-ranking model.
        
        Args:
            vectorstore: VectorStore instance for similarity search
        """
        self.vectorstore = vectorstore
        self._reranker = None  # Lazy loading

    @property
    def reranker(self):
        """Lazy-load the cross-encoder re-ranking model."""
        if self._reranker is None:
            print("Loading re-ranking model...")
            self._reranker = CrossEncoder(RERANKER_MODEL, max_length=512)
            print("Re-ranking model loaded.")
        return self._reranker

    def retrieve(
        self,
        query: str,
        brand: str,
        model: str,
        top_k: int = TOP_K_RETRIEVAL,
        top_n: int = TOP_N_RERANK
    ) -> List[Dict]:
        """
        Full retrieval pipeline:
        1. Metadata-filtered vector search (top-K)
        2. Cross-encoder re-ranking
        3. Context window control (top-N)
        
        Args:
            query: User's natural language question
            brand: Selected car brand for metadata filtering
            model: Selected car model for metadata filtering
            top_k: Number of initial vector search results
            top_n: Number of final re-ranked results
            
        Returns:
            List of re-ranked result dicts with 'text', 'metadata', 
            'distance', and 'rerank_score' keys
        """
        # Step 1: Metadata-filtered vector search
        initial_results = self.vectorstore.query(
            query_text=query,
            brand=brand,
            model=model,
            n_results=top_k
        )

        if not initial_results:
            return []

        # Step 2: Cross-encoder re-ranking
        # Create query-document pairs for the cross-encoder
        pairs = [(query, result["text"]) for result in initial_results]

        try:
            rerank_scores = self.reranker.predict(pairs).tolist()
        except Exception as e:
            print(f"Re-ranking failed: {e}. Using original order.")
            # Fallback: use vector similarity scores
            for result in initial_results:
                result["rerank_score"] = 1.0 - result.get("distance", 0.5)
            return initial_results[:top_n]

        # Attach re-rank scores to results
        for result, score in zip(initial_results, rerank_scores):
            result["rerank_score"] = float(score)

        # Step 3: Sort by re-rank score (descending) and apply context window
        ranked_results = sorted(
            initial_results,
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        # Context window control: keep only top-N results
        top_results = ranked_results[:top_n]

        return top_results

    def get_context_string(self, results: List[Dict]) -> str:
        """
        Format retrieved results into a context string for the LLM.
        
        Args:
            results: List of re-ranked results
            
        Returns:
            Formatted context string with source attribution
        """
        if not results:
            return "No relevant brochure content found."

        context_parts = []
        for i, result in enumerate(results, 1):
            metadata = result.get("metadata", {})
            section = metadata.get("section", "Unknown Section")
            page = metadata.get("page_number", "N/A")
            brochure = metadata.get("brochure_name", "Unknown Brochure")

            context_parts.append(
                f"[Source {i}] Section: {section} | Page: {page} | Brochure: {brochure}\n"
                f"{result['text']}"
            )

        return "\n\n---\n\n".join(context_parts)

    def compute_context_relevance(self, query: str, results: List[Dict]) -> float:
        """
        Compute how relevant the retrieved context is to the query.
        Uses the average re-rank score normalized to 0-1.
        
        Args:
            query: User's question
            results: Retrieved and re-ranked results
            
        Returns:
            Context relevance score (0-1)
        """
        if not results:
            return 0.0

        scores = [r.get("rerank_score", 0.0) for r in results]
        avg_score = sum(scores) / len(scores)

        # Normalize cross-encoder scores to 0-1 range
        # Cross-encoder scores are typically in range [-10, 10]
        normalized = max(0.0, min(1.0, (avg_score + 5) / 10))

        return round(normalized, 3)
