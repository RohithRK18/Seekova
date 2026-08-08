# pyright: reportMissingImports=false
# pyrefly: ignore [missing-import]

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.search import router as search_router
from app.routes.upload import router as upload_router
from app.routes.history import router as history_router


app = FastAPI(
    title="Seekova Search Engine",
    description="TF-IDF powered intelligent search engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os

app.include_router(search_router)
app.include_router(upload_router)
app.include_router(history_router)

FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")

if os.path.exists(FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="static_assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api"):
            return None
        file_path = os.path.join(FRONTEND_DIST, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))


from fastapi.responses import HTMLResponse

@app.get("/system", response_class=HTMLResponse)
async def system_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Seekova Control Hub</title>
        <style>
            body { margin:0; font-family: system-ui, sans-serif; background: #08090c; color: white; display: flex; flex-direction: column; height: 100vh; }
            header { background: #121319; border-bottom: 1px solid #22242b; padding: 12px 20px; display: flex; gap: 20px; align-items: center; }
            header h2 { margin:0; font-size: 18px; color: #8b5cf6; }
            nav a { color: #a0a5b5; text-decoration: none; padding: 8px 14px; border-radius: 8px; font-weight: 600; font-size: 14px; }
            nav a.active, nav a:hover { background: #7c3aed; color: white; }
            .container { flex: 1; display: flex; }
            iframe { flex: 1; border: none; width: 50%; height: 100%; }
            .divider { width: 2px; background: #22242b; }
        </style>
    </head>
    <body>
        <header>
            <h2>Seekova Control Hub</h2>
            <nav>
                <a href="http://localhost:5173" target="appFrame">Frontend App</a>
                <a href="http://localhost:8000/docs" target="docsFrame">API Docs (Swagger)</a>
            </nav>
        </header>
        <div class="container">
            <iframe name="appFrame" src="http://localhost:5173"></iframe>
            <div class="divider"></div>
            <iframe name="docsFrame" src="http://localhost:8000/docs"></iframe>
        </div>
    </body>
    </html>
    """



@app.get("/")
async def root():
    return {
        "name": "Seekova",
        "status": "online",
        "message": "Seekova Search API is running"
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy"
    }
