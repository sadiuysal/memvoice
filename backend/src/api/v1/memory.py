from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.services.memory import MemoryService
from src.schemas.memory import (
    MemoryCreate,
    MemoryUpdate,
    MemoryResponse,
    MemoryQuery
)

router = APIRouter()

@router.post("/", response_model=MemoryResponse)
async def create_memory(
    memory: MemoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new memory entry"""
    service = MemoryService(db)
    return await service.create_memory(memory)

@router.get("/{memory_id}", response_model=MemoryResponse)
async def get_memory(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific memory entry"""
    service = MemoryService(db)
    memory = await service.get_memory(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return memory

@router.put("/{memory_id}", response_model=MemoryResponse)
async def update_memory(
    memory_id: int,
    memory: MemoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a memory entry"""
    service = MemoryService(db)
    updated_memory = await service.update_memory(memory_id, memory)
    if not updated_memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return updated_memory

@router.delete("/{memory_id}")
async def delete_memory(
    memory_id: int,
    db: Session = Depends(get_db)
):
    """Delete a memory entry"""
    service = MemoryService(db)
    success = await service.delete_memory(memory_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"status": "success"}

@router.get("/search/", response_model=List[MemoryResponse])
async def search_memories(
    user_id: str = Query(..., description="User ID to search memories for"),
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    min_relevance: float = Query(0.0, ge=0.0, le=1.0, description="Minimum relevance score"),
    db: Session = Depends(get_db)
):
    """Search memories using semantic search"""
    service = MemoryService(db)
    search_query = MemoryQuery(
        user_id=user_id,
        query=query,
        limit=limit,
        min_relevance=min_relevance
    )
    return await service.search_memories(search_query)

@router.post("/cleanup/")
async def cleanup_expired_memories(
    db: Session = Depends(get_db)
):
    """Clean up expired short-term memories"""
    service = MemoryService(db)
    count = await service.cleanup_expired_memories()
    return {"cleaned_up_count": count} 