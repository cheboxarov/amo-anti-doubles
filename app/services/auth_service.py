from repository.widgets_repository import WidgetsRepository
from repository.projects_repository import ProjectsRepository
from schemas.project_schema import ProjectSchema
from api.amo_tokens_api import AmoTokensApi
from loguru import logger


class WidgetNotFoundException(Exception):
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.message = f"Widget not found for client_id: {client_id}"
        super().__init__(self.message)


class AuthService:

    def __init__(
        self,
        widgets_repository: WidgetsRepository,
        projects_repository: ProjectsRepository,
    ):
        self.widgets_repository = widgets_repository
        self.projects_repository = projects_repository

    async def install_widget(
        self, code: str, client_id: str, subdomain: str
    ) -> ProjectSchema:
        widget = await self.widgets_repository.get_by_client_id(client_id)
        if widget is None:
            raise WidgetNotFoundException(client_id)

        response = await AmoTokensApi.get_tokens_by_code(
            widget.client_id, widget.secret_key, code, subdomain
        )
        access_token = response.get("access_token")
        refresh_token = response.get("refresh_token")

        project = await self.projects_repository.get_by_subdomain(subdomain)

        create_args = {
            "subdomain": subdomain,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "widget_id": widget.id,
        }

        if project:
            create_args["is_active"] = project.is_active
            create_args["is_admin"] = project.is_admin
            if not await self.projects_repository.delete(project.id):
                raise ValueError(f"Failed to delete project with id {project.id}")

        project = await self.projects_repository.create(ProjectSchema(**create_args))

        return project

    async def update_token(self, project: ProjectSchema) -> ProjectSchema:
        widget = project.widget
        response = await AmoTokensApi.get_tokens_by_refresh(
            widget.client_id,
            widget.secret_key,
            project.refresh_token,
            project.subdomain,
        )
        project.access_token = response.get("access_token")
        project.refresh_token = response.get("refresh_token")
        await self.projects_repository.update(project.id, project)
