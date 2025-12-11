from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import uuid
import time

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(round(duration, 4))

        return response


def setup_middleware(app):
    app.add_middleware(RequestContextMiddleware)
