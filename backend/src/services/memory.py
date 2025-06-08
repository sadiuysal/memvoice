import base64
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import numpy as np
from zep_python import ZepEnvironment, Memory, SearchType, SearchScope
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.core.config import settings
from src.models.memory import MemoryEntry
from src.schemas.memory import MemoryCreate, MemoryUpdate, MemoryQuery

class MemoryService:
    def __init__(self, db: Session):
        self.db = db
        self.zep_env = ZepEnvironment(settings.ZEP_API_URL)
        self.token_optimizer = TokenOptimizer()

    async def create_memory(self, memory: MemoryCreate) -> MemoryEntry:
        # Create memory entry in database
        db_memory = MemoryEntry(
            user_id=memory.user_id,
            content=memory.content,
            meta=memory.meta,
            relevance_score=memory.relevance_score,
            expires_at=memory.expires_at
        )
        self.db.add(db_memory)
        self.db.commit()
        self.db.refresh(db_memory)

        # Add to Zep for vector search
        await self._add_to_zep(db_memory)
        return db_memory

    async def get_memory(self, memory_id: int) -> Optional[MemoryEntry]:
        return self.db.query(MemoryEntry).filter(MemoryEntry.id == memory_id).first()

    async def update_memory(self, memory_id: int, memory: MemoryUpdate) -> Optional[MemoryEntry]:
        db_memory = await self.get_memory(memory_id)
        if not db_memory:
            return None

        update_data = memory.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_memory, field, value)

        self.db.commit()
        self.db.refresh(db_memory)
        await self._update_in_zep(db_memory)
        return db_memory

    async def delete_memory(self, memory_id: int) -> bool:
        db_memory = await self.get_memory(memory_id)
        if not db_memory:
            return False

        self.db.delete(db_memory)
        self.db.commit()
        await self._delete_from_zep(db_memory)
        return True

    async def search_memories(self, query: MemoryQuery) -> List[MemoryEntry]:
        # Search in Zep for relevant memories
        search_results = await self.zep_env.memory.search(
            collection_name=f"user_{query.user_id}",
            query=query.query,
            limit=query.limit
        )

        # Get memory IDs from search results
        memory_ids = [int(result.metadata.get("memory_id")) for result in search_results]
        
        # Fetch full memory entries from database
        memories = self.db.query(MemoryEntry).filter(
            and_(
                MemoryEntry.id.in_(memory_ids),
                MemoryEntry.user_id == query.user_id
            )
        ).all()

        # Sort memories by relevance score
        memories.sort(key=lambda x: x.relevance_score or 0, reverse=True)
        return memories

    async def cleanup_expired_memories(self) -> int:
        """Clean up expired short-term memories"""
        expired_memories = self.db.query(MemoryEntry).filter(
            and_(
                MemoryEntry.expires_at.isnot(None),
                MemoryEntry.expires_at < datetime.utcnow()
            )
        ).all()

        for memory in expired_memories:
            await self.delete_memory(memory.id)

        return len(expired_memories)

    async def _add_to_zep(self, memory: MemoryEntry) -> None:
        """Add memory to Zep vector store"""
        # Create Zep memory object
        zep_memory = Memory(
            content=memory.content,
            metadata={
                "memory_id": str(memory.id),
                "user_id": memory.user_id,
                "created_at": memory.created_at.isoformat(),
                "relevance_score": memory.relevance_score,
                **(memory.meta or {})
            }
        )

        # Add to Zep collection
        await self.zep_env.memory.add(
            collection_name=f"user_{memory.user_id}",
            memory=zep_memory
        )

        # Store embedding in database if available
        if hasattr(zep_memory, 'embedding') and zep_memory.embedding is not None:
            memory.embedding = base64.b64encode(zep_memory.embedding.tobytes()).decode()
            self.db.commit()

    async def _update_in_zep(self, memory: MemoryEntry) -> None:
        """Update memory in Zep vector store"""
        await self._delete_from_zep(memory)
        await self._add_to_zep(memory)

    async def _delete_from_zep(self, memory: MemoryEntry) -> None:
        """Delete memory from Zep vector store"""
        await self.zep_env.memory.delete(
            collection_name=f"user_{memory.user_id}",
            memory_id=str(memory.id)
        )

class TokenOptimizer:
    """Handles token optimization for memory content"""
    
    def __init__(self):
        self.target_reduction = 0.7  # Target 70% token reduction

    def optimize_content(self, content: str) -> str:
        """Optimize content to reduce token usage while maintaining meaning"""
        # TODO: Implement token optimization strategies
        # 1. Remove redundant words and phrases
        # 2. Use shorter synonyms
        # 3. Compress numerical data
        # 4. Remove unnecessary punctuation
        return content

    def calculate_token_reduction(self, original: str, optimized: str) -> float:
        """Calculate the percentage of token reduction"""
        # TODO: Implement token counting and reduction calculation
        return 0.0 