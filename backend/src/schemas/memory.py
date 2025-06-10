from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class MemoryBase(BaseModel):
    content: str = Field(..., description="The content of the memory entry")
    meta: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata for the memory entry"
    )
    relevance_score: Optional[float] = Field(
        None, description="Relevance score for the memory entry"
    )
    expires_at: Optional[datetime] = Field(
        None, description="Expiration time for short-term memory entries"
    )


class MemoryCreate(MemoryBase):
    user_id: str = Field(..., description="The ID of the user who owns this memory")


class MemoryUpdate(MemoryBase):
    content: Optional[str] = Field(None, description="The content of the memory entry")
    meta: Optional[Dict[str, Any]] = Field(
        None, description="Additional metadata for the memory entry"
    )
    relevance_score: Optional[float] = Field(
        None, description="Relevance score for the memory entry"
    )
    expires_at: Optional[datetime] = Field(
        None, description="Expiration time for short-term memory entries"
    )


class MemoryInDB(MemoryBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    embedding: Optional[str] = None

    class Config:
        from_attributes = True


class MemoryResponse(MemoryInDB):
    pass


class MemoryQuery(BaseModel):
    user_id: str
    query: str
    limit: int = Field(default=10, ge=1, le=100)
    min_relevance: float = Field(default=0.0, ge=0.0, le=1.0)
