"""
Configuration management for EPS Proxy Service
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # EPS API credentials
    TOKEN: str = ""
    USER_ID: str = ""
    PASSWORD: str = ""
    
    # API Configuration
    EPS_BASE_URL: str = "http://api.epspl.co.in/api/Client/TrackingDetail"
    REQUEST_TIMEOUT: int = 20
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "https://deepikachadha.com",
        "https://kapdadori.com",
        "https://www.deepikachadhaofficial.com",
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def validate_env_vars(self) -> List[str]:
        """Check for missing required environment variables"""
        missing = []
        for key in ["TOKEN", "USER_ID", "PASSWORD"]:
            if not getattr(self, key):
                missing.append(key)
        return missing


settings = Settings()
