import asyncio
import json
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.search_engine import search_engine

router = APIRouter(prefix="/api/search", tags=["Search"])

class CustomDoc(BaseModel):
    id: str
    title: str
    content: str
    file_type: str = "text"

class ConversationalMessage(BaseModel):
    role: str
    content: str

class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    mode: str = "deep"
    custom_documents: Optional[List[CustomDoc]] = []
    conversation_history: Optional[List[ConversationalMessage]] = []

@router.post("")
async def search(request: SearchRequest):
    custom_docs_list = [doc.dict() for doc in request.custom_documents] if request.custom_documents else []
    conv_history_list = [msg.dict() for msg in request.conversation_history] if request.conversation_history else []

    output = search_engine.search(
        query=request.query,
        top_k=request.limit,
        mode=request.mode,
        custom_documents=custom_docs_list,
        conversation_context=conv_history_list
    )

    return {
        "success": True,
        "query": request.query,
        "mode": request.mode,
        "count": len(output["results"]),
        "answer": output["answer"],
        "results": output["results"],
        "analysis": output.get("analysis", {})
    }

@router.get("/stream")
async def stream_search(query: str, mode: str = "deep"):
    """
    Streaming Server-Sent Events (SSE) endpoint for progressive answer generation
    and status updates during multi-stage processing.
    """
    async def event_generator():
        # Stage 1: Question Understanding
        yield f"data: {json.dumps({'stage': 'understanding', 'message': 'Understanding question & intent...'})}\n\n"
        await asyncio.sleep(0.15)

        # Stage 2: Knowledge Ingestion & Vector Retrieval
        yield f"data: {json.dumps({'stage': 'retrieving', 'message': 'Searching TF-IDF knowledge base & live sources...'})}\n\n"
        await asyncio.sleep(0.2)

        output = search_engine.search(query=query, mode=mode)
        ans = output["answer"]

        sources_cnt = len(ans.get("sources", []))
        yield f"data: {json.dumps({'stage': 'synthesizing', 'message': f'Analyzing {sources_cnt} sources & generating structured answer...'})}\n\n"
        await asyncio.sleep(0.2)

        # Stream answer chunks progressively
        words = ans["text"].split(" ")
        chunk_size = 6
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size]) + " "
            yield f"data: {json.dumps({'stage': 'chunk', 'text_chunk': chunk})}\n\n"
            await asyncio.sleep(0.04)

        # Complete event with full payload metadata
        yield f"data: {json.dumps({'stage': 'complete', 'answer': ans, 'results': output['results']})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
