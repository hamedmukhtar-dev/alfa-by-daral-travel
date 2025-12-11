from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
import logging

logger = logging.getLogger("alfa.middleware")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs each request with execution time.
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        duration = time.time() - start_time

        logger.info(
            f"{request.method} {request.url.path} | {response.status_code} | {duration:.3f}s"
        )

        return response
