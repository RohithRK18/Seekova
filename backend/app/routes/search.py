from fastapi import APIRouter
from pydantic import BaseModel

from app.search_engine import search_engine


router = APIRouter(prefix="/api/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    mode: str = "deep"


@router.post("")
async def search(request: SearchRequest):
    output = search_engine.search(
        query=request.query,
        top_k=request.limit,
        mode=request.mode
    )

    return {
        "success": True,
        "query": request.query,
        "mode": request.mode,
        "count": len(output["results"]),
        "answer": output["answer"],
        "results": output["results"]
    }
