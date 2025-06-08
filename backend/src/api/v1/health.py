"""
Health check and system status endpoints.
"""

from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.deps import get_db
from ...core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "MemVoice API",
        "version": settings.VERSION,
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Detailed health check including database connectivity."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "service": "MemVoice API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "checks": {},
    }

    # Database connectivity check
    try:
        await db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful",
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
        }

    # Application configuration check
    config_issues = []
    if not settings.SECRET_KEY:
        config_issues.append("SECRET_KEY not configured")
    if not settings.DATABASE_URL:
        config_issues.append("DATABASE_URL not configured")

    if config_issues:
        health_status["status"] = "unhealthy"
        health_status["checks"]["configuration"] = {
            "status": "unhealthy",
            "message": f"Configuration issues: {', '.join(config_issues)}",
        }
    else:
        health_status["checks"]["configuration"] = {
            "status": "healthy",
            "message": "All required configuration present",
        }

    return health_status


@router.get("/ping")
async def ping():
    """Simple ping endpoint for load balancer checks."""
    return {"message": "pong"}
