from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, HTTPException


class AuthorizeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        headers = request.headers
        auth_header = headers.get("authorization", None)

        if auth_header is None or len(auth_header.split(" ")) != 2:
            raise HTTPException(status_code=401, detail="Not authorized")

        scheme, token = auth_header.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Not authorized")
        request.state.token = token
        response: Response = await call_next(request)
        return response