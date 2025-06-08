"""
User service for business logic and database operations.
"""
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import get_password_hash, verify_password
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Get user by username."""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
        """Create a new user."""
        # Check if user already exists
        existing_user = await UserService.get_user_by_email(db, user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        existing_username = await UserService.get_user_by_username(db, user_create.username)
        if existing_username:
            raise ValueError("User with this username already exists")
        
        # Create new user
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            is_active=user_create.is_active,
            is_superuser=user_create.is_superuser,
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """Authenticate user with username/password."""
        user = await UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def update_user(
        db: AsyncSession, user_id: int, user_update: UserUpdate
    ) -> Optional[User]:
        """Update user information."""
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        
        # Hash password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await db.commit()
        await db.refresh(user)
        return user 