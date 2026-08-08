# Seekova - Intelligent AI-Powered Document Search Engine

Seekova is an intelligent document and knowledge search engine inspired by modern AI search interaction patterns, built with a **FastAPI backend** and a **React + Vite frontend**.

## 🚀 Stack & Features
- **Frontend:** React + Vite + Lucide Icons + Custom Glassmorphism CSS
- **Backend:** Python + FastAPI + Uvicorn
- **Search Engine:** TF-IDF n-gram vectorization + Cosine Similarity ranking (`scikit-learn`)
- **Document Extractors:** PDF (`pypdf`), DOCX (`python-docx`), TXT, MD
- **Features:** Voice Search (Web Speech API), Search Modes (`⚡ Quick`, `📚 Deep`, `📄 Docs`, `🎙️ Voice`), Seekova Insight Panels, Query History.

---

## 📁 Repository Structure
```text
seekova/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── search_engine.py
│   │   ├── file_parser.py
│   │   └── routes/
│   │       ├── search.py
│   │       ├── upload.py
│   │       └── history.py
│   ├── requirements.txt
│   └── uploads/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── SearchResult.jsx
│   │   │   └── WelcomeScreen.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   └── package.json
├── package.json
└── README.md
```

---

## 🛠️ Local Development

### Quick Start (Both Frontend & Backend)
```bash
npm install
npm run dev
```
- **Frontend Application:** [http://localhost:5173](http://localhost:5173)
- **Backend API & Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Combined Control Hub:** [http://localhost:8000/system](http://localhost:8000/system)

---

## 🌐 Hosting & Deployment Instructions

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit of Seekova AI search app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Seekova.git
git push -u origin main
```

### 2. Host Backend (Render / Railway)
- **Service Type:** Web Service (Python 3)
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Host Frontend (Vercel / Netlify)
- **Framework Preset:** Vite / React
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Environment Variable:** `VITE_API_URL=https://your-backend.onrender.com`
