from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from app.search_engine import search_engine


router = APIRouter(prefix="/api/search", tags=["Search"])


class CustomDoc(BaseModel):
    id: str
    title: str
    content: str
    file_type: str = "text"


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    mode: str = "deep"
    custom_documents: Optional[List[CustomDoc]] = []


@router.post("")
async def search(request: SearchRequest):
    custom_docs_list = [doc.dict() for doc in request.custom_documents] if request.custom_documents else []

    output = search_engine.search(
        query=request.query,
        top_k=request.limit,
        mode=request.mode,
        custom_documents=custom_docs_list
    )

    return {
        "success": True,
        "query": request.query,
        "mode": request.mode,
        "count": len(output["results"]),
        "answer": output["answer"],
        "results": output["results"]
    }
