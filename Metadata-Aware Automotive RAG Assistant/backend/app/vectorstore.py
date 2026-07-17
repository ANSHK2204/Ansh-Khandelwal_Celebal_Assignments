"""
Drive Wise - Vector Store Module
ChromaDB wrapper with metadata filtering for car brochure embeddings.
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional
import hashlib

from app.config import (
    CHROMA_PERSIST_DIR, CHROMA_COLLECTION,
    EMBEDDING_MODEL, TOP_K_RETRIEVAL
)


class VectorStore:
    """
    ChromaDB-based vector store with metadata filtering support.
    Uses sentence-transformers for embedding generation.
    """

    def __init__(self):
        """Initialize ChromaDB client and embedding function."""
        # Persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)

        # Sentence-transformers embedding function
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

        # Get or create the collection
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def _generate_id(self, text: str, metadata: Dict) -> str:
        """Generate a unique document ID from content and metadata."""
        content = f"{metadata.get('brand', '')}_{metadata.get('model', '')}_{metadata.get('section', '')}_{text[:100]}"
        return hashlib.md5(content.encode()).hexdigest()

    def add_documents(self, chunks: List[Dict]) -> int:
        """
        Add brochure chunks to the vector store.
        
        Args:
            chunks: List of dicts with 'text' and 'metadata' keys
            
        Returns:
            Number of documents added
        """
        if not chunks:
            return 0

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:
            doc_id = self._generate_id(chunk["text"], chunk["metadata"])

            # Skip duplicates
            try:
                existing = self.collection.get(ids=[doc_id])
                if existing and existing["ids"]:
                    continue
            except Exception:
                pass

            ids.append(doc_id)
            documents.append(chunk["text"])
            metadatas.append(chunk["metadata"])

        if ids:
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

        return len(ids)

    def query(
        self,
        query_text: str,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        n_results: int = TOP_K_RETRIEVAL
    ) -> List[Dict]:
        """
        Query the vector store with optional metadata filtering.
        
        Args:
            query_text: User's search query
            brand: Filter by car brand (optional)
            model: Filter by car model (optional)
            n_results: Number of results to return
            
        Returns:
            List of result dicts with 'text', 'metadata', and 'distance' keys
        """
        # Build metadata filter
        where_filter = None
        if brand and model:
            where_filter = {
                "$and": [
                    {"brand": {"$eq": brand}},
                    {"model": {"$eq": model}}
                ]
            }
        elif brand:
            where_filter = {"brand": {"$eq": brand}}
        elif model:
            where_filter = {"model": {"$eq": model}}

        # Query with filter
        try:
            # Ensure we don't request more results than available
            total_docs = self.collection.count()
            actual_n = min(n_results, total_docs) if total_docs > 0 else n_results

            if actual_n == 0:
                return []

            results = self.collection.query(
                query_texts=[query_text],
                n_results=actual_n,
                where=where_filter
            )
        except Exception as e:
            # If filtered query fails (e.g., no docs match filter), try without filter
            print(f"Filtered query failed: {e}. Trying without filter...")
            try:
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results
                )
            except Exception as e2:
                print(f"Query failed: {e2}")
                return []

        # Format results
        formatted_results = []
        if results and results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else 0.0
                })

        return formatted_results

    def get_available_brands(self) -> List[str]:
        """Get list of unique brands in the vector store."""
        try:
            all_metadata = self.collection.get()
            if all_metadata and all_metadata["metadatas"]:
                brands = set()
                for meta in all_metadata["metadatas"]:
                    if "brand" in meta:
                        brands.add(meta["brand"])
                return sorted(brands)
        except Exception as e:
            print(f"Error getting brands: {e}")
        return []

    def get_models_for_brand(self, brand: str) -> List[str]:
        """Get list of available models for a specific brand."""
        try:
            results = self.collection.get(
                where={"brand": {"$eq": brand}}
            )
            if results and results["metadatas"]:
                models = set()
                for meta in results["metadatas"]:
                    if "model" in meta:
                        models.add(meta["model"])
                return sorted(models)
        except Exception as e:
            print(f"Error getting models for {brand}: {e}")
        return []

    def get_document_count(self) -> int:
        """Get total number of documents in the vector store."""
        return self.collection.count()

    def delete_brand_model(self, brand: str, model: str) -> int:
        """Delete all documents for a specific brand and model."""
        try:
            results = self.collection.get(
                where={
                    "$and": [
                        {"brand": {"$eq": brand}},
                        {"model": {"$eq": model}}
                    ]
                }
            )
            if results and results["ids"]:
                self.collection.delete(ids=results["ids"])
                return len(results["ids"])
        except Exception as e:
            print(f"Error deleting documents: {e}")
        return 0

    def reset(self):
        """Delete all documents and reset the collection."""
        self.client.delete_collection(CHROMA_COLLECTION)
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )
