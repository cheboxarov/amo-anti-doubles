from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from loguru import logger
import traceback


class ExcLoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:

        try:
            return await call_next(request)
        except Exception as error:
            logger.error(f"Unhandled exception: {error} LogException={traceback.format_exc()}")
            raise