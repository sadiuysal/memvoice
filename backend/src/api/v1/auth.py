"""
Authentication endpoints.
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.deps import get_current_active_user, get_db
from ...core.config import settings
from ...core.security import create_access_token
from ...models.user import User
from ...schemas.user import Token
from ...schemas.user import User as UserSchema
from ...schemas.user import UserCreate
from ...services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserSchema)
async def register(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    try:
        user = await UserService.create_user(db, user_create)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login and get access token."""
    user = await UserService.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user information."""
    return current_user
