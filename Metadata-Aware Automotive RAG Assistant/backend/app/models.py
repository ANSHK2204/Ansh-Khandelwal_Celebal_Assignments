"""
Drive Wise - Pydantic Models
Request/Response schemas for the FastAPI endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ──────────────────────────────────────────────
# Request Models
# ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    """User chat query with selected vehicle context."""
    query: str = Field(..., description="User's natural language question")
    brand: str = Field(..., description="Selected car brand")
    model: str = Field(..., description="Selected car model")


class UploadRequest(BaseModel):
    """Metadata for brochure upload."""
    brand: str = Field(..., description="Car brand name")
    model: str = Field(..., description="Car model name")
    document_version: str = Field(default="2024", description="Document version/year")


# ──────────────────────────────────────────────
# Response Models
# ──────────────────────────────────────────────

class SourceInfo(BaseModel):
    """Source attribution details for a retrieved chunk."""
    brochure_name: str = Field(..., description="Name of the source brochure")
    section: str = Field(..., description="Brochure section title")
    page_number: int = Field(..., description="Page number in the brochure")
    chunk_text: str = Field(..., description="Retrieved text chunk")
    relevance_score: float = Field(..., description="Re-ranking relevance score")


class EvaluationMetrics(BaseModel):
    """Quality evaluation metrics for the response."""
    context_relevance: float = Field(
        default=0.0,
        description="How relevant the retrieved chunks are to the query (0-1)"
    )
    answer_groundedness: float = Field(
        default=0.0,
        description="How grounded the answer is in the retrieved context (0-1)"
    )
    answer_completeness: float = Field(
        default=0.0,
        description="How completely the answer addresses the query (0-1)"
    )


class ChatResponse(BaseModel):
    """Complete response to a user chat query."""
    answer: str = Field(..., description="Generated answer grounded in brochure content")
    sources: List[SourceInfo] = Field(
        default_factory=list,
        description="Source attribution details"
    )
    response_time_ms: float = Field(..., description="Total response time in milliseconds")
    evaluation: EvaluationMetrics = Field(
        default_factory=EvaluationMetrics,
        description="Quality evaluation metrics"
    )
    brand: str = Field(..., description="Selected car brand")
    model: str = Field(..., description="Selected car model")


class UploadResponse(BaseModel):
    """Response after brochure upload and ingestion."""
    message: str
    brand: str
    model: str
    chunks_created: int


class BrandListResponse(BaseModel):
    """List of available car brands."""
    brands: List[str]


class ModelListResponse(BaseModel):
    """List of available car models for a brand."""
    brand: str
    models: List[str]


class LogEntry(BaseModel):
    """Single query log entry."""
    id: int
    timestamp: str
    query: str
    brand: str
    model: str
    response_time_ms: float
    chunks_retrieved: int
    status: str
    sources_used: str


class LogsResponse(BaseModel):
    """Response containing query logs."""
    logs: List[LogEntry]
    total_queries: int
    avg_response_time_ms: float
    success_rate: float
