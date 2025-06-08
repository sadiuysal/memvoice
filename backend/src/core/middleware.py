"""
Middleware for error handling, logging, and request processing.
"""

import logging
import time
import uuid
from typing import Callable

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def error_handling_middleware(request: Request, call_next: Callable) -> Response:
    """Global error handling middleware."""
    # Generate request ID for tracing
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    try:
        response = await call_next(request)

        # Log successful requests
        process_time = time.time() - start_time
        logger.info(
            f"Request completed - ID: {request_id}, "
            f"Method: {request.method}, "
            f"URL: {request.url}, "
            f"Status: {response.status_code}, "
            f"Duration: {process_time:.4f}s"
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response

    except HTTPException as exc:
        # Handle FastAPI HTTP exceptions
        process_time = time.time() - start_time
        logger.warning(
            f"HTTP Exception - ID: {request_id}, "
            f"Method: {request.method}, "
            f"URL: {request.url}, "
            f"Status: {exc.status_code}, "
            f"Detail: {exc.detail}, "
            f"Duration: {process_time:.4f}s"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "HTTPException",
                    "message": exc.detail,
                    "status_code": exc.status_code,
                    "request_id": request_id,
                }
            },
            headers={"X-Request-ID": request_id},
        )

    except Exception as exc:
        # Handle unexpected exceptions
        process_time = time.time() - start_time
        logger.error(
            f"Unexpected error - ID: {request_id}, "
            f"Method: {request.method}, "
            f"URL: {request.url}, "
            f"Error: {str(exc)}, "
            f"Duration: {process_time:.4f}s",
            exc_info=True,
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "InternalServerError",
                    "message": "An unexpected error occurred",
                    "status_code": 500,
                    "request_id": request_id,
                }
            },
            headers={"X-Request-ID": request_id},
        )
