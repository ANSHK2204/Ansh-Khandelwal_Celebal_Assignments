import os
import uvicorn
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import RAG Engine
from rag_engine import RAGEngine

app = FastAPI(title="RAG Question Answering System API")

# Configure CORS for React UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAGEngine
data_dir = os.path.join(os.path.dirname(__file__), "data")
db_dir = os.path.join(os.path.dirname(__file__), "chroma_db")
metadata_file = os.path.join(os.path.dirname(__file__), "metadata.json")

rag_engine = RAGEngine(data_dir=data_dir, db_dir=db_dir, metadata_file=metadata_file)

# Request Models
class QueryRequest(BaseModel):
    query: str
    retrieval_type: str = "hybrid" # "vector", "keyword", "hybrid"
    top_k: int = 5
    temperature: float = 0.2
    model_name: str = "gemini-3.1-flash-lite"
    vector_weight: float = 0.5
    keyword_weight: float = 0.5
    use_reranker: bool = True

@app.get("/")
def read_root():
    return {"message": "RAG System API is running successfully"}

@app.post("/query")
def run_query(request: QueryRequest):
    """Retrieves relevant chunks and generates an answer."""
    try:
        # 1. Retrieve chunks
        retrieved_docs = rag_engine.retrieve(
            query=request.query,
            retrieval_type=request.retrieval_type,
            top_k=request.top_k,
            vector_weight=request.vector_weight,
            keyword_weight=request.keyword_weight,
            use_reranker=request.use_reranker
        )
        
        # 2. Check if documents exist in DB
        if not retrieved_docs:
            return {
                "answer": "No documents found in the database. Please upload and ingest documents first.",
                "model_used": "N/A",
                "sources": []
            }
            
        # 3. Generate answer
        result = rag_engine.generate_answer(
            query=request.query,
            context_docs=retrieved_docs,
            temperature=request.temperature,
            model_name=request.model_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunk_size: int = Form(1000),
    chunk_overlap: int = Form(200)
):
    """Uploads and indexes a PDF/TXT document."""
    try:
        filename = file.filename
        if not filename.lower().endswith((".pdf", ".txt")):
            raise HTTPException(status_code=400, detail="Unsupported file format. Only PDF and TXT are supported.")
        
        # Save file to upload directory
        file_path = os.path.join(rag_engine.data_dir, filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ingest document
        ingest_res = rag_engine.ingest_document(
            file_path=file_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return ingest_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload and ingest file: {str(e)}")

@app.get("/documents")
def list_documents():
    """Lists all currently ingested documents and chunk metadata."""
    try:
        return {
            "documents": rag_engine.metadata.get("documents", {}),
            "total_documents": len(rag_engine.metadata.get("documents", {}))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{filename}")
def delete_document(filename: str):
    """Deletes document from disk and vector store index."""
    try:
        return rag_engine.delete_document(filename)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
def clear_all(delete_files: bool = True):
    """Clears the search index and (optionally) all document files."""
    try:
        rag_engine.clear_all(delete_files=delete_files)
        return {"status": "success", "message": "All databases cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
def get_config():
    """Returns application setup status and default configs."""
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    return {
        "available_models": [
            "gemini-3.1-flash-lite",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gpt-4o-mini",
            "gpt-4o"
        ],
        "default_model": "gemini-3.1-flash-lite",
        "gemini_key_configured": bool(gemini_key),
        "openai_key_configured": bool(openai_key)
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
