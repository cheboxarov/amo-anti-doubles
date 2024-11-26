from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response, HTTPException, Depends
from services.service import create_services, Service
from services.project_service import ProjectsService
import json
from fastapi.responses import JSONResponse
import redis_client


class AuthorizeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        """The dispatch function of the middleware is called for each incoming request.

        This function checks if the request is authorized by checking the "Authorization" header.
        If the header is not present or is not in the format "Bearer <access token>" and the token is not found in the list of admin users' tokens in the project, it raises an HTTPException with a status code of 401.
        If the request is authorized, it sets the request.state.is_admin and request.state.project and calls the next middleware in the chain with the modified request.
        The response from the next middleware is returned.
        """

        project_service = (await create_services()).projects

        error_response = JSONResponse(
            content={"error": "Not authorized"}, status_code=401
        )

        authorization_header = request.headers.get("Authorization")
        subdomain = request.headers.get("Host", "example.com").split(".")[0]

        if authorization_header is None or len(authorization_header.split(" ")) != 2:
            return error_response

        scheme, token = authorization_header.split(" ")
        if scheme.lower() != "bearer":
            return error_response

        project = await project_service.get_by_subdomain(subdomain)

        if project is None:
            return error_response

        if (user_data := await redis_client.redis.get(f"token:{token}")) is not None:
            is_admin = json.loads(user_data)["is_admin"]
        else:
            amo_api = project_service.get_api(project)
            users = await amo_api.users.get_all(with_="uuid")
            try:
                is_admin = {user.uuid: user.role for user in users}[token] == "admin"
                await redis_client.redis.set(
                    f"token:{token}", json.dumps({"is_admin": is_admin}), ex=900
                )
            except KeyError:
                return error_response

        request.state.project = project
        request.state.is_admin = is_admin

        response: Response = await call_next(request)
        return response
