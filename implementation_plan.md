# Seekova - AI-Powered Intelligent Search & Knowledge Engine Plan

Seekova is an intelligent document and knowledge search engine featuring a Claude-inspired modern dark UI, TF-IDF + Cosine Similarity ranking engine, multi-format file extraction (PDF, DOCX, TXT, MD, Image OCR fallback structure), Web Speech API voice search, search history, search modes, and "Seekova Insight" panels.

## Proposed Components & Architecture

- **Backend (`seekova/backend`)**:
  - Python FastAPI app (`app/main.py`) with CORS enabled.
  - TF-IDF Search Engine (`app/search_engine.py`) using `scikit-learn` TF-IDF Vectorizer and Cosine Similarity.
  - File Parser (`app/file_parser.py`) supporting PDF (`pypdf`), DOCX (`python-docx`), TXT, and MD.
  - Routers (`app/routes/search.py`, `app/routes/upload.py`, `app/routes/history.py`).
  - Storage directory (`uploads/`).
  - Requirements & Environment setup.

- **Frontend (`seekova/frontend`)**:
  - React + Vite + Vanilla CSS / Lucide icons.
  - Components: `Sidebar.jsx`, `SearchBar.jsx`, `SearchResult.jsx`, `WelcomeScreen.jsx`, `SeekovaInsightModal.jsx`.
  - Rich modern dark theme with Glassmorphism, animations, gradient accents, responsive sidebar, file preview, search modes, and voice search recognition.

## Proposed Implementation Steps

1. Create `seekova` root structure (`frontend/` and `backend/`).
2. Build Python backend environment configuration and requirements file.
3. Write backend modules: `search_engine.py`, `file_parser.py`, `search.py`, `upload.py`, `history.py`, `main.py`.
4. Initialize React frontend with Vite & install dependencies (`lucide-react`).
5. Write frontend React components, application logic in `App.jsx`, and custom CSS in `index.css`.
6. Verify backend startup script and frontend build.

## User Review Required

> [!IMPORTANT]
> The backend requires Python packages (`fastapi`, `uvicorn`, `scikit-learn`, `pypdf`, `python-docx`, `python-multipart`, etc.). We will generate virtualenv creation and package installation commands for execution.

## Verification Plan

### Automated / Command Verification
- Check Python backend imports and startup using `uvicorn`.
- Run `npm run build` on frontend to verify zero build or lint issues.

### Manual Verification
- Test file upload (PDF/DOCX/TXT/MD), search query execution, relevance scoring display, voice search activation, search history persistence, and Seekova Insight panel toggles.
