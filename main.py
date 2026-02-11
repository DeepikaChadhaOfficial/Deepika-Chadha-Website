"""
EPS Proxy Service - Main Application Entry Point
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.middleware.cors import setup_cors
from app.middleware.error_handler import setup_error_handlers
from app.api.routes import tracking

# Setup logging
setup_logging()
logger = logging.getLogger("eps-proxy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # ---- STARTUP ----
    logger.info("Starting EPS proxy service")
    
    missing = settings.validate_env_vars()
    if missing:
        logger.critical(f"Missing ENV variables: {missing}")
    else:
        logger.info("All EPS env variables loaded successfully")

    yield

    # ---- SHUTDOWN ----
    logger.info("Shutting down EPS proxy service")


# Initialize FastAPI app
app = FastAPI(
    title="EPS Proxy Service",
    description="Proxy service for EPS tracking API",
    version="1.0.0",
    lifespan=lifespan
)

# Setup middleware
setup_cors(app)
setup_error_handlers(app)

# Include routers
app.include_router(tracking.router, prefix="/track", tags=["tracking"])


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "EPS Proxy"}


@app.get("/health", tags=["health"])
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "EPS Proxy",
        "env_configured": len(settings.validate_env_vars()) == 0
    }
