import os
import json
import shutil
from typing import List, Dict, Any, Optional, Tuple
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from sentence_transformers import CrossEncoder

class RAGEngine:
    def __init__(self, data_dir: str = "./data", db_dir: str = "./chroma_db", metadata_file: str = "./metadata.json"):
        self.data_dir = data_dir
        self.db_dir = db_dir
        self.metadata_file = metadata_file
        
        # Ensure directories exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.db_dir, exist_ok=True)
        
        # Load or initialize metadata
        self.metadata = self._load_metadata()
        
        # Initialize Embeddings (runs locally and cached)
        print("Initializing Embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize Cross-Encoder for Re-ranking (runs locally and cached)
        self.reranker = None
        self.reranker_loaded = False
        
        # Vector database instance
        self.vector_store = None
        self.bm25_retriever = None
        self.chunks: List[Document] = []
        
        # Load existing database if metadata has items
        self.load_database()

    def _load_metadata(self) -> Dict[str, Any]:
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading metadata: {e}")
        return {"documents": {}, "config": {}}

    def _save_metadata(self):
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(self.metadata, f, indent=4)
        except Exception as e:
            print(f"Error saving metadata: {e}")

    def load_database(self):
        """Load vector store and BM25 index from disk if documents exist."""
        doc_count = len(self.metadata.get("documents", {}))
        if doc_count > 0:
            print(f"Loading existing vector database with {doc_count} documents...")
            self.vector_store = Chroma(
                persist_directory=self.db_dir,
                embedding_function=self.embeddings
            )
            # Rebuild chunks cache and BM25 index
            self._rebuild_cache_and_bm25()
        else:
            print("Vector database is empty. Waiting for ingestion.")

    def _rebuild_cache_and_bm25(self):
        """Extracts chunks from current database to rebuild BM25 and cached list."""
        if not self.vector_store:
            return
        
        try:
            # chroma allows fetching all records
            db_data = self.vector_store.get()
            self.chunks = []
            if db_data and 'documents' in db_data:
                for doc_text, metadata in zip(db_data['documents'], db_data['metadatas']):
                    self.chunks.append(Document(page_content=doc_text, metadata=metadata))
            
            if self.chunks:
                self.bm25_retriever = BM25Retriever.from_documents(self.chunks)
                print(f"Rebuilt BM25 retriever with {len(self.chunks)} chunks.")
            else:
                self.bm25_retriever = None
        except Exception as e:
            print(f"Error rebuilding cache and BM25: {e}")

    def ingest_document(self, file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> Dict[str, Any]:
        """Loads, chunks, and indexes a single document."""
        filename = os.path.basename(file_path)
        print(f"Ingesting document: {filename} (Size: {chunk_size}, Overlap: {chunk_overlap})")
        
        # 1. Load document
        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.lower().endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError("Unsupported file format. Only PDF and TXT are supported.")
            
        docs = loader.load()
        
        # 2. Text Chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        chunks = text_splitter.split_documents(docs)
        
        # Add metadata source tag
        for chunk in chunks:
            chunk.metadata["source"] = filename
            
        # 3. Add to Chroma
        if not self.vector_store:
            self.vector_store = Chroma(
                persist_directory=self.db_dir,
                embedding_function=self.embeddings
            )
            
        self.vector_store.add_documents(chunks)
        
        # Update metadata
        self.metadata["documents"][filename] = {
            "path": file_path,
            "chunk_count": len(chunks),
            "original_docs_count": len(docs)
        }
        self._save_metadata()
        
        # 4. Rebuild BM25
        self._rebuild_cache_and_bm25()
        
        return {
            "status": "success",
            "filename": filename,
            "chunks_created": len(chunks)
        }

    def delete_document(self, filename: str) -> Dict[str, Any]:
        """Deletes a document from the vector store and metadata."""
        if filename not in self.metadata["documents"]:
            raise ValueError(f"Document {filename} not found in database.")
            
        print(f"Deleting document: {filename}")
        
        # Remove file from data dir
        file_path = self.metadata["documents"][filename]["path"]
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Re-initialize vector store by building a new one without this file's chunks
        # ChromaDB doesn't always support easy delete by metadata filter out of the box in langchain interface,
        # so rebuilding DB or deleting where metadata source == filename is needed.
        if self.vector_store:
            try:
                # Get all documents
                db_data = self.vector_store.get()
                ids_to_delete = []
                if db_data and 'metadatas' in db_data:
                    for i, meta in enumerate(db_data['metadatas']):
                        if meta.get("source") == filename:
                            ids_to_delete.append(db_data['ids'][i])
                
                if ids_to_delete:
                    self.vector_store.delete(ids=ids_to_delete)
                    print(f"Deleted {len(ids_to_delete)} vectors from Chroma.")
            except Exception as e:
                print(f"Chroma delete error, performing fresh rebuild: {e}")
                # Fallback: recreate db directory and re-ingest others
                self.clear_all(delete_files=False)
                # Re-ingest other documents in metadata
                remaining_docs = list(self.metadata["documents"].keys())
                for doc in remaining_docs:
                    if doc != filename:
                        doc_path = self.metadata["documents"][doc]["path"]
                        self.ingest_document(doc_path)
        
        # Clean metadata entry
        if filename in self.metadata["documents"]:
            del self.metadata["documents"][filename]
        self._save_metadata()
        
        # Rebuild cache
        self._rebuild_cache_and_bm25()
        
        return {"status": "success", "message": f"Deleted {filename}"}

    def clear_all(self, delete_files: bool = True):
        """Clears vector store and optionally uploaded files."""
        print("Clearing all databases and caches...")
        
        # Remove directory chroma_db
        if os.path.exists(self.db_dir):
            shutil.rmtree(self.db_dir)
        os.makedirs(self.db_dir, exist_ok=True)
        
        if delete_files:
            if os.path.exists(self.data_dir):
                shutil.rmtree(self.data_dir)
            os.makedirs(self.data_dir, exist_ok=True)
            self.metadata["documents"] = {}
        
        self.vector_store = None
        self.bm25_retriever = None
        self.chunks = []
        self._save_metadata()

    def _lazy_load_reranker(self):
        """Loads cross-encoder reranker model only when needed."""
        if not self.reranker_loaded:
            try:
                print("Loading CrossEncoder Re-ranker (cross-encoder/ms-marco-MiniLM-L-6-v2)...")
                # Using a very small model (approx 80MB)
                self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device='cpu')
                self.reranker_loaded = True
            except Exception as e:
                print(f"Warning: Failed to load cross-encoder reranker: {e}. Falling back to normal retrieval.")
                self.reranker_loaded = True # Prevent retry loop
                self.reranker = None

    def retrieve(
        self, 
        query: str, 
        retrieval_type: str = "hybrid", 
        top_k: int = 5, 
        vector_weight: float = 0.5, 
        keyword_weight: float = 0.5,
        use_reranker: bool = True
    ) -> List[Dict[str, Any]]:
        """Retrieves most relevant chunks using Vector, Keyword, or Hybrid search, with optional Re-ranking."""
        if not self.vector_store or not self.chunks:
            return []
            
        retrieved_docs = []
        
        # 1. Fetch Candidates
        if retrieval_type == "vector":
            retrieved_docs = self.vector_store.similarity_search(query, k=top_k * 2 if use_reranker else top_k)
        elif retrieval_type == "keyword":
            if self.bm25_retriever:
                retrieved_docs = self.bm25_retriever.invoke(query)[:top_k * 2 if use_reranker else top_k]
            else:
                retrieved_docs = self.vector_store.similarity_search(query, k=top_k * 2 if use_reranker else top_k)
        else: # Hybrid
            if self.bm25_retriever:
                vector_retriever = self.vector_store.as_retriever(search_kwargs={"k": top_k * 2 if use_reranker else top_k})
                ensemble_retriever = EnsembleRetriever(
                    retrievers=[vector_retriever, self.bm25_retriever],
                    weights=[vector_weight, keyword_weight]
                )
                retrieved_docs = ensemble_retriever.invoke(query)
            else:
                retrieved_docs = self.vector_store.similarity_search(query, k=top_k * 2 if use_reranker else top_k)
                
        # Remove duplicate chunks
        seen = set()
        unique_docs = []
        for doc in retrieved_docs:
            content_hash = hash(doc.page_content)
            if content_hash not in seen:
                seen.add(content_hash)
                unique_docs.append(doc)
        
        # 2. Optional Re-ranking using Cross-Encoder
        if use_reranker and unique_docs:
            self._lazy_load_reranker()
            if self.reranker:
                pairs = [[query, doc.page_content] for doc in unique_docs]
                scores = self.reranker.predict(pairs)
                
                # Pair document with score and sort
                doc_scores = sorted(zip(unique_docs, scores), key=lambda x: x[1], reverse=True)
                # Keep top K
                final_docs = doc_scores[:top_k]
                
                # Format output with rerank score
                return [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "score": float(score)
                    }
                    for doc, score in final_docs
                ]
        
        # If not reranked, format with dummy scores or similarity distance
        # Chroma similarity search doesn't return distances in default langchain wrapper easily, we assign default order scores
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": float(len(unique_docs) - i) / len(unique_docs) if unique_docs else 1.0
            }
            for i, doc in enumerate(unique_docs[:top_k])
        ]

    def generate_answer(
        self, 
        query: str, 
        context_docs: List[Dict[str, Any]], 
        temperature: float = 0.2, 
        model_name: str = "gemini-3.1-flash-lite"
    ) -> Dict[str, Any]:
        """Generates grounded answer using context and a selection of LLM (Gemini, OpenAI, or Mock)."""
        context_str = "\n\n".join([
            f"[Source: {doc['metadata'].get('source', 'Unknown')}]\n{doc['content']}" 
            for doc in context_docs
        ])
        
        system_prompt = (
            "You are a helpful and precise assistant. Answer the user's question based strictly on the provided context. "
            "If the context does not contain enough information to answer the question, state clearly that you do not "
            "know or cannot find the answer in the provided documents. Do not make up facts. "
            "Cite the source documents by name (e.g., [document_name.pdf]) where appropriate in your response.\n\n"
            f"Context:\n{context_str}"
        )
        
        messages = [
            ("system", system_prompt),
            ("user", query)
        ]
        
        prompt_tmpl = ChatPromptTemplate.from_messages(messages)
        
        gemini_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        
        # Check model prefix or configurations to choose LLM
        use_openai = openai_api_key and ("gpt" in model_name.lower() or not gemini_api_key)
        
        answer = ""
        used_model = model_name
        
        try:
            if use_openai:
                print(f"Generating answer with OpenAI model: {model_name}...")
                llm = ChatOpenAI(model=model_name, temperature=temperature, openai_api_key=openai_api_key)
                chain = prompt_tmpl | llm | StrOutputParser()
                answer = chain.invoke({})
            elif gemini_api_key:
                # Map user custom request model name to google's official SDK name if necessary
                # In google SDK, the model is usually 'gemini-2.5-flash', 'gemini-1.5-flash', etc.
                # If they say gemini-3.1-flash-lite, we will pass it directly. If it fails, fallback to gemini-2.5-flash or gemini-1.5-flash.
                google_model = model_name
                print(f"Generating answer with Gemini model: {google_model}...")
                try:
                    llm = ChatGoogleGenerativeAI(model=google_model, temperature=temperature, google_api_key=gemini_api_key)
                    chain = prompt_tmpl | llm | StrOutputParser()
                    answer = chain.invoke({})
                except Exception as e:
                    print(f"Model {google_model} error: {e}. Trying fallback 'gemini-1.5-flash'...")
                    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=temperature, google_api_key=gemini_api_key)
                    chain = prompt_tmpl | llm | StrOutputParser()
                    answer = chain.invoke({})
                    used_model = "gemini-1.5-flash (fallback)"
            else:
                # Fallback mock answer if no API keys are provided
                print("No API keys found. Generating a mock response with citations...")
                used_model = "Mock Generator (No API Key)"
                if not context_docs:
                    answer = "I'm sorry, I don't have any documents ingested in the database to answer your question."
                else:
                    sources = list(set([doc['metadata'].get('source', 'Unknown') for doc in context_docs]))
                    answer = (
                        f"**[SIMULATED RESPONSE - Please configure your GEMINI_API_KEY in the environment / .env file to generate actual LLM answers]**\n\n"
                        f"I retrieved the following information from {', '.join(sources)}:\n\n"
                        f"Here is a summary of the context that relates to your query: '{query}'\n\n"
                        + "\n\n".join([f"- From *{doc['metadata'].get('source', 'Unknown')}*: \"{doc['content'][:150]}...\"" for doc in context_docs[:3]])
                    )
        except Exception as e:
            print(f"Error during generation: {e}")
            answer = f"Error generating answer: {str(e)}. Please check your API keys and model configuration."
            
        return {
            "answer": answer,
            "model_used": used_model,
            "sources": context_docs
        }
