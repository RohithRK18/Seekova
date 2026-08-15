import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.search import router as search_router
from app.routes.upload import router as upload_router
from app.routes.history import router as history_router
from app.routes.projects import router as projects_router
from app.routes.auth import router as auth_router


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

app.include_router(search_router)
app.include_router(upload_router)
app.include_router(history_router)
app.include_router(projects_router)
app.include_router(auth_router)


@app.get("/api")
async def api_root():
    return {
        "name": "Seekova Search API",
        "status": "online",
        "message": "Seekova Search API is running"
    }


@app.get("/api/health")
async def health():
    return {
        "status": "healthy"
    }


# Serve local frontend dist only when not running on Vercel
IS_VERCEL = bool(os.environ.get("VERCEL"))

if not IS_VERCEL:
    FRONTEND_DIST = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend", "dist")
    if os.path.exists(FRONTEND_DIST):
        assets_dir = os.path.join(FRONTEND_DIST, "assets")
        if os.path.exists(assets_dir):
            app.mount("/assets", StaticFiles(directory=assets_dir), name="static_assets")

        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            if full_path.startswith("api/"):
                raise HTTPException(status_code=404, detail="API endpoint not found")
            file_path = os.path.join(FRONTEND_DIST, full_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return FileResponse(file_path)
            return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))
