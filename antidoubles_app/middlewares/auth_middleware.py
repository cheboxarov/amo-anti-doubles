from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, HTTPException, Depends
import json
from fastapi.responses import JSONResponse
import redis_client
from schemas.project_schema import ProjectSchema
from httpx import AsyncClient
from config import AUTH_SERVICE_URL
from typing import Optional
from loguru import logger


class AuthorizeMiddleware(BaseHTTPMiddleware):

    ERROR_RESPONSE = JSONResponse(
        content={"error": "Not authorized"}, status_code=401
    )

    @classmethod
    async def get_token_from_request(cls, request: Request) -> tuple[Optional[str], Optional[JSONResponse]]:
        authorization_header = request.headers.get("Authorization")

        if authorization_header is None or len(authorization_header.split(" ")) != 2:
            return None, cls.ERROR_RESPONSE

        scheme, token = authorization_header.split(" ")
        if scheme.lower() != "bearer":
            return None, cls.ERROR_RESPONSE

        return token, None
 
    async def dispatch(self, request: Request, call_next):
        token, error = await self.get_token_from_request(request)
        if error is not None:
            return error
        
        if (user_data := await redis_client.redis.get(f"token:{token}")) is not None:
            request.state.project = ProjectSchema.model_validate(json.loads(user_data)["project"])
            return await call_next(request)

        async with AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {token}",
                "Origin": request.headers.get("Origin"),
                "widget": "antidoubles",
                "private": "t"
            }
            auth_response = await client.get(AUTH_SERVICE_URL, headers=headers)
            if auth_response.status_code != 200:
                return self.ERROR_RESPONSE
            project = ProjectSchema.model_validate(auth_response.json())
            request.state.project = project
        return await call_next(request)