from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/history",
    tags=["History"]
)

search_history = []


class HistoryItem(BaseModel):
    query: str


@router.post("")
async def add_history(
    item: HistoryItem
):
    if item.query and item.query not in search_history:
        search_history.insert(0, item.query)

    return {
        "success": True
    }


@router.get("")
async def get_history():
    return {
        "success": True,
        "history": search_history[:30]
    }


@router.delete("")
async def clear_history():
    search_history.clear()
    return {
        "success": True
    }
