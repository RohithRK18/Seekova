from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

router = APIRouter(prefix="/api/projects", tags=["Research Projects"])

# In-memory store for research projects & saved insights
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-1": {
        "id": "proj-1",
        "title": "Apache Kafka Architecture",
        "domain": "Technology",
        "created_at": "2026-08-15",
        "items": [
            {
                "query": "What is Apache Kafka?",
                "answer_snippet": "Apache Kafka is a distributed event-streaming platform..."
            }
        ]
    }
}

class CreateProjectRequest(BaseModel):
    title: str
    domain: str = "General"

class AddInsightRequest(BaseModel):
    project_id: str
    query: str
    answer: Dict[str, Any]

@router.get("")
async def get_projects():
    return {"projects": list(PROJECTS_DB.values())}

@router.post("")
async def create_project(req: CreateProjectRequest):
    proj_id = f"proj-{len(PROJECTS_DB) + 1}"
    new_proj = {
        "id": proj_id,
        "title": req.title,
        "domain": req.domain,
        "items": []
    }
    PROJECTS_DB[proj_id] = new_proj
    return {"success": True, "project": new_proj}

@router.post("/insight")
async def add_insight(req: AddInsightRequest):
    if req.project_id in PROJECTS_DB:
        PROJECTS_DB[req.project_id]["items"].append({
            "query": req.query,
            "answer": req.answer
        })
        return {"success": True, "project": PROJECTS_DB[req.project_id]}
    return {"success": False, "message": "Project not found"}
