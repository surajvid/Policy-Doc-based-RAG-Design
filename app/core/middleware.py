"""
middleware.py

Non-technical explanation:
- Middleware runs "around" every API request.
- It allows us to log:
  - which endpoint was called
  - how long it took
  - a unique trace_id to track the request end-to-end
"""

import time
import uuid
import logging
from fastapi import Request

logger = logging.getLogger("newpage-docs-rag")


async def request_logging_middleware(request: Request, call_next):
    trace_id = str(uuid.uuid4())
    start = time.time()

    # Attach trace_id so endpoints can reuse it if needed
    request.state.trace_id = trace_id

    response = await call_next(request)

    duration_ms = int((time.time() - start) * 1000)

    logger.info(
        "trace_id=%s method=%s path=%s status=%s duration_ms=%s",
        trace_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    # Also return trace_id to caller (helps debugging)
    response.headers["X-Trace-Id"] = trace_id
    return response