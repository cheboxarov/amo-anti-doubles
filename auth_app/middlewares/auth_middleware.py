from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from services.services_factory import create_services_factory, ServicesFactory
from services.project_service import ProjectsService
import json
from fastapi.responses import JSONResponse
import redis_client
from typing import Optional
from schemas.widget_schema import WidgetSchema
from services.widgets_service import WidgetsService
from schemas.project_schema import ProjectSchema
from loguru import logger
import asyncio


token_update_locks = {}


class AuthorizeMiddleware(BaseHTTPMiddleware):

    ERROR_RESPONSE = JSONResponse(
        content={"error": "Not authorized"}, status_code=401
    )

    @classmethod
    async def get_subdomain_from_request(cls, request: Request) -> tuple[Optional[str], Optional[JSONResponse]]:
        subdomain = request.headers.get("Origin", "https://example.com").split("//")[1].split(".")[0]

        if subdomain == "example":
            return None, cls.ERROR_RESPONSE
        
        return subdomain, None

    @classmethod
    async def get_token_from_request(cls, request: Request) -> tuple[Optional[str], Optional[JSONResponse]]:
        authorization_header = request.headers.get("Authorization")

        if authorization_header is None or len(authorization_header.split(" ")) != 2:
            return None, cls.ERROR_RESPONSE

        scheme, token = authorization_header.split(" ")
        if scheme.lower() != "bearer":
            return None, cls.ERROR_RESPONSE

        return token, None
    
    @classmethod
    async def get_widget_from_request(cls, request: Request, widget_service: WidgetsService, subdomain: str) -> tuple[Optional[WidgetSchema], Optional[JSONResponse]]:

        widget_name = request.headers.get("widget")
        if request.headers.get("private"):
            logger.info(f"private widget {widget_name}")
            widget_name = f"{widget_name}_{subdomain}"
        logger.info(f"widget_name {widget_name}")
        if widget_name is None:
            return None, cls.ERROR_RESPONSE
        
        widget = await widget_service.get_by_name(widget_name)
        logger.info(f"widget {widget}")
        if widget is None:
            return None, cls.ERROR_RESPONSE
        
        return widget, None


    async def dispatch(self, request: Request, call_next):
        """The dispatch function of the middleware is called for each incoming request.

        This function checks if the request is authorized by checking the "Authorization" header.
        If the header is not present or is not in the format "Bearer <access token>" and the token is not found in the list of admin users' tokens in the project, it raises an HTTPException with a status code of 401.
        If the request is authorized, it sets the request.state.is_admin and request.state.project and calls the next middleware in the chain with the modified request.
        The response from the next middleware is returned.
        """

        if request.url.path == "/install":
            return await call_next(request)

        services = await create_services_factory()
        project_service = services.projects
        widget_service = services.widgets
        auth_service = services.auth

        error_response = JSONResponse(
            content={"error": "Not authorized"}, status_code=401
        )

        token, error = await self.get_token_from_request(request)
        if error is not None:
            return error

        subdomain, error = await self.get_subdomain_from_request(request)
        if error is not None:
            return error
    
        widget, error = await self.get_widget_from_request(request, widget_service, subdomain)
        if error is not None:
            return error
        
        user_data = await redis_client.redis.get(f"token:{token}-{subdomain}")

        if user_data is not None:

            user_data = json.loads(user_data)
            is_admin = user_data["is_admin"]
            project = ProjectSchema.model_validate(user_data["project"])

        else: 

            project = await project_service.get_by_widget_and_subdomain(subdomain, widget.id)
            
            if project is None:
                return error
            
            if project.access_token != project.refresh_token and not await redis_client.redis.get(f"project:{subdomain}"):

                if subdomain not in token_update_locks:
                    token_update_locks[subdomain] = asyncio.Lock()

                lock = token_update_locks[subdomain]
                try:
                    async with lock:
                        if not await redis_client.redis.get(f"project:{subdomain}"):
                            await auth_service.update_token(project)
                            await redis_client.redis.set(
                                f"project:{subdomain}", json.dumps(project.model_dump()), ex=300
                            )
                finally:
                    token_update_locks.pop(subdomain, None)

            project_data = await redis_client.redis.get(f"project:{subdomain}")
            if project_data:
                project = ProjectSchema.model_validate(json.loads(project_data))
            else:
                return error_response
            
            amo_api = project_service.get_api(project)
            users = await amo_api.users.get_all(with_="uuid")

            try:
                is_admin = {user.uuid: user for user in users}[token].role == "admin"
                await redis_client.redis.set(
                    f"token:{token}-{subdomain}", json.dumps({
                        "is_admin": is_admin,
                        "project": project.model_dump()
                        }), ex=60*30
                )
            except KeyError:
                return error_response

        request.state.project = project
        request.state.is_admin = is_admin

        response = await call_next(request)

        response.headers["Token-Exp"] = str(await redis_client.redis.ttl(f"project:{subdomain}"))

        return response
