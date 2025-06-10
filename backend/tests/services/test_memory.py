from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest
from zep_python import Memory, SearchScope, SearchType

from src.models.memory import MemoryEntry
from src.schemas.memory import MemoryCreate, MemoryQuery, MemoryUpdate
from src.services.memory import MemoryService, TokenOptimizer


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_zep_env():
    with patch("src.services.memory.ZepEnvironment") as mock:
        env = MagicMock()
        env.memory = AsyncMock()
        mock.return_value = env
        yield env


@pytest.fixture
def memory_service(mock_db, mock_zep_env):
    return MemoryService(mock_db)


@pytest.mark.asyncio
async def test_create_memory(memory_service, mock_db, mock_zep_env):
    # Arrange
    memory_data = MemoryCreate(
        user_id="test_user",
        content="Test memory content",
        meta={"type": "test"},
        relevance_score=0.8,
    )
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock(
        side_effect=lambda obj: setattr(obj, "created_at", datetime.utcnow())
        or setattr(obj, "updated_at", datetime.utcnow())
    )
    mock_memory = MagicMock()
    mock_memory.content = memory_data.content
    mock_memory.metadata = memory_data.meta
    mock_memory.embedding = np.array([0.1, 0.2, 0.3])
    mock_zep_env.memory.add = AsyncMock(return_value=mock_memory)

    # Act
    result = await memory_service.create_memory(memory_data)

    # Assert
    assert isinstance(result, MemoryEntry)
    assert result.user_id == memory_data.user_id
    assert result.content == memory_data.content
    assert result.meta == memory_data.meta
    assert result.relevance_score == memory_data.relevance_score
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called_once()
    mock_zep_env.memory.add.assert_called_once()


@pytest.mark.asyncio
async def test_get_memory(memory_service, mock_db):
    memory_id = 1
    mock_memory = MemoryEntry(
        id=memory_id,
        user_id="test_user",
        content="Test content",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    mock_db.query.return_value.filter.return_value.first.return_value = mock_memory
    result = await memory_service.get_memory(memory_id)
    assert result == mock_memory
    mock_db.query.assert_called_once()


@pytest.mark.asyncio
async def test_update_memory(memory_service, mock_db, mock_zep_env):
    memory_id = 1
    existing_memory = MemoryEntry(
        id=memory_id,
        user_id="test_user",
        content="Old content",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    update_data = MemoryUpdate(content="Updated content", relevance_score=0.9)
    mock_db.query.return_value.filter.return_value.first.return_value = existing_memory
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    mock_memory = MagicMock()
    mock_memory.content = update_data.content
    mock_memory.metadata = {"relevance_score": update_data.relevance_score}
    mock_memory.embedding = np.array([0.1, 0.2, 0.3])
    mock_zep_env.memory.add = AsyncMock(return_value=mock_memory)
    mock_zep_env.memory.delete = AsyncMock()
    result = await memory_service.update_memory(memory_id, update_data)
    assert result.content == update_data.content
    assert result.relevance_score == update_data.relevance_score
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called_once()
    mock_zep_env.memory.delete.assert_called_once()
    mock_zep_env.memory.add.assert_called_once()


@pytest.mark.asyncio
async def test_delete_memory(memory_service, mock_db, mock_zep_env):
    memory_id = 1
    mock_memory = MemoryEntry(
        id=memory_id,
        user_id="test_user",
        content="Test content",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    mock_db.query.return_value.filter.return_value.first.return_value = mock_memory
    mock_db.delete = MagicMock()
    mock_db.commit = MagicMock()
    mock_zep_env.memory.delete = AsyncMock()
    result = await memory_service.delete_memory(memory_id)
    assert result is True
    mock_db.delete.assert_called_once_with(mock_memory)
    mock_db.commit.assert_called_once()
    mock_zep_env.memory.delete.assert_called_once()


@pytest.mark.asyncio
async def test_search_memories(memory_service, mock_db, mock_zep_env):
    query = MemoryQuery(user_id="test_user", query="test query", limit=5)
    mock_search_results = [
        MagicMock(metadata={"memory_id": "1"}),
        MagicMock(metadata={"memory_id": "2"}),
    ]
    mock_memories = [
        MemoryEntry(
            id=1,
            user_id="test_user",
            content="Memory 1",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
        MemoryEntry(
            id=2,
            user_id="test_user",
            content="Memory 2",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        ),
    ]
    mock_zep_env.memory.search = AsyncMock(return_value=mock_search_results)
    mock_db.query.return_value.filter.return_value.all.return_value = mock_memories
    result = await memory_service.search_memories(query)
    assert len(result) == 2
    assert result == mock_memories
    mock_zep_env.memory.search.assert_called_once()


@pytest.mark.asyncio
async def test_cleanup_expired_memories(memory_service, mock_db, mock_zep_env):
    expired_memory = MemoryEntry(
        id=1,
        user_id="test_user",
        content="Expired content",
        expires_at=datetime.utcnow() - timedelta(days=1),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    mock_db.query.return_value.filter.return_value.all.return_value = [expired_memory]
    mock_zep_env.memory.delete = AsyncMock()
    result = await memory_service.cleanup_expired_memories()
    assert result == 1
    mock_zep_env.memory.delete.assert_called_once()


def test_token_optimizer():
    # Arrange
    optimizer = TokenOptimizer()
    content = "This is a test content that needs to be optimized for token reduction."

    # Act
    optimized = optimizer.optimize_content(content)
    reduction = optimizer.calculate_token_reduction(content, optimized)

    # Assert
    assert isinstance(optimized, str)
    assert isinstance(reduction, float)
    assert 0 <= reduction <= 1
