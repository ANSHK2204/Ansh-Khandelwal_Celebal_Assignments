"""
Drive Wise - Ingestion Module
Handles PDF parsing, structured chunking, and metadata extraction from car brochures.
"""

import re
from typing import List, Dict, Optional
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from app.config import BROCHURES_DIR, CHUNK_SIZE, CHUNK_OVERLAP


# ──────────────────────────────────────────────
# Section Detection Patterns
# ──────────────────────────────────────────────
SECTION_KEYWORDS = {
    "Engine & Performance": [
        "engine", "performance", "power", "torque", "transmission",
        "horsepower", "cylinder", "turbo", "petrol", "diesel",
        "rpm", "gear", "drivetrain", "bhp", "ps"
    ],
    "Mileage & Fuel Efficiency": [
        "mileage", "fuel", "efficiency", "km/l", "kmpl",
        "consumption", "economy", "range", "arai", "hybrid"
    ],
    "Safety Features": [
        "safety", "airbag", "abs", "ebd", "esc", "esp",
        "ncap", "braking", "collision", "adas", "traction",
        "stability", "parking sensor", "camera"
    ],
    "Dimensions & Space": [
        "dimension", "length", "width", "height", "wheelbase",
        "boot", "luggage", "ground clearance", "kerb weight",
        "turning radius", "seating capacity"
    ],
    "Interior & Comfort": [
        "interior", "comfort", "seat", "climate", "sunroof",
        "steering", "dashboard", "ambient", "leather", "ventilated",
        "armrest", "push button", "upholstery"
    ],
    "Infotainment & Connectivity": [
        "infotainment", "touchscreen", "android auto", "apple carplay",
        "bluetooth", "speaker", "navigation", "connected", "wireless",
        "display", "sound system", "usb", "voice"
    ],
    "Exterior Design": [
        "exterior", "design", "headlamp", "tail lamp", "alloy",
        "grille", "bumper", "color", "colour", "roof rail",
        "fog lamp", "drl", "spoiler", "chrome"
    ],
    "Warranty & Service": [
        "warranty", "service", "maintenance", "roadside",
        "spare", "dealer", "cost of ownership", "annual"
    ]
}


def classify_section(text: str) -> str:
    """
    Classify a text block into a brochure section based on keyword matching.
    Returns the section name with the highest keyword match count.
    """
    text_lower = text.lower()
    scores = {}

    for section, keywords in SECTION_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[section] = score

    if scores:
        return max(scores, key=scores.get)
    return "General Information"


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract text from a PDF file page by page.
    Returns a list of dicts with page_number and text.
    """
    if fitz is None:
        raise ImportError(
            "PyMuPDF (fitz) is required for PDF parsing. "
            "Install it with: pip install PyMuPDF"
        )

    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        if text:
            pages.append({
                "page_number": page_num + 1,
                "text": text
            })

    doc.close()
    return pages


def structured_chunk(
    pages: List[Dict],
    brand: str,
    model: str,
    document_version: str = "2024"
) -> List[Dict]:
    """
    Create structured chunks from extracted PDF pages.
    
    Strategy:
    1. Try to detect section boundaries based on headings and keywords
    2. Group related pages into sections
    3. If sections are too large, split with overlap
    4. Attach metadata to each chunk
    """
    chunks = []
    brochure_name = f"{brand} {model} Brochure - {document_version}"

    # First pass: combine all text and try section detection
    current_section_text = ""
    current_section_name = "General Information"
    current_page_start = 1

    for page_data in pages:
        page_text = page_data["text"]
        page_num = page_data["page_number"]

        # Detect if this page starts a new section
        detected_section = classify_section(page_text)

        if detected_section != current_section_name and current_section_text:
            # Save the previous section as a chunk
            chunks.extend(
                _create_chunks_from_section(
                    text=current_section_text,
                    section_name=current_section_name,
                    page_number=current_page_start,
                    brand=brand,
                    model=model,
                    document_version=document_version,
                    brochure_name=brochure_name
                )
            )
            current_section_text = page_text
            current_section_name = detected_section
            current_page_start = page_num
        else:
            current_section_text += "\n\n" + page_text
            if not current_section_text.strip():
                current_page_start = page_num

    # Don't forget the last section
    if current_section_text.strip():
        chunks.extend(
            _create_chunks_from_section(
                text=current_section_text,
                section_name=current_section_name,
                page_number=current_page_start,
                brand=brand,
                model=model,
                document_version=document_version,
                brochure_name=brochure_name
            )
        )

    return chunks


def _create_chunks_from_section(
    text: str,
    section_name: str,
    page_number: int,
    brand: str,
    model: str,
    document_version: str,
    brochure_name: str
) -> List[Dict]:
    """
    Create one or more chunks from a section text.
    If the text is too long, split it with overlap.
    """
    chunks = []
    words = text.split()

    if len(words) <= CHUNK_SIZE:
        # Section fits in one chunk
        chunks.append({
            "text": text.strip(),
            "metadata": {
                "brand": brand,
                "model": model,
                "section": section_name,
                "page_number": page_number,
                "document_version": document_version,
                "brochure_name": brochure_name,
                "source": "pdf_upload"
            }
        })
    else:
        # Split into overlapping chunks
        start = 0
        chunk_index = 0
        while start < len(words):
            end = start + CHUNK_SIZE
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append({
                "text": chunk_text.strip(),
                "metadata": {
                    "brand": brand,
                    "model": model,
                    "section": f"{section_name} (Part {chunk_index + 1})",
                    "page_number": page_number,
                    "document_version": document_version,
                    "brochure_name": brochure_name,
                    "source": "pdf_upload"
                }
            })

            start = end - CHUNK_OVERLAP
            chunk_index += 1

    return chunks


def ingest_pdf(
    pdf_path: str,
    brand: str,
    model: str,
    document_version: str = "2024"
) -> List[Dict]:
    """
    Full ingestion pipeline: PDF → pages → structured chunks with metadata.
    
    Args:
        pdf_path: Path to the PDF brochure file
        brand: Car brand name
        model: Car model name  
        document_version: Document version/year
    
    Returns:
        List of chunk dicts with 'text' and 'metadata' keys
    """
    # Extract pages from PDF
    pages = extract_text_from_pdf(pdf_path)

    if not pages:
        return []

    # Create structured chunks with metadata
    chunks = structured_chunk(pages, brand, model, document_version)

    return chunks
