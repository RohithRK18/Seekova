from fastapi import APIRouter
from pydantic import BaseModel

from app.search_engine import search_engine


router = APIRouter(prefix="/api/search", tags=["Search"])


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


@router.post("")
async def search(request: SearchRequest):
    results = search_engine.search(
        request.query,
        request.limit
    )

    return {
        "success": True,
        "query": request.query,
        "count": len(results),
        "results": results
    }
