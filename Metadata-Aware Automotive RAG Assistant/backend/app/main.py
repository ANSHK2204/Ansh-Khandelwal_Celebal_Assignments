"""
Drive Wise - Main Application
FastAPI server with all API endpoints for the automotive RAG assistant.
"""

import time
import os
import shutil
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import BROCHURES_DIR, FRONTEND_DIR
from app.models import (
    ChatRequest, ChatResponse, SourceInfo, EvaluationMetrics,
    UploadResponse, BrandListResponse, ModelListResponse,
    LogsResponse, LogEntry
)
from app.sample_data import get_all_chunks
from app.vectorstore import VectorStore
from app.retriever import Retriever
from app.generator import Generator
from app.ingestion import ingest_pdf
from app.logger import QueryLogger


# ──────────────────────────────────────────────
# Global instances (initialized on startup)
# ──────────────────────────────────────────────
vectorstore: Optional[VectorStore] = None
retriever: Optional[Retriever] = None
generator: Optional[Generator] = None
logger: Optional[QueryLogger] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    global vectorstore, retriever, generator, logger

    print("\n" + "=" * 60)
    print("  [*] Drive Wise - Starting Up...")
    print("=" * 60)

    # Initialize components
    print("\n[+] Initializing Vector Store...")
    vectorstore = VectorStore()

    print("[+] Initializing Retriever...")
    retriever = Retriever(vectorstore)

    print("[+] Initializing Generator...")
    generator = Generator()

    print("[+] Initializing Query Logger...")
    logger = QueryLogger()

    # Load sample data if vector store is empty
    if vectorstore.get_document_count() == 0:
        print("\n[+] Loading sample brochure data...")
        sample_chunks = get_all_chunks()
        count = vectorstore.add_documents(sample_chunks)
        print(f"   [OK] Loaded {count} chunks from sample brochures.")
    else:
        print(f"\n[OK] Vector store already contains {vectorstore.get_document_count()} documents.")

    print("\n" + "=" * 60)
    print("  [OK] Drive Wise is ready!")
    print(f"  Frontend: {FRONTEND_DIR}")
    print(f"  Open: http://localhost:8000")
    print("=" * 60 + "\n")

    yield

    # Cleanup on shutdown
    print("\n[*] Drive Wise shutting down...")


# ──────────────────────────────────────────────
# FastAPI Application
# ──────────────────────────────────────────────
app = FastAPI(
    title="Drive Wise",
    description="Metadata-aware Automotive RAG Assistant",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# API Endpoints
# ──────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    doc_count = vectorstore.get_document_count() if vectorstore else 0
    return {
        "status": "healthy",
        "documents_loaded": doc_count,
        "gemini_available": generator.is_available if generator else False
    }


@app.get("/api/brands", response_model=BrandListResponse)
async def get_brands():
    """Get list of available car brands."""
    brands = vectorstore.get_available_brands()
    return BrandListResponse(brands=brands)


@app.get("/api/models/{brand}", response_model=ModelListResponse)
async def get_models(brand: str):
    """Get list of available car models for a brand."""
    models = vectorstore.get_models_for_brand(brand)
    return ModelListResponse(brand=brand, models=models)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Takes a user query with brand/model context and returns a grounded answer.
    """
    start_time = time.time()

    try:
        # Step 1: Retrieve relevant chunks with metadata filtering and re-ranking
        results = retriever.retrieve(
            query=request.query,
            brand=request.brand,
            model=request.model
        )

        # Step 2: Build context string from retrieved chunks
        context = retriever.get_context_string(results)

        # Step 3: Compute context relevance
        context_relevance = retriever.compute_context_relevance(
            request.query, results
        )

        # Step 4: Generate grounded response
        gen_result = generator.generate(
            query=request.query,
            context=context,
            brand=request.brand,
            model=request.model,
            sources=results
        )

        # Step 5: Build source attribution
        sources = []
        for result in results:
            meta = result.get("metadata", {})
            sources.append(SourceInfo(
                brochure_name=meta.get("brochure_name", "Unknown"),
                section=meta.get("section", "Unknown"),
                page_number=meta.get("page_number", 0),
                chunk_text=result["text"][:300] + "..." if len(result["text"]) > 300 else result["text"],
                relevance_score=round(result.get("rerank_score", 0.0), 3)
            ))

        # Calculate response time
        response_time_ms = round((time.time() - start_time) * 1000, 2)

        # Build evaluation metrics
        eval_data = gen_result.get("evaluation", {})
        eval_data["context_relevance"] = context_relevance
        evaluation = EvaluationMetrics(**eval_data)

        # Step 6: Log the query
        source_sections = [s.section for s in sources]
        logger.log_query(
            query=request.query,
            brand=request.brand,
            model=request.model,
            response_time_ms=response_time_ms,
            chunks_retrieved=len(results),
            status="success",
            sources_used=source_sections,
            answer_preview=gen_result["answer"][:200],
            evaluation=eval_data
        )

        return ChatResponse(
            answer=gen_result["answer"],
            sources=sources,
            response_time_ms=response_time_ms,
            evaluation=evaluation,
            brand=request.brand,
            model=request.model
        )

    except Exception as e:
        response_time_ms = round((time.time() - start_time) * 1000, 2)

        # Log the error
        logger.log_query(
            query=request.query,
            brand=request.brand,
            model=request.model,
            response_time_ms=response_time_ms,
            status="error",
            error_message=str(e)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.post("/api/upload", response_model=UploadResponse)
async def upload_brochure(
    file: UploadFile = File(...),
    brand: str = Form(...),
    model: str = Form(...),
    document_version: str = Form(default="2024")
):
    """
    Upload a car brochure PDF for ingestion.
    The PDF is parsed, chunked, and indexed in the vector store.
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # Save the uploaded file
    file_path = BROCHURES_DIR / f"{brand}_{model}_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    # Ingest the PDF
    try:
        chunks = ingest_pdf(
            pdf_path=str(file_path),
            brand=brand,
            model=model,
            document_version=document_version
        )

        # Add to vector store
        count = vectorstore.add_documents(chunks)

        return UploadResponse(
            message=f"Successfully ingested {count} chunks from {file.filename}",
            brand=brand,
            model=model,
            chunks_created=count
        )
    except Exception as e:
        # Clean up the file on failure
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )


@app.get("/api/logs")
async def get_logs(limit: int = 50):
    """Get recent query logs with aggregate statistics."""
    logs = logger.get_logs(limit=limit)
    stats = logger.get_stats()

    log_entries = []
    for log in logs:
        log_entries.append(LogEntry(
            id=log["id"],
            timestamp=log["timestamp"],
            query=log["query"],
            brand=log["brand"],
            model=log["model"],
            response_time_ms=log["response_time_ms"],
            chunks_retrieved=log["chunks_retrieved"],
            status=log["status"],
            sources_used=log["sources_used"]
        ))

    return LogsResponse(
        logs=log_entries,
        total_queries=stats["total_queries"],
        avg_response_time_ms=stats["avg_response_time_ms"],
        success_rate=stats["success_rate"]
    )


# ──────────────────────────────────────────────
# Static File Serving (Frontend)
# ──────────────────────────────────────────────

@app.get("/")
async def serve_frontend():
    """Serve the main frontend HTML page."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return JSONResponse(
        content={"message": "Frontend not found. Place index.html in the frontend/ directory."},
        status_code=404
    )


# Mount static files for CSS, JS, and assets
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
