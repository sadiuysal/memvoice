from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String

from src.core.database import Base

# from sqlalchemy.orm import relationship



class MemoryEntry(Base):
    __tablename__ = "memory_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(String, nullable=False)
    meta = Column(JSON, nullable=True)  # Renamed from 'metadata' to 'meta'
    embedding = Column(String, nullable=True)  # Store vector embedding as base64 string
    relevance_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # For short-term memory entries

    # Relationships
    # user = relationship("User", back_populates="memories")

    def __repr__(self):
        return f"<MemoryEntry(id={self.id}, user_id={self.user_id}, created_at={self.created_at})>"
