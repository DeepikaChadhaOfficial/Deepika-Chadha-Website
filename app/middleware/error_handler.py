"""
Global error handler middleware
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger("eps-proxy")


def setup_error_handlers(app: FastAPI):
    """Setup global error handlers"""
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception on {request.url}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
        )
