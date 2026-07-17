# 🚗 Drive Wise — Metadata-aware Automotive RAG Assistant

> **Helping Users Make Informed Car Decisions Through a Brochure-Grounded AI Assistant**

Drive Wise is an intelligent conversational AI assistant designed to help users understand car brochures in a simple and user-friendly manner. It uses **Retrieval-Augmented Generation (RAG)** with metadata filtering, structured chunking, and re-ranking to deliver accurate, context-aware responses with full source attribution.

---

## 🌟 Key Features

- **Brand & Model Selection** — Select a car brand and model to filter brochure data
- **Brochure-Grounded Responses** — Answers are generated strictly from official brochure content
- **Metadata Filtering** — Chunks are tagged with brand, model, section, and page metadata
- **Structured Chunking** — Documents are split by logical sections (engine, safety, dimensions, etc.)
- **Cross-Encoder Re-ranking** — Retrieved chunks are re-ranked for maximum relevance
- **Source Attribution** — Every answer shows exactly which brochure sections were used
- **Evaluation Metrics** — Context relevance, answer groundedness, and completeness scores
- **Query Logging** — All queries are logged with response times for monitoring
- **PDF Upload** — Upload new car brochure PDFs for automatic ingestion

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend API | Python + FastAPI |
| Vector Database | ChromaDB (persistent) |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Re-ranking | Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) |
| LLM | Google Gemini API (`gemini-2.0-flash`) |
| PDF Parsing | PyMuPDF |
| Frontend | HTML + CSS + JavaScript |
| Logging | SQLite |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Key (Optional)

Copy the environment template and add your Gemini API key:

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

> **Note:** The app works without a Gemini API key in "fallback mode", showing direct brochure excerpts instead of AI-generated answers. Get a free key at [Google AI Studio](https://aistudio.google.com/apikey).

### 3. Run the Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open the App

Visit **http://localhost:8000** in your browser.

---

## 📁 Project Structure

```
drive-wise/
├── backend/
│   ├── app/
│   │   ├── __init__.py         # Package init
│   │   ├── main.py             # FastAPI application & routes
│   │   ├── config.py           # Configuration & environment
│   │   ├── models.py           # Pydantic request/response schemas
│   │   ├── ingestion.py        # PDF parsing & structured chunking
│   │   ├── vectorstore.py      # ChromaDB vector store wrapper
│   │   ├── retriever.py        # Metadata filtering & re-ranking
│   │   ├── generator.py        # LLM response generation
│   │   ├── logger.py           # SQLite query logging
│   │   └── sample_data.py      # Demo brochure data
│   ├── brochures/              # Uploaded PDF storage
│   ├── data/                   # ChromaDB persistent data
│   ├── logs/                   # SQLite log database
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html              # Main chat interface
│   ├── style.css               # Premium dark theme
│   └── script.js               # Chat logic & API integration
└── README.md
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check & status |
| `/api/brands` | GET | List available car brands |
| `/api/models/{brand}` | GET | List models for a brand |
| `/api/chat` | POST | Send query, get grounded answer |
| `/api/upload` | POST | Upload new brochure PDF |
| `/api/logs` | GET | Retrieve query logs |

---

## 📊 RAG Pipeline

```
User Query → Metadata Filter (brand/model) → Vector Search (top-10) 
→ Cross-Encoder Re-ranking → Context Window (top-4) → LLM Generation 
→ Answer + Source Attribution + Evaluation Metrics
```

---

## 📦 Demo Data

The app comes pre-loaded with sample brochure data for:
- **Hyundai** — Creta, Venue
- **Tata** — Nexon
- **Maruti Suzuki** — Brezza, Grand Vitara
- **Mahindra** — XUV700

Each car has 8 sections: Engine, Mileage, Safety, Dimensions, Interior, Infotainment, Exterior, and Warranty.
