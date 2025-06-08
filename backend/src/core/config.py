"""
Configuration management for MemVoice API.
"""
from typing import Any, Dict, Optional, Union
from pydantic import Field, field_validator, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    PROJECT_NAME: str = "MemVoice API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Memory-Optimized Voice Agent Pipeline"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production", alias="JWT_SECRET", description="Secret key for JWT encoding")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./memvoice.db", description="Database connection URL")
    
    # Redis Cache
    REDIS_URL: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # External API Keys
    OPENAI_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    PINECONE_API_KEY: Optional[str] = None
    ZEP_API_KEY: Optional[str] = None
    
    # Voice Processing Settings
    MAX_AUDIO_FILE_SIZE: int = 25 * 1024 * 1024  # 25MB
    SUPPORTED_AUDIO_FORMATS: list = ["mp3", "wav", "flac", "m4a"]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, list]) -> list:
        """Parse CORS origins from environment variable."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError("Invalid CORS origins format")
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings() 